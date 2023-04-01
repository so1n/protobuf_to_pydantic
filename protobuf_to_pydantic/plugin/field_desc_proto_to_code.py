import inspect
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterable, Optional, Set, Tuple

from mypy_protobuf.main import PYTHON_RESERVED, Descriptors, SourceCodeLocation
from pydantic import BaseModel
from pydantic.fields import FieldInfo, Undefined

from protobuf_to_pydantic import customer_validator
from protobuf_to_pydantic.customer_con_type import pydantic_con_dict
from protobuf_to_pydantic.gen_code import BaseP2C
from protobuf_to_pydantic.gen_model import (
    DescTemplate,
    MessagePaitModel,
    field_param_dict_handle,
    python_type_default_value_dict,
    type_dict,
)
from protobuf_to_pydantic.get_desc.from_pb_option.base import field_option_handle, protobuf_common_type_dict
from protobuf_to_pydantic.grpc_types import (
    AnyMessage,
    DescriptorProto,
    EnumDescriptorProto,
    FieldDescriptorProto,
    FileDescriptorProto,
)
from protobuf_to_pydantic.plugin.my_types import ProtobufTypeModel

if TYPE_CHECKING:
    from protobuf_to_pydantic.plugin.config import ConfigModel

logger: logging.Logger = logging.getLogger(__name__)


class FileDescriptorProtoToCode(BaseP2C):
    def __init__(self, fd: FileDescriptorProto, descriptors: Descriptors, config: "ConfigModel"):
        # Prevent mutable variables from being shared with other configs
        config = config.copy(deep=True)
        super().__init__(
            customer_import_set=config.customer_import_set,
            customer_deque=config.customer_deque,
            module_path=config.module_path,
            code_indent=config.code_indent,
            pyproject_file_path=config.pyproject_file_path,
        )
        self.config = config
        self._fd: FileDescriptorProto = fd
        self._descriptors: Descriptors = descriptors
        self._desc_template: DescTemplate = config.desc_template_instance

        if config.base_model_class is BaseModel:
            self._import_set.add("from pydantic import BaseModel")
        else:
            self._add_import_code(config.base_model_class.__module__, config.base_model_class.__name__)
        self._parse_desc_name_dict: Dict[str, str] = {}
        self._parse_field_descriptor()

    def _add_other_module_pkg(self, other_fd: FileDescriptorProto, type_str: str) -> None:
        if other_fd.name == self._fd.name:
            return
        # Generate the corresponding import statement
        # e.g:
        #   fd name:example_proto/demo/demo.proto
        #   other_fd name: example_proto/common/single.proto
        #   output: from ..common.single_p2p import DemoMessage
        fd_path_list: Tuple[str, ...] = Path(self._fd.name).parts
        message_path_list: Tuple[str, ...] = Path(other_fd.name).parts
        index: int = -1
        for _index in range(min(len(fd_path_list), len(message_path_list))):
            if message_path_list[_index] == fd_path_list[_index]:
                index = _index

        module_name: str = (
            ".".join(message_path_list[index + 1 : -1])
            + "."
            + message_path_list[-1].replace(".proto", "")
            + self.config.file_name_suffix
        )
        logger.info((self._fd.name, other_fd.name, index))
        if index != "-1":
            module_name = "." * (len(message_path_list) - (index + 1)) + module_name
        self._add_import_code(module_name, type_str)

    def _enum(self, enums: Iterable[EnumDescriptorProto], scl_prefix: SourceCodeLocation, indent: int = 0) -> str:
        """
        e.g:
            enums:
                {
                    "name": "State",
                    [
                        "value": {
                            name: "INACTIVE"
                            number: 0
                        }
                    ]
                }
            python code:
                from enum import IntEnum

                class State(IntEnum):
                    INACTIVE = 0
        """
        if not enums:
            return ""
        self._add_import_code("enum", "IntEnum")
        content: str = ""
        for i, enum in enumerate(enums):
            class_name = enum.name if enum.name not in PYTHON_RESERVED else "_r_" + enum.name
            content += " " * indent + f"class {class_name}(IntEnum):\n"
            for enum_item in enum.value:
                content += " " * (self.code_indent + indent) + f"{enum_item.name} = {enum_item.number}\n"
            content += "\n\n"
        return content

    def _message_nested_type_handle(
        self, desc: DescriptorProto, scl_prefix: SourceCodeLocation, indent: int, nested_message_config_dict: dict
    ) -> str:
        """Parse the nested information of Message"""
        content: str = ""
        for nested_message in desc.nested_type:
            if nested_message.options.map_entry:
                # Some data of Map Entry in nested type array
                continue
            skip_validate_rule = nested_message_config_dict.get(nested_message.name, {}).get("skip", False)
            content += self._message(
                nested_message, scl_prefix, indent + self.code_indent, skip_validate_rule=skip_validate_rule
            )
        return content

    # flake8: noqa: C901
    def _message_field_handle(
        self,
        desc: DescriptorProto,
        field: FieldDescriptorProto,
        indent: int,
        nested_message_config_dict: dict,
        skip_validate_rule: bool = False,
    ) -> Optional[Tuple[str, str]]:
        """generate message's field to Pydantic.FieldInfo code"""
        field_info_dict: dict = {}
        rule_type_str: Optional[str] = None
        nested_message_name: Optional[str] = None
        if field.type == 11:
            # message handle
            message = self._descriptors.messages[field.type_name]

            if message.options.map_entry:
                key_msg, value_msg = message.field
                self._add_import_code("typing")
                type_str: str = (
                    f"typing.Dict[{self._get_protobuf_type_model(key_msg).py_type_str},"
                    f" {self._get_protobuf_type_model(value_msg).py_type_str}]"
                )
                field_info_dict["default_factory"] = dict
                rule_type_str = "map"
            elif field.type_name.startswith(".google.protobuf"):
                protobuf_type_model = self._get_protobuf_type_model(field)
                type_str = protobuf_type_model.py_type_str
                rule_type_str = protobuf_type_model.rule_type_str
                field_info_dict["default_factory"] = protobuf_type_model.type_factory
            else:
                protobuf_type_model = self._get_protobuf_type_model(field)
                type_str = protobuf_type_model.py_type_str
                rule_type_str = protobuf_type_model.rule_type_str
                nested_message_name = type_str

                message_fd: FileDescriptorProto = self._descriptors.message_to_fd[field.type_name]
                self._add_other_module_pkg(message_fd, type_str)
                if message == desc:
                    # if self-referencing, need use Python type hints postponed annotations
                    type_str = f'"{type_str}"'
                elif message_fd.name == self._fd.name and message.name not in {i.name for i in desc.nested_type}:
                    # If the referenced Message is generated later, it needs to be generated in advance
                    self._content_deque.append(self._message(message, [FileDescriptorProto.ENUM_TYPE_FIELD_NUMBER]))

        elif field.type == 14:
            # enum handle
            type_str = field.type_name.split(".")[-1]
            field_info_dict["default"] = 0
            rule_type_str = "enum"
            message_fd = self._descriptors.message_to_fd[field.type_name]
            self._add_other_module_pkg(message_fd, type_str)
        elif field.type not in type_dict:
            logger.error(f"Not found {field.type} in type_dict")
            return None
        else:
            field_info_dict["default"] = python_type_default_value_dict[type_dict[field.type]]
            protobuf_type_model = self._get_protobuf_type_model(field)
            type_str = protobuf_type_model.py_type_str
            rule_type_str = protobuf_type_model.rule_type_str

        if field.label == field.LABEL_REPEATED and not field.type_name.endswith("Entry"):
            # repeated support
            self._add_import_code("typing")
            type_str = f"typing.List[{type_str}]"
            field_info_dict.pop("default", "")
            field_info_dict["default_factory"] = list
            rule_type_str = "repeated"
        if len(field.options.ListFields()) != 0 and rule_type_str and not skip_validate_rule:
            # protobuf option support
            field_option_info_dict: dict = field_option_handle(rule_type_str, field.type_name, field)  # type: ignore

            skip = field_option_info_dict.pop("skip", False)
            if nested_message_name:
                if nested_message_name not in nested_message_config_dict:
                    nested_message_config_dict[nested_message_name] = {}
                nested_message_config_dict[nested_message_name]["skip"] = skip

            field_option_info_dict = MessagePaitModel(
                **self._desc_template.handle_template_var(field_option_info_dict)
            ).dict()
            if not field_option_info_dict.pop("enable", False):
                return None
            field_param_dict_handle(
                field_option_info_dict,
                field_info_dict.get("default", Undefined),
                field_info_dict.get("default_factory", None),
            )
            field_info_dict = field_option_info_dict

        validator_dict = field_info_dict.pop("validator", None)
        class_head_content = ""
        if validator_dict:
            # validator support
            self._add_import_code("pydantic", "validator")
            for validator_name, validator_class in validator_dict.items():
                param, validator_instance = validator_class.__validator_config__
                func = validator_instance.func
                # TODO get allow_reuse, pre from validator_instance
                if func.__module__ != customer_validator.__name__:
                    continue

                self._add_import_code(func.__module__, func.__name__)
                param_str = ", ".join([self._get_value_code(i) for i in param])
                class_head_content += (
                    " " * (self.code_indent + indent)
                    + f"{validator_name} = validator({param_str},  allow_reuse=True)({func.__name__})\n"
                )

        # type support
        type_: Any = field_info_dict.pop("type_", None)
        map_type_dict: dict = field_info_dict.pop("map_type", {})
        if type_:
            # Custom types have the highest priority
            if inspect.isclass(type_) and type_.__mro__[1] in pydantic_con_dict:
                type_str = self.pydantic_con_type_handle(type_)
            else:
                type_str = self._get_value_code(type_)
        elif map_type_dict:
            # For `map type`, the string of type needs to be regenerated
            message = self._descriptors.messages[field.type_name]
            if "keys" in map_type_dict:
                key_type_str = self._get_value_code(map_type_dict["keys"])
            else:
                key_type_str = self._get_protobuf_type_model(message.field[0]).py_type_str
            if "values" in map_type_dict:
                value_type_str = self._get_value_code(map_type_dict["values"])
            else:
                value_type_str = self._get_protobuf_type_model(message.field[1]).py_type_str
            type_str = f"typing.Dict[{key_type_str}, {value_type_str}]"

        # custom field support
        field_class: Optional[FieldInfo] = field_info_dict.pop("field", None)
        if field_class:
            field_name: str = self._get_value_code(field_class)
        else:
            field_name = "FieldInfo"
            self._add_import_code("pydantic.fields", "FieldInfo")

        # arranging  field info parameters
        for key in FieldInfo.__slots__:
            value: Any = field_info_dict.get(key, None)
            if value is getattr(FieldInfo(), key):
                field_info_dict.pop(key, None)

        field_info_str: str = ", ".join([f"{k}={self._get_value_code(v)}" for k, v in field_info_dict.items()]) or ""
        class_field_content: str = (
            " " * (self.code_indent + indent) + f"{field.name}: {type_str} = {field_name}({field_info_str}) \n"
        )
        return class_head_content, class_field_content

    @staticmethod
    def _gen_one_of_dict(desc: DescriptorProto) -> Dict:
        one_of_dict = {}
        index_field_name_dict: Dict[int, Set[str]] = {}
        for field in desc.field:
            if not field.HasField("oneof_index"):
                continue
            if field.oneof_index not in index_field_name_dict:
                index_field_name_dict[field.oneof_index] = set()
            index_field_name_dict[field.oneof_index].add(field.name)

        for index, one_of_item in enumerate(desc.oneof_decl):
            option_dict = {}
            for option_descriptor, option_value in one_of_item.options.ListFields():
                pkg, rule_name = option_descriptor.full_name.split(".")
                if not pkg.endswith("validate"):
                    continue
                if rule_name in ("required",):
                    # Now only support `required`
                    option_dict[rule_name] = option_value
            option_dict["fields"] = index_field_name_dict[index]
            if option_dict:
                # Only when the rules are used, will the number of fields of one_of be checked to see if they match
                one_of_dict[desc.name + "." + one_of_item.name] = option_dict
        return one_of_dict

    def _message(
        self, desc: DescriptorProto, scl_prefix: SourceCodeLocation, indent: int = 0, skip_validate_rule: bool = False
    ) -> str:
        self._add_import_code("google.protobuf.message", "Message")
        content: str = ""
        class_name = desc.name if desc.name not in PYTHON_RESERVED else "_r_" + desc.name
        if class_name in self._parse_desc_name_dict:
            return self._parse_desc_name_dict[class_name]
        class_content = " " * indent + f"class {class_name}(BaseModel):\n"
        class_head_content = ""
        class_field_content = ""

        use_custom_type: bool = False
        nested_message_config_dict: dict = {}
        for idx, field in enumerate(desc.field):
            if field.name in PYTHON_RESERVED:
                continue
            if field.type == 11 and self._get_protobuf_type_model(field).type_factory is AnyMessage:
                use_custom_type = True

            _content_tuple: Optional[Tuple[str, str]] = self._message_field_handle(
                desc, field, indent, nested_message_config_dict, skip_validate_rule=skip_validate_rule
            )
            if _content_tuple:
                class_head_content += _content_tuple[0]
                class_field_content += _content_tuple[1]

        if desc.nested_type:
            class_head_content += self._message_nested_type_handle(desc, scl_prefix, indent, nested_message_config_dict)
        if desc.enum_type:
            class_head_content += self._enum(desc.enum_type, scl_prefix, indent + self.code_indent)

        if desc.oneof_decl:
            one_of_dict: dict = self._gen_one_of_dict(desc)
            if one_of_dict:
                class_head_content += (
                    f"{' ' * (indent + self.code_indent)}_one_of_dict = {self._get_value_code(one_of_dict)}\n"
                )
                class_head_content += (
                    f"{' ' * (indent + self.code_indent)}"
                    f"_check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)\n"
                )
                self._add_import_code("pydantic", "root_validator")
                self._add_import_code("protobuf_to_pydantic.customer_validator", "check_one_of")

        if use_custom_type:
            config_content: str = f"{' ' * (indent + self.code_indent)}class Config:\n"
            config_content += f"{' ' * (indent + self.code_indent * 2)}arbitrary_types_allowed = True\n\n"
            class_head_content = config_content + class_head_content
        content += "\n".join([i for i in [class_content, class_head_content, class_field_content] if i])
        content += "\n" if indent > 0 else "\n\n"
        self._parse_desc_name_dict[class_name] = content
        return content

    def _get_protobuf_type_model(self, field: FieldDescriptorProto) -> ProtobufTypeModel:
        rule_type_str: str = ""
        type_factory: Optional[Any] = None
        if field.type in type_dict:
            type_factory = type_dict[field.type]
            return ProtobufTypeModel(
                type_factory=type_factory,
                py_type_str=self._get_value_code(type_factory),
                rule_type_str=protobuf_common_type_dict.get(field.type, ""),
            )
        elif field.type_name.startswith(".google.protobuf"):
            _type_str = field.type_name.split(".")[-1]
            if _type_str == "Empty":
                py_type_str = "None"
                rule_type_str = ""
            elif _type_str == "Timestamp":
                py_type_str = "datetime"
                rule_type_str = "timestamp"
                type_factory = datetime.now
                self._add_import_code("datetime", "datetime")
            elif _type_str == "Duration":
                py_type_str = "Timedelta"
                rule_type_str = "duration"
                type_factory = timedelta
                self._add_import_code("datetime", "timedelta")
                self._add_import_code("protobuf_to_pydantic.util", py_type_str)
            elif _type_str == "Any":
                py_type_str = "Any"
                rule_type_str = "any"
                type_factory = AnyMessage
                self._add_import_code("google.protobuf.any_pb2", "Any")
            elif field.type_name.split(".")[-2] == "Struct":
                py_type_str = "Dict"
                rule_type_str = "struct"
                type_factory = dict
            else:
                logger.error(f"Not support type {field.type_name}")
                py_type_str = "Any"
                rule_type_str = "any"
                type_factory = AnyMessage
                self._add_import_code("google.protobuf.any_pb2", "Any")
            return ProtobufTypeModel(
                type_factory=type_factory,
                rule_type_str=rule_type_str,
                py_type_str=py_type_str,
            )
        else:
            return ProtobufTypeModel(
                # When relying on other Messages, it will only be used in the type of pydantic.Model,
                # and the type_ field will not be used at this time
                type_factory=None,
                rule_type_str="message",
                py_type_str=field.type_name.split(".")[-1],
            )

    def _parse_field_descriptor(self) -> None:
        self._content_deque.append(self._enum(self._fd.enum_type, [FileDescriptorProto.ENUM_TYPE_FIELD_NUMBER]))
        for desc in self._fd.message_type:
            self._content_deque.append(self._message(desc, [FileDescriptorProto.ENUM_TYPE_FIELD_NUMBER]))
