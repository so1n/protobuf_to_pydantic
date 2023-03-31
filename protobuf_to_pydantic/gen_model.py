import datetime
import inspect
import json
from dataclasses import MISSING
from enum import IntEnum
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Type, Union

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

if TYPE_CHECKING:
    from protobuf_to_pydantic.types import DescFromOptionTypedDict, FieldInfoTypedDict, OneOfTypedDict

type_dict: Dict[int, Type] = {
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

python_type_default_value_dict: Dict[type, Any] = {
    float: 0.0,
    int: 0,
    bool: False,
    str: "",
    bytes: b"",
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
    """Check if the key also appears in the dict"""
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
        raise RuntimeError(f"Field:{key_list} cannot have both values: {desc_dict}")
    return True


def replace_file_name_to_class_name(filename: str) -> str:
    """Convert the protobuf file name to the class name(PEP-8)"""
    # example_proto/common/single.proto -> Example_protoCommonSingle
    prefix: str = "".join([str(i).title() for i in Path(filename.split(".")[0]).joinpath().parts])
    # Example_protoCommonSingle -> ExampleProtoCommonSingle
    prefix = prefix.replace("_", "")
    return prefix


def field_param_dict_handle(field_param_dict: dict, default: Any, default_factory: Optional[NoArgAnyCallable]) -> None:
    """Convert the data of field param to the data that pydantic.Base Model can receive"""
    # Handle complex relationships with different defaults
    check_dict_one_of(field_param_dict, ["miss_default", "default", "default_factory"])
    if field_param_dict.get("default_factory", None) is not None:
        field_param_dict.pop("default", "")
    elif field_param_dict.get("default", None) is None:
        if default_factory:
            field_param_dict["default_factory"] = default_factory
            field_param_dict.pop("default", "")
        else:
            field_param_dict["default"] = default
            field_param_dict.pop("default_factory", None)

    if field_param_dict.get("miss_default", None) is True:
        field_param_dict.pop("default", "")
        field_param_dict.pop("default_factory", "")
    field_param_dict.pop("miss_default", None)

    # PGV&P2P const handler
    if field_param_dict.get("const", MISSING).__class__ != MISSING.__class__:
        field_param_dict["default"] = field_param_dict["const"]
        field_param_dict["const"] = True
    else:
        field_param_dict.pop("const", None)

    # example handle
    check_dict_one_of(field_param_dict, ["example", "example_factory"])
    if field_param_dict.get("example", MISSING).__class__ == MISSING.__class__:
        field_param_dict.pop("example", None)
    example_factory = field_param_dict.pop("example_factory", None)
    if example_factory:
        field_param_dict["example"] = example_factory

    # extra handle
    extra = field_param_dict.pop("extra", None)
    if extra:
        field_param_dict.update(extra)

    # type handle
    field_type = field_param_dict.get("type_")
    sub_field_param_dict: Optional[dict] = field_param_dict.pop("sub", None)
    field_type_model: Optional[ModuleType] = inspect.getmodule(field_type)

    if (
        field_type
        and not inspect.isclass(field_type)
        and field_type_model
        and field_type_model.__name__ in ("pydantic.types", "protobuf_to_pydantic.customer_con_type")
    ):
        # support https://pydantic-docs.helpmanual.io/usage/types/#constrained-types
        # Parameters needed to extract `constrained-types`
        type_param_dict: dict = {}
        for key in inspect.signature(field_type).parameters.keys():
            if key in field_param_dict:
                type_param_dict[key] = field_param_dict.pop(key)

        if sub_field_param_dict and "type_" in sub_field_param_dict:
            # If a nested type is found, use the same treatment
            field_param_dict_handle(sub_field_param_dict, default, default_factory)
            field_param_dict["type_"] = field_type(sub_field_param_dict["type_"], **type_param_dict)
        else:
            field_param_dict["type_"] = field_type(**type_param_dict)


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

    def template_import_instance(self, module_str: str, var_str: str, json_param: str) -> Any:
        module: Any = import_module(module_str, module_str)
        for sub_var_str in var_str.split("."):
            module = getattr(module, sub_var_str)
        if json_param:
            var = module(**json.loads(json_param))  # type: ignore
        else:
            var = module
        return var

    def template_import(self, module_str: str, var_str: str) -> Any:
        module = import_module(module_str, module_str)
        for sub_var_str in var_str.split("."):
            module = getattr(module, sub_var_str)
        return module

    def template_local(self, local_var_name: str) -> Any:
        return self._local_dict[local_var_name]

    def template_builtin(self, builtin_name: str) -> Any:
        return __builtins__.get(builtin_name)  # type: ignore

    def _template_str_handler(self, template_str: str) -> Any:
        try:
            template_str_list: List[str] = template_str.split("|")
            template_rule, *template_var_list = template_str_list
            template_fn: Optional[Callable] = getattr(self, f"template_{template_rule}", None)
            if not template_fn:
                raise ValueError(f"Only support {' ,'.join(self._support_template_list)}. not {template_str}")
            return template_fn(*template_var_list)
        except Exception as e:
            raise ValueError(f"parse {template_str} error: {e}") from e

    def handle_template_var(self, container: Any) -> Any:
        if isinstance(container, (list, RepeatedCompositeContainer, RepeatedScalarContainer)):
            return [self.handle_template_var(i) for i in container]
        elif isinstance(container, dict):
            return {k: self.handle_template_var(v) for k, v in container.items()}
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
        message_field_dict: Dict[str, "DescFromOptionTypedDict"] = {}

        if proto_file_name.endswith("empty.proto") or parse_msg_desc_method == "ignore":
            pass
        elif isinstance(parse_msg_desc_method, str) and Path(parse_msg_desc_method).exists():
            file_str: str = parse_msg_desc_method
            if not file_str.endswith("/"):
                file_str += "/"
            message_field_dict = get_desc_from_proto_file(file_str + proto_file_name, comment_prefix)
        elif inspect.ismodule(parse_msg_desc_method):
            if getattr(parse_msg_desc_method, msg.__name__, None) is not msg:  # type: ignore
                raise ValueError(f"Not the module corresponding to {msg}")
            pyi_file_name = parse_msg_desc_method.__file__ + "i"  # type: ignore
            if not Path(pyi_file_name).exists():
                raise RuntimeError(f"Can not found {msg} pyi file")
            message_field_dict = get_desc_from_pyi_file(pyi_file_name, comment_prefix)
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
        self._field_doc_dict: Dict[str, DescFromOptionTypedDict] = message_field_dict
        self._default_field = default_field
        self._comment_prefix = comment_prefix
        self._creat_cache: Dict[Union[Type[Message], Descriptor], Type[BaseModel]] = {}
        self._pydantic_base: Type["BaseModel"] = pydantic_base or BaseModel
        self._pydantic_module: str = pydantic_module or __name__
        self._desc_template: DescTemplate = (desc_template or DescTemplate)(local_dict or {}, self._comment_prefix)
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

    def _one_of_handle(self, descriptor: Descriptor) -> Dict[str, "OneOfTypedDict"]:
        desc_dict: "DescFromOptionTypedDict" = self._field_doc_dict.get(descriptor.name, {})  # type: ignore
        one_of_dict: Dict[str, "OneOfTypedDict"] = {}
        for one_of in descriptor.oneofs:
            column_name: str = one_of.full_name
            if column_name not in one_of_dict:
                one_of_dict[column_name] = {"required": False, "fields": set()}
            if desc_dict and column_name in desc_dict["one_of"]:
                # only PGV or P2P support
                one_of_dict[column_name]["required"] = desc_dict["one_of"][column_name].get("required", False)
            for _field in one_of.fields:
                one_of_dict[column_name]["fields"].add(_field.name)
        return one_of_dict

    def _get_pydantic_base(self, config_dict: Dict[str, Any]) -> Type[BaseModel]:
        if config_dict:
            # Changing the configuration of Config by inheritance
            pydantic_base: Type[BaseModel] = type(  # type: ignore
                self._pydantic_base.__name__,
                (self._pydantic_base,),
                {"Config": type(self._pydantic_base.Config.__name__, (self._pydantic_base.Config,), config_dict)},
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
        one_of_dict: Dict[str, "OneOfTypedDict"] = self._one_of_handle(descriptor)
        if one_of_dict:
            validators["one_of_validator"] = root_validator(pre=True, allow_reuse=True)(check_one_of)

        # nested support
        nested_message_dict: Dict[str, Type[Union[BaseModel, IntEnum]]] = {}
        for message in descriptor.nested_types:
            if message.name.endswith("Entry"):
                continue
            nested_type: Any = self._parse_msg_to_pydantic_model(descriptor=message)
            nested_message_dict[message.full_name] = nested_type
            # Facilitate the analysis of `gen code`
            setattr(nested_type, "_is_nested", True)

        for enum_type in descriptor.enum_types:
            class_dict: dict = {v.name: v.number for v in enum_type.values}
            class_dict["__doc__"] = ""
            nested_type = IntEnum(enum_type.name, class_dict)  # type: ignore
            nested_message_dict[enum_type.full_name] = nested_type
            # Facilitate the analysis of `gen code`
            setattr(nested_type, "_is_nested", True)

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
                        # Default factory has a higher priority
                        default_factory = self._message_default_factory_dict_by_type_name[column.message_type.name]
                elif column.message_type.name.endswith("Entry"):
                    # support google.protobuf.MapEntry
                    # key, value = column.message_type.fields

                    dict_type_param_list = []
                    for k_v_field in column.message_type.fields:
                        if not k_v_field.message_type:
                            k_v_type: Any = type_dict[k_v_field.type]
                        elif k_v_field.message_type.name in self._message_type_dict_by_type_name:
                            k_v_type = self._message_type_dict_by_type_name[k_v_field.message_type.name]
                        else:
                            k_v_type = self._parse_msg_to_pydantic_model(descriptor=k_v_field.message_type)
                        dict_type_param_list.append(k_v_type)

                    type_ = Dict[tuple(dict_type_param_list)]  # type: ignore
                    default_factory = dict
                else:
                    # support google.protobuf.Message
                    if column.message_type.full_name in nested_message_dict:
                        type_ = nested_message_dict[column.message_type.full_name]
                    else:
                        is_same_pkg: bool = descriptor.file.name == column.message_type.file.name
                        _class_name: str = column.message_type.name
                        if not is_same_pkg:
                            _class_name = replace_file_name_to_class_name(column.message_type.file.name) + _class_name
                            type_ = self._parse_msg_to_pydantic_model(
                                descriptor=column.message_type, class_name=_class_name
                            )
                            _class_doc: str = (
                                "Note: The current class does not belong to the package\n"
                                f"{_class_name} protobuf path:{column.message_type.file.name}"
                            )
                            setattr(type_, "__doc__", _class_doc)
                        else:
                            if column.message_type.full_name == descriptor.full_name:
                                # if self-referencing, need use Python type hints postponed annotations
                                type_ = f'"{_class_name}"'
                            else:
                                type_ = self._parse_msg_to_pydantic_model(
                                    descriptor=column.message_type, class_name=_class_name
                                )
            elif column.type == FieldDescriptor.TYPE_ENUM:
                # support google.protobuf.Enum
                default = 0
                if column.enum_type.full_name in nested_message_dict:
                    type_ = nested_message_dict[column.enum_type.full_name]
                else:
                    enum_class_dict = {v.name: v.number for v in column.enum_type.values}
                    _class_name = column.enum_type.name
                    _class_doc = ""
                    if descriptor.file.name != column.enum_type.file.name:
                        _class_name = replace_file_name_to_class_name(column.enum_type.file.name) + _class_name
                        _class_doc = (
                            "Note: The current class does not belong to the package\n"
                            f"{_class_name} protobuf path:{column.enum_type.file.name}"
                        )
                    enum_class_dict["__doc__"] = _class_doc
                    type_ = IntEnum(_class_name, enum_class_dict)  # type: ignore
            else:
                if column.label == FieldDescriptor.LABEL_REQUIRED:
                    default = Undefined
                else:
                    default = column.default_value

            if column.label == FieldDescriptor.LABEL_REPEATED:
                # support google.protobuf.array
                if not (column.message_type and column.message_type.name.endswith("Entry")):
                    # I didn't know that Protobuf's Design of Maps and Lists would be so weird
                    type_ = List[type_]  # type: ignore
                    default_factory = list
                    # TODO support lambda
                    if default is not Undefined:
                        default = Undefined

            field = self._default_field
            field_doc_dict = self._get_field_info_dict_by_full_name(column.full_name)
            if field_doc_dict is not None:
                if self._parse_msg_desc_method != "PGV":
                    # pgv method not support template var
                    field_doc_dict = self._desc_template.handle_template_var(field_doc_dict)

                field_param_dict: dict = MessagePaitModel(**field_doc_dict).dict()  # type: ignore
                # Nested types do not include the `enable`, `field` and `validator`  attributes
                if not field_param_dict.pop("enable"):
                    continue
                _field = field_param_dict.pop("field")
                if _field:
                    field = _field
                validator_dict = field_param_dict.pop("validator")
                if validator_dict:
                    validators.update(validator_dict)

                # Unified field parameter handling
                field_param_dict_handle(field_param_dict, default, default_factory)

                # Type will change in the unified processing logic
                field_type = field_param_dict.pop("type_", type_)
                map_type_dict = field_param_dict.pop("map_type", {})
                if field_type:
                    type_ = field_type
                elif map_type_dict and type_._name == "Dict":
                    new_args_list: List = list(type_.__args__)
                    for index, k_v_column in enumerate(["keys", "values"]):
                        raw_k_v_type = new_args_list[index]
                        if k_v_column not in map_type_dict:
                            continue
                        new_k_v_type = map_type_dict[k_v_column]
                        if issubclass(new_k_v_type, raw_k_v_type) or raw_k_v_type is datetime.datetime:
                            new_args_list[index] = new_k_v_type
                    type_ = Dict[tuple(new_args_list)]  # type: ignore
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
        # Facilitate the analysis of `gen code`
        setattr(pydantic_model, "_nested_message_dict", nested_message_dict)
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

    def _get_field_info_dict_by_full_name(self, full_name: str) -> Optional["FieldInfoTypedDict"]:
        message_name, *key_list = full_name.split(".")[1:]  # ignore package name
        if message_name not in self._field_doc_dict:
            return None
        desc_dict: "DescFromOptionTypedDict" = self._field_doc_dict[message_name]

        for key in key_list:
            if key in desc_dict["message"]:
                return desc_dict["message"][key]
            elif key in desc_dict["nested"]:
                desc_dict = desc_dict["nested"][key]
            else:
                return None
        return None


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
    :param default_field: gen pydantic_model default Field, apply only to the outermost pydantic model
    :param comment_prefix: Customize the prefixes that need to be parsed for comments
    :param parse_msg_desc_method:
        Define a method for extracting the message extension property
        1.If the value is 'ignore', it means that no extraction is made
        2.If the value is the Protobuf file path, the Protobuf file is parsed and the information is extracted from
         the comments in the file
         Note: The extracted content is a text comment in the Protobuf file
        3.If the value is a Message object's module, it is extracted from the corresponding pyi file
         (pyi file is generated by mypy-protobuf)
         Note: The extracted content is a text comment in the Protobuf file
        4.If the value is PGV, the corresponding PGV information is extracted from the Message object
        5.If the value is None (default), the P2P information is extracted from the Message)
    :param local_dict: The variables corresponding to the p2p@local template
    :param pydantic_base: custom pydantic.BaseModel
    :param pydantic_module: custom create model's module name
    :param desc_template: DescTemplate object, which can extend and modify template adaptation rules through inheritance
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
