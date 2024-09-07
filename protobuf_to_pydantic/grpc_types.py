from google.protobuf.any_pb2 import Any as AnyMessage  # type: ignore
from google.protobuf.descriptor import Descriptor, FieldDescriptor  # type: ignore
from google.protobuf.descriptor_pb2 import (  # type: ignore
    DescriptorProto,
    EnumDescriptorProto,
    FieldDescriptorProto,
    FileDescriptorProto,
)
from google.protobuf.duration_pb2 import Duration  # type: ignore
from google.protobuf.timestamp_pb2 import Timestamp # type: ignore
from google.protobuf.field_mask_pb2 import FieldMask  # type: ignore
from google.protobuf.json_format import MessageToDict  # type: ignore
from google.protobuf.message import Message  # type: ignore

try:
    from google.protobuf.pyext._message import RepeatedCompositeContainer, RepeatedScalarContainer  # type: ignore
except ModuleNotFoundError:
    try:
        from google._upb._message import RepeatedCompositeContainer, RepeatedScalarContainer  # type: ignore
    except ModuleNotFoundError:

        class RepeatedCompositeContainer(object):
            """A Repeated scalar container"""

            def add(self, *args, **kwargs):  # real signature unknown
                """Adds an object to the repeated container."""

            def append(self, *args, **kwargs):  # real signature unknown
                """Appends a message to the end of the repeated container."""

            def extend(self, *args, **kwargs):  # real signature unknown
                """Adds objects to the repeated container."""

            def insert(self, *args, **kwargs):  # real signature unknown
                """Inserts a message before the specified index."""

            def MergeFrom(self, *args, **kwargs):  # real signature unknown
                """Adds objects to the repeated container."""

            def pop(self, *args, **kwargs):  # real signature unknown
                """Removes an object from the repeated container and returns it."""

            def remove(self, *args, **kwargs):  # real signature unknown
                """Removes an object from the repeated container."""

            def reverse(self, *args, **kwargs):  # real signature unknown
                """Reverses elements order of the repeated container."""

            def sort(self, *args, **kwargs):  # real signature unknown
                """Sorts the repeated container."""

            def __deepcopy__(self, *args, **kwargs):  # real signature unknown
                """Makes a deep copy of the class."""

            def __delitem__(self, *args, **kwargs):  # real signature unknown
                """Delete self[key]."""

            def __eq__(self, *args, **kwargs):  # real signature unknown
                """Return self==value."""

            def __getitem__(self, *args, **kwargs):  # real signature unknown
                """Return self[key]."""

            def __ge__(self, *args, **kwargs):  # real signature unknown
                """Return self>=value."""

            def __gt__(self, *args, **kwargs):  # real signature unknown
                """Return self>value."""

            def __init__(self, *args, **kwargs):  # real signature unknown
                pass

            def __len__(self, *args, **kwargs):  # real signature unknown
                """Return len(self)."""

            def __le__(self, *args, **kwargs):  # real signature unknown
                """Return self<=value."""

            def __lt__(self, *args, **kwargs):  # real signature unknown
                """Return self<value."""

            def __ne__(self, *args, **kwargs):  # real signature unknown
                """Return self!=value."""

            def __repr__(self, *args, **kwargs):  # real signature unknown
                """Return repr(self)."""

            def __setitem__(self, *args, **kwargs):  # real signature unknown
                """Set self[key] to value."""

            __hash__ = None

        class RepeatedScalarContainer(object):
            """A Repeated scalar container"""

            def append(self, *args, **kwargs):  # real signature unknown
                """Appends an object to the repeated container."""

            def extend(self, *args, **kwargs):  # real signature unknown
                """Appends objects to the repeated container."""

            def insert(self, *args, **kwargs):  # real signature unknown
                """Inserts an object at the specified position in the container."""

            def MergeFrom(self, *args, **kwargs):  # real signature unknown
                """Merges a repeated container into the current container."""

            def pop(self, *args, **kwargs):  # real signature unknown
                """Removes an object from the repeated container and returns it."""

            def remove(self, *args, **kwargs):  # real signature unknown
                """Removes an object from the repeated container."""

            def reverse(self, *args, **kwargs):  # real signature unknown
                """Reverses elements order of the repeated container."""

            def sort(self, *args, **kwargs):  # real signature unknown
                """Sorts the repeated container."""

            def __deepcopy__(self, *args, **kwargs):  # real signature unknown
                """Makes a deep copy of the class."""

            def __delitem__(self, *args, **kwargs):  # real signature unknown
                """Delete self[key]."""

            def __eq__(self, *args, **kwargs):  # real signature unknown
                """Return self==value."""

            def __getitem__(self, *args, **kwargs):  # real signature unknown
                """Return self[key]."""

            def __ge__(self, *args, **kwargs):  # real signature unknown
                """Return self>=value."""

            def __gt__(self, *args, **kwargs):  # real signature unknown
                """Return self>value."""

            def __init__(self, *args, **kwargs):  # real signature unknown
                pass

            def __len__(self, *args, **kwargs):  # real signature unknown
                """Return len(self)."""

            def __le__(self, *args, **kwargs):  # real signature unknown
                """Return self<=value."""

            def __lt__(self, *args, **kwargs):  # real signature unknown
                """Return self<value."""

            def __ne__(self, *args, **kwargs):  # real signature unknown
                """Return self!=value."""

            def __reduce__(self, *args, **kwargs):  # real signature unknown
                """Outputs picklable representation of the repeated field."""

            def __repr__(self, *args, **kwargs):  # real signature unknown
                """Return repr(self)."""

            def __setitem__(self, *args, **kwargs):  # real signature unknown
                """Set self[key] to value."""

            __hash__ = None


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
    "FieldMask",
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
