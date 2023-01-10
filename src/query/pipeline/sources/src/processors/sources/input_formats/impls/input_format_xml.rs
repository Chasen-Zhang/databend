//  Copyright 2022 Datafuse Labs.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
use std::collections::HashMap;
use std::io::Cursor;
use std::sync::Arc;

use common_exception::ErrorCode;
use common_exception::Result;
use common_expression::TableSchemaRef;
use common_expression::TypeDeserializer;
use common_expression::TypeDeserializerImpl;
use common_formats::FieldDecoder;
use common_formats::FieldDecoderRowBased;
use common_formats::FieldDecoderXML;
use common_formats::FileFormatOptionsExt;
use common_io::cursor_ext::*;
use common_meta_types::OnErrorMode;
use common_meta_types::StageFileFormatType;
use xml::reader::XmlEvent;
use xml::ParserConfig;

use crate::processors::sources::input_formats::input_format_text::AligningStateTextBased;
use crate::processors::sources::input_formats::input_format_text::BlockBuilder;
use crate::processors::sources::input_formats::input_format_text::InputFormatTextBase;
use crate::processors::sources::input_formats::input_format_text::RowBatch;
use crate::processors::sources::input_formats::InputContext;
use crate::processors::sources::input_formats::SplitInfo;

pub struct InputFormatXML {}

impl InputFormatXML {
    pub fn create() -> Self {
        Self {}
    }
    fn read_row(
        field_decoder: &FieldDecoderXML,
        row_data: &mut HashMap<String, Vec<u8>>,
        deserializers: &mut [TypeDeserializerImpl],
        schema: &TableSchemaRef,
        path: &str,
        row_index: usize,
    ) -> Result<()> {
        let raw_data = if !field_decoder.ident_case_sensitive {
            row_data
                .drain()
                .map(|(k, v)| (k.to_lowercase(), v))
                .collect()
        } else {
            row_data.clone()
        };

        for (field, deserializer) in schema.fields().iter().zip(deserializers.iter_mut()) {
            let value = if field_decoder.ident_case_sensitive {
                raw_data.get(field.name())
            } else {
                raw_data.get(&field.name().to_lowercase())
            };
            if let Some(value) = value {
                let mut reader = Cursor::new(&**value);
                if reader.eof() {
                    deserializer.de_default();
                } else {
                    if let Err(e) = field_decoder.read_field(deserializer, &mut reader, true) {
                        let value_str = format!("{value:?}");
                        let err_msg = format!("{}. column={} value={}", e, field.name(), value_str);
                        return Err(xml_error(&err_msg, path, row_index));
                    };
                    if reader.must_eof().is_err() {
                        let value_str = format!("{value:?}");
                        let err_msg =
                            format!("bad field end. column={} value={}", field.name(), value_str);
                        return Err(xml_error(&err_msg, path, row_index));
                    }
                }
            } else {
                deserializer.de_default();
            }
        }
        Ok(())
    }
}

pub struct AligningStateWholeFile {
    #[allow(unused)]
    split_info: Arc<SplitInfo>,
    bufs: Vec<Vec<u8>>,
}

impl AligningStateTextBased for AligningStateWholeFile {
    fn try_create(_ctx: &Arc<InputContext>, split_info: &Arc<SplitInfo>) -> Result<Self> {
        Ok(Self {
            split_info: split_info.clone(),
            bufs: vec![],
        })
    }

    fn align(&mut self, buf: &[u8]) -> Result<Vec<RowBatch>> {
        self.bufs.push(buf.to_vec());
        Ok(vec![])
    }

    fn align_flush(&mut self) -> Result<Vec<RowBatch>> {
        let data = self.bufs.concat();

        Ok(vec![RowBatch {
            data,
            row_ends: vec![],
            field_ends: vec![],
            path: self.split_info.file.path.clone(),
            batch_id: 0,
            split_info: self.split_info.clone(),
            start_offset_in_split: 0,
            start_row_in_split: 0,
            start_row_of_split: Some(0),
        }])
    }
}

impl InputFormatTextBase for InputFormatXML {
    type AligningState = AligningStateWholeFile;

    fn format_type() -> StageFileFormatType {
        StageFileFormatType::Xml
    }

    fn create_field_decoder(options: &FileFormatOptionsExt) -> Arc<dyn FieldDecoder> {
        Arc::new(FieldDecoderXML::create(options))
    }

    fn deserialize(builder: &mut BlockBuilder<Self>, batch: RowBatch) -> Result<()> {
        let field_decoder = builder
            .field_decoder
            .as_any()
            .downcast_ref::<FieldDecoderXML>()
            .expect("must success");
        let columns = &mut builder.mutable_columns;

        let path = &batch.path;
        let row_tag = builder.ctx.format_options.stage.row_tag.as_bytes().to_vec();
        let field_tag = vec![b'f', b'i', b'e', b'l', b'd'];

        let mut buf = Cursor::new(&batch.data);
        let num_fields = builder.ctx.schema.fields().len();
        let reader = ParserConfig::new().create_reader(&mut buf);

        let mut rows_to_skip = builder.ctx.format_options.stage.skip_header as usize;

        let mut cols = HashMap::with_capacity(num_fields);

        let mut key = None;
        let mut has_start_row = false;
        let mut num_rows = 0;
        for e in reader {
            if rows_to_skip != 0 {
                match e {
                    Ok(XmlEvent::EndElement { name }) => {
                        // Arrived one row end and skip.
                        if name.local_name.into_bytes().eq(&row_tag) {
                            rows_to_skip -= 1;
                        }
                    }
                    Err(e) => {
                        return Err(xml_error(e.msg(), path, num_rows));
                    }
                    _ => {}
                }
            } else {
                match e {
                    Ok(XmlEvent::StartElement {
                        name, attributes, ..
                    }) => {
                        let name_byte = name.local_name.clone().into_bytes();
                        match attributes.is_empty() {
                            true => {
                                // Column names as tags and column values as the content of these tags.
                                if !name_byte.eq(&row_tag) && has_start_row {
                                    key = Some(name.local_name);
                                } else if name_byte.eq(&row_tag) {
                                    has_start_row = true;
                                }
                            }
                            false => {
                                // Column name as attributes and column values as attribute values.
                                if name_byte.eq(&row_tag) {
                                    for attr in attributes {
                                        let key = attr.name.local_name;
                                        let value = attr.value;
                                        cols.insert(key, value.into_bytes());
                                    }
                                } else if name_byte.eq(&field_tag) {
                                    if attributes.len() > 1 {
                                        return Err(xml_error(
                                            &format!(
                                                "invalid field tag, expect 1 attr, but got {}",
                                                attributes.len()
                                            ),
                                            path,
                                            num_rows,
                                        ));
                                    }
                                    let attr = attributes.get(0).unwrap();
                                    key = Some(attr.value.clone());
                                }
                            }
                        }
                    }
                    Ok(XmlEvent::EndElement { name }) => {
                        if name.local_name.into_bytes().eq(&row_tag) {
                            if let Err(e) = Self::read_row(
                                field_decoder,
                                &mut cols,
                                columns,
                                &builder.ctx.schema,
                                &batch.path,
                                num_rows,
                            ) {
                                if builder.ctx.on_error_mode == OnErrorMode::Continue {
                                    columns.iter_mut().for_each(|c| {
                                        // check if parts of columns inserted data, if so, pop it.
                                        if c.len() > num_rows {
                                            c.pop_data_value().expect("must success");
                                        }
                                    });
                                    continue;
                                } else {
                                    return Err(e);
                                }
                            };
                            cols.clear();
                            has_start_row = false;
                            num_rows += 1;
                        }
                    }
                    Ok(XmlEvent::Characters(v)) => {
                        if let Some(key) = key.take() {
                            cols.insert(key, v.into_bytes());
                        }
                    }
                    Err(e) => {
                        return Err(xml_error(e.msg(), path, num_rows));
                    }
                    _ => {}
                }
            }
        }
        Ok(())
    }
}

fn xml_error(msg: &str, path: &str, row: usize) -> ErrorCode {
    let row = row + 1;
    let msg = format!("fail to parse XML {path}:{row} {msg} ");

    ErrorCode::BadBytes(msg)
}
