import datetime
import inspect
import json
from dataclasses import MISSING
from enum import IntEnum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from pydantic import BaseModel, Field, validator
from pydantic.fields import FieldInfo, Undefined
from pydantic.typing import NoArgAnyCallable

from protobuf_to_pydantic.get_desc import get_desc_from_proto_file, get_desc_from_pyi_file
from protobuf_to_pydantic.grpc_types import Descriptor, FieldDescriptor, Message, Timestamp
from protobuf_to_pydantic.util import create_pydantic_model

type_dict: Dict[str, Type] = {
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

GRPC_TIMESTAMP_HANDLER_TUPLE_T = Tuple[Any, Optional[Callable[[Any, Any], Timestamp]]]


class MessagePaitModel(BaseModel):
    field: Optional[Type[FieldInfo]] = Field(None)
    enable: bool = Field(True)
    miss_default: bool = Field(False)
    example: Any = Field(MISSING)
    alias: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    const: Optional[bool] = Field(None)
    gt: Union[int, float, None] = Field(None)
    ge: Union[int, float, None] = Field(None)
    lt: Union[int, float, None] = Field(None)
    le: Union[int, float, None] = Field(None)
    min_length: Optional[int] = Field(None)
    max_length: Optional[int] = Field(None)
    min_items: Optional[int] = Field(None)
    max_items: Optional[int] = Field(None)
    multiple_of: Optional[int] = Field(None)
    regex: Optional[str] = Field(None)
    extra: dict = Field(default_factory=dict)


def get_pait_info_from_grpc_desc(comment_prefix: str, desc: str, field_dict: Dict[str, FieldInfo]) -> MessagePaitModel:
    pait_dict: dict = {}
    for line in desc.split("\n"):
        line = line.strip()
        if not line.startswith(comment_prefix):
            continue
        line = line.replace(comment_prefix, "")
        pait_dict.update(json.loads(line))
    field_name: str = pait_dict.pop("field", "")
    if field_name in field_dict:
        pait_dict["field"] = field_dict[field_name]
    return MessagePaitModel(**pait_dict)


def grpc_timestamp_int_handler(cls: Any, v: int) -> Timestamp:
    t: Timestamp = Timestamp()

    if v:
        t.FromDatetime(datetime.datetime.fromtimestamp(v))
    return t


def _get_field_doc_by_full_name(full_name: str, field_doc_dict: dict) -> Any:
    key_list = full_name.split(".")[1:]  # ignore package name
    for key in key_list:
        if key in field_doc_dict:
            field_doc_dict = field_doc_dict[key]
        else:
            return None
    return field_doc_dict


def _parse_msg_to_pydantic_model(
    *,
    descriptor: Descriptor,
    grpc_timestamp_handler_tuple: GRPC_TIMESTAMP_HANDLER_TUPLE_T,
    field_doc_dict: dict,
    field_dict: Dict[str, FieldInfo],
    comment_prefix: str,
    default_field: Type[FieldInfo],
) -> Type[BaseModel]:
    annotation_dict: Dict[str, Tuple[Type, Any]] = {}
    validators: Dict[str, classmethod] = {}
    timestamp_handler_field_silt: List[str] = []
    timestamp_type, _grpc_timestamp_handler = grpc_timestamp_handler_tuple

    for column in descriptor.fields:
        type_: Any = type_dict.get(column.type, None)
        name: str = column.name
        default: Any = Undefined
        default_factory: Optional[NoArgAnyCallable] = None

        if column.type == FieldDescriptor.TYPE_MESSAGE:
            if column.message_type.name == "Timestamp":
                # support google.protobuf.Timestamp
                type_ = timestamp_type
                timestamp_handler_field_silt.append(column.name)
            elif column.message_type.name.endswith("Entry"):
                # support google.protobuf.MapEntry
                key, value = column.message_type.fields
                key_type: Any = (
                    type_dict[key.type]
                    if not key.message_type
                    else _parse_msg_to_pydantic_model(
                        descriptor=key.message_type,
                        grpc_timestamp_handler_tuple=grpc_timestamp_handler_tuple,
                        field_doc_dict=field_doc_dict,
                        field_dict=field_dict,
                        comment_prefix=comment_prefix,
                        default_field=default_field,
                    )
                )
                value_type: Any = (
                    type_dict[value.type]
                    if not value.message_type
                    else _parse_msg_to_pydantic_model(
                        descriptor=value.message_type,
                        grpc_timestamp_handler_tuple=grpc_timestamp_handler_tuple,
                        field_doc_dict=field_doc_dict,
                        field_dict=field_dict,
                        comment_prefix=comment_prefix,
                        default_field=default_field,
                    )
                )
                type_ = Dict[key_type, value_type]
            elif column.message_type.name == "Struct":
                # support google.protobuf.Struct
                type_ = Dict[str, Any]
            elif column.name == "empty":
                type_ = Any
            else:
                # support google.protobuf.Message
                type_ = _parse_msg_to_pydantic_model(
                    descriptor=column.message_type,
                    grpc_timestamp_handler_tuple=grpc_timestamp_handler_tuple,
                    field_doc_dict=field_doc_dict,
                    field_dict=field_dict,
                    comment_prefix=comment_prefix,
                    default_field=default_field,
                )
        elif column.type == FieldDescriptor.TYPE_ENUM:
            # support google.protobuf.Enum
            type_ = IntEnum(column.enum_type.name, {v.name: v.number for v in column.enum_type.values})  # type: ignore
            default = 0
        else:
            if column.label == FieldDescriptor.LABEL_REQUIRED:
                default = Undefined
            elif column.label == FieldDescriptor.LABEL_REPEATED:
                type_ = List[type_]  # type: ignore
                default_factory = list
            else:
                default = column.default_value

        field = default_field
        field_doc: str = _get_field_doc_by_full_name(column.full_name, field_doc_dict)
        if field_doc:
            msg_pait_model: MessagePaitModel = get_pait_info_from_grpc_desc(comment_prefix, field_doc, field_dict)
            field_param_dict: dict = msg_pait_model.dict()
            if not field_param_dict.pop("enable"):
                continue
            if field_param_dict.pop("miss_default") is not True:
                field_param_dict["default"] = default
            field_param_dict["default_factory"] = default_factory
            if field_param_dict.get("example").__class__ == MISSING.__class__:
                field_param_dict.pop("example")

            _field = field_param_dict.pop("field")
            if _field:
                field = field
            extra = field_param_dict.pop("extra")
            if extra:
                field_param_dict.update(extra)
        else:
            field_param_dict = {"default": default, "default_factory": default_factory}
        use_field = field(**field_param_dict)  # type: ignore
        annotation_dict[name] = (type_, use_field)

    if timestamp_handler_field_silt and _grpc_timestamp_handler:
        validators["timestamp_validator"] = validator(
            *timestamp_handler_field_silt,
            allow_reuse=True,
            check_fields=True,
            always=True,
        )(_grpc_timestamp_handler)
    return create_pydantic_model(annotation_dict, class_name=descriptor.name, pydantic_validators=validators or None)


def msg_to_pydantic_model(
    msg: Union[Type[Message], Descriptor],
    default_field: Type[FieldInfo] = FieldInfo,
    grpc_timestamp_handler_tuple: Optional[GRPC_TIMESTAMP_HANDLER_TUPLE_T] = None,
    field_dict: Optional[Dict[str, FieldInfo]] = None,
    comment_prefix: str = "p2p:",
    parse_msg_desc_method: Any = None,
) -> Type[BaseModel]:
    """
    Parse a message to a pydantic model
    :param msg: grpc Message or descriptor
    :param default_field: gen pydantic_model default Field,
        apply only to the outermost pydantic model
    :param grpc_timestamp_handler_tuple:
    :param field_dict: Define which FieldInfo should be used for the parameter (to support the pait framework)
    :param comment_prefix: Customize the prefixes that need to be parsed for comments
    :param parse_msg_desc_method: Define the type of comment to be parsed, if the value is a protobuf file path,
        it will be parsed by protobuf file; if it is a module of message object, it will be parsed by pyi file
    """
    message_field_dict: Dict[str, Dict[str, str]] = {}

    proto_file_name = msg.DESCRIPTOR.file.name
    if proto_file_name.endswith("empty.proto"):
        raise ValueError("Not support Empty Message")
    if isinstance(parse_msg_desc_method, str) and Path(parse_msg_desc_method).exists():
        file_str: str = parse_msg_desc_method
        if not file_str.endswith("/"):
            file_str += "/"
        message_field_dict = get_desc_from_proto_file(file_str + proto_file_name)
    elif inspect.ismodule(parse_msg_desc_method):
        if getattr(parse_msg_desc_method, msg.__name__, None) is not msg:
            raise ValueError(f"Not the module corresponding to {msg}")
        pyi_file_name = parse_msg_desc_method.__file__ + "i"  # type: ignore
        if not Path(pyi_file_name).exists():
            raise RuntimeError(f"Can not found {msg} pyi file")
        message_field_dict = get_desc_from_pyi_file(pyi_file_name)
    elif parse_msg_desc_method is not None:
        raise ValueError(
            f"parse_msg_desc_method param must be exist path or `by_mypy` or `by_pait`, not {parse_msg_desc_method})"
        )

    return _parse_msg_to_pydantic_model(
        descriptor=msg if isinstance(msg, Descriptor) else msg.DESCRIPTOR,
        grpc_timestamp_handler_tuple=grpc_timestamp_handler_tuple or (str, None),
        field_doc_dict=message_field_dict,
        field_dict=field_dict or {},
        default_field=default_field,
        comment_prefix=comment_prefix,
    )
