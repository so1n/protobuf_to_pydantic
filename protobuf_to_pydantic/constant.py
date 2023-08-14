import datetime
from typing import Any, Dict, Type

from google.protobuf.any_pb2 import Any as AnyMessage
from google.protobuf.descriptor import FieldDescriptor

from protobuf_to_pydantic import _pydantic_adapter
from protobuf_to_pydantic.util import Timedelta

message_name_default_factory_dict: Dict[str, Any] = {
    "Timestamp": datetime.datetime.now,
    "Struct": Dict[str, Any],
    "Duration": Timedelta,
    "Any": AnyMessage,
}
pydantic_field_v1_migration_v2_dict = {
    "min_items": "min_length",
    "max_items": "max_length",
    "allow_mutation": "frozen",
    "regex": "pattern",
    "const": None,
    "unique_items": None,
}
message_name_type_dict: Dict[str, Any] = {
    "Timestamp": datetime.datetime,
    "Struct": Dict[str, Any],
    "Empty": Any,
    "Duration": Timedelta,
    "Any": AnyMessage,
}

if not _pydantic_adapter.is_v1:
    from pydantic import BeforeValidator
    from typing_extensions import Annotated

    message_name_type_dict["Duration"] = Annotated[datetime.timedelta, BeforeValidator(Timedelta.validate)]
python_type_default_value_dict: Dict[type, Any] = {
    float: 0.0,
    int: 0,
    bool: False,
    str: "",
    bytes: b"",
}
protobuf_desc_python_type_dict: Dict[int, Type] = {
    FieldDescriptor.TYPE_DOUBLE: float,
    FieldDescriptor.TYPE_FLOAT: float,
    FieldDescriptor.TYPE_INT64: int,
    FieldDescriptor.TYPE_UINT64: int,
    FieldDescriptor.TYPE_INT32: int,
    FieldDescriptor.TYPE_FIXED64: float,
    FieldDescriptor.TYPE_FIXED32: float,
    FieldDescriptor.TYPE_BOOL: bool,
    FieldDescriptor.TYPE_STRING: str,
    FieldDescriptor.TYPE_BYTES: bytes,
    FieldDescriptor.TYPE_UINT32: int,
    FieldDescriptor.TYPE_SFIXED32: float,
    FieldDescriptor.TYPE_SFIXED64: float,
    FieldDescriptor.TYPE_SINT32: int,
    FieldDescriptor.TYPE_SINT64: int,
}
