# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: task.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\ntask.proto\x12\ttaskproto"\xe9\x01\n\x0fScheduleOptions\x12\x15\n\x08interval\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x11\n\x04\x63ron\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x16\n\ttime_zone\x18\x03 \x01(\tH\x02\x88\x01\x01\x12>\n\rschedule_type\x18\x04 \x01(\x0e\x32\'.taskproto.ScheduleOptions.ScheduleType"0\n\x0cScheduleType\x12\x11\n\rinterval_type\x10\x00\x12\r\n\tcron_type\x10\x01\x42\x0b\n\t_intervalB\x07\n\x05_cronB\x0c\n\n_time_zone"t\n\x10WarehouseOptions\x12\x16\n\twarehouse\x18\x01 \x01(\tH\x00\x88\x01\x01\x12!\n\x14using_warehouse_size\x18\x02 \x01(\tH\x01\x88\x01\x01\x42\x0c\n\n_warehouseB\x17\n\x15_using_warehouse_size"\xd4\x02\n\x11\x43reateTaskRequest\x12\x11\n\ttask_name\x18\x01 \x01(\t\x12\x11\n\ttenant_id\x18\x02 \x01(\t\x12\x12\n\nquery_text\x18\x03 \x01(\t\x12\r\n\x05owner\x18\x04 \x01(\t\x12\x14\n\x07\x63omment\x18\x05 \x01(\tH\x00\x88\x01\x01\x12\x34\n\x10schedule_options\x18\x07 \x01(\x0b\x32\x1a.taskproto.ScheduleOptions\x12\x36\n\x11warehouse_options\x18\x08 \x01(\x0b\x32\x1b.taskproto.WarehouseOptions\x12,\n\x1fsuspend_task_after_num_failures\x18\t \x01(\x05H\x01\x88\x01\x01\x12\x14\n\x0cif_not_exist\x18\n \x01(\x08\x42\n\n\x08_commentB"\n _suspend_task_after_num_failures"8\n\tTaskError\x12\x0c\n\x04kind\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0c\n\x04\x63ode\x18\x03 \x01(\x05"Y\n\x12\x43reateTaskResponse\x12(\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x14.taskproto.TaskErrorH\x00\x88\x01\x01\x12\x0f\n\x07task_id\x18\x02 \x01(\x04\x42\x08\n\x06_error"I\n\x0f\x44ropTaskRequest\x12\x11\n\ttenant_id\x18\x01 \x01(\t\x12\x11\n\ttask_name\x18\x02 \x01(\t\x12\x10\n\x08if_exist\x18\x03 \x01(\x08"F\n\x10\x44ropTaskResponse\x12(\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x14.taskproto.TaskErrorH\x00\x88\x01\x01\x42\x08\n\x06_error":\n\x12\x45xecuteTaskRequest\x12\x11\n\ttenant_id\x18\x01 \x01(\t\x12\x11\n\ttask_name\x18\x02 \x01(\t"I\n\x13\x45xecuteTaskResponse\x12(\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x14.taskproto.TaskErrorH\x00\x88\x01\x01\x42\x08\n\x06_error"M\n\x13\x44\x65scribeTaskRequest\x12\x11\n\ttenant_id\x18\x01 \x01(\t\x12\x11\n\ttask_name\x18\x02 \x01(\t\x12\x10\n\x08if_exist\x18\x03 \x01(\x08"\x91\x04\n\x04Task\x12\x0f\n\x07task_id\x18\x01 \x01(\x04\x12\x11\n\ttask_name\x18\x02 \x01(\t\x12\x12\n\nquery_text\x18\x04 \x01(\t\x12\x14\n\x07\x63omment\x18\x05 \x01(\tH\x00\x88\x01\x01\x12\r\n\x05owner\x18\x06 \x01(\t\x12\x34\n\x10schedule_options\x18\x07 \x01(\x0b\x32\x1a.taskproto.ScheduleOptions\x12\x36\n\x11warehouse_options\x18\x08 \x01(\x0b\x32\x1b.taskproto.WarehouseOptions\x12\x1e\n\x11next_scheduled_at\x18\t \x01(\tH\x01\x88\x01\x01\x12,\n\x1fsuspend_task_after_num_failures\x18\n \x01(\x05H\x02\x88\x01\x01\x12&\n\x06status\x18\x0c \x01(\x0e\x32\x16.taskproto.Task.Status\x12\x12\n\ncreated_at\x18\x0e \x01(\t\x12\x12\n\nupdated_at\x18\x0f \x01(\t\x12\x1e\n\x11last_suspended_at\x18\x10 \x01(\tH\x03\x88\x01\x01"$\n\x06Status\x12\r\n\tSuspended\x10\x00\x12\x0b\n\x07Started\x10\x01\x42\n\n\x08_commentB\x14\n\x12_next_scheduled_atB"\n _suspend_task_after_num_failuresB\x14\n\x12_last_suspended_at"i\n\x14\x44\x65scribeTaskResponse\x12\x1d\n\x04task\x18\x01 \x01(\x0b\x32\x0f.taskproto.Task\x12(\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x14.taskproto.TaskErrorH\x00\x88\x01\x01\x42\x08\n\x06_error"p\n\x10ShowTasksRequest\x12\x11\n\ttenant_id\x18\x01 \x01(\t\x12\x11\n\tname_like\x18\x02 \x01(\t\x12\x14\n\x0cresult_limit\x18\x04 \x01(\x05\x12\x0e\n\x06owners\x18\x05 \x03(\t\x12\x10\n\x08task_ids\x18\x06 \x03(\t"g\n\x11ShowTasksResponse\x12\x1e\n\x05tasks\x18\x01 \x03(\x0b\x32\x0f.taskproto.Task\x12(\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x14.taskproto.TaskErrorH\x00\x88\x01\x01\x42\x08\n\x06_error"\xe8\x03\n\x10\x41lterTaskRequest\x12\x11\n\ttask_name\x18\x01 \x01(\t\x12\x11\n\ttenant_id\x18\x02 \x01(\t\x12\x17\n\nquery_text\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x14\n\x07\x63omment\x18\x04 \x01(\tH\x01\x88\x01\x01\x12\x42\n\x0f\x61lter_task_type\x18\x05 \x01(\x0e\x32).taskproto.AlterTaskRequest.AlterTaskType\x12\r\n\x05owner\x18\x06 \x01(\t\x12\x34\n\x10schedule_options\x18\x07 \x01(\x0b\x32\x1a.taskproto.ScheduleOptions\x12\x10\n\x08if_exist\x18\x08 \x01(\x08\x12\x36\n\x11warehouse_options\x18\t \x01(\x0b\x32\x1b.taskproto.WarehouseOptions\x12,\n\x1fsuspend_task_after_num_failures\x18\n \x01(\x05H\x02\x88\x01\x01"?\n\rAlterTaskType\x12\x0b\n\x07Suspend\x10\x00\x12\n\n\x06Resume\x10\x01\x12\x07\n\x03Set\x10\x02\x12\x0c\n\x08ModifyAs\x10\x03\x42\r\n\x0b_query_textB\n\n\x08_commentB"\n _suspend_task_after_num_failures"f\n\x11\x41lterTaskResponse\x12(\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x14.taskproto.TaskErrorH\x00\x88\x01\x01\x12\x1d\n\x04task\x18\x02 \x01(\x0b\x32\x0f.taskproto.TaskB\x08\n\x06_error"\xc1\x01\n\x13ShowTaskRunsRequest\x12\x11\n\ttenant_id\x18\x01 \x01(\t\x12\x1c\n\x14scheduled_time_start\x18\x02 \x01(\t\x12\x1a\n\x12scheduled_time_end\x18\x03 \x01(\t\x12\x14\n\x0cresult_limit\x18\x04 \x01(\x05\x12\x12\n\nerror_only\x18\x05 \x01(\x08\x12\x0e\n\x06owners\x18\x06 \x03(\t\x12\x10\n\x08task_ids\x18\x07 \x03(\t\x12\x11\n\ttask_name\x18\x08 \x01(\t"\xb1\x04\n\x07TaskRun\x12\x0f\n\x07task_id\x18\x01 \x01(\x04\x12\x11\n\ttask_name\x18\x02 \x01(\t\x12\x11\n\ttenant_id\x18\x03 \x01(\t\x12\x12\n\nquery_text\x18\x04 \x01(\t\x12\x14\n\x07\x63omment\x18\x05 \x01(\tH\x00\x88\x01\x01\x12\r\n\x05owner\x18\x06 \x01(\t\x12\x34\n\x10schedule_options\x18\x07 \x01(\x0b\x32\x1a.taskproto.ScheduleOptions\x12\x0e\n\x06run_id\x18\x08 \x01(\t\x12\x16\n\x0e\x61ttempt_number\x18\t \x01(\x05\x12\x36\n\x11warehouse_options\x18\n \x01(\x0b\x32\x1b.taskproto.WarehouseOptions\x12\'\n\x05state\x18\x0b \x01(\x0e\x32\x18.taskproto.TaskRun.State\x12\x12\n\nerror_code\x18\x0c \x01(\x03\x12\x1a\n\rerror_message\x18\r \x01(\tH\x01\x88\x01\x01\x12\x16\n\x0escheduled_time\x18\x0e \x01(\t\x12\x1b\n\x0e\x63ompleted_time\x18\x10 \x01(\tH\x02\x88\x01\x01\x12\x10\n\x08query_id\x18\x11 \x01(\t"O\n\x05State\x12\r\n\tSCHEDULED\x10\x00\x12\r\n\tEXECUTING\x10\x01\x12\r\n\tSUCCEEDED\x10\x02\x12\n\n\x06\x46\x41ILED\x10\x03\x12\r\n\tCANCELLED\x10\x04\x42\n\n\x08_commentB\x10\n\x0e_error_messageB\x11\n\x0f_completed_time"q\n\x14ShowTaskRunsResponse\x12%\n\ttask_runs\x18\x01 \x03(\x0b\x32\x12.taskproto.TaskRun\x12(\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x14.taskproto.TaskErrorH\x00\x88\x01\x01\x42\x08\n\x06_error2\x9d\x04\n\x0bTaskService\x12I\n\nCreateTask\x12\x1c.taskproto.CreateTaskRequest\x1a\x1d.taskproto.CreateTaskResponse\x12O\n\x0c\x44\x65scribeTask\x12\x1e.taskproto.DescribeTaskRequest\x1a\x1f.taskproto.DescribeTaskResponse\x12L\n\x0b\x45xecuteTask\x12\x1d.taskproto.ExecuteTaskRequest\x1a\x1e.taskproto.ExecuteTaskResponse\x12\x43\n\x08\x44ropTask\x12\x1a.taskproto.DropTaskRequest\x1a\x1b.taskproto.DropTaskResponse\x12\x46\n\tAlterTask\x12\x1b.taskproto.AlterTaskRequest\x1a\x1c.taskproto.AlterTaskResponse\x12\x46\n\tShowTasks\x12\x1b.taskproto.ShowTasksRequest\x1a\x1c.taskproto.ShowTasksResponse\x12O\n\x0cShowTaskRuns\x12\x1e.taskproto.ShowTaskRunsRequest\x1a\x1f.taskproto.ShowTaskRunsResponseB!Z\x1f\x64\x61tabend.com/cloudcontrol/protob\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "task_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"Z\037databend.com/cloudcontrol/proto"
    _globals["_SCHEDULEOPTIONS"]._serialized_start = 26
    _globals["_SCHEDULEOPTIONS"]._serialized_end = 259
    _globals["_SCHEDULEOPTIONS_SCHEDULETYPE"]._serialized_start = 175
    _globals["_SCHEDULEOPTIONS_SCHEDULETYPE"]._serialized_end = 223
    _globals["_WAREHOUSEOPTIONS"]._serialized_start = 261
    _globals["_WAREHOUSEOPTIONS"]._serialized_end = 377
    _globals["_CREATETASKREQUEST"]._serialized_start = 380
    _globals["_CREATETASKREQUEST"]._serialized_end = 720
    _globals["_TASKERROR"]._serialized_start = 722
    _globals["_TASKERROR"]._serialized_end = 778
    _globals["_CREATETASKRESPONSE"]._serialized_start = 780
    _globals["_CREATETASKRESPONSE"]._serialized_end = 869
    _globals["_DROPTASKREQUEST"]._serialized_start = 871
    _globals["_DROPTASKREQUEST"]._serialized_end = 944
    _globals["_DROPTASKRESPONSE"]._serialized_start = 946
    _globals["_DROPTASKRESPONSE"]._serialized_end = 1016
    _globals["_EXECUTETASKREQUEST"]._serialized_start = 1018
    _globals["_EXECUTETASKREQUEST"]._serialized_end = 1076
    _globals["_EXECUTETASKRESPONSE"]._serialized_start = 1078
    _globals["_EXECUTETASKRESPONSE"]._serialized_end = 1151
    _globals["_DESCRIBETASKREQUEST"]._serialized_start = 1153
    _globals["_DESCRIBETASKREQUEST"]._serialized_end = 1230
    _globals["_TASK"]._serialized_start = 1233
    _globals["_TASK"]._serialized_end = 1762
    _globals["_TASK_STATUS"]._serialized_start = 1634
    _globals["_TASK_STATUS"]._serialized_end = 1670
    _globals["_DESCRIBETASKRESPONSE"]._serialized_start = 1764
    _globals["_DESCRIBETASKRESPONSE"]._serialized_end = 1869
    _globals["_SHOWTASKSREQUEST"]._serialized_start = 1871
    _globals["_SHOWTASKSREQUEST"]._serialized_end = 1983
    _globals["_SHOWTASKSRESPONSE"]._serialized_start = 1985
    _globals["_SHOWTASKSRESPONSE"]._serialized_end = 2088
    _globals["_ALTERTASKREQUEST"]._serialized_start = 2091
    _globals["_ALTERTASKREQUEST"]._serialized_end = 2579
    _globals["_ALTERTASKREQUEST_ALTERTASKTYPE"]._serialized_start = 2453
    _globals["_ALTERTASKREQUEST_ALTERTASKTYPE"]._serialized_end = 2516
    _globals["_ALTERTASKRESPONSE"]._serialized_start = 2581
    _globals["_ALTERTASKRESPONSE"]._serialized_end = 2683
    _globals["_SHOWTASKRUNSREQUEST"]._serialized_start = 2686
    _globals["_SHOWTASKRUNSREQUEST"]._serialized_end = 2879
    _globals["_TASKRUN"]._serialized_start = 2882
    _globals["_TASKRUN"]._serialized_end = 3443
    _globals["_TASKRUN_STATE"]._serialized_start = 3315
    _globals["_TASKRUN_STATE"]._serialized_end = 3394
    _globals["_SHOWTASKRUNSRESPONSE"]._serialized_start = 3445
    _globals["_SHOWTASKRUNSRESPONSE"]._serialized_end = 3558
    _globals["_TASKSERVICE"]._serialized_start = 3561
    _globals["_TASKSERVICE"]._serialized_end = 4102
# @@protoc_insertion_point(module_scope)
