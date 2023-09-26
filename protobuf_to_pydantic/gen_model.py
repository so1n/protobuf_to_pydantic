import dataclasses
import datetime
import inspect
import warnings
from dataclasses import MISSING
from enum import IntEnum
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo
from typing_extensions import Annotated, Literal, get_args, get_origin

from protobuf_to_pydantic import _pydantic_adapter, constant
from protobuf_to_pydantic.customer_validator import check_one_of
from protobuf_to_pydantic.desc_template import DescTemplate
from protobuf_to_pydantic.get_desc import (
    get_desc_from_p2p,
    get_desc_from_pgv,
    get_desc_from_proto_file,
    get_desc_from_pyi_file,
)
from protobuf_to_pydantic.grpc_types import AnyMessage, Descriptor, FieldDescriptor, Message
from protobuf_to_pydantic.types import JsonAndDict
from protobuf_to_pydantic.util import check_dict_one_of, create_pydantic_model

if TYPE_CHECKING:
    from protobuf_to_pydantic.types import DescFromOptionTypedDict, FieldInfoTypedDict, OneOfTypedDict


def field_param_dict_migration_v2_handler(field_param_dict: Dict[str, Any], is_warnings: bool = True) -> None:
    json_schema_extra = {}
    for k in list(field_param_dict.keys()):
        new_k = constant.pydantic_field_v1_migration_v2_dict.get(k, k)
        if new_k != k:
            if new_k is None:
                if is_warnings:
                    warnings.warn(
                        f"field param `{k}` is deprecated, "
                        f"https://docs.pydantic.dev/latest/migration/#changes-to-pydanticfield"
                    )
                field_param_dict.pop(k)
            else:
                if is_warnings:
                    warnings.warn(
                        f"field param `{k}` is deprecated, please use `{new_k}` instead,"
                        f" https://docs.pydantic.dev/latest/migration/#changes-to-pydanticfield"
                    )
                value = field_param_dict.pop(k)
                if value:
                    field_param_dict[new_k] = value
        else:
            if k not in field_param_set:
                json_schema_extra[k] = field_param_dict.pop(k)
    field_param_dict["json_schema_extra"] = json_schema_extra


def replace_file_name_to_class_name(filename: str) -> str:
    """Convert the protobuf file name to the class name(PEP-8)"""
    # example_proto/common/single.proto -> Example_protoCommonSingle
    prefix: str = "".join([str(i).title() for i in Path(filename.split(".")[0]).joinpath().parts])
    # Example_protoCommonSingle -> ExampleProtoCommonSingle
    prefix = prefix.replace("_", "")
    return prefix


def field_param_dict_handle(
    field_param_dict: dict,
    default: Any,
    default_factory: Optional[_pydantic_adapter.NoArgAnyCallable],
    field_type: Optional[type] = None,
    nested_call_count: int = 1,
) -> None:
    """
    Convert the field_param_dict data to Pydantic Field parameters

    :param field_param_dict:
    :param default: Pydantic Field default value
    :param default_factory: Pydantic Field default_factory value
    :param field_type: Pydantic Field type value
    :param nested_call_count: Each call will only process one level of type,
        if it is a nested type, a recursive call is required,
        and this parameter is used to record the number of layers of recursive calls

        e.g: List[str], List is the first layer, str is the second layer,
    :return:
    """
    # default_template support
    if field_param_dict.get("default", None) is None and field_param_dict.get("default_template", None) is not None:
        field_param_dict["default"] = field_param_dict["default_template"]
    field_param_dict.pop("default_template", None)

    # Handle complex relationships with different defaults
    check_dict_one_of(field_param_dict, ["required", "default", "default_factory"])
    if field_param_dict.get("default_factory", None) is not None:
        field_param_dict.pop("default", "")
    elif field_param_dict.get("default", None) is None:
        if default_factory:
            field_param_dict["default_factory"] = default_factory
            field_param_dict.pop("default", "")
        else:
            field_param_dict["default"] = default
            field_param_dict.pop("default_factory", None)

    if field_param_dict.get("required", None) is True:
        field_param_dict.pop("default", "")
        field_param_dict.pop("default_factory", "")
    field_param_dict.pop("required", None)

    _const = field_param_dict.pop("const", MISSING)
    # PGV&P2P const handler
    if _const.__class__ != MISSING.__class__:
        if _pydantic_adapter.is_v1:
            field_param_dict["default"] = _const
            field_param_dict["const"] = True
        else:
            # pydantic v2 not support const, only support Literal
            field_param_dict["type_"] = Literal.__getitem__(_const)

    if not _pydantic_adapter.is_v1 and field_param_dict.get("unique_items", None) is not None:
        # In pydantic v2, not support unique_items
        # only use the Set type instead of this feature
        if not field_type or get_origin(field_type) != list:
            raise RuntimeError(f"unique_items only support type List (protobuf type: repeated) not {field_type}")
        field_param_dict["type_"] = Set.__getitem__(get_args(field_type))  # type: ignore[index]
        if field_param_dict["default_factory"]:
            field_param_dict["default_factory"] = set

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
    if not field_type:
        return

    if (
        field_type
        and not inspect.isclass(field_type)
        and field_type_model
        and field_type_model.__name__
        in ("pydantic.types", "protobuf_to_pydantic.customer_con_type.v1", "protobuf_to_pydantic.customer_con_type.v2")
    ):
        # support https://pydantic-docs.helpmanual.io/usage/types/#constrained-types
        # Parameters needed to extract `constrained-types`
        type_param_dict: dict = {}

        if _pydantic_adapter.is_v1 or nested_call_count != 1:
            # In pydantic v2
            # If it is the first layer, all parameters need to be passed to Field, not Type
            for key in inspect.signature(field_type).parameters.keys():
                if key in field_param_dict:
                    type_param_dict[key] = field_param_dict.pop(key)
        if sub_field_param_dict and "type_" in sub_field_param_dict:
            # If a nested type is found, use the same treatment
            field_param_dict_handle(
                sub_field_param_dict, default, default_factory, nested_call_count=nested_call_count + 1
            )
            field_param_dict["type_"] = field_type(sub_field_param_dict["type_"], **type_param_dict)
        else:
            field_param_dict["type_"] = field_type(**type_param_dict)


class MessagePaitModel(BaseModel):
    field: Optional[Type[FieldInfo]] = Field(None)
    enable: bool = Field(True)
    required: bool = Field(False)
    default: Optional[Any] = Field(None)
    default_factory: Optional[Callable] = Field(None)
    default_template: Any = Field(None)
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
    extra: JsonAndDict = Field(default_factory=dict)
    type_: Any = Field(None, alias="type")
    validator: Optional[Dict[str, Any]] = Field(None)
    sub: Optional["MessagePaitModel"] = Field(None)
    map_type: Optional[dict] = Field(None)


class CodeRefModel(object):
    def __init__(
        self,
        one_of_dict: Dict[str, "OneOfTypedDict"],
        base_model: Type["BaseModel"],
        nested_message_dict: Dict[str, Type[Union[BaseModel, IntEnum]]],
        validators: Dict[str, classmethod],
    ) -> None:
        self.one_of_dict = one_of_dict
        self.base_model = base_model
        self.nested_message_dict = nested_message_dict
        self.validators = validators

    @classmethod
    def from_model(cls, model: Type[BaseModel]) -> "CodeRefModel":
        code_ref_model = getattr(model, "_code_ref", None)
        if code_ref_model and isinstance(code_ref_model, cls):
            return code_ref_model
        raise ValueError("Not found CodeRefModel, please set `enable_code_ref_gen==True` in gen_model func or class")

    @classmethod
    def set_to_model(
        cls,
        model: Type[BaseModel],
        *,
        one_of_dict: Dict[str, "OneOfTypedDict"],
        base_model: Type["BaseModel"],
        nested_message_dict: Dict[str, Type[Union[BaseModel, IntEnum]]],
        validators: Dict[str, classmethod],
    ) -> None:
        code_ref = cls(
            one_of_dict=one_of_dict,
            base_model=base_model,
            nested_message_dict=nested_message_dict,
            validators=validators,
        )
        setattr(model, "_code_ref", code_ref)


# You can decide whether to generate the 'Field' parameter by modifying the 'field_param_set'
field_param_set = set(inspect.signature(Field).parameters.keys())


@dataclasses.dataclass
class FieldDataClass(object):
    # field data
    field_name: str
    field_type: Any
    field_default: Any
    field_default_factory: Optional[_pydantic_adapter.NoArgAnyCallable]
    # metadate
    protobuf_field: FieldDescriptor
    nested_message_dict: Dict[str, Type[Union[BaseModel, IntEnum]]]
    descriptor: Descriptor
    validators: Dict[str, classmethod]


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
            message_type_dict_by_type_name or constant.message_name_type_dict
        )
        self._message_default_factory_dict_by_type_name: Dict[str, Any] = (
            message_default_factory_dict_by_type_name or constant.message_name_default_factory_dict
        )

        self._gen_model: Type[BaseModel] = self._parse_msg_to_pydantic_model(
            descriptor=msg if isinstance(msg, Descriptor) else msg.DESCRIPTOR,
        )

    #################
    # caller method #
    #################
    @property
    def model(self) -> Type[BaseModel]:
        return self._gen_model

    ###############
    # util method #
    ###############
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

    def _one_of_handle(self, descriptor: Descriptor) -> Tuple[Dict[str, "OneOfTypedDict"], Dict[str, Any]]:
        desc_dict: "DescFromOptionTypedDict" = self._field_doc_dict.get(descriptor.name, {})  # type: ignore
        one_of_dict: Dict[str, "OneOfTypedDict"] = {}
        optional_dict: Dict[str, Any] = {}
        for one_of in descriptor.oneofs:
            if one_of == descriptor.fields[one_of.index].containing_oneof:
                # support optional field
                # e.g.:
                #   message OptionalMessage{
                #     optional string name = 1;
                #     optional int32 age= 2;
                #   };

                # one_of name is `_name`, `_age`
                # but need name is `name`, `age`
                optional_dict[descriptor.fields[one_of.index].full_name] = {"is_proto3_optional": True}
            else:
                column_name: str = one_of.full_name
                if column_name not in one_of_dict:
                    one_of_dict[column_name] = {"required": False, "fields": set()}
                if desc_dict and column_name in desc_dict["one_of"]:
                    # only PGV or P2P support
                    one_of_dict[column_name]["required"] = desc_dict["one_of"][column_name].get("required", False)
                for _field in one_of.fields:
                    one_of_dict[column_name]["fields"].add(_field.name)
        return one_of_dict, optional_dict

    def _get_pydantic_base(self, config_dict: Dict[str, Any]) -> Type[BaseModel]:
        if config_dict:
            if _pydantic_adapter.is_v1:
                config_class = self._pydantic_base.Config  # type: ignore
                _config_dict: Dict[str, Any] = {"Config": type(config_class.__name__, (config_class,), config_dict)}
            else:
                from pydantic import ConfigDict

                _config_dict = {"model_config": ConfigDict(**config_dict)}  # type: ignore[misc]

            # Changing the configuration of Config by inheritance
            pydantic_base: Type[BaseModel] = type(  # type: ignore
                self._pydantic_base.__name__, (self._pydantic_base,), _config_dict
            )
        else:
            pydantic_base = self._pydantic_base
        return pydantic_base

    def get_nested_message_dict_by_message(self, descriptor: Descriptor) -> Dict[str, Type[Union[BaseModel, IntEnum]]]:
        # nested support
        nested_message_dict: Dict[str, Type[Union[BaseModel, IntEnum]]] = {}
        for message in descriptor.nested_types:
            if message.name.endswith("Entry"):
                continue
            nested_type: Any = self._parse_msg_to_pydantic_model(descriptor=message)
            nested_message_dict[message.full_name] = nested_type
            # Facilitate the analysis of `gen code`
            setattr(nested_type, "_is_nested", True)
        # enum support
        for enum_type in descriptor.enum_types:
            class_dict: dict = {v.name: v.number for v in enum_type.values}
            class_dict["__doc__"] = ""
            nested_type = IntEnum(enum_type.name, class_dict)  # type: ignore
            nested_message_dict[enum_type.full_name] = nested_type
            # Facilitate the analysis of `gen code`
            setattr(nested_type, "_is_nested", True)
        return nested_message_dict

    ####################
    # field  handler   #
    ####################
    def _protobuf_field_type_is_type_message_handler(self, field_dataclass: FieldDataClass) -> None:
        protobuf_field = field_dataclass.protobuf_field
        if protobuf_field.message_type.name in self._message_type_dict_by_type_name:
            # Timestamp, Struct, Empty, Duration, Any support
            field_dataclass.field_type = self._message_type_dict_by_type_name[protobuf_field.message_type.name]
            if protobuf_field.message_type.name in self._message_default_factory_dict_by_type_name:
                # Default factory has a higher priority
                field_dataclass.field_default_factory = self._message_default_factory_dict_by_type_name[
                    protobuf_field.message_type.name
                ]
        elif protobuf_field.message_type.name.endswith("Entry"):
            # support google.protobuf.MapEntry
            # key, value = column.message_type.fields
            dict_type_param_list = []
            for k_v_field in protobuf_field.message_type.fields:
                if not k_v_field.message_type:
                    k_v_type: Any = constant.protobuf_desc_python_type_dict[k_v_field.type]
                elif k_v_field.message_type.name in self._message_type_dict_by_type_name:
                    k_v_type = self._message_type_dict_by_type_name[k_v_field.message_type.name]
                else:
                    k_v_type = self._parse_msg_to_pydantic_model(descriptor=k_v_field.message_type)
                dict_type_param_list.append(k_v_type)

            field_dataclass.field_type = Dict[tuple(dict_type_param_list)]  # type: ignore
            field_dataclass.field_default_factory = dict
        else:
            # support google.protobuf.Message
            if protobuf_field.message_type.full_name in field_dataclass.nested_message_dict:
                field_dataclass.field_type = field_dataclass.nested_message_dict[protobuf_field.message_type.full_name]
            else:
                # Python Protobuf does not solve the namespace problem of modules,
                # so there is no uniform cross-module reference
                # see issue: https://github.com/protocolbuffers/protobuf/issues/1491
                is_same_pkg: bool = field_dataclass.descriptor.file.name == protobuf_field.message_type.file.name
                _class_name: str = protobuf_field.message_type.name
                if not is_same_pkg:
                    _class_name = replace_file_name_to_class_name(protobuf_field.message_type.file.name) + _class_name
                    field_dataclass.field_type = self._parse_msg_to_pydantic_model(
                        descriptor=protobuf_field.message_type, class_name=_class_name
                    )
                    _class_doc: str = (
                        "Note: The current class does not belong to the package\n"
                        f"{_class_name} protobuf path:{protobuf_field.message_type.file.name}"
                    )
                    setattr(field_dataclass.field_type, "__doc__", _class_doc)
                else:
                    if protobuf_field.message_type.full_name == field_dataclass.descriptor.full_name:
                        # if self-referencing, need use Python type hints postponed annotations
                        field_dataclass.field_type = f'"{_class_name}"'
                    else:
                        field_dataclass.field_type = self._parse_msg_to_pydantic_model(
                            descriptor=protobuf_field.message_type, class_name=_class_name
                        )

    def _protobuf_field_type_is_type_enum_handler(self, field_dataclass: FieldDataClass) -> None:
        # support google.protobuf.Enum
        field_dataclass.field_default = 0
        protobuf_field = field_dataclass.protobuf_field
        if protobuf_field.enum_type.full_name in field_dataclass.nested_message_dict:
            field_dataclass.field_type = field_dataclass.nested_message_dict[protobuf_field.enum_type.full_name]
        else:
            enum_class_dict = {v.name: v.number for v in protobuf_field.enum_type.values}
            _class_name = protobuf_field.enum_type.name
            _class_doc = ""
            if field_dataclass.descriptor.file.name != protobuf_field.enum_type.file.name:
                _class_name = replace_file_name_to_class_name(protobuf_field.enum_type.file.name) + _class_name
                _class_doc = (
                    "Note: The current class does not belong to the package\n"
                    f"{_class_name} protobuf path:{protobuf_field.enum_type.file.name}"
                )
            enum_class_dict["__doc__"] = _class_doc
            field_dataclass.field_type = IntEnum(_class_name, enum_class_dict)  # type: ignore

    def _protobuf_field_lable_is_label_repeated_handler(self, field_dataclass: FieldDataClass) -> None:
        # support google.protobuf.array
        protobuf_field = field_dataclass.protobuf_field
        if not (protobuf_field.message_type and protobuf_field.message_type.name.endswith("Entry")):
            # I didn't know that Protobuf's Design of Maps and Lists would be so weird
            field_dataclass.field_type = List[field_dataclass.field_type]  # type: ignore
            field_dataclass.field_default_factory = list
            # TODO support lambda
            if field_dataclass.field_default is not _pydantic_adapter.PydanticUndefined:
                field_dataclass.field_default = _pydantic_adapter.PydanticUndefined

    def _gen_field_info(self, field_dataclass: FieldDataClass) -> Optional[FieldInfo]:
        field = self._default_field
        field_doc_dict = self._get_field_info_dict_by_full_name(field_dataclass.protobuf_field.full_name)

        if field_doc_dict is not None:
            if self._parse_msg_desc_method != "PGV":
                # pgv method not support template var
                field_doc_dict = self._desc_template.handle_template_var(field_doc_dict)
            field_param_dict: dict = MessagePaitModel(**field_doc_dict).dict()  # type: ignore
            # Nested types do not include the `enable`, `field` and `validator`  attributes
            if not field_param_dict.pop("enable"):
                return None
            _field = field_param_dict.pop("field")
            if _field:
                field = _field
            validator_dict = field_param_dict.pop("validator")
            if validator_dict:
                if _pydantic_adapter.is_v1:
                    field_dataclass.validators.update(validator_dict)
                else:
                    # In Pydantic v2:
                    #     field_doc_dict["validatos"] = {
                    #       'not_in_test_any_not_in_validator': PydanticDescriptorProxy(
                    #             wrapped=<classmethod object at 0x7f28943c8128>,
                    #             decorator_info=FieldValidatorDecoratorInfo(fields=('not_in_test',),
                    #             mode='after', check_fields=None),
                    #             shim=None
                    #        )
                    #     }
                    #  But validator_dict output:
                    #   {
                    #       'not_in_test_any_not_in_validator': {
                    #           'wrapped': <classmethod object at 0x7f28943c8128>,
                    #           'decorator_info': {
                    #               'fields': ('not_in_test',),
                    #               'mode': 'after',
                    #               'check_fields': None
                    #            },
                    #           'shim': None
                    #       }
                    #   }
                    field_dataclass.validators.update(field_doc_dict["validator"])  # type: ignore[index]

            # Unified field parameter handling
            field_param_dict_handle(
                field_param_dict,
                field_dataclass.field_default,
                field_dataclass.field_default_factory,
                field_dataclass.field_type,
            )

            # Type will change in the unified processing logic
            field_type = field_param_dict.pop("type_", field_dataclass.field_type)
            map_type_dict = field_param_dict.pop("map_type", {})
            if field_type:
                field_dataclass.field_type = field_type
            elif map_type_dict and field_dataclass.field_type._name == "Dict":
                new_args_list: List = list(field_dataclass.field_type.__args__)
                for index, k_v_column in enumerate(["keys", "values"]):
                    raw_k_v_type = new_args_list[index]
                    if k_v_column not in map_type_dict:
                        continue
                    new_k_v_type = map_type_dict[k_v_column]

                    if (
                        get_origin(new_k_v_type) is Annotated
                        or issubclass(new_k_v_type, raw_k_v_type)
                        or raw_k_v_type is datetime.datetime
                    ):
                        new_args_list[index] = new_k_v_type
                field_dataclass.field_type = Dict[tuple(new_args_list)]  # type: ignore
        else:
            field_param_dict = {
                "default": field_dataclass.field_default,
                "default_factory": field_dataclass.field_default_factory,
            }
        if not _pydantic_adapter.is_v1:
            field_param_dict_migration_v2_handler(field_param_dict)
        return field(**field_param_dict)  # type: ignore

    def _parse_msg_to_pydantic_model(self, *, descriptor: Descriptor, class_name: str = "") -> Type[BaseModel]:
        if descriptor in self._creat_cache:
            return self._creat_cache[descriptor]

        annotation_dict: Dict[str, Tuple[Type, Any]] = {}
        validators: Dict[str, classmethod] = {}
        pydantic_model_config_dict: Dict[str, Any] = {}
        nested_message_dict = self.get_nested_message_dict_by_message(descriptor)
        one_of_dict, optional_dict = self._one_of_handle(descriptor)

        # parse field
        for protobuf_field in descriptor.fields:
            field_dataclass = FieldDataClass(
                field_name=protobuf_field.name,
                field_type=constant.protobuf_desc_python_type_dict.get(protobuf_field.type, None),
                field_default=_pydantic_adapter.PydanticUndefined,
                field_default_factory=None,
                protobuf_field=protobuf_field,
                nested_message_dict=nested_message_dict,
                descriptor=descriptor,
                validators=validators,
            )
            if protobuf_field.type == FieldDescriptor.TYPE_MESSAGE:
                self._protobuf_field_type_is_type_message_handler(field_dataclass)
            elif protobuf_field.type == FieldDescriptor.TYPE_ENUM:
                self._protobuf_field_type_is_type_enum_handler(field_dataclass)
            else:
                field_dataclass.field_default = protobuf_field.default_value

            # At this time, the field type may be modified by the above logic, so it needs to be handled separately
            if protobuf_field.label == FieldDescriptor.LABEL_REPEATED:
                self._protobuf_field_lable_is_label_repeated_handler(field_dataclass)

            field_info = self._gen_field_info(field_dataclass)
            if not field_info:
                continue
            if optional_dict.get(protobuf_field.full_name, {}).get("is_proto3_optional", False):
                field_dataclass.field_type = Optional[field_dataclass.field_type]
                if field_dataclass.field_default is _pydantic_adapter.PydanticUndefined:
                    field_dataclass.field_default = None

            annotation_dict[field_dataclass.field_name] = (field_dataclass.field_type, field_info)

            if field_dataclass.field_type in (AnyMessage,) and not _pydantic_adapter.get_model_config_value(
                self._pydantic_base, "arbitrary_types_allowed"
            ):
                pydantic_model_config_dict["arbitrary_types_allowed"] = True

        if one_of_dict:
            validators["one_of_validator"] = _pydantic_adapter.model_validator(mode="before", allow_reuse=True)(
                check_one_of
            )
        pydantic_model: Type[BaseModel] = create_pydantic_model(
            annotation_dict,
            class_name=class_name or descriptor.name,
            pydantic_validators=validators or None,
            pydantic_module=self._pydantic_module,
            pydantic_base=self._get_pydantic_base(pydantic_model_config_dict),
        )
        CodeRefModel.set_to_model(
            pydantic_model,
            one_of_dict=one_of_dict,
            base_model=self._pydantic_base,
            # Facilitate the analysis of `gen code`
            nested_message_dict=nested_message_dict,
            validators=validators,
        )
        setattr(pydantic_model, "_one_of_dict", one_of_dict)
        self._creat_cache[descriptor] = pydantic_model
        return pydantic_model


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
