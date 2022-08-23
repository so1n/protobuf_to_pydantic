import datetime
import inspect
import json
import logging
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
from protobuf_to_pydantic.get_desc import (
    get_desc_from_p2p,
    get_desc_from_pgv,
    get_desc_from_proto_file,
    get_desc_from_pyi_file,
)
from protobuf_to_pydantic.grpc_types import (
    AnyMessage,
    Descriptor,
    FieldDescriptor,
    Message,
    RepeatedCompositeContainer,
    RepeatedScalarContainer,
)
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
_message_type_dict_by_type_name: Dict[str, Any] = {
    "Timestamp": datetime.datetime,
    "Struct": Dict[str, Any],
    "Empty": Any,
    "Duration": Timedelta,
    "Any": AnyMessage,
}
_message_default_factory_dict_by_type_name: Dict[str, Any] = {
    "Timestamp": datetime.datetime.now,
    "Struct": Dict[str, Any],
    "Duration": Timedelta,
    "Any": AnyMessage,
}


def check_dict_one_of(desc_dict: dict, key_list: List[str]) -> bool:
    if (
        len(
            [
                desc_dict.get(key, None)
                for key in key_list
                if desc_dict.get(key, None) and desc_dict[key].__class__ != MISSING.__class__
            ]
        )
        > 1
    ):
        raise RuntimeError(f"Field:{key_list} cannot have both values")
    return True


class MessagePaitModel(BaseModel):
    field: Optional[Type[FieldInfo]] = Field(None)
    enable: bool = Field(True)
    miss_default: bool = Field(False)
    default: Optional[Any] = Field(None)
    default_factory: Optional[Callable] = Field(None)
    example: Any = Field(MISSING)
    example_factory: Optional[Callable] = Field(None)
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
    map_type: Optional[Dict[str, type]] = Field(None)


class DescTemplate(object):
    def __init__(self, local_dict: dict, comment_prefix: str) -> None:
        self._local_dict: dict = local_dict
        self._comment_prefix: str = comment_prefix
        self._support_template_list: List[str] = [i for i in dir(self) if i.startswith("template")]

    def template_import_instance(self, template_var_list: List[str]) -> Any:
        module_str, var_str, json_param = template_var_list
        module: Any = import_module(module_str, module_str)
        for sub_var_str in var_str.split("."):
            module = getattr(module, sub_var_str)
        if json_param:
            var = module(**json.loads(json_param))  # type: ignore
        else:
            var = module
        return var

    def template_import(self, template_var_list: List[str]) -> Any:
        module_str, var_str = template_var_list
        module = import_module(module_str, module_str)
        for sub_var_str in var_str.split("."):
            module = getattr(module, sub_var_str)
        return module

    def template_local(self, template_var_list: List[str]) -> Any:
        return self._local_dict[template_var_list[0]]

    def template_builtin(self, template_var_list: List[str]) -> Any:
        return __builtins__.get(template_var_list[0])  # type: ignore

    def _template_str_handler(self, template_str: str) -> Any:
        try:
            template_str_list: List[str] = template_str.split("|")
            template_rule, *template_var_list = template_str_list
            template_fn: Optional[Callable] = getattr(self, f"template_{template_rule}", None)
            if not template_fn:
                raise ValueError(f"Only support {' ,'.join(self._support_template_list)}. not {template_str}")
            return template_fn(template_var_list)
        except Exception as e:
            raise ValueError(f"parse {template_str} error: {e}") from e

    def get_value(self, container: Any) -> Any:
        if isinstance(container, (list, RepeatedCompositeContainer, RepeatedScalarContainer)):
            return [self.get_value(i) for i in container]
        elif isinstance(container, dict):
            return {k: self.get_value(v) for k, v in container.items()}
        elif isinstance(container, str) and container.startswith(f"{self._comment_prefix}@"):
            container = container.replace(f"{self._comment_prefix}@", "")
            return self._template_str_handler(container)
        else:
            return container


class M2P(object):
    def __init__(
        self,
        msg: Union[Type[Message], Descriptor],
        default_field: Type[FieldInfo] = FieldInfo,
        comment_prefix: str = "p2p",
        parse_msg_desc_method: Any = None,
        pydantic_base: Optional[Type["BaseModel"]] = None,
        pydantic_module: Optional[str] = None,
        local_dict: Optional[Dict[str, Any]] = None,
        desc_template: Optional[Type[DescTemplate]] = None,
        message_type_dict_by_type_name: Optional[Dict[str, Any]] = None,
        message_default_factory_dict_by_type_name: Optional[Dict[str, Any]] = None,
    ):
        proto_file_name = msg.DESCRIPTOR.file.name  # type: ignore
        message_field_dict: Dict[str, Dict[str, str]] = {}
        if proto_file_name.endswith("empty.proto"):
            logging.warning("parse_msg_desc not support Empty message")
        elif parse_msg_desc_method == "ignore":
            pass
        elif isinstance(parse_msg_desc_method, str) and Path(parse_msg_desc_method).exists():
            file_str: str = parse_msg_desc_method
            if not file_str.endswith("/"):
                file_str += "/"
            message_field_dict = get_desc_from_proto_file(file_str + proto_file_name)
        elif inspect.ismodule(parse_msg_desc_method):
            if getattr(parse_msg_desc_method, msg.__name__, None) is not msg:  # type: ignore
                raise ValueError(f"Not the module corresponding to {msg}")
            pyi_file_name = parse_msg_desc_method.__file__ + "i"  # type: ignore
            if not Path(pyi_file_name).exists():
                raise RuntimeError(f"Can not found {msg} pyi file")
            message_field_dict = get_desc_from_pyi_file(pyi_file_name)
        elif parse_msg_desc_method == "PGV":
            message_field_dict = get_desc_from_pgv(message=msg)  # type: ignore
        elif parse_msg_desc_method is not None:
            import os

            raise ValueError(
                f"parse_msg_desc_method param must be exist path, `ignore` or `PGV`,"
                f" not {parse_msg_desc_method}), now path:{os.getcwd()}"
            )
        else:
            message_field_dict = get_desc_from_p2p(message=msg)  # type: ignore
        self._parse_msg_desc_method: Optional[str] = parse_msg_desc_method
        self._field_doc_dict = message_field_dict
        self._default_field = default_field
        self._comment_prefix = comment_prefix
        self._local_dict = local_dict or {}
        self._creat_cache: Dict[Union[Type[Message], Descriptor], Type[BaseModel]] = {}
        self._pydantic_base: Type["BaseModel"] = pydantic_base or BaseModel
        self._pydantic_module: str = pydantic_module or __name__
        self._desc_template: DescTemplate = (desc_template or DescTemplate)(self._local_dict, self._comment_prefix)
        self._message_type_dict_by_type_name: Dict[str, Any] = (
            message_type_dict_by_type_name or _message_type_dict_by_type_name
        )
        self._message_default_factory_dict_by_type_name: Dict[str, Any] = (
            message_default_factory_dict_by_type_name or _message_default_factory_dict_by_type_name
        )

        self._gen_model: Type[BaseModel] = self._parse_msg_to_pydantic_model(
            descriptor=msg if isinstance(msg, Descriptor) else msg.DESCRIPTOR,
        )

    @property
    def model(self) -> Type[BaseModel]:
        return self._gen_model

    def _field_param_dict_handle(self, field_param_dict: dict) -> None:
        # PGV const handler
        if field_param_dict.get("const").__class__ != MISSING.__class__:
            field_param_dict["default"] = field_param_dict["const"]
            field_param_dict["const"] = True
        else:
            field_param_dict.pop("const")

        if field_param_dict.get("example").__class__ == MISSING.__class__:
            field_param_dict.pop("example")
        example_factory = field_param_dict.pop("example_factory")
        if example_factory:
            field_param_dict["example"] = example_factory

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
                self._field_param_dict_handle(sub_field_param_dict)
                field_param_dict["type_"] = field_type(sub_field_param_dict["type_"], **type_param_dict)
            else:
                field_param_dict["type_"] = field_type(**type_param_dict)

    def _one_of_handle(self, descriptor: Descriptor) -> Dict[str, Any]:
        one_of_dict: Dict[str, Any] = {}
        for one_of in descriptor.oneofs:
            if one_of.full_name not in one_of_dict:
                one_of_dict[one_of.full_name] = {"required": False, "fields": set()}
            if one_of.full_name in self._field_doc_dict:
                # only PGV support
                # The use of full name here and the use of name elsewhere will lead to confusion in the storage
                # range of field_doc_dict, which must be changed later.
                one_of_dict[one_of.full_name]["required"] = self._field_doc_dict[one_of.full_name].get(
                    "required", False
                )
            for _field in one_of.fields:
                one_of_dict[one_of.full_name]["fields"].add(_field.name)
        return one_of_dict

    def _get_pydantic_base(self, pydantic_model_config_dict: Dict[str, Any]) -> Type[BaseModel]:
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
        return pydantic_base

    # flake8: noqa: C901
    def _parse_msg_to_pydantic_model(self, *, descriptor: Descriptor, class_name: str = "") -> Type[BaseModel]:
        if descriptor in self._creat_cache:
            return self._creat_cache[descriptor]

        annotation_dict: Dict[str, Tuple[Type, Any]] = {}
        validators: Dict[str, classmethod] = {}
        pydantic_model_config_dict: Dict[str, Any] = {}
        one_of_dict: Dict[str, Any] = self._one_of_handle(descriptor)
        if one_of_dict:
            validators["one_of_validator"] = root_validator(pre=True, allow_reuse=True)(check_one_of)

        # parse field
        for column in descriptor.fields:
            type_: Any = type_dict.get(column.type, None)
            name: str = column.name
            default: Any = Undefined
            default_factory: Optional[NoArgAnyCallable] = None

            if column.type == FieldDescriptor.TYPE_MESSAGE:
                if column.message_type.name in self._message_type_dict_by_type_name:
                    type_ = self._message_type_dict_by_type_name[column.message_type.name]
                    if column.message_type.name in self._message_default_factory_dict_by_type_name:
                        default_factory = self._message_default_factory_dict_by_type_name[column.message_type.name]
                elif column.message_type.name.endswith("Entry"):
                    # support google.protobuf.MapEntry
                    key, value = column.message_type.fields

                    if not key.message_type:
                        key_type: Any = type_dict[key.type]
                    elif key.message_type.name in self._message_type_dict_by_type_name:
                        key_type = self._message_type_dict_by_type_name[key.message_type.name]
                    else:
                        key_type = self._parse_msg_to_pydantic_model(descriptor=key.message_type)
                    if not value.message_type:
                        value_type: Any = type_dict[value.type]
                    elif value.message_type.name in self._message_type_dict_by_type_name:
                        value_type = self._message_type_dict_by_type_name[value.message_type.name]
                    else:
                        value_type = self._parse_msg_to_pydantic_model(descriptor=value.message_type)
                    type_ = Dict[key_type, value_type]
                    default_factory = dict
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
                # Refine field properties with data from desc
                if isinstance(field_doc, str):
                    # support protobuf optional by comment
                    field_doc_dict = self._gen_dict_from_desc_str(field_doc)
                else:
                    field_doc_dict = field_doc
                if self._parse_msg_desc_method != "PGV":
                    # pgv method not support template var
                    field_doc_dict = self._desc_template.get_value(field_doc_dict)

                field_param_dict: dict = MessagePaitModel(**field_doc_dict).dict()
                # Nested types do not include the `enable`, `field`, `validator` and `type`  attributes
                if not field_param_dict.pop("enable"):
                    continue
                _field = field_param_dict.pop("field")
                if _field:
                    field = _field
                validator_dict = field_param_dict.pop("validator")
                if validator_dict:
                    validators.update(validator_dict)

                check_dict_one_of(field_param_dict, ["miss_default", "default", "default_factory"])
                check_dict_one_of(field_param_dict, ["example", "example_factory"])
                if field_param_dict["default_factory"] is not None:
                    field_param_dict.pop("default", "")
                elif field_param_dict["miss_default"] is True:
                    field_param_dict.pop("default", "")
                    field_param_dict.pop("default_factory", "")
                elif field_param_dict["default"] is None:
                    field_param_dict["default"] = default
                if field_param_dict.get("default", None) is default:
                    field_param_dict["default_factory"] = default_factory
                field_param_dict.pop("miss_default", None)

                # Unified field parameter handling
                self._field_param_dict_handle(field_param_dict)

                # Type will change in the unified processing logic
                field_type = field_param_dict.pop("type_", type_)
                map_type_dict = field_param_dict.pop("map_type", {})
                if field_type:
                    type_ = field_type
                elif map_type_dict and type_._name == "Dict":
                    raw_keys_type, raw_values_type = type_.__args__
                    if "keys" in map_type_dict:
                        new_keys_type = map_type_dict["keys"]
                        if issubclass(new_keys_type, raw_keys_type) or raw_keys_type is datetime.datetime:
                            raw_keys_type = new_keys_type
                    if "values" in map_type_dict:
                        new_values_type = map_type_dict["values"]
                        if issubclass(new_values_type, raw_values_type) or raw_values_type is datetime.datetime:
                            raw_values_type = new_values_type

                    type_ = Dict[raw_keys_type, raw_values_type]  # type: ignore
            else:
                field_param_dict = {"default": default, "default_factory": default_factory}
            use_field = field(**field_param_dict)  # type: ignore
            annotation_dict[name] = (type_, use_field)

            if type_ in (AnyMessage,) and not self._pydantic_base.Config.arbitrary_types_allowed:
                pydantic_model_config_dict["arbitrary_types_allowed"] = True

        pydantic_model: Type[BaseModel] = create_pydantic_model(
            annotation_dict,
            class_name=class_name or descriptor.name,
            pydantic_validators=validators or None,
            pydantic_module=self._pydantic_module,
            pydantic_base=self._get_pydantic_base(pydantic_model_config_dict),
        )
        setattr(pydantic_model, "_one_of_dict", one_of_dict)
        setattr(pydantic_model, "_base_model", self._pydantic_base)
        self._creat_cache[descriptor] = pydantic_model
        return pydantic_model

    def _gen_dict_from_desc_str(self, desc: str) -> dict:
        pait_dict: dict = {}
        for line in desc.split("\n"):
            line = line.strip()
            if not line.startswith(f"{self._comment_prefix}:"):
                continue
            line = line.replace(f"{self._comment_prefix}:", "")
            pait_dict.update(json.loads(line))
        return pait_dict

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
    comment_prefix: str = "p2p",
    parse_msg_desc_method: Any = None,
    local_dict: Optional[Dict[str, Any]] = None,
    pydantic_base: Optional[Type["BaseModel"]] = None,
    pydantic_module: Optional[str] = None,
    desc_template: Optional[Type[DescTemplate]] = None,
    message_type_dict_by_type_name: Optional[Dict[str, Any]] = None,
    message_default_factory_dict_by_type_name: Optional[Dict[str, Any]] = None,
) -> Type[BaseModel]:
    """
    Parse a message to a pydantic model
    :param msg: grpc Message or descriptor
    :param default_field: gen pydantic_model default Field,
        apply only to the outermost pydantic model
    :param comment_prefix: Customize the prefixes that need to be parsed for comments
    :param parse_msg_desc_method: Define the type of comment to be parsed, if the value is a protobuf file path,
        it will be parsed by protobuf file; if it is a module of message object, it will be parsed by pyi file
    :param local_dict: The variables corresponding to the p2p@local template
    :param pydantic_base: custom pydantic.BaseModel
    :param pydantic_module: custom create model's module name
    :param desc_template: Template object, which can extend and modify template adaptation rules through inheritance
    :param message_type_dict_by_type_name: Define the Python type mapping corresponding to each Protobuf Type
    :param message_default_factory_dict_by_type_name: Define the default_factory corresponding to each Protobuf Type
    """
    return M2P(
        msg=msg,
        default_field=default_field,
        comment_prefix=comment_prefix,
        parse_msg_desc_method=parse_msg_desc_method,
        local_dict=local_dict,
        pydantic_module=pydantic_module,
        pydantic_base=pydantic_base,
        desc_template=desc_template,
        message_type_dict_by_type_name=message_type_dict_by_type_name,
        message_default_factory_dict_by_type_name=message_default_factory_dict_by_type_name,
    ).model
