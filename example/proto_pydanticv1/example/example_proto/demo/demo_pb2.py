# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example/example_proto/demo/demo.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from example.proto_pydanticv1.example.example_proto.common import single_pb2 as example_dot_example__proto_dot_common_dot_single__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%example/example_proto/demo/demo.proto\x12\x04user\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a google/protobuf/field_mask.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a)example/example_proto/common/single.proto\"\xc3\x01\n\x0bUserMessage\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x0b\n\x03\x61ge\x18\x02 \x01(\x05\x12\x0e\n\x06height\x18\x03 \x01(\x02\x12\x1a\n\x03sex\x18\x04 \x01(\x0e\x32\r.user.SexType\x12\x1e\n\x04\x64\x65mo\x18\x06 \x01(\x0e\x32\x10.single.DemoEnum\x12\x10\n\x08is_adult\x18\x07 \x01(\x08\x12\x11\n\tuser_name\x18\x08 \x01(\t\x12)\n\x0c\x64\x65mo_message\x18\t \x01(\x0b\x32\x13.single.DemoMessage\"\xb1\x01\n\x0cOtherMessage\x12)\n\x08metadata\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x32\n\x0c\x64ouble_value\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x33\n\nfield_mask\x18\x64 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskH\x00\x88\x01\x01\x42\r\n\x0b_field_mask\"\xe4\x01\n\nMapMessage\x12/\n\x08user_map\x18\x01 \x03(\x0b\x32\x1d.user.MapMessage.UserMapEntry\x12\x31\n\tuser_flag\x18\x02 \x03(\x0b\x32\x1e.user.MapMessage.UserFlagEntry\x1a\x41\n\x0cUserMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12 \n\x05value\x18\x02 \x01(\x0b\x32\x11.user.UserMessage:\x02\x38\x01\x1a/\n\rUserFlagEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x08:\x02\x38\x01\"[\n\x0fRepeatedMessage\x12\x10\n\x08str_list\x18\x01 \x03(\t\x12\x10\n\x08int_list\x18\x02 \x03(\x05\x12$\n\tuser_list\x18\x03 \x03(\x0b\x32\x11.user.UserMessage\"\x99\x05\n\rNestedMessage\x12;\n\ruser_list_map\x18\x01 \x03(\x0b\x32$.user.NestedMessage.UserListMapEntry\x12\x32\n\x08user_map\x18\x02 \x03(\x0b\x32 .user.NestedMessage.UserMapEntry\x12\x34\n\x08user_pay\x18\x03 \x01(\x0b\x32\".user.NestedMessage.UserPayMessage\x12\x35\n\x0cinclude_enum\x18\x04 \x01(\x0e\x32\x1f.user.NestedMessage.IncludeEnum\x12?\n\x13not_enable_user_pay\x18\x05 \x01(\x0b\x32\".user.NestedMessage.UserPayMessage\x12%\n\x05\x65mpty\x18\x06 \x01(\x0b\x32\x16.google.protobuf.Empty\x12,\n\x0b\x61\x66ter_refer\x18\x07 \x01(\x0b\x32\x17.user.AfterReferMessage\x1a\\\n\x0eUserPayMessage\x12\x13\n\x0b\x62\x61nk_number\x18\x01 \x01(\t\x12\'\n\x03\x65xp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04uuid\x18\x03 \x01(\t\x1aI\n\x10UserListMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12$\n\x05value\x18\x02 \x01(\x0b\x32\x15.user.RepeatedMessage:\x02\x38\x01\x1a@\n\x0cUserMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1f\n\x05value\x18\x02 \x01(\x0b\x32\x10.user.MapMessage:\x02\x38\x01\")\n\x0bIncludeEnum\x12\x08\n\x04zero\x10\x00\x12\x07\n\x03one\x10\x01\x12\x07\n\x03two\x10\x02\"-\n\x11\x41\x66terReferMessage\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x0b\n\x03\x61ge\x18\x02 \x01(\x05\"_\n\x0bInvoiceItem\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x05\x12\x10\n\x08quantity\x18\x03 \x01(\x05\x12 \n\x05items\x18\x04 \x03(\x0b\x32\x11.user.InvoiceItem\"\x0e\n\x0c\x45mptyMessage\"\xa9\x02\n\x0fOptionalMessage\x12\x0b\n\x01x\x18\x01 \x01(\tH\x00\x12\x0b\n\x01y\x18\x02 \x01(\x05H\x00\x12\x11\n\x04name\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x10\n\x03\x61ge\x18\x04 \x01(\x05H\x02\x88\x01\x01\x12$\n\x04item\x18\x05 \x01(\x0b\x32\x11.user.InvoiceItemH\x03\x88\x01\x01\x12\x10\n\x08str_list\x18\x06 \x03(\t\x12\x32\n\x07int_map\x18\x07 \x03(\x0b\x32!.user.OptionalMessage.IntMapEntry\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x08 \x01(\x02\x1a-\n\x0bIntMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x42\x03\n\x01\x61\x42\x07\n\x05_nameB\x06\n\x04_ageB\x07\n\x05_item\"\x82\x01\n\x0cInvoiceItem2\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x05\x12\x10\n\x08quantity\x18\x03 \x01(\x05\x12!\n\x05items\x18\x04 \x03(\x0b\x32\x12.user.InvoiceItem2\x12\x1f\n\x07invoice\x18\x05 \x01(\x0b\x32\x0e.user.Invoice3\"]\n\x08Invoice3\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x05\x12\x10\n\x08quantity\x18\x03 \x01(\x05\x12!\n\x05items\x18\x04 \x03(\x0b\x32\x12.user.InvoiceItem2\"C\n\x0bRootMessage\x12\x0e\n\x06\x66ield1\x18\x01 \x01(\t\x12$\n\x06\x66ield2\x18\x02 \x01(\x0b\x32\x14.user.AnOtherMessage\"m\n\x0e\x41nOtherMessage\x12\x0e\n\x06\x66ield1\x18\x01 \x01(\t\x12/\n\x06\x66ield2\x18\x02 \x01(\x0b\x32\x1f.user.AnOtherMessage.SubMessage\x1a\x1a\n\nSubMessage\x12\x0c\n\x04text\x18\x01 \x01(\t\"\xc4\x01\n\rTestSameName0\x12&\n\x04\x62ody\x18\x01 \x01(\x0b\x32\x18.user.TestSameName0.Body\x1a\x8a\x01\n\x04\x42ody\x12\x13\n\x0binput_model\x18\x01 \x01(\t\x12;\n\ninput_info\x18\x03 \x03(\x0b\x32\'.user.TestSameName0.Body.InputInfoEntry\x1a\x30\n\x0eInputInfoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xc8\x01\n\rTestSameName1\x12&\n\x04\x62ody\x18\x01 \x01(\x0b\x32\x18.user.TestSameName1.Body\x1a\x8e\x01\n\x04\x42ody\x12\x14\n\x0coutput_model\x18\x01 \x01(\t\x12=\n\x0boutput_info\x18\x03 \x03(\x0b\x32(.user.TestSameName1.Body.OutputInfoEntry\x1a\x31\n\x0fOutputInfoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xa8\x01\n\x08\x44\x65moResp\x12\x30\n\tdemoState\x18\x01 \x03(\x0b\x32\x1d.user.DemoResp.DemoStateEntry\x12\x11\n\tpramsArea\x18\x02 \x01(\x03\x12\x14\n\x0cparamsSeason\x18\x03 \x01(\x08\x1a\x41\n\x0e\x44\x65moStateEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x1e\n\x05value\x18\x02 \x01(\x0b\x32\x0f.user.DemoState:\x02\x38\x01\"\x1e\n\tDemoState\x12\x11\n\tparamsDID\x18\x04 \x01(\x03\"J\n\x18WithOptionalEnumMsgEntry\x12%\n\x04\x65num\x18\x01 \x01(\x0e\x32\x12.user.OptionalEnumH\x00\x88\x01\x01\x42\x07\n\x05_enum*\x1d\n\x07SexType\x12\x07\n\x03man\x10\x00\x12\t\n\x05women\x10\x01*)\n\x0cOptionalEnum\x12\x07\n\x03\x46OO\x10\x00\x12\x07\n\x03\x42\x41R\x10\x01\x12\x07\n\x03\x42\x41Z\x10\x02\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'example.example_proto.demo.demo_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MAPMESSAGE_USERMAPENTRY._options = None
  _MAPMESSAGE_USERMAPENTRY._serialized_options = b'8\001'
  _MAPMESSAGE_USERFLAGENTRY._options = None
  _MAPMESSAGE_USERFLAGENTRY._serialized_options = b'8\001'
  _NESTEDMESSAGE_USERLISTMAPENTRY._options = None
  _NESTEDMESSAGE_USERLISTMAPENTRY._serialized_options = b'8\001'
  _NESTEDMESSAGE_USERMAPENTRY._options = None
  _NESTEDMESSAGE_USERMAPENTRY._serialized_options = b'8\001'
  _OPTIONALMESSAGE_INTMAPENTRY._options = None
  _OPTIONALMESSAGE_INTMAPENTRY._serialized_options = b'8\001'
  _TESTSAMENAME0_BODY_INPUTINFOENTRY._options = None
  _TESTSAMENAME0_BODY_INPUTINFOENTRY._serialized_options = b'8\001'
  _TESTSAMENAME1_BODY_OUTPUTINFOENTRY._options = None
  _TESTSAMENAME1_BODY_OUTPUTINFOENTRY._serialized_options = b'8\001'
  _DEMORESP_DEMOSTATEENTRY._options = None
  _DEMORESP_DEMOSTATEENTRY._serialized_options = b'8\001'
  _SEXTYPE._serialized_start=3167
  _SEXTYPE._serialized_end=3196
  _OPTIONALENUM._serialized_start=3198
  _OPTIONALENUM._serialized_end=3239
  _USERMESSAGE._serialized_start=249
  _USERMESSAGE._serialized_end=444
  _OTHERMESSAGE._serialized_start=447
  _OTHERMESSAGE._serialized_end=624
  _MAPMESSAGE._serialized_start=627
  _MAPMESSAGE._serialized_end=855
  _MAPMESSAGE_USERMAPENTRY._serialized_start=741
  _MAPMESSAGE_USERMAPENTRY._serialized_end=806
  _MAPMESSAGE_USERFLAGENTRY._serialized_start=808
  _MAPMESSAGE_USERFLAGENTRY._serialized_end=855
  _REPEATEDMESSAGE._serialized_start=857
  _REPEATEDMESSAGE._serialized_end=948
  _NESTEDMESSAGE._serialized_start=951
  _NESTEDMESSAGE._serialized_end=1616
  _NESTEDMESSAGE_USERPAYMESSAGE._serialized_start=1340
  _NESTEDMESSAGE_USERPAYMESSAGE._serialized_end=1432
  _NESTEDMESSAGE_USERLISTMAPENTRY._serialized_start=1434
  _NESTEDMESSAGE_USERLISTMAPENTRY._serialized_end=1507
  _NESTEDMESSAGE_USERMAPENTRY._serialized_start=1509
  _NESTEDMESSAGE_USERMAPENTRY._serialized_end=1573
  _NESTEDMESSAGE_INCLUDEENUM._serialized_start=1575
  _NESTEDMESSAGE_INCLUDEENUM._serialized_end=1616
  _AFTERREFERMESSAGE._serialized_start=1618
  _AFTERREFERMESSAGE._serialized_end=1663
  _INVOICEITEM._serialized_start=1665
  _INVOICEITEM._serialized_end=1760
  _EMPTYMESSAGE._serialized_start=1762
  _EMPTYMESSAGE._serialized_end=1776
  _OPTIONALMESSAGE._serialized_start=1779
  _OPTIONALMESSAGE._serialized_end=2076
  _OPTIONALMESSAGE_INTMAPENTRY._serialized_start=2000
  _OPTIONALMESSAGE_INTMAPENTRY._serialized_end=2045
  _INVOICEITEM2._serialized_start=2079
  _INVOICEITEM2._serialized_end=2209
  _INVOICE3._serialized_start=2211
  _INVOICE3._serialized_end=2304
  _ROOTMESSAGE._serialized_start=2306
  _ROOTMESSAGE._serialized_end=2373
  _ANOTHERMESSAGE._serialized_start=2375
  _ANOTHERMESSAGE._serialized_end=2484
  _ANOTHERMESSAGE_SUBMESSAGE._serialized_start=2458
  _ANOTHERMESSAGE_SUBMESSAGE._serialized_end=2484
  _TESTSAMENAME0._serialized_start=2487
  _TESTSAMENAME0._serialized_end=2683
  _TESTSAMENAME0_BODY._serialized_start=2545
  _TESTSAMENAME0_BODY._serialized_end=2683
  _TESTSAMENAME0_BODY_INPUTINFOENTRY._serialized_start=2635
  _TESTSAMENAME0_BODY_INPUTINFOENTRY._serialized_end=2683
  _TESTSAMENAME1._serialized_start=2686
  _TESTSAMENAME1._serialized_end=2886
  _TESTSAMENAME1_BODY._serialized_start=2744
  _TESTSAMENAME1_BODY._serialized_end=2886
  _TESTSAMENAME1_BODY_OUTPUTINFOENTRY._serialized_start=2837
  _TESTSAMENAME1_BODY_OUTPUTINFOENTRY._serialized_end=2886
  _DEMORESP._serialized_start=2889
  _DEMORESP._serialized_end=3057
  _DEMORESP_DEMOSTATEENTRY._serialized_start=2992
  _DEMORESP_DEMOSTATEENTRY._serialized_end=3057
  _DEMOSTATE._serialized_start=3059
  _DEMOSTATE._serialized_end=3089
  _WITHOPTIONALENUMMSGENTRY._serialized_start=3091
  _WITHOPTIONALENUMMSGENTRY._serialized_end=3165
# @@protoc_insertion_point(module_scope)
