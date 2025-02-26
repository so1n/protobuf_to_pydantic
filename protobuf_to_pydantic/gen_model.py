import dataclasses
import datetime
import importlib
import inspect
import logging
import os
from enum import IntEnum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple, Type, Union

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from typing_extensions import Annotated, get_origin

from protobuf_to_pydantic import _pydantic_adapter, constant
from protobuf_to_pydantic.constant import protobuf_common_type_dict
from protobuf_to_pydantic.customer_validator import check_one_of
from protobuf_to_pydantic.exceptions import WaitingToCompleteException
from protobuf_to_pydantic.field_info_rule.field_info_param import (
    FieldInfoParamModel,
    field_info_param_dict_handle,
    field_info_param_dict_migration_v2_handler,
)
from protobuf_to_pydantic.field_info_rule.protobuf_option_to_field_info.comment import (
    gen_field_rule_info_dict_from_field_comment_dict,
)
from protobuf_to_pydantic.get_message_option import (
    get_message_option_dict_from_message_with_p2p,
    get_message_option_dict_from_message_with_pgv,
    get_message_option_dict_from_proto_file,
    get_message_option_dict_from_pyi_file,
)
from protobuf_to_pydantic.grpc_types import AnyMessage, Descriptor, FieldDescriptor, FieldMask, Message
from protobuf_to_pydantic.template import Template
from protobuf_to_pydantic.util import create_pydantic_model, pydantic_allow_validation_field_handler

if TYPE_CHECKING:
    from protobuf_to_pydantic.field_info_rule.types import FieldInfoTypedDict, MessageOptionTypedDict, UseOneOfTypedDict

logger: logging.Logger = logging.getLogger(__name__)

SKIP_RULE_MESSAGE_SUFFIX = "WithSkipRule"
ALLOW_ARBITRARY_TYPE = (AnyMessage, FieldMask)


def replace_file_name_to_class_name(filename: str) -> str:
    """Convert the protobuf file name to the class name(PEP-8)"""
    # example_proto/common/single.proto -> Example_protoCommonSingle
    prefix: str = "".join([str(i).title() for i in Path(filename.split(".")[0]).joinpath().parts])
    # Example_protoCommonSingle -> ExampleProtoCommonSingle
    prefix = prefix.replace("_", "")
    return prefix


class CodeRefModel(object):
    def __init__(
        self,
        one_of_dict: Dict[str, "UseOneOfTypedDict"],
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
        one_of_dict: Dict[str, "UseOneOfTypedDict"],
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


@dataclasses.dataclass
class FieldDataClass(object):
    # field data
    field_name: str
    field_type: Any
    field_type_name: str
    field_default: Any
    field_default_factory: Optional[_pydantic_adapter.NoArgAnyCallable]
    # metadate
    is_required: bool
    protobuf_field: FieldDescriptor
    nested_message_dict: Dict[str, Type[Union[BaseModel, IntEnum]]]
    descriptor: Descriptor
    validators: Dict[str, classmethod]


CREATE_MODEL_CACHE_T = Dict[Union[str, tuple], Optional[Type[BaseModel]]]
_create_model_cache: CREATE_MODEL_CACHE_T = {}


def clear_create_model_cache() -> None:
    _create_model_cache.clear()


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
        template: Optional[Type[Template]] = None,
        message_type_dict_by_type_name: Optional[Dict[str, Any]] = None,
        message_default_factory_dict_by_type_name: Optional[Dict[str, Any]] = None,
        all_field_set_optional: bool = False,
        create_model_cache: Optional[CREATE_MODEL_CACHE_T] = None,
    ):
        proto_file_name = msg.DESCRIPTOR.file.name  # type: ignore
        global_message_option_dict: Dict[str, "MessageOptionTypedDict"] = {}

        if proto_file_name.endswith("empty.proto") or parse_msg_desc_method == "ignore":
            pass
        elif isinstance(parse_msg_desc_method, str) and Path(parse_msg_desc_method).exists():
            # get field dict from proto file
            file_str: str = parse_msg_desc_method
            if not file_str.endswith("/"):
                file_str += "/"
            global_message_option_dict = get_message_option_dict_from_proto_file(
                file_str + proto_file_name, comment_prefix
            )
        elif inspect.ismodule(parse_msg_desc_method):
            # get field dict from pyi file
            if getattr(parse_msg_desc_method, msg.__name__, None) is not msg:  # type: ignore
                raise ValueError(f"Not the module corresponding to {msg}")
            pyi_file_name = parse_msg_desc_method.__file__ + "i"  # type: ignore
            if not Path(pyi_file_name).exists():
                raise RuntimeError(f"Can not found {msg} pyi file")
            global_message_option_dict = get_message_option_dict_from_pyi_file(pyi_file_name, comment_prefix)
        elif parse_msg_desc_method == "PGV":
            # get field dict from pgv
            global_message_option_dict = get_message_option_dict_from_message_with_pgv(message=msg)  # type: ignore
        elif parse_msg_desc_method is not None:
            raise ValueError(
                f"parse_msg_desc_method param must be exist path, `ignore` or `PGV`,"
                f" not {parse_msg_desc_method}), now path:{os.getcwd()}"
            )
        else:
            # get field dict from p2p
            global_message_option_dict = get_message_option_dict_from_message_with_p2p(message=msg)  # type: ignore

        self._all_field_set_optional: bool = all_field_set_optional
        self._parse_msg_desc_method = parse_msg_desc_method
        self._message_option_dict = global_message_option_dict
        self._default_field = default_field
        self._comment_prefix = comment_prefix
        self._creat_cache: CREATE_MODEL_CACHE_T = create_model_cache or _create_model_cache
        self._pydantic_base: Type["BaseModel"] = pydantic_base or BaseModel
        self._pydantic_module: str = pydantic_module or __name__
        self._comment_template: Template = (template or Template)(local_dict or {}, comment_prefix)
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

    def get_model(self, full_name: str) -> Type[BaseModel]:
        model = self._creat_cache.get(full_name, None)
        if model is None:
            raise ValueError(f"Can not found {full_name} model")
        return model

    ###############
    # util method #
    ###############
    def _get_field_info_dict_by_full_name(self, full_name: str) -> Optional["FieldInfoTypedDict"]:
        split_full_name = full_name.split(".")
        if len(split_full_name) == 2:
            message_name, *key_list = split_full_name
        else:
            # TODO Maybe fix the problem that multiple packages have the same message
            message_name, *key_list = split_full_name[1:]  # ignore package name
        if message_name not in self._message_option_dict:
            return None
        message_option_dict: "MessageOptionTypedDict" = self._message_option_dict[message_name]
        if message_option_dict["metadata"].get("ignore", False):
            return None

        for key in key_list:
            if key in message_option_dict["message"]:
                return message_option_dict["message"][key]
            elif key in message_option_dict["nested"]:
                message_option_dict = message_option_dict["nested"][key]
                if message_option_dict["metadata"].get("ignored", False):
                    return None
            else:
                return None
        return None

    def _one_of_handle(self, descriptor: Descriptor) -> Tuple[Dict[str, "UseOneOfTypedDict"], Dict[str, Any]]:
        message_option_dict: "MessageOptionTypedDict" = self._message_option_dict.get(
            descriptor.name, {"message": {}, "one_of": {}, "nested": {}, "metadata": {}}
        )
        ignore_parse_rule = message_option_dict.get("metadata", {}).get("ignored", False)
        one_of_desc_dict = {}
        if not ignore_parse_rule:
            one_of_desc_dict = message_option_dict.get("one_of", {})

        one_of_dict: Dict[str, "UseOneOfTypedDict"] = {}
        optional_dict: Dict[str, Any] = {}
        optional_id_set: Set[str] = set()

        for field in descriptor.fields:
            if not field.containing_oneof:
                continue
            if "_" + field.name == field.containing_oneof.name:
                optional_id_set.add(field.containing_oneof.full_name)
                # support optional field
                # e.g.:
                #   message OptionalMessage{
                #     optional string name = 1;
                #     optional int32 age= 2;
                #   };

                # one_of name is `_name`, `_age`
                # but need name is `name`, `age`
                optional_dict[field.full_name] = {"is_proto3_optional": True}

        for one_of in descriptor.oneofs:
            field_full_name: str = one_of.full_name
            if field_full_name in optional_id_set:
                continue

            if field_full_name not in one_of_dict:
                one_of_dict[field_full_name] = {"required": False, "fields": set()}
            # pyi file not include pkg info
            for found_column_name in [field_full_name, ".".join(field_full_name.split(".")[1:])]:
                if found_column_name not in one_of_desc_dict:
                    continue
                # only PGV or P2P support
                one_of_dict[field_full_name]["required"] = one_of_desc_dict[found_column_name].get("required", False)
                optional_fields = one_of_desc_dict[found_column_name].get("optional_fields", set())
                if optional_fields:
                    for field_name in optional_fields:
                        optional_dict[descriptor.full_name + "." + field_name] = {"is_proto3_optional": True}

            for _field in one_of.fields:
                one_of_dict[field_full_name]["fields"].add(_field.name)
        return one_of_dict, optional_dict

    def _get_pydantic_base(self, config_dict: Dict[str, Any]) -> Type[BaseModel]:
        if config_dict:
            if _pydantic_adapter.is_v1:
                config_class = self._pydantic_base.Config  # type: ignore
                _config_dict: Dict[str, Any] = {"Config": type(config_class.__name__, (config_class,), config_dict)}
            else:
                from pydantic import ConfigDict

                _config_dict = {"model_config": ConfigDict(**config_dict)}  # type: ignore[typeddict-item]

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
            nested_type: Any = self._parse_msg_to_pydantic_model(descriptor=message, root_descriptor=descriptor)
            nested_message_dict[message.full_name] = nested_type
        # enum support
        for enum_type in descriptor.enum_types:
            class_dict: dict = {v.name: v.number for v in enum_type.values}
            class_dict["__doc__"] = ""
            nested_type = IntEnum(enum_type.name, class_dict)  # type: ignore
            nested_message_dict[enum_type.full_name] = nested_type
        return nested_message_dict

    ####################
    # field  handler   #
    ####################
    def _protobuf_field_type_is_type_message_handler(self, field_dataclass: FieldDataClass) -> None:
        protobuf_field = field_dataclass.protobuf_field
        if protobuf_field.message_type.name in self._message_type_dict_by_type_name:
            # Timestamp, Struct, Empty, Duration, Any support
            field_dataclass.field_type_name = protobuf_field.message_type.name.lower()
            field_dataclass.field_type = self._message_type_dict_by_type_name[protobuf_field.message_type.name]
            if protobuf_field.message_type.name in self._message_default_factory_dict_by_type_name:
                # Default factory has a higher priority
                field_dataclass.field_default_factory = self._message_default_factory_dict_by_type_name[
                    protobuf_field.message_type.name
                ]
        elif protobuf_field.message_type.name.endswith("Entry"):
            # support google.protobuf.MapEntry
            # key, value = column.message_type.fields
            field_dataclass.field_type_name = "map"
            dict_type_param_list = []
            for k_v_field in protobuf_field.message_type.fields:
                if not k_v_field.message_type:
                    k_v_type: Any = constant.protobuf_desc_python_type_dict[k_v_field.type]
                elif k_v_field.message_type.name in self._message_type_dict_by_type_name:
                    k_v_type = self._message_type_dict_by_type_name[k_v_field.message_type.name]
                else:
                    k_v_type = self._parse_msg_to_pydantic_model(
                        descriptor=k_v_field.message_type, root_descriptor=protobuf_field.message_type
                    )
                dict_type_param_list.append(k_v_type)

            field_dataclass.field_type = Dict[tuple(dict_type_param_list)]  # type: ignore
            field_dataclass.field_default_factory = dict
        elif protobuf_field.message_type.file.name.startswith("google/protobuf/"):
            module_name = protobuf_field.message_type.file.name.split(".")[0].replace("/", ".") + "_pb2"
            type_factory = getattr(importlib.import_module(module_name), protobuf_field.message_type.name)
            field_dataclass.field_type = type_factory
            field_dataclass.field_default_factory = type_factory
        else:
            # support google.protobuf.Message
            field_info_dict: Union[FieldInfoTypedDict, dict] = (
                self._get_field_info_dict_by_full_name(field_dataclass.protobuf_field.full_name) or {}
            )
            skip_validate_rule = field_info_dict.get("skip", False)
            full_name = protobuf_field.message_type.full_name
            if full_name in field_dataclass.nested_message_dict:
                _cache_full_name = full_name + SKIP_RULE_MESSAGE_SUFFIX if skip_validate_rule else full_name
                if _cache_full_name not in field_dataclass.nested_message_dict:
                    # found and gen new message, finally, register to nested_message_dict
                    nested_message = [i for i in field_dataclass.descriptor.nested_types if i.full_name == full_name][0]
                    nested_type: Any = self._parse_msg_to_pydantic_model(
                        descriptor=nested_message,
                        class_name=protobuf_field.message_type.name + SKIP_RULE_MESSAGE_SUFFIX,
                        skip_validate_rule=skip_validate_rule,
                    )
                    field_dataclass.nested_message_dict[_cache_full_name] = nested_type
                    field_dataclass.field_type = field_dataclass.nested_message_dict[_cache_full_name]
                else:
                    field_dataclass.field_type = field_dataclass.nested_message_dict[full_name]
                # Facilitate the analysis of `gen code`
                setattr(field_dataclass.field_type, "_is_nested", True)
                field_dataclass.field_default_factory = field_dataclass.field_type
            else:
                # Python Protobuf does not solve the namespace problem of modules,
                # so there is no uniform cross-module reference
                # see issue: https://github.com/protocolbuffers/protobuf/issues/1491
                is_same_pkg: bool = field_dataclass.descriptor.file.name == protobuf_field.message_type.file.name
                if not is_same_pkg:
                    field_dataclass.field_type = self._parse_msg_to_pydantic_model(
                        descriptor=protobuf_field.message_type,
                        skip_validate_rule=skip_validate_rule,
                        root_descriptor=field_dataclass.descriptor,
                    )
                    field_dataclass.field_default_factory = field_dataclass.field_type
                    # _class_name = replace_file_name_to_class_name(protobuf_field.message_type.file.name) + _class_name
                    # field_dataclass.field_type = self._parse_msg_to_pydantic_model(
                    #     descriptor=protobuf_field.message_type,
                    #     class_name=_class_name,
                    #     skip_validate_rule=skip_validate_rule,
                    # )
                    # _class_doc: str = (
                    #     "Note: The current class does not belong to the package\n"
                    #     f"{_class_name} protobuf path:{protobuf_field.message_type.file.name}"
                    # )
                    # setattr(field_dataclass.field_type, "__doc__", _class_doc)
                else:
                    # if self-referencing, need use Python type hints postponed annotations
                    _class_name: str = protobuf_field.message_type.name
                    field_dataclass.field_type = f'"{_class_name}"'
                    if (
                        skip_validate_rule
                        or protobuf_field.message_type.full_name != field_dataclass.descriptor.full_name
                    ):
                        try:
                            field_dataclass.field_type = self._parse_msg_to_pydantic_model(
                                descriptor=protobuf_field.message_type,
                                class_name=_class_name if not skip_validate_rule else _class_name + "OnlyUseSkipRule",
                                skip_validate_rule=skip_validate_rule,
                            )
                        except WaitingToCompleteException:
                            pass
                    if isinstance(field_dataclass.field_type, str):
                        logger.warning(
                            f"{field_dataclass.protobuf_field.full_name}'s default_factory attr value:{_class_name} "
                            f"is not generated and cannot be referenced now"
                        )
                    else:
                        field_dataclass.field_default_factory = field_dataclass.field_type

    def _protobuf_field_type_is_type_enum_handler(self, field_dataclass: FieldDataClass) -> None:
        # support google.protobuf.Enum
        field_dataclass.field_default = 0
        protobuf_field = field_dataclass.protobuf_field
        field_dataclass.field_type_name = "enum"
        if protobuf_field.enum_type.full_name in field_dataclass.nested_message_dict:
            field_dataclass.field_type = field_dataclass.nested_message_dict[protobuf_field.enum_type.full_name]
            # Facilitate the analysis of `gen code`
            setattr(field_dataclass.field_type, "_is_nested", True)
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
            field_dataclass.field_type_name = "repeated"
            # TODO support lambda
            if field_dataclass.field_default is not _pydantic_adapter.PydanticUndefined:
                field_dataclass.field_default = _pydantic_adapter.PydanticUndefined

    def _gen_field_info(self, field_dataclass: FieldDataClass, skip_validate_rule: bool) -> Optional[FieldInfo]:
        field_class = self._default_field
        field_info_dict = self._get_field_info_dict_by_full_name(field_dataclass.protobuf_field.full_name)

        if field_info_dict is not None and not skip_validate_rule:
            if self._parse_msg_desc_method != "PGV":
                # pgv method not support template var
                field_info_dict = self._comment_template.handle_template_var(field_info_dict)
            if not (self._parse_msg_desc_method is None or self._parse_msg_desc_method == "PGV"):
                # comment rule need handler
                field_info_dict = gen_field_rule_info_dict_from_field_comment_dict(
                    field_info_dict,  # type:ignore[arg-type]
                    field=field_dataclass.protobuf_field,
                    type_name=field_dataclass.field_type_name,
                    full_name=field_dataclass.protobuf_field.full_name,
                )

            raw_validator_dict = field_info_dict.get("validator", {})
            field_info_dict: FieldInfoTypedDict = FieldInfoParamModel(**field_info_dict).dict()  # type: ignore
            field_info_dict.pop("skip")

            is_required = field_info_dict.get("required", None)
            if is_required:
                field_dataclass.is_required = is_required

            # Nested types do not include the `enable`, `field` and `validator`  attributes
            if not field_info_dict.pop("enable"):
                return None
            _field = field_info_dict.pop("field")
            if _field:
                field_class = _field
            validator_dict = field_info_dict.pop("validator")
            if validator_dict:
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
                field_dataclass.validators.update(raw_validator_dict)

            # Unified field parameter handling
            field_info_param_dict_handle(
                field_info_dict,  # type: ignore[arg-type]
                field_dataclass.field_default,
                field_dataclass.field_default_factory,
                field_dataclass.field_type,
            )

            # Type will change in the unified processing logic
            field_type = field_info_dict.pop("type_", field_dataclass.field_type)
            map_type_dict = field_info_dict.pop("map_type", {})
            if field_type:
                field_dataclass.field_type = field_type
            elif map_type_dict and field_dataclass.field_type._name == "Dict":
                new_args_list: List = list(field_dataclass.field_type.__args__)
                for index, k_v_column in enumerate(["keys", "values"]):
                    if k_v_column not in map_type_dict:
                        continue

                    raw_k_v_type = new_args_list[index]
                    new_k_v_type = map_type_dict[k_v_column]

                    if (
                        get_origin(new_k_v_type) is Annotated
                        or issubclass(new_k_v_type, raw_k_v_type)
                        or raw_k_v_type is datetime.datetime
                    ):
                        new_args_list[index] = new_k_v_type
                field_dataclass.field_type = Dict[tuple(new_args_list)]  # type: ignore
        else:
            field_info_dict = {
                "default": field_dataclass.field_default,
                "default_factory": field_dataclass.field_default_factory,
                "extra": {},
            }
        if not _pydantic_adapter.is_v1:
            field_info_param_dict_migration_v2_handler(field_info_dict)  # type: ignore[arg-type]

        for remove_key in ("extra", "json_schema_extra"):
            if not field_info_dict.get(remove_key, True):  # type: ignore[misc]
                field_info_dict.pop(remove_key)  # type: ignore[misc]

        return field_class(**field_info_dict)  # type: ignore

    def _parse_msg_to_pydantic_model(
        self,
        *,
        descriptor: Descriptor,
        class_name: str = "",
        skip_validate_rule: bool = False,
        root_descriptor: Optional[Descriptor] = None,
    ) -> Type[BaseModel]:
        is_same_pkg = descriptor.file.name == root_descriptor.file.name if root_descriptor else True
        class_name = class_name or descriptor.name

        if not is_same_pkg:
            class_name = replace_file_name_to_class_name(descriptor.file.name) + class_name

        message_key = (descriptor.full_name, class_name, skip_validate_rule)
        if message_key in self._creat_cache:
            if self._creat_cache[message_key] is None:
                raise WaitingToCompleteException(f"The model:{message_key} is being generated")
            return self._creat_cache[message_key]  # type: ignore[return-value]
        else:
            self._creat_cache[message_key] = None

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
                field_type_name=protobuf_common_type_dict.get(protobuf_field.type, None),  # type: ignore
                field_default=_pydantic_adapter.PydanticUndefined,
                field_default_factory=None,
                is_required=False,
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
            field_info = self._gen_field_info(field_dataclass, skip_validate_rule)
            if not field_info:
                continue

            is_proto3_optional = optional_dict.get(protobuf_field.full_name, {}).get("is_proto3_optional", False)
            if is_proto3_optional or self._all_field_set_optional:
                field_dataclass.field_type = Optional[field_dataclass.field_type]
                if (
                    field_dataclass.is_required is not True
                    and field_info.default is _pydantic_adapter.PydanticUndefined
                    and field_info.default_factory is None
                ):
                    field_info.default = None
            annotation_dict[field_dataclass.field_name] = (field_dataclass.field_type, field_info)
            if one_of_dict:
                model_config_dict = _pydantic_adapter.get_model_config_dict(
                    self._get_pydantic_base(pydantic_model_config_dict)
                )
                for one_of_name, sub_one_of_dict in one_of_dict.items():
                    pydantic_allow_validation_field_handler(
                        field_dataclass.field_name, field_info.alias, sub_one_of_dict["fields"], model_config_dict
                    )

            if field_dataclass.field_type in ALLOW_ARBITRARY_TYPE and not _pydantic_adapter.get_model_config_value(
                self._pydantic_base, "arbitrary_types_allowed"
            ):
                pydantic_model_config_dict["arbitrary_types_allowed"] = True

        if one_of_dict:
            validators["one_of_validator"] = _pydantic_adapter.model_validator(mode="before", allow_reuse=True)(
                check_one_of
            )
        try:
            pydantic_model: Type[BaseModel] = create_pydantic_model(
                annotation_dict,
                class_name=class_name,
                pydantic_validators=validators or None,
                pydantic_module=self._pydantic_module,
                pydantic_base=self._get_pydantic_base(pydantic_model_config_dict),
            )
        except Exception as e:
            if "arbitrary_types_allowed" in str(e):
                # It looks ugly, but it's an easy way to recognise
                pydantic_model_config_dict["arbitrary_types_allowed"] = True
                pydantic_model = create_pydantic_model(
                    annotation_dict,
                    class_name=class_name,
                    pydantic_validators=validators or None,
                    pydantic_module=self._pydantic_module,
                    pydantic_base=self._get_pydantic_base(pydantic_model_config_dict),
                )
            else:
                raise e

        CodeRefModel.set_to_model(
            pydantic_model,
            one_of_dict=one_of_dict,
            base_model=self._pydantic_base,
            # Facilitate the analysis of `gen code`
            nested_message_dict={k: v for k, v in nested_message_dict.items() if getattr(v, "_is_nested", False)},
            validators=validators,
        )
        setattr(pydantic_model, "_one_of_dict", one_of_dict)
        if not is_same_pkg:
            class_doc = (
                "Note: The current class does not belong to the package\n"
                f"{class_name} protobuf path:{descriptor.file.name}"
            )
            setattr(pydantic_model, "__doc__", class_doc)
        self._creat_cache[message_key] = pydantic_model
        return pydantic_model


def msg_to_pydantic_model(
    msg: Union[Type[Message], Descriptor],
    default_field: Type[FieldInfo] = FieldInfo,
    comment_prefix: str = "p2p",
    parse_msg_desc_method: Any = None,
    local_dict: Optional[Dict[str, Any]] = None,
    pydantic_base: Optional[Type["BaseModel"]] = None,
    pydantic_module: Optional[str] = None,
    template: Optional[Type[Template]] = None,
    message_type_dict_by_type_name: Optional[Dict[str, Any]] = None,
    message_default_factory_dict_by_type_name: Optional[Dict[str, Any]] = None,
    all_field_set_optional: bool = False,
    create_model_cache: Optional[CREATE_MODEL_CACHE_T] = None,
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
    :param template: DescTemplate object, which can extend and modify template adaptation rules through inheritance
    :param message_type_dict_by_type_name: Define the Python type mapping corresponding to each Protobuf Type
    :param message_default_factory_dict_by_type_name: Define the default_factory corresponding to each Protobuf Type
    :param create_model_cache: Cache the generated model
    :param all_field_set_optional: If true, all fields become optional,
        see: https://github.com/so1n/protobuf_to_pydantic/issues/60
    """
    return M2P(
        msg=msg,
        default_field=default_field,
        comment_prefix=comment_prefix,
        parse_msg_desc_method=parse_msg_desc_method,
        local_dict=local_dict,
        pydantic_module=pydantic_module,
        pydantic_base=pydantic_base,
        template=template,
        message_type_dict_by_type_name=message_type_dict_by_type_name,
        message_default_factory_dict_by_type_name=message_default_factory_dict_by_type_name,
        create_model_cache=create_model_cache,
        all_field_set_optional=all_field_set_optional,
    ).model
