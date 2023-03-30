from google.protobuf.any_pb2 import Any as AnyMessage  # type: ignore
from google.protobuf.descriptor import Descriptor, FieldDescriptor  # type: ignore
from google.protobuf.descriptor_pb2 import (  # type: ignore
    DescriptorProto,
    EnumDescriptorProto,
    FieldDescriptorProto,
    FileDescriptorProto,
)
from google.protobuf.duration_pb2 import Duration  # type: ignore
from google.protobuf.json_format import MessageToDict  # type: ignore
from google.protobuf.message import Message  # type: ignore

try:
    from google.protobuf.pyext._message import RepeatedCompositeContainer, RepeatedScalarContainer  # type: ignore
except ModuleNotFoundError:
    from google._upb._message import RepeatedCompositeContainer, RepeatedScalarContainer  # type: ignore

from google.protobuf.internal.containers import RepeatedCompositeFieldContainer, RepeatedScalarFieldContainer
from google.protobuf.timestamp_pb2 import Timestamp  # type: ignore

__all__ = [
    "AnyMessage",
    "Descriptor",
    "DescriptorProto",
    "Duration",
    "EnumDescriptorProto",
    "FieldDescriptor",
    "FieldDescriptorProto",
    "FileDescriptorProto",
    "Message",
    "Timestamp",
    "MessageToDict",
    "RepeatedCompositeContainer",
    "RepeatedScalarContainer",
    "RepeatedScalarFieldContainer",
    "RepeatedCompositeFieldContainer",
    "ProtobufRepeatedType",
]
ProtobufRepeatedType = [
    RepeatedScalarFieldContainer,
    RepeatedCompositeFieldContainer,
    RepeatedScalarContainer,
    RepeatedCompositeContainer,
]
