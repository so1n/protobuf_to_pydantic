# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example/example_proto/demo/diff_pkg_refer_2.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from example.proto_3_20_pydanticv1.example.example_proto.demo import diff_pkg_refer_1_pb2 as example_dot_example__proto_dot_demo_dot_diff__pkg__refer__1__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='example/example_proto/demo/diff_pkg_refer_2.proto',
  package='diff_pkg_refer_2',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n1example/example_proto/demo/diff_pkg_refer_2.proto\x12\x10\x64iff_pkg_refer_2\x1a\x31\x65xample/example_proto/demo/diff_pkg_refer_1.proto\"\x87\x01\n\x05\x44\x65mo2\x12\x35\n\x07myField\x18\x01 \x03(\x0b\x32$.diff_pkg_refer_2.Demo2.MyFieldEntry\x1aG\n\x0cMyFieldEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.diff_pkg_refer_1.Demo1:\x02\x38\x01\x62\x06proto3'
  ,
  dependencies=[example_dot_example__proto_dot_demo_dot_diff__pkg__refer__1__pb2.DESCRIPTOR,])




_DEMO2_MYFIELDENTRY = _descriptor.Descriptor(
  name='MyFieldEntry',
  full_name='diff_pkg_refer_2.Demo2.MyFieldEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='diff_pkg_refer_2.Demo2.MyFieldEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='diff_pkg_refer_2.Demo2.MyFieldEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=187,
  serialized_end=258,
)

_DEMO2 = _descriptor.Descriptor(
  name='Demo2',
  full_name='diff_pkg_refer_2.Demo2',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='myField', full_name='diff_pkg_refer_2.Demo2.myField', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_DEMO2_MYFIELDENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=123,
  serialized_end=258,
)

_DEMO2_MYFIELDENTRY.fields_by_name['value'].message_type = example_dot_example__proto_dot_demo_dot_diff__pkg__refer__1__pb2._DEMO1
_DEMO2_MYFIELDENTRY.containing_type = _DEMO2
_DEMO2.fields_by_name['myField'].message_type = _DEMO2_MYFIELDENTRY
DESCRIPTOR.message_types_by_name['Demo2'] = _DEMO2
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Demo2 = _reflection.GeneratedProtocolMessageType('Demo2', (_message.Message,), {

  'MyFieldEntry' : _reflection.GeneratedProtocolMessageType('MyFieldEntry', (_message.Message,), {
    'DESCRIPTOR' : _DEMO2_MYFIELDENTRY,
    '__module__' : 'example.example_proto.demo.diff_pkg_refer_2_pb2'
    # @@protoc_insertion_point(class_scope:diff_pkg_refer_2.Demo2.MyFieldEntry)
    })
  ,
  'DESCRIPTOR' : _DEMO2,
  '__module__' : 'example.example_proto.demo.diff_pkg_refer_2_pb2'
  # @@protoc_insertion_point(class_scope:diff_pkg_refer_2.Demo2)
  })
_sym_db.RegisterMessage(Demo2)
_sym_db.RegisterMessage(Demo2.MyFieldEntry)


_DEMO2_MYFIELDENTRY._options = None
# @@protoc_insertion_point(module_scope)
