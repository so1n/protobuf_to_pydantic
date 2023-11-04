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
    try:
        from google._upb._message import RepeatedCompositeContainer, RepeatedScalarContainer  # type: ignore
    except ModuleNotFoundError:
        class RepeatedCompositeContainer(object):
            """ A Repeated scalar container """

            def add(self, *args, **kwargs):  # real signature unknown
                """ Adds an object to the repeated container. """
                pass

            def append(self, *args, **kwargs):  # real signature unknown
                """ Appends a message to the end of the repeated container. """
                pass

            def extend(self, *args, **kwargs):  # real signature unknown
                """ Adds objects to the repeated container. """
                pass

            def insert(self, *args, **kwargs):  # real signature unknown
                """ Inserts a message before the specified index. """
                pass

            def MergeFrom(self, *args, **kwargs):  # real signature unknown
                """ Adds objects to the repeated container. """
                pass

            def pop(self, *args, **kwargs):  # real signature unknown
                """ Removes an object from the repeated container and returns it. """
                pass

            def remove(self, *args, **kwargs):  # real signature unknown
                """ Removes an object from the repeated container. """
                pass

            def reverse(self, *args, **kwargs):  # real signature unknown
                """ Reverses elements order of the repeated container. """
                pass

            def sort(self, *args, **kwargs):  # real signature unknown
                """ Sorts the repeated container. """
                pass

            def __deepcopy__(self, *args, **kwargs):  # real signature unknown
                """ Makes a deep copy of the class. """
                pass

            def __delitem__(self, *args, **kwargs):  # real signature unknown
                """ Delete self[key]. """
                pass

            def __eq__(self, *args, **kwargs):  # real signature unknown
                """ Return self==value. """
                pass

            def __getitem__(self, *args, **kwargs):  # real signature unknown
                """ Return self[key]. """
                pass

            def __ge__(self, *args, **kwargs):  # real signature unknown
                """ Return self>=value. """
                pass

            def __gt__(self, *args, **kwargs):  # real signature unknown
                """ Return self>value. """
                pass

            def __init__(self, *args, **kwargs):  # real signature unknown
                pass

            def __len__(self, *args, **kwargs):  # real signature unknown
                """ Return len(self). """
                pass

            def __le__(self, *args, **kwargs):  # real signature unknown
                """ Return self<=value. """
                pass

            def __lt__(self, *args, **kwargs):  # real signature unknown
                """ Return self<value. """
                pass

            def __ne__(self, *args, **kwargs):  # real signature unknown
                """ Return self!=value. """
                pass

            def __repr__(self, *args, **kwargs):  # real signature unknown
                """ Return repr(self). """
                pass

            def __setitem__(self, *args, **kwargs):  # real signature unknown
                """ Set self[key] to value. """
                pass

            __hash__ = None


        class RepeatedScalarContainer(object):
            """ A Repeated scalar container """

            def append(self, *args, **kwargs):  # real signature unknown
                """ Appends an object to the repeated container. """
                pass

            def extend(self, *args, **kwargs):  # real signature unknown
                """ Appends objects to the repeated container. """
                pass

            def insert(self, *args, **kwargs):  # real signature unknown
                """ Inserts an object at the specified position in the container. """
                pass

            def MergeFrom(self, *args, **kwargs):  # real signature unknown
                """ Merges a repeated container into the current container. """
                pass

            def pop(self, *args, **kwargs):  # real signature unknown
                """ Removes an object from the repeated container and returns it. """
                pass

            def remove(self, *args, **kwargs):  # real signature unknown
                """ Removes an object from the repeated container. """
                pass

            def reverse(self, *args, **kwargs):  # real signature unknown
                """ Reverses elements order of the repeated container. """
                pass

            def sort(self, *args, **kwargs):  # real signature unknown
                """ Sorts the repeated container. """
                pass

            def __deepcopy__(self, *args, **kwargs):  # real signature unknown
                """ Makes a deep copy of the class. """
                pass

            def __delitem__(self, *args, **kwargs):  # real signature unknown
                """ Delete self[key]. """
                pass

            def __eq__(self, *args, **kwargs):  # real signature unknown
                """ Return self==value. """
                pass

            def __getitem__(self, *args, **kwargs):  # real signature unknown
                """ Return self[key]. """
                pass

            def __ge__(self, *args, **kwargs):  # real signature unknown
                """ Return self>=value. """
                pass

            def __gt__(self, *args, **kwargs):  # real signature unknown
                """ Return self>value. """
                pass

            def __init__(self, *args, **kwargs):  # real signature unknown
                pass

            def __len__(self, *args, **kwargs):  # real signature unknown
                """ Return len(self). """
                pass

            def __le__(self, *args, **kwargs):  # real signature unknown
                """ Return self<=value. """
                pass

            def __lt__(self, *args, **kwargs):  # real signature unknown
                """ Return self<value. """
                pass

            def __ne__(self, *args, **kwargs):  # real signature unknown
                """ Return self!=value. """
                pass

            def __reduce__(self, *args, **kwargs):  # real signature unknown
                """ Outputs picklable representation of the repeated field. """
                pass

            def __repr__(self, *args, **kwargs):  # real signature unknown
                """ Return repr(self). """
                pass

            def __setitem__(self, *args, **kwargs):  # real signature unknown
                """ Set self[key] to value. """
                pass

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
