// Copyright 2022 Datafuse Labs.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use std::collections::HashMap;
use std::collections::HashSet;
use std::fs::File;

use common_arrow::arrow::array::UInt64Array;
use common_arrow::arrow::buffer::Buffer;
use common_arrow::arrow::datatypes::DataType as ArrowDataType;
use common_arrow::arrow::datatypes::Field as ArrowField;
use common_arrow::arrow::datatypes::Schema as ArrowSchema;
use common_arrow::arrow::io::parquet::read as pread;
use common_arrow::parquet::metadata::FileMetaData;
use common_arrow::parquet::metadata::RowGroupMetaData;
use common_exception::ErrorCode;
use common_exception::Result;
use common_expression::types::DataType;
use common_expression::Column;
use common_expression::TableDataType;
use storages_common_table_meta::meta::ColumnStatistics;
use storages_common_table_meta::meta::StatisticsOfColumns;

use crate::ParquetReader;

fn lower_field_name(field: &mut ArrowField) {
    field.name = field.name.to_lowercase();
    match &mut field.data_type {
        ArrowDataType::List(f)
        | ArrowDataType::LargeList(f)
        | ArrowDataType::FixedSizeList(f, _) => {
            lower_field_name(f.as_mut());
        }
        ArrowDataType::Struct(ref mut fields) => {
            for f in fields {
                lower_field_name(f);
            }
        }
        _ => {}
    }
}

impl ParquetReader {
    pub fn read_meta(location: &str) -> Result<FileMetaData> {
        let mut file = File::open(location).map_err(|e| {
            ErrorCode::Internal(format!("Failed to open file '{location}': {e}"))
        })?;
        pread::read_metadata(&mut file).map_err(|e| {
            ErrorCode::Internal(format!(
                "Read parquet file '{location}''s meta error: {e}"
            ))
        })
    }

    #[inline]
    pub fn infer_schema(meta: &FileMetaData) -> Result<ArrowSchema> {
        let mut arrow_schema = pread::infer_schema(meta)?;
        arrow_schema.fields.iter_mut().for_each(|f| {
            lower_field_name(f);
        });
        Ok(arrow_schema)
    }

    /// Collect statistics of a batch of row groups of the specified columns.
    ///
    /// The retuened vector's length is the same as `rgs`.
    pub fn collect_row_group_stats(
        schema: &ArrowSchema,
        rgs: &[RowGroupMetaData],
        indices: &HashSet<usize>,
    ) -> Result<Vec<StatisticsOfColumns>> {
        let mut stats = Vec::with_capacity(rgs.len());
        let mut stats_of_row_groups = HashMap::with_capacity(rgs.len());

        for index in indices {
            if rgs
                .iter()
                .any(|rg| rg.columns()[*index].metadata().statistics.is_none())
            {
                return Err(ErrorCode::InvalidArgument(
                    "Some columns of the row groups have no statistics",
                ));
            }

            let field = &schema.fields[*index];
            let table_type: TableDataType = field.into();
            let data_type = (&table_type).into();
            let column_stats = pread::statistics::deserialize(field, rgs)?;
            stats_of_row_groups.insert(
                *index,
                BatchStatistics::from_statistics(column_stats, &data_type)?,
            );
        }

        for (rg_idx, _) in rgs.iter().enumerate() {
            let mut cols_stats = HashMap::with_capacity(stats.capacity());
            for index in indices {
                let col_stats = stats_of_row_groups[index].get(rg_idx);
                cols_stats.insert(*index as u32, col_stats);
            }
            stats.push(cols_stats);
        }

        Ok(stats)
    }
}

/// A temporary struct to present [`pread::statistics::Statistics`].
///
/// Convert the inner fields into Databend data structures.
pub struct BatchStatistics {
    pub null_count: Buffer<u64>,
    pub distinct_count: Buffer<u64>,
    pub min_values: Column,
    pub max_values: Column,
}

impl BatchStatistics {
    pub fn get(&self, index: usize) -> ColumnStatistics {
        ColumnStatistics {
            min: unsafe { self.min_values.index_unchecked(index).to_owned() },
            max: unsafe { self.max_values.index_unchecked(index).to_owned() },
            null_count: self.null_count[index],
            in_memory_size: 0, // this field is not used.
            distinct_of_values: Some(self.distinct_count[index]),
        }
    }

    pub fn from_statistics(
        stats: pread::statistics::Statistics,
        data_type: &DataType,
    ) -> Result<Self> {
        let null_count = stats
            .null_count
            .as_any()
            .downcast_ref::<UInt64Array>()
            .ok_or_else(|| {
                ErrorCode::Internal(format!(
                    "null_count should be UInt64Array, but is {:?}",
                    stats.null_count.data_type()
                ))
            })?
            .values()
            .clone();
        let distinct_count = stats
            .distinct_count
            .as_any()
            .downcast_ref::<UInt64Array>()
            .ok_or_else(|| {
                ErrorCode::Internal(format!(
                    "distinct_count should be UInt64Array, but is {:?}",
                    stats.distinct_count.data_type()
                ))
            })?
            .values()
            .clone();
        let min_values = Column::from_arrow(&*stats.min_value, data_type);
        let max_values = Column::from_arrow(&*stats.max_value, data_type);
        Ok(Self {
            null_count,
            distinct_count,
            min_values,
            max_values,
        })
    }
}
