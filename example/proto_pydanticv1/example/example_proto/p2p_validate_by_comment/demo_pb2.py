# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example/example_proto/p2p_validate_by_comment/demo.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n8example/example_proto/p2p_validate_by_comment/demo.proto\x12\x19p2p_validate_comment_test\x1a\x19google/protobuf/any.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xcc\x03\n\tFloatTest\x12\x12\n\nconst_test\x18\x01 \x01(\x02\x12\x14\n\x0crange_e_test\x18\x02 \x01(\x02\x12\x12\n\nrange_test\x18\x03 \x01(\x02\x12\x0f\n\x07in_test\x18\x04 \x01(\x02\x12\x13\n\x0bnot_in_test\x18\x05 \x01(\x02\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x06 \x01(\x02\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x14 \x01(\x02\x12\x17\n\x0fnot_enable_test\x18\x07 \x01(\x02\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x08 \x01(\x02\x12\x19\n\x11miss_default_test\x18\t \x01(\x02\x12\x15\n\rrequired_test\x18\x13 \x01(\x02\x12\x12\n\nalias_test\x18\n \x01(\x02\x12\x11\n\tdesc_test\x18\x0b \x01(\x02\x12\x18\n\x10multiple_of_test\x18\x0c \x01(\x02\x12\x14\n\x0c\x65xample_test\x18\r \x01(\x02\x12\x17\n\x0f\x65xample_factory\x18\x0e \x01(\x02\x12\x12\n\nfield_test\x18\x0f \x01(\x02\x12\x11\n\ttype_test\x18\x10 \x01(\x02\x12\x12\n\ntitle_test\x18\x11 \x01(\x02\x12\x12\n\nextra_test\x18\x12 \x01(\x02\"\xcd\x03\n\nDoubleTest\x12\x12\n\nconst_test\x18\x01 \x01(\x01\x12\x14\n\x0crange_e_test\x18\x02 \x01(\x01\x12\x12\n\nrange_test\x18\x03 \x01(\x01\x12\x0f\n\x07in_test\x18\x04 \x01(\x01\x12\x13\n\x0bnot_in_test\x18\x05 \x01(\x01\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x06 \x01(\x01\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x14 \x01(\x01\x12\x17\n\x0fnot_enable_test\x18\x07 \x01(\x01\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x08 \x01(\x01\x12\x19\n\x11miss_default_test\x18\t \x01(\x01\x12\x15\n\rrequired_test\x18\x13 \x01(\x01\x12\x12\n\nalias_test\x18\n \x01(\x01\x12\x11\n\tdesc_test\x18\x0b \x01(\x01\x12\x18\n\x10multiple_of_test\x18\x0c \x01(\x01\x12\x14\n\x0c\x65xample_test\x18\r \x01(\x01\x12\x17\n\x0f\x65xample_factory\x18\x0e \x01(\x01\x12\x12\n\nfield_test\x18\x0f \x01(\x01\x12\x11\n\ttype_test\x18\x10 \x01(\x01\x12\x12\n\ntitle_test\x18\x11 \x01(\x01\x12\x12\n\nextra_test\x18\x12 \x01(\x01\"\xcc\x03\n\tInt32Test\x12\x12\n\nconst_test\x18\x01 \x01(\x05\x12\x14\n\x0crange_e_test\x18\x02 \x01(\x05\x12\x12\n\nrange_test\x18\x03 \x01(\x05\x12\x0f\n\x07in_test\x18\x04 \x01(\x05\x12\x13\n\x0bnot_in_test\x18\x05 \x01(\x05\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x06 \x01(\x05\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x14 \x01(\x05\x12\x17\n\x0fnot_enable_test\x18\x07 \x01(\x05\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x08 \x01(\x05\x12\x19\n\x11miss_default_test\x18\t \x01(\x05\x12\x15\n\rrequired_test\x18\x13 \x01(\x05\x12\x12\n\nalias_test\x18\n \x01(\x05\x12\x11\n\tdesc_test\x18\x0b \x01(\x05\x12\x18\n\x10multiple_of_test\x18\x0c \x01(\x05\x12\x14\n\x0c\x65xample_test\x18\r \x01(\x05\x12\x17\n\x0f\x65xample_factory\x18\x0e \x01(\x05\x12\x12\n\nfield_test\x18\x0f \x01(\x05\x12\x11\n\ttype_test\x18\x10 \x01(\x05\x12\x12\n\ntitle_test\x18\x11 \x01(\x05\x12\x12\n\nextra_test\x18\x12 \x01(\x05\"\xcc\x03\n\tInt64Test\x12\x12\n\nconst_test\x18\x01 \x01(\x03\x12\x14\n\x0crange_e_test\x18\x02 \x01(\x03\x12\x12\n\nrange_test\x18\x03 \x01(\x03\x12\x0f\n\x07in_test\x18\x04 \x01(\x03\x12\x13\n\x0bnot_in_test\x18\x05 \x01(\x03\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x06 \x01(\x03\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x14 \x01(\x03\x12\x17\n\x0fnot_enable_test\x18\x07 \x01(\x03\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x08 \x01(\x03\x12\x19\n\x11miss_default_test\x18\t \x01(\x03\x12\x15\n\rrequired_test\x18\x13 \x01(\x03\x12\x12\n\nalias_test\x18\n \x01(\x03\x12\x11\n\tdesc_test\x18\x0b \x01(\x03\x12\x18\n\x10multiple_of_test\x18\x0c \x01(\x03\x12\x14\n\x0c\x65xample_test\x18\r \x01(\x03\x12\x17\n\x0f\x65xample_factory\x18\x0e \x01(\x03\x12\x12\n\nfield_test\x18\x0f \x01(\x03\x12\x11\n\ttype_test\x18\x10 \x01(\x03\x12\x12\n\ntitle_test\x18\x11 \x01(\x03\x12\x12\n\nextra_test\x18\x12 \x01(\x03\"\xcd\x03\n\nUint32Test\x12\x12\n\nconst_test\x18\x01 \x01(\r\x12\x14\n\x0crange_e_test\x18\x02 \x01(\r\x12\x12\n\nrange_test\x18\x03 \x01(\r\x12\x0f\n\x07in_test\x18\x04 \x01(\r\x12\x13\n\x0bnot_in_test\x18\x05 \x01(\r\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x06 \x01(\r\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x14 \x01(\r\x12\x17\n\x0fnot_enable_test\x18\x07 \x01(\r\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x08 \x01(\r\x12\x19\n\x11miss_default_test\x18\t \x01(\r\x12\x15\n\rrequired_test\x18\x13 \x01(\r\x12\x12\n\nalias_test\x18\n \x01(\r\x12\x11\n\tdesc_test\x18\x0b \x01(\r\x12\x18\n\x10multiple_of_test\x18\x0c \x01(\r\x12\x14\n\x0c\x65xample_test\x18\r \x01(\r\x12\x17\n\x0f\x65xample_factory\x18\x0e \x01(\r\x12\x12\n\nfield_test\x18\x0f \x01(\r\x12\x11\n\ttype_test\x18\x10 \x01(\r\x12\x12\n\ntitle_test\x18\x11 \x01(\r\x12\x12\n\nextra_test\x18\x12 \x01(\r\"\xcd\x03\n\nSint32Test\x12\x12\n\nconst_test\x18\x01 \x01(\x11\x12\x14\n\x0crange_e_test\x18\x02 \x01(\x11\x12\x12\n\nrange_test\x18\x03 \x01(\x11\x12\x0f\n\x07in_test\x18\x04 \x01(\x11\x12\x13\n\x0bnot_in_test\x18\x05 \x01(\x11\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x06 \x01(\x11\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x14 \x01(\x11\x12\x17\n\x0fnot_enable_test\x18\x07 \x01(\x11\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x08 \x01(\x11\x12\x19\n\x11miss_default_test\x18\t \x01(\x11\x12\x15\n\rrequired_test\x18\x13 \x01(\x11\x12\x12\n\nalias_test\x18\n \x01(\x11\x12\x11\n\tdesc_test\x18\x0b \x01(\x11\x12\x18\n\x10multiple_of_test\x18\x0c \x01(\x11\x12\x14\n\x0c\x65xample_test\x18\r \x01(\x11\x12\x17\n\x0f\x65xample_factory\x18\x0e \x01(\x11\x12\x12\n\nfield_test\x18\x0f \x01(\x11\x12\x11\n\ttype_test\x18\x10 \x01(\x11\x12\x12\n\ntitle_test\x18\x11 \x01(\x11\x12\x12\n\nextra_test\x18\x12 \x01(\x11\"\xcd\x03\n\nUint64Test\x12\x12\n\nconst_test\x18\x01 \x01(\x04\x12\x14\n\x0crange_e_test\x18\x02 \x01(\x04\x12\x12\n\nrange_test\x18\x03 \x01(\x04\x12\x0f\n\x07in_test\x18\x04 \x01(\x04\x12\x13\n\x0bnot_in_test\x18\x05 \x01(\x04\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x06 \x01(\x04\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x14 \x01(\x04\x12\x17\n\x0fnot_enable_test\x18\x07 \x01(\x04\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x08 \x01(\x04\x12\x19\n\x11miss_default_test\x18\t \x01(\x04\x12\x15\n\rrequired_test\x18\x13 \x01(\x04\x12\x12\n\nalias_test\x18\n \x01(\x04\x12\x11\n\tdesc_test\x18\x0b \x01(\x04\x12\x18\n\x10multiple_of_test\x18\x0c \x01(\x04\x12\x14\n\x0c\x65xample_test\x18\r \x01(\x04\x12\x17\n\x0f\x65xample_factory\x18\x0e \x01(\x04\x12\x12\n\nfield_test\x18\x0f \x01(\x04\x12\x11\n\ttype_test\x18\x10 \x01(\x04\x12\x12\n\ntitle_test\x18\x11 \x01(\x04\x12\x12\n\nextra_test\x18\x12 \x01(\x04\"\xcd\x03\n\nSint64Test\x12\x12\n\nconst_test\x18\x01 \x01(\x12\x12\x14\n\x0crange_e_test\x18\x02 \x01(\x12\x12\x12\n\nrange_test\x18\x03 \x01(\x12\x12\x0f\n\x07in_test\x18\x04 \x01(\x12\x12\x13\n\x0bnot_in_test\x18\x05 \x01(\x12\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x06 \x01(\x12\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x14 \x01(\x12\x12\x17\n\x0fnot_enable_test\x18\x07 \x01(\x12\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x08 \x01(\x12\x12\x19\n\x11miss_default_test\x18\t \x01(\x12\x12\x15\n\rrequired_test\x18\x13 \x01(\x12\x12\x12\n\nalias_test\x18\n \x01(\x12\x12\x11\n\tdesc_test\x18\x0b \x01(\x12\x12\x18\n\x10multiple_of_test\x18\x0c \x01(\x12\x12\x14\n\x0c\x65xample_test\x18\r \x01(\x12\x12\x17\n\x0f\x65xample_factory\x18\x0e \x01(\x12\x12\x12\n\nfield_test\x18\x0f \x01(\x12\x12\x11\n\ttype_test\x18\x10 \x01(\x12\x12\x12\n\ntitle_test\x18\x11 \x01(\x12\x12\x12\n\nextra_test\x18\x12 \x01(\x12\"\xce\x03\n\x0b\x46ixed32Test\x12\x12\n\nconst_test\x18\x01 \x01(\x07\x12\x14\n\x0crange_e_test\x18\x02 \x01(\x07\x12\x12\n\nrange_test\x18\x03 \x01(\x07\x12\x0f\n\x07in_test\x18\x04 \x01(\x07\x12\x13\n\x0bnot_in_test\x18\x05 \x01(\x07\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x06 \x01(\x07\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x14 \x01(\x07\x12\x17\n\x0fnot_enable_test\x18\x07 \x01(\x07\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x08 \x01(\x07\x12\x19\n\x11miss_default_test\x18\t \x01(\x07\x12\x15\n\rrequired_test\x18\x13 \x01(\x07\x12\x12\n\nalias_test\x18\n \x01(\x07\x12\x11\n\tdesc_test\x18\x0b \x01(\x07\x12\x18\n\x10multiple_of_test\x18\x0c \x01(\x07\x12\x14\n\x0c\x65xample_test\x18\r \x01(\x07\x12\x17\n\x0f\x65xample_factory\x18\x0e \x01(\x07\x12\x12\n\nfield_test\x18\x0f \x01(\x07\x12\x11\n\ttype_test\x18\x10 \x01(\x07\x12\x12\n\ntitle_test\x18\x11 \x01(\x07\x12\x12\n\nextra_test\x18\x12 \x01(\x07\"\xce\x03\n\x0b\x46ixed64Test\x12\x12\n\nconst_test\x18\x01 \x01(\x06\x12\x14\n\x0crange_e_test\x18\x02 \x01(\x06\x12\x12\n\nrange_test\x18\x03 \x01(\x06\x12\x0f\n\x07in_test\x18\x04 \x01(\x06\x12\x13\n\x0bnot_in_test\x18\x05 \x01(\x06\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x06 \x01(\x06\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x14 \x01(\x06\x12\x17\n\x0fnot_enable_test\x18\x07 \x01(\x06\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x08 \x01(\x06\x12\x19\n\x11miss_default_test\x18\t \x01(\x06\x12\x15\n\rrequired_test\x18\x13 \x01(\x06\x12\x12\n\nalias_test\x18\n \x01(\x06\x12\x11\n\tdesc_test\x18\x0b \x01(\x06\x12\x18\n\x10multiple_of_test\x18\x0c \x01(\x06\x12\x14\n\x0c\x65xample_test\x18\r \x01(\x06\x12\x17\n\x0f\x65xample_factory\x18\x0e \x01(\x06\x12\x12\n\nfield_test\x18\x0f \x01(\x06\x12\x11\n\ttype_test\x18\x10 \x01(\x06\x12\x12\n\ntitle_test\x18\x11 \x01(\x06\x12\x12\n\nextra_test\x18\x12 \x01(\x06\"\xcf\x03\n\x0cSfixed32Test\x12\x12\n\nconst_test\x18\x01 \x01(\x0f\x12\x14\n\x0crange_e_test\x18\x02 \x01(\x0f\x12\x12\n\nrange_test\x18\x03 \x01(\x0f\x12\x0f\n\x07in_test\x18\x04 \x01(\x0f\x12\x13\n\x0bnot_in_test\x18\x05 \x01(\x0f\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x06 \x01(\x0f\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x14 \x01(\x0f\x12\x17\n\x0fnot_enable_test\x18\x07 \x01(\x0f\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x08 \x01(\x0f\x12\x19\n\x11miss_default_test\x18\t \x01(\x0f\x12\x15\n\rrequired_test\x18\x13 \x01(\x0f\x12\x12\n\nalias_test\x18\n \x01(\x0f\x12\x11\n\tdesc_test\x18\x0b \x01(\x0f\x12\x18\n\x10multiple_of_test\x18\x0c \x01(\x0f\x12\x14\n\x0c\x65xample_test\x18\r \x01(\x0f\x12\x17\n\x0f\x65xample_factory\x18\x0e \x01(\x0f\x12\x12\n\nfield_test\x18\x0f \x01(\x0f\x12\x11\n\ttype_test\x18\x10 \x01(\x0f\x12\x12\n\ntitle_test\x18\x11 \x01(\x0f\x12\x12\n\nextra_test\x18\x12 \x01(\x0f\"\xcf\x03\n\x0cSfixed64Test\x12\x12\n\nconst_test\x18\x01 \x01(\x10\x12\x14\n\x0crange_e_test\x18\x02 \x01(\x10\x12\x12\n\nrange_test\x18\x03 \x01(\x10\x12\x0f\n\x07in_test\x18\x04 \x01(\x10\x12\x13\n\x0bnot_in_test\x18\x05 \x01(\x10\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x06 \x01(\x10\x12\x1d\n\x15\x64\x65\x66\x61ult_template_test\x18\x14 \x01(\x10\x12\x17\n\x0fnot_enable_test\x18\x07 \x01(\x10\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x08 \x01(\x10\x12\x19\n\x11miss_default_test\x18\t \x01(\x10\x12\x15\n\rrequired_test\x18\x13 \x01(\x10\x12\x12\n\nalias_test\x18\n \x01(\x10\x12\x11\n\tdesc_test\x18\x0b \x01(\x10\x12\x18\n\x10multiple_of_test\x18\x0c \x01(\x10\x12\x14\n\x0c\x65xample_test\x18\r \x01(\x10\x12\x17\n\x0f\x65xample_factory\x18\x0e \x01(\x10\x12\x12\n\nfield_test\x18\x0f \x01(\x10\x12\x11\n\ttype_test\x18\x10 \x01(\x10\x12\x12\n\ntitle_test\x18\x11 \x01(\x10\x12\x12\n\nextra_test\x18\x12 \x01(\x10\"\x8a\x02\n\x08\x42oolTest\x12\x13\n\x0b\x62ool_1_test\x18\x01 \x01(\x08\x12\x13\n\x0b\x62ool_2_test\x18\x02 \x01(\x08\x12\x13\n\x0b\x65nable_test\x18\x03 \x01(\x08\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x04 \x01(\x08\x12\x19\n\x11miss_default_test\x18\x05 \x01(\x08\x12\x15\n\rrequired_test\x18\x13 \x01(\x08\x12\x12\n\nalias_test\x18\n \x01(\x08\x12\x11\n\tdesc_test\x18\x0b \x01(\x08\x12\x14\n\x0c\x65xample_test\x18\r \x01(\x08\x12\x12\n\nfield_test\x18\x0f \x01(\x08\x12\x12\n\ntitle_test\x18\x11 \x01(\x08\x12\x12\n\nextra_test\x18\x12 \x01(\x08\"\xd8\x05\n\nStringTest\x12\x12\n\nconst_test\x18\x01 \x01(\t\x12\x10\n\x08len_test\x18\x02 \x01(\t\x12\x18\n\x10s_range_len_test\x18\x03 \x01(\t\x12\x14\n\x0cpattern_test\x18\x05 \x01(\t\x12\x13\n\x0bprefix_test\x18\x06 \x01(\t\x12\x13\n\x0bsuffix_test\x18\x07 \x01(\t\x12\x15\n\rcontains_test\x18\x08 \x01(\t\x12\x19\n\x11not_contains_test\x18\t \x01(\t\x12\x0f\n\x07in_test\x18\n \x01(\t\x12\x13\n\x0bnot_in_test\x18\x0b \x01(\t\x12\x12\n\nemail_test\x18\x0c \x01(\t\x12\x15\n\rhostname_test\x18\r \x01(\t\x12\x0f\n\x07ip_test\x18\x0e \x01(\t\x12\x11\n\tipv4_test\x18\x0f \x01(\t\x12\x11\n\tipv6_test\x18\x10 \x01(\t\x12\x10\n\x08uri_test\x18\x11 \x01(\t\x12\x14\n\x0curi_ref_test\x18\x12 \x01(\t\x12\x14\n\x0c\x61\x64\x64ress_test\x18\x13 \x01(\t\x12\x11\n\tuuid_test\x18\x14 \x01(\t\x12\x1a\n\x12pydantic_type_test\x18\x15 \x01(\t\x12\x13\n\x0b\x65nable_test\x18\x16 \x01(\t\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x17 \x01(\t\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x18 \x01(\t\x12\x19\n\x11miss_default_test\x18\x19 \x01(\t\x12\x15\n\rrequired_test\x18\" \x01(\t\x12\x12\n\nalias_test\x18\x1a \x01(\t\x12\x11\n\tdesc_test\x18\x1b \x01(\t\x12\x14\n\x0c\x65xample_test\x18\x1c \x01(\t\x12\x1c\n\x14\x65xample_factory_test\x18\x1d \x01(\t\x12\x12\n\nfield_test\x18\x1e \x01(\t\x12\x12\n\ntitle_test\x18\x1f \x01(\t\x12\x11\n\ttype_test\x18  \x01(\t\x12\x12\n\nextra_test\x18! \x01(\t\"\xc3\x03\n\tBytesTest\x12\x12\n\nconst_test\x18\x01 \x01(\x0c\x12\x16\n\x0erange_len_test\x18\x03 \x01(\x0c\x12\x13\n\x0bprefix_test\x18\x05 \x01(\x0c\x12\x13\n\x0bsuffix_test\x18\x06 \x01(\x0c\x12\x15\n\rcontains_test\x18\x07 \x01(\x0c\x12\x0f\n\x07in_test\x18\x08 \x01(\x0c\x12\x13\n\x0bnot_in_test\x18\t \x01(\x0c\x12\x13\n\x0b\x65nable_test\x18\x16 \x01(\x0c\x12\x14\n\x0c\x64\x65\x66\x61ult_test\x18\x17 \x01(\x0c\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x18 \x01(\x0c\x12\x19\n\x11miss_default_test\x18\x19 \x01(\x0c\x12\x15\n\rrequired_test\x18\" \x01(\x0c\x12\x12\n\nalias_test\x18\x1a \x01(\x0c\x12\x11\n\tdesc_test\x18\x1b \x01(\x0c\x12\x14\n\x0c\x65xample_test\x18\x1c \x01(\x0c\x12\x1c\n\x14\x65xample_factory_test\x18\x1d \x01(\x0c\x12\x12\n\nfield_test\x18\x1e \x01(\x0c\x12\x12\n\ntitle_test\x18\x1f \x01(\x0c\x12\x11\n\ttype_test\x18  \x01(\x0c\x12\x12\n\nextra_test\x18! \x01(\x0c\"\xd4\x05\n\x08\x45numTest\x12\x34\n\nconst_test\x18\x01 \x01(\x0e\x32 .p2p_validate_comment_test.State\x12\x31\n\x07in_test\x18\x03 \x01(\x0e\x32 .p2p_validate_comment_test.State\x12\x35\n\x0bnot_in_test\x18\x04 \x01(\x0e\x32 .p2p_validate_comment_test.State\x12\x35\n\x0b\x65nable_test\x18\x16 \x01(\x0e\x32 .p2p_validate_comment_test.State\x12\x36\n\x0c\x64\x65\x66\x61ult_test\x18\x17 \x01(\x0e\x32 .p2p_validate_comment_test.State\x12;\n\x11miss_default_test\x18\x19 \x01(\x0e\x32 .p2p_validate_comment_test.State\x12\x37\n\rrequired_test\x18\" \x01(\x0e\x32 .p2p_validate_comment_test.State\x12\x34\n\nalias_test\x18\x1a \x01(\x0e\x32 .p2p_validate_comment_test.State\x12\x33\n\tdesc_test\x18\x1b \x01(\x0e\x32 .p2p_validate_comment_test.State\x12\x36\n\x0c\x65xample_test\x18\x1c \x01(\x0e\x32 .p2p_validate_comment_test.State\x12\x34\n\nfield_test\x18\x1e \x01(\x0e\x32 .p2p_validate_comment_test.State\x12\x34\n\ntitle_test\x18\x1f \x01(\x0e\x32 .p2p_validate_comment_test.State\x12\x34\n\nextra_test\x18! \x01(\x0e\x32 .p2p_validate_comment_test.State\"\x9a\x0f\n\x07MapTest\x12\x43\n\tpair_test\x18\x01 \x03(\x0b\x32\x30.p2p_validate_comment_test.MapTest.PairTestEntry\x12\x43\n\tkeys_test\x18\x03 \x03(\x0b\x32\x30.p2p_validate_comment_test.MapTest.KeysTestEntry\x12G\n\x0bvalues_test\x18\x04 \x03(\x0b\x32\x32.p2p_validate_comment_test.MapTest.ValuesTestEntry\x12P\n\x10keys_values_test\x18\x05 \x03(\x0b\x32\x36.p2p_validate_comment_test.MapTest.KeysValuesTestEntry\x12G\n\x0b\x65nable_test\x18\x06 \x03(\x0b\x32\x32.p2p_validate_comment_test.MapTest.EnableTestEntry\x12X\n\x14\x64\x65\x66\x61ult_factory_test\x18\x18 \x03(\x0b\x32:.p2p_validate_comment_test.MapTest.DefaultFactoryTestEntry\x12R\n\x11miss_default_test\x18\x19 \x03(\x0b\x32\x37.p2p_validate_comment_test.MapTest.MissDefaultTestEntry\x12K\n\rrequired_test\x18\" \x03(\x0b\x32\x34.p2p_validate_comment_test.MapTest.RequiredTestEntry\x12\x45\n\nalias_test\x18\x1a \x03(\x0b\x32\x31.p2p_validate_comment_test.MapTest.AliasTestEntry\x12\x43\n\tdesc_test\x18\x1b \x03(\x0b\x32\x30.p2p_validate_comment_test.MapTest.DescTestEntry\x12X\n\x14\x65xample_factory_test\x18\x1d \x03(\x0b\x32:.p2p_validate_comment_test.MapTest.ExampleFactoryTestEntry\x12\x45\n\nfield_test\x18\x1e \x03(\x0b\x32\x31.p2p_validate_comment_test.MapTest.FieldTestEntry\x12\x45\n\ntitle_test\x18\x1f \x03(\x0b\x32\x31.p2p_validate_comment_test.MapTest.TitleTestEntry\x12\x43\n\ttype_test\x18  \x03(\x0b\x32\x30.p2p_validate_comment_test.MapTest.TypeTestEntry\x12\x45\n\nextra_test\x18! \x03(\x0b\x32\x31.p2p_validate_comment_test.MapTest.ExtraTestEntry\x1a/\n\rPairTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a/\n\rKeysTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x31\n\x0fValuesTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1aQ\n\x13KeysValuesTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp:\x02\x38\x01\x1a\x31\n\x0f\x45nableTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x39\n\x17\x44\x65\x66\x61ultFactoryTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x36\n\x14MissDefaultTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x33\n\x11RequiredTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x30\n\x0e\x41liasTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a/\n\rDescTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x39\n\x17\x45xampleFactoryTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x30\n\x0e\x46ieldTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x30\n\x0eTitleTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a/\n\rTypeTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x30\n\x0e\x45xtraTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"K\n\x0bMessageTest\x12\x11\n\tskip_test\x18\x01 \x01(\t\x12\x15\n\rrequired_test\x18\x02 \x01(\t\x12\x12\n\nextra_test\x18! \x01(\t\"\x8c\x04\n\x0cRepeatedTest\x12\x12\n\nrange_test\x18\x01 \x03(\t\x12\x13\n\x0bunique_test\x18\x02 \x03(\t\x12\x19\n\x11items_string_test\x18\x03 \x03(\t\x12\x19\n\x11items_double_test\x18\x04 \x03(\x01\x12\x18\n\x10items_int32_test\x18\x05 \x03(\x05\x12\x38\n\x14items_timestamp_test\x18\x06 \x03(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x36\n\x13items_duration_test\x18\x07 \x03(\x0b\x32\x19.google.protobuf.Duration\x12\x18\n\x10items_bytes_test\x18\x08 \x03(\x0c\x12\x13\n\x0b\x65nable_test\x18\t \x03(\t\x12\x1c\n\x14\x64\x65\x66\x61ult_factory_test\x18\x18 \x03(\t\x12\x19\n\x11miss_default_test\x18\x19 \x03(\t\x12\x15\n\rrequired_test\x18\" \x03(\t\x12\x12\n\nalias_test\x18\x1a \x03(\t\x12\x11\n\tdesc_test\x18\x1b \x03(\t\x12\x1c\n\x14\x65xample_factory_test\x18\x1d \x03(\t\x12\x12\n\nfield_test\x18\x1e \x03(\t\x12\x12\n\ntitle_test\x18\x1f \x03(\t\x12\x11\n\ttype_test\x18  \x03(\t\x12\x12\n\nextra_test\x18! \x03(\t\"\xf5\x04\n\x07\x41nyTest\x12+\n\rrequired_test\x18\x01 \x01(\x0b\x32\x14.google.protobuf.Any\x12)\n\x0bnot_in_test\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\x12%\n\x07in_test\x18\x03 \x01(\x0b\x32\x14.google.protobuf.Any\x12)\n\x0b\x65nable_test\x18\x04 \x01(\x0b\x32\x14.google.protobuf.Any\x12*\n\x0c\x64\x65\x66\x61ult_test\x18\x17 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x32\n\x14\x64\x65\x66\x61ult_factory_test\x18\x18 \x01(\x0b\x32\x14.google.protobuf.Any\x12/\n\x11miss_default_test\x18\x19 \x01(\x0b\x32\x14.google.protobuf.Any\x12(\n\nalias_test\x18\x1a \x01(\x0b\x32\x14.google.protobuf.Any\x12\'\n\tdesc_test\x18\x1b \x01(\x0b\x32\x14.google.protobuf.Any\x12*\n\x0c\x65xample_test\x18\x1c \x01(\x0b\x32\x14.google.protobuf.Any\x12\x32\n\x14\x65xample_factory_test\x18\x1d \x01(\x0b\x32\x14.google.protobuf.Any\x12(\n\nfield_test\x18\x1e \x01(\x0b\x32\x14.google.protobuf.Any\x12(\n\ntitle_test\x18\x1f \x01(\x0b\x32\x14.google.protobuf.Any\x12(\n\nextra_test\x18! \x01(\x0b\x32\x14.google.protobuf.Any\"\xfd\x06\n\x0c\x44urationTest\x12-\n\nconst_test\x18\x02 \x01(\x0b\x32\x19.google.protobuf.Duration\x12-\n\nrange_test\x18\x03 \x01(\x0b\x32\x19.google.protobuf.Duration\x12/\n\x0crange_e_test\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\x12*\n\x07in_test\x18\x05 \x01(\x0b\x32\x19.google.protobuf.Duration\x12.\n\x0bnot_in_test\x18\x06 \x01(\x0b\x32\x19.google.protobuf.Duration\x12.\n\x0b\x65nable_test\x18\x16 \x01(\x0b\x32\x19.google.protobuf.Duration\x12/\n\x0c\x64\x65\x66\x61ult_test\x18\x17 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x37\n\x14\x64\x65\x66\x61ult_factory_test\x18\x18 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x34\n\x11miss_default_test\x18\x19 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x30\n\rrequired_test\x18\" \x01(\x0b\x32\x19.google.protobuf.Duration\x12-\n\nalias_test\x18\x1a \x01(\x0b\x32\x19.google.protobuf.Duration\x12,\n\tdesc_test\x18\x1b \x01(\x0b\x32\x19.google.protobuf.Duration\x12/\n\x0c\x65xample_test\x18\x1c \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x37\n\x14\x65xample_factory_test\x18\x1d \x01(\x0b\x32\x19.google.protobuf.Duration\x12-\n\nfield_test\x18\x1e \x01(\x0b\x32\x19.google.protobuf.Duration\x12-\n\ntitle_test\x18\x1f \x01(\x0b\x32\x19.google.protobuf.Duration\x12,\n\ttype_test\x18  \x01(\x0b\x32\x19.google.protobuf.Duration\x12-\n\nextra_test\x18! \x01(\x0b\x32\x19.google.protobuf.Duration\"\x81\x08\n\rTimestampTest\x12.\n\nconst_test\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nrange_test\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0crange_e_test\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0blt_now_test\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bgt_now_test\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bwithin_test\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12:\n\x16within_and_gt_now_test\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0b\x65nable_test\x18\x16 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0c\x64\x65\x66\x61ult_test\x18\x17 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x38\n\x14\x64\x65\x66\x61ult_factory_test\x18\x18 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x35\n\x11miss_default_test\x18\x19 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rrequired_test\x18\" \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nalias_test\x18\x1a \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\tdesc_test\x18\x1b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0c\x65xample_test\x18\x1c \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x38\n\x14\x65xample_factory_test\x18\x1d \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nfield_test\x18\x1e \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\ntitle_test\x18\x1f \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\ttype_test\x18  \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nextra_test\x18! \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"R\n\x12MessageIgnoredTest\x12\x12\n\nconst_test\x18\x01 \x01(\x05\x12\x14\n\x0crange_e_test\x18\x02 \x01(\x05\x12\x12\n\nrange_test\x18\x03 \x01(\x05\";\n\tOneOfTest\x12\x0e\n\x06header\x18\x01 \x01(\t\x12\x0b\n\x01x\x18\x02 \x01(\tH\x00\x12\x0b\n\x01y\x18\x03 \x01(\x05H\x00\x42\x04\n\x02id\">\n\x0cOneOfNotTest\x12\x0e\n\x06header\x18\x01 \x01(\t\x12\x0b\n\x01x\x18\x02 \x01(\tH\x00\x12\x0b\n\x01y\x18\x03 \x01(\x05H\x00\x42\x04\n\x02id\"\x92\x02\n\x11OneOfOptionalTest\x12\x0e\n\x06header\x18\x01 \x01(\t\x12\x0b\n\x01x\x18\x02 \x01(\tH\x00\x12\x0b\n\x01y\x18\x03 \x01(\x05H\x00\x12\x0b\n\x01z\x18\x04 \x01(\x08H\x00\x12\x11\n\x04name\x18\x05 \x01(\tH\x01\x88\x01\x01\x12\x10\n\x03\x61ge\x18\x06 \x01(\x05H\x02\x88\x01\x01\x12\x10\n\x08str_list\x18\x07 \x03(\t\x12I\n\x07int_map\x18\x08 \x03(\x0b\x32\x38.p2p_validate_comment_test.OneOfOptionalTest.IntMapEntry\x1a-\n\x0bIntMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x42\x04\n\x02idB\x07\n\x05_nameB\x06\n\x04_age\"\xd0\x06\n\rNestedMessage\x12Y\n\x12string_in_map_test\x18\x01 \x03(\x0b\x32=.p2p_validate_comment_test.NestedMessage.StringInMapTestEntry\x12S\n\x0fmap_in_map_test\x18\x02 \x03(\x0b\x32:.p2p_validate_comment_test.NestedMessage.MapInMapTestEntry\x12I\n\x08user_pay\x18\x03 \x01(\x0b\x32\x37.p2p_validate_comment_test.NestedMessage.UserPayMessage\x12]\n\x13not_enable_user_pay\x18\x04 \x01(\x0b\x32@.p2p_validate_comment_test.NestedMessage.NotEnableUserPayMessage\x12%\n\x05\x65mpty\x18\x05 \x01(\x0b\x32\x16.google.protobuf.Empty\x12\x41\n\x0b\x61\x66ter_refer\x18\x07 \x01(\x0b\x32,.p2p_validate_comment_test.AfterReferMessage\x1a\\\n\x0eUserPayMessage\x12\x13\n\x0b\x62\x61nk_number\x18\x01 \x01(\t\x12\'\n\x03\x65xp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04uuid\x18\x03 \x01(\t\x1a\x65\n\x17NotEnableUserPayMessage\x12\x13\n\x0b\x62\x61nk_number\x18\x01 \x01(\t\x12\'\n\x03\x65xp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04uuid\x18\x03 \x01(\t\x1a]\n\x14StringInMapTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x34\n\x05value\x18\x02 \x01(\x0b\x32%.p2p_validate_comment_test.StringTest:\x02\x38\x01\x1aW\n\x11MapInMapTestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".p2p_validate_comment_test.MapTest:\x02\x38\x01\"-\n\x11\x41\x66terReferMessage\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x0b\n\x03\x61ge\x18\x02 \x01(\x05\"\xa6\x03\n\x0fOptionalMessage\x12G\n\x0bmy_message1\x18\x01 \x01(\x0b\x32-.p2p_validate_comment_test.MessageIgnoredTestH\x00\x88\x01\x01\x12G\n\x0bmy_message2\x18\x02 \x01(\x0b\x32-.p2p_validate_comment_test.MessageIgnoredTestH\x01\x88\x01\x01\x12\x42\n\x0bmy_message3\x18\x03 \x01(\x0b\x32-.p2p_validate_comment_test.MessageIgnoredTest\x12\x42\n\x0bmy_message4\x18\x04 \x01(\x0b\x32-.p2p_validate_comment_test.MessageIgnoredTest\x12H\n\x0cmy_message_5\x18\x05 \x01(\x0b\x32-.p2p_validate_comment_test.MessageIgnoredTestH\x02\x88\x01\x01\x42\x0e\n\x0c_my_message1B\x0e\n\x0c_my_message2B\x0f\n\r_my_message_5*.\n\x05State\x12\x0c\n\x08INACTIVE\x10\x00\x12\x0b\n\x07PENDING\x10\x01\x12\n\n\x06\x41\x43TIVE\x10\x02\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'example.example_proto.p2p_validate_by_comment.demo_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MAPTEST_PAIRTESTENTRY._options = None
  _MAPTEST_PAIRTESTENTRY._serialized_options = b'8\001'
  _MAPTEST_KEYSTESTENTRY._options = None
  _MAPTEST_KEYSTESTENTRY._serialized_options = b'8\001'
  _MAPTEST_VALUESTESTENTRY._options = None
  _MAPTEST_VALUESTESTENTRY._serialized_options = b'8\001'
  _MAPTEST_KEYSVALUESTESTENTRY._options = None
  _MAPTEST_KEYSVALUESTESTENTRY._serialized_options = b'8\001'
  _MAPTEST_ENABLETESTENTRY._options = None
  _MAPTEST_ENABLETESTENTRY._serialized_options = b'8\001'
  _MAPTEST_DEFAULTFACTORYTESTENTRY._options = None
  _MAPTEST_DEFAULTFACTORYTESTENTRY._serialized_options = b'8\001'
  _MAPTEST_MISSDEFAULTTESTENTRY._options = None
  _MAPTEST_MISSDEFAULTTESTENTRY._serialized_options = b'8\001'
  _MAPTEST_REQUIREDTESTENTRY._options = None
  _MAPTEST_REQUIREDTESTENTRY._serialized_options = b'8\001'
  _MAPTEST_ALIASTESTENTRY._options = None
  _MAPTEST_ALIASTESTENTRY._serialized_options = b'8\001'
  _MAPTEST_DESCTESTENTRY._options = None
  _MAPTEST_DESCTESTENTRY._serialized_options = b'8\001'
  _MAPTEST_EXAMPLEFACTORYTESTENTRY._options = None
  _MAPTEST_EXAMPLEFACTORYTESTENTRY._serialized_options = b'8\001'
  _MAPTEST_FIELDTESTENTRY._options = None
  _MAPTEST_FIELDTESTENTRY._serialized_options = b'8\001'
  _MAPTEST_TITLETESTENTRY._options = None
  _MAPTEST_TITLETESTENTRY._serialized_options = b'8\001'
  _MAPTEST_TYPETESTENTRY._options = None
  _MAPTEST_TYPETESTENTRY._serialized_options = b'8\001'
  _MAPTEST_EXTRATESTENTRY._options = None
  _MAPTEST_EXTRATESTENTRY._serialized_options = b'8\001'
  _ONEOFOPTIONALTEST_INTMAPENTRY._options = None
  _ONEOFOPTIONALTEST_INTMAPENTRY._serialized_options = b'8\001'
  _NESTEDMESSAGE_STRINGINMAPTESTENTRY._options = None
  _NESTEDMESSAGE_STRINGINMAPTESTENTRY._serialized_options = b'8\001'
  _NESTEDMESSAGE_MAPINMAPTESTENTRY._options = None
  _NESTEDMESSAGE_MAPINMAPTESTENTRY._serialized_options = b'8\001'
  _STATE._serialized_start=14878
  _STATE._serialized_end=14924
  _FLOATTEST._serialized_start=209
  _FLOATTEST._serialized_end=669
  _DOUBLETEST._serialized_start=672
  _DOUBLETEST._serialized_end=1133
  _INT32TEST._serialized_start=1136
  _INT32TEST._serialized_end=1596
  _INT64TEST._serialized_start=1599
  _INT64TEST._serialized_end=2059
  _UINT32TEST._serialized_start=2062
  _UINT32TEST._serialized_end=2523
  _SINT32TEST._serialized_start=2526
  _SINT32TEST._serialized_end=2987
  _UINT64TEST._serialized_start=2990
  _UINT64TEST._serialized_end=3451
  _SINT64TEST._serialized_start=3454
  _SINT64TEST._serialized_end=3915
  _FIXED32TEST._serialized_start=3918
  _FIXED32TEST._serialized_end=4380
  _FIXED64TEST._serialized_start=4383
  _FIXED64TEST._serialized_end=4845
  _SFIXED32TEST._serialized_start=4848
  _SFIXED32TEST._serialized_end=5311
  _SFIXED64TEST._serialized_start=5314
  _SFIXED64TEST._serialized_end=5777
  _BOOLTEST._serialized_start=5780
  _BOOLTEST._serialized_end=6046
  _STRINGTEST._serialized_start=6049
  _STRINGTEST._serialized_end=6777
  _BYTESTEST._serialized_start=6780
  _BYTESTEST._serialized_end=7231
  _ENUMTEST._serialized_start=7234
  _ENUMTEST._serialized_end=7958
  _MAPTEST._serialized_start=7961
  _MAPTEST._serialized_end=9907
  _MAPTEST_PAIRTESTENTRY._serialized_start=9101
  _MAPTEST_PAIRTESTENTRY._serialized_end=9148
  _MAPTEST_KEYSTESTENTRY._serialized_start=9150
  _MAPTEST_KEYSTESTENTRY._serialized_end=9197
  _MAPTEST_VALUESTESTENTRY._serialized_start=9199
  _MAPTEST_VALUESTESTENTRY._serialized_end=9248
  _MAPTEST_KEYSVALUESTESTENTRY._serialized_start=9250
  _MAPTEST_KEYSVALUESTESTENTRY._serialized_end=9331
  _MAPTEST_ENABLETESTENTRY._serialized_start=9333
  _MAPTEST_ENABLETESTENTRY._serialized_end=9382
  _MAPTEST_DEFAULTFACTORYTESTENTRY._serialized_start=9384
  _MAPTEST_DEFAULTFACTORYTESTENTRY._serialized_end=9441
  _MAPTEST_MISSDEFAULTTESTENTRY._serialized_start=9443
  _MAPTEST_MISSDEFAULTTESTENTRY._serialized_end=9497
  _MAPTEST_REQUIREDTESTENTRY._serialized_start=9499
  _MAPTEST_REQUIREDTESTENTRY._serialized_end=9550
  _MAPTEST_ALIASTESTENTRY._serialized_start=9552
  _MAPTEST_ALIASTESTENTRY._serialized_end=9600
  _MAPTEST_DESCTESTENTRY._serialized_start=9602
  _MAPTEST_DESCTESTENTRY._serialized_end=9649
  _MAPTEST_EXAMPLEFACTORYTESTENTRY._serialized_start=9651
  _MAPTEST_EXAMPLEFACTORYTESTENTRY._serialized_end=9708
  _MAPTEST_FIELDTESTENTRY._serialized_start=9710
  _MAPTEST_FIELDTESTENTRY._serialized_end=9758
  _MAPTEST_TITLETESTENTRY._serialized_start=9760
  _MAPTEST_TITLETESTENTRY._serialized_end=9808
  _MAPTEST_TYPETESTENTRY._serialized_start=9810
  _MAPTEST_TYPETESTENTRY._serialized_end=9857
  _MAPTEST_EXTRATESTENTRY._serialized_start=9859
  _MAPTEST_EXTRATESTENTRY._serialized_end=9907
  _MESSAGETEST._serialized_start=9909
  _MESSAGETEST._serialized_end=9984
  _REPEATEDTEST._serialized_start=9987
  _REPEATEDTEST._serialized_end=10511
  _ANYTEST._serialized_start=10514
  _ANYTEST._serialized_end=11143
  _DURATIONTEST._serialized_start=11146
  _DURATIONTEST._serialized_end=12039
  _TIMESTAMPTEST._serialized_start=12042
  _TIMESTAMPTEST._serialized_end=13067
  _MESSAGEIGNOREDTEST._serialized_start=13069
  _MESSAGEIGNOREDTEST._serialized_end=13151
  _ONEOFTEST._serialized_start=13153
  _ONEOFTEST._serialized_end=13212
  _ONEOFNOTTEST._serialized_start=13214
  _ONEOFNOTTEST._serialized_end=13276
  _ONEOFOPTIONALTEST._serialized_start=13279
  _ONEOFOPTIONALTEST._serialized_end=13553
  _ONEOFOPTIONALTEST_INTMAPENTRY._serialized_start=13485
  _ONEOFOPTIONALTEST_INTMAPENTRY._serialized_end=13530
  _NESTEDMESSAGE._serialized_start=13556
  _NESTEDMESSAGE._serialized_end=14404
  _NESTEDMESSAGE_USERPAYMESSAGE._serialized_start=14025
  _NESTEDMESSAGE_USERPAYMESSAGE._serialized_end=14117
  _NESTEDMESSAGE_NOTENABLEUSERPAYMESSAGE._serialized_start=14119
  _NESTEDMESSAGE_NOTENABLEUSERPAYMESSAGE._serialized_end=14220
  _NESTEDMESSAGE_STRINGINMAPTESTENTRY._serialized_start=14222
  _NESTEDMESSAGE_STRINGINMAPTESTENTRY._serialized_end=14315
  _NESTEDMESSAGE_MAPINMAPTESTENTRY._serialized_start=14317
  _NESTEDMESSAGE_MAPINMAPTESTENTRY._serialized_end=14404
  _AFTERREFERMESSAGE._serialized_start=14406
  _AFTERREFERMESSAGE._serialized_end=14451
  _OPTIONALMESSAGE._serialized_start=14454
  _OPTIONALMESSAGE._serialized_end=14876
# @@protoc_insertion_point(module_scope)
