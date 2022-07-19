import datetime
import inspect
import json
from dataclasses import MISSING
from enum import IntEnum
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from pydantic import BaseModel, Field, root_validator
from pydantic.fields import FieldInfo, Undefined
from pydantic.typing import NoArgAnyCallable

from protobuf_to_pydantic.customer_validator import check_one_of
from protobuf_to_pydantic.get_desc import get_desc_from_pgv, get_desc_from_proto_file, get_desc_from_pyi_file
from protobuf_to_pydantic.grpc_types import AnyMessage, Descriptor, FieldDescriptor, Message, Timestamp
from protobuf_to_pydantic.util import Timedelta, create_pydantic_model

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
    default_factory: Optional[Callable] = Field(None)
    example: Any = Field(MISSING)
    alias: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    const: Any = Field(MISSING)
    gt: Union[int, float, None] = Field(None)
    ge: Union[int, float, None] = Field(None)
    lt: Union[int, float, None] = Field(None)
    le: Union[int, float, None] = Field(None)
    min_length: Optional[int] = Field(None)
    max_length: Optional[int] = Field(None)
    min_items: Optional[int] = Field(None)
    max_items: Optional[int] = Field(None)
    unique_items: Optional[bool] = Field(None)
    multiple_of: Optional[int] = Field(None)
    regex: Optional[str] = Field(None)
    extra: dict = Field(default_factory=dict)
    type_: Any = Field(None, alias="type")
    validator: Optional[Dict[str, Any]] = Field(None)
    sub: Optional["MessagePaitModel"] = Field(None)


class M2P(object):
    def __init__(
        self,
        msg: Union[Type[Message], Descriptor],
        default_field: Type[FieldInfo] = FieldInfo,
        field_dict: Optional[Dict[str, FieldInfo]] = None,
        comment_prefix: str = "p2p:",
        parse_msg_desc_method: Any = None,
        pydantic_base: Optional[Type["BaseModel"]] = None,
        pydantic_module: Optional[str] = None,
        local_dict: Optional[Dict[str, Any]] = None,
    ):
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
        elif parse_msg_desc_method == "PGV":
            message_field_dict = get_desc_from_pgv(message=msg)
        elif parse_msg_desc_method is not None:
            raise ValueError(
                f"parse_msg_desc_method param must be exist path or `PGV` or message model,"
                f" not {parse_msg_desc_method})"
            )
        self._parse_msg_desc_method: Optional[str] = parse_msg_desc_method
        self._field_doc_dict = message_field_dict
        self._field_dict = field_dict or {}
        self._default_field = default_field
        self._comment_prefix = comment_prefix
        self._local_dict = local_dict
        self._creat_cache: Dict[Union[Type[Message], Descriptor], Type[BaseModel]] = {}
        self._pydantic_base: Type["BaseModel"] = pydantic_base or BaseModel
        self._pydantic_module: str = pydantic_module or __name__

        self._gen_model: Type[BaseModel] = self._parse_msg_to_pydantic_model(
            descriptor=msg if isinstance(msg, Descriptor) else msg.DESCRIPTOR,
        )

    @property
    def model(self) -> Type[BaseModel]:
        return self._gen_model

    def _field_param_dict_handle(self, field_param_dict: dict, default: Any) -> None:
        if field_param_dict.pop("miss_default") is not True:
            field_param_dict["default"] = default
        if field_param_dict["default_factory"]:
            field_param_dict.pop("default", "")
        if field_param_dict.get("const").__class__ != MISSING.__class__:
            field_param_dict["default"] = field_param_dict["const"]
            field_param_dict["const"] = True
        else:
            field_param_dict.pop("const")

        if field_param_dict.get("example").__class__ == MISSING.__class__:
            field_param_dict.pop("example")

        extra = field_param_dict.pop("extra")
        if extra:
            field_param_dict.update(extra)

        field_type = field_param_dict.get("type_")
        sub_field_param_dict: Optional[dict] = field_param_dict.pop("sub", None)
        field_type_model: Optional[ModuleType] = inspect.getmodule(field_type)
        if (
            field_type
            and not inspect.isclass(field_type)
            and field_type_model
            and field_type_model.__name__
            in (
                "pydantic.types",
                "protobuf_to_pydantic.customer_con_type",
            )
        ):
            # support https://pydantic-docs.helpmanual.io/usage/types/#constrained-types
            # Parameters needed to extract `constrained-types`
            type_param_dict: dict = {}
            for key in inspect.signature(field_type).parameters.keys():
                if key in field_param_dict:
                    type_param_dict[key] = field_param_dict.pop(key)

            if sub_field_param_dict and "type_" in sub_field_param_dict:
                # If a nested type is found, use the same treatment
                self._field_param_dict_handle(sub_field_param_dict, default)
                field_param_dict["type_"] = field_type(sub_field_param_dict["type_"], **type_param_dict)
            else:
                field_param_dict["type_"] = field_type(**type_param_dict)

    # flake8: noqa: C901
    def _parse_msg_to_pydantic_model(self, *, descriptor: Descriptor, class_name: str = "") -> Type[BaseModel]:
        if descriptor in self._creat_cache:
            return self._creat_cache[descriptor]

        annotation_dict: Dict[str, Tuple[Type, Any]] = {}
        validators: Dict[str, classmethod] = {}
        pydantic_model_config_dict: Dict[str, Any] = {}
        one_of_dict: Dict[str, Any] = {}

        for one_of in descriptor.oneofs:
            if one_of.full_name not in one_of_dict:
                one_of_dict[one_of.full_name] = {"required": False, "fields": set()}
            if one_of.full_name in self._field_doc_dict:
                one_of_dict[one_of.full_name]["required"] = self._field_doc_dict[one_of.full_name].get(
                    "required", False
                )
            for _field in one_of.fields:
                one_of_dict[one_of.full_name]["fields"].add(_field.name)
        for column in descriptor.fields:
            type_: Any = type_dict.get(column.type, None)
            name: str = column.name
            default: Any = Undefined
            default_factory: Optional[NoArgAnyCallable] = None

            if column.type == FieldDescriptor.TYPE_MESSAGE:
                if column.message_type.name == "Timestamp":
                    # support google.protobuf.Timestamp
                    type_ = datetime.datetime
                elif column.message_type.name.endswith("Entry"):
                    # support google.protobuf.MapEntry
                    key, value = column.message_type.fields
                    key_type: Any = (
                        type_dict[key.type]
                        if not key.message_type
                        else self._parse_msg_to_pydantic_model(descriptor=key.message_type)
                    )
                    value_type: Any = (
                        type_dict[value.type]
                        if not value.message_type
                        else self._parse_msg_to_pydantic_model(descriptor=value.message_type)
                    )
                    type_ = Dict[key_type, value_type]
                elif column.message_type.name == "Struct":
                    # support google.protobuf.Struct
                    type_ = Dict[str, Any]
                elif column.name == "empty":
                    type_ = Any
                elif column.message_type.name == "Duration":
                    type_ = Timedelta
                elif column.message_type.name == "Any":
                    type_ = AnyMessage
                    if not self._pydantic_base.Config.arbitrary_types_allowed:
                        pydantic_model_config_dict["arbitrary_types_allowed"] = True
                else:
                    # support google.protobuf.Message
                    if column.message_type.full_name.startswith(".".join(column.full_name.split(".")[:-1])):
                        # A dynamically generated class cannot be a subclass of a class,
                        # so it can only be distinguished by adding the beginning of the subclass name
                        _class_name: str = "".join(column.message_type.full_name.split(".")[-2:])
                    else:
                        _class_name = column.message_type.name
                    type_ = self._parse_msg_to_pydantic_model(descriptor=column.message_type, class_name=_class_name)

            elif column.type == FieldDescriptor.TYPE_ENUM:
                # support google.protobuf.Enum
                type_ = IntEnum(  # type: ignore
                    column.enum_type.name, {v.name: v.number for v in column.enum_type.values}
                )
                default = 0
            else:
                if column.label == FieldDescriptor.LABEL_REQUIRED:
                    default = Undefined
                else:
                    default = column.default_value

            if column.label == FieldDescriptor.LABEL_REPEATED:
                if not (column.message_type and column.message_type.name.endswith("Entry")):
                    type_ = List[type_]  # type: ignore
                    default_factory = list
                    # TODO support lambda
                    if default is not Undefined:
                        default = Undefined

            field = self._default_field
            field_doc: Union[str, dict] = self._get_field_doc_by_full_name(column.full_name)
            if field_doc:
                if isinstance(field_doc, str):
                    msg_pait_model: MessagePaitModel = self._get_pait_info_from_grpc_desc(field_doc)
                else:
                    # support from pgv
                    msg_pait_model = MessagePaitModel(**field_doc)
                    # TODO support
                    if "map_type" in field_doc and type_._name == "Dict":
                        raw_keys_type, raw_values_type = type_.__args__
                        if "keys" in field_doc["map_type"]:
                            new_keys_type = field_doc["map_type"]["keys"]
                            if issubclass(new_keys_type, raw_keys_type):
                                raw_keys_type = new_keys_type
                        if "values" in field_doc["map_type"]:
                            new_values_type = field_doc["map_type"]["values"]
                            if issubclass(new_values_type, raw_values_type):
                                raw_values_type = new_values_type
                        type_ = Dict[raw_keys_type, raw_values_type]  # type: ignore

                field_param_dict: dict = msg_pait_model.dict()
                # Nested types do not include the `enable`, `field` and `validator`  attributes
                if not field_param_dict.pop("enable"):
                    continue
                _field = field_param_dict.pop("field")
                if _field:
                    field = field
                validator_dict = field_param_dict.pop("validator")
                if validator_dict:
                    validators.update(validator_dict)

                # Unified field parameter handling
                self._field_param_dict_handle(field_param_dict, default)
                field_type = field_param_dict.pop("type_")
                if field_type:
                    type_ = field_type
            else:
                field_param_dict = {"default": default, "default_factory": default_factory}
            use_field = field(**field_param_dict)  # type: ignore
            annotation_dict[name] = (type_, use_field)

        if one_of_dict:
            validators["one_of_validator"] = root_validator(pre=True, allow_reuse=True)(check_one_of)

        if descriptor.name == "Any":
            # Message.Any and typing.Any with the same name, need to change the name of Message.Any.
            class_name = "AnyMessage"
        elif not class_name:
            class_name = descriptor.name

        if pydantic_model_config_dict:
            # Changing the configuration of Config by inheritance
            pydantic_base: Type[BaseModel] = type(  # type: ignore
                self._pydantic_base.__name__,
                (self._pydantic_base,),
                {
                    "Config": type(
                        self._pydantic_base.Config.__name__, (self._pydantic_base.Config,), pydantic_model_config_dict
                    )
                },
            )
        else:
            pydantic_base = self._pydantic_base
        pydantic_model: Type[BaseModel] = create_pydantic_model(
            annotation_dict,
            class_name=class_name,
            pydantic_validators=validators or None,
            pydantic_module=self._pydantic_module,
            pydantic_base=pydantic_base,
        )
        setattr(pydantic_model, "_one_of_dict", one_of_dict)
        self._creat_cache[descriptor] = pydantic_model
        return pydantic_model

    def _get_pait_info_from_grpc_desc(self, desc: str) -> MessagePaitModel:
        pait_dict: dict = {}
        for line in desc.split("\n"):
            line = line.strip()
            if not line.startswith(self._comment_prefix):
                continue
            line = line.replace(self._comment_prefix, "")
            pait_dict.update(json.loads(line))
        for k, v in pait_dict.items():
            if not isinstance(v, str):
                continue
            try:
                if v.startswith("p2p@import"):
                    _, var_str, module_str = v.split("|")
                    v = getattr(import_module(module_str.split(".")[0], module_str), var_str)
                elif v.startswith("p2p@local") and self._local_dict:
                    _, var_str = v.split("|")
                    v = self._local_dict[var_str]
                elif v.startswith("p2p@"):
                    raise ValueError(f"Only support p2p@import, p2p@local prefix. not {v}")
                else:
                    continue
                pait_dict[k] = v
            except Exception as e:
                raise ValueError(f"parse {v} error: {e}")

        field_name: str = pait_dict.pop("field", "")
        if field_name in self._field_dict:
            pait_dict["field"] = self._field_dict[field_name]
        return MessagePaitModel(**pait_dict)

    def _get_field_doc_by_full_name(self, full_name: str) -> Any:
        field_doc_dict: dict = self._field_doc_dict
        key_list = full_name.split(".")[1:]  # ignore package name
        for key in key_list:
            if key in field_doc_dict:
                field_doc_dict = field_doc_dict[key]
            else:
                return None
        return field_doc_dict


def msg_to_pydantic_model(
    msg: Union[Type[Message], Descriptor],
    default_field: Type[FieldInfo] = FieldInfo,
    field_dict: Optional[Dict[str, FieldInfo]] = None,
    comment_prefix: str = "p2p:",
    parse_msg_desc_method: Any = None,
    local_dict: Optional[Dict[str, Any]] = None,
    pydantic_base: Optional[Type["BaseModel"]] = None,
    pydantic_module: Optional[str] = None,
) -> Type[BaseModel]:
    """
    Parse a message to a pydantic model
    :param msg: grpc Message or descriptor
    :param default_field: gen pydantic_model default Field,
        apply only to the outermost pydantic model
    :param field_dict: Define which FieldInfo should be used for the parameter (to support the pait framework)
    :param comment_prefix: Customize the prefixes that need to be parsed for comments
    :param parse_msg_desc_method: Define the type of comment to be parsed, if the value is a protobuf file path,
        it will be parsed by protobuf file; if it is a module of message object, it will be parsed by pyi file
    :param local_dict: The variables corresponding to the p2p@local template
    """
    return M2P(
        msg=msg,
        default_field=default_field,
        field_dict=field_dict,
        comment_prefix=comment_prefix,
        parse_msg_desc_method=parse_msg_desc_method,
        local_dict=local_dict,
        pydantic_module=pydantic_module,
        pydantic_base=pydantic_base,
    ).model
