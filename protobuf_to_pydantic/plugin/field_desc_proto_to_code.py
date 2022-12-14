import inspect
import logging
from typing import Any, Iterable, Optional, Tuple

from google.protobuf.descriptor_pb2 import (  # type: ignore
    DescriptorProto,
    EnumDescriptorProto,
    FieldDescriptorProto,
    FileDescriptorProto,
)
from mypy_protobuf.main import PYTHON_RESERVED, Descriptors, SourceCodeLocation
from pydantic.fields import FieldInfo, Undefined

from protobuf_to_pydantic.customer_con_type import pydantic_con_dict
from protobuf_to_pydantic.gen_code import BaseP2C
from protobuf_to_pydantic.gen_model import (
    DescTemplate,
    MessagePaitModel,
    field_param_dict_handle,
    python_type_default_value_dict,
    type_dict,
)
from protobuf_to_pydantic.get_desc.from_pb_option.base import field_optional_handle, protobuf_common_type_dict
from protobuf_to_pydantic.plugin.config import Config

logger: logging.Logger = logging.getLogger(__name__)


class FileDescriptorProtoToCode(BaseP2C):
    def __init__(self, fd: FileDescriptorProto, descriptors: Descriptors, config: Config):
        super().__init__(
            customer_import_set=config.customer_import_set,
            customer_deque=config.customer_deque,
            module_path=config.module_path,
            code_indent=config.code_indent,
        )
        self._fd: FileDescriptorProto = fd
        self._descriptors: Descriptors = descriptors
        self._desc_template: DescTemplate = config.desc_template
        self._parse_field_descriptor()

    def _enum(self, enums: Iterable[EnumDescriptorProto], scl_prefix: SourceCodeLocation) -> str:
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
            content += f"class {class_name}(IntEnum):\n"
            for enum_item in enum.value:
                content += " " * self.code_indent + f"{enum_item.name} = {enum_item.number}\n"
            content += "\n\n"
        return content

    def _message_nested_type_handle(self, desc: DescriptorProto, scl_prefix: SourceCodeLocation, indent: int) -> str:
        """Parse the nested information of Message"""
        nested_type_list = [
            nested_message
            for nested_message in desc.nested_type
            # Some data of Map Entry in nested type array
            if not nested_message.options.map_entry
        ]
        return self._message(nested_type_list, scl_prefix, indent + self.code_indent)

    def _message_field_handle(self, field: FieldDescriptorProto, indent: int) -> Optional[str]:
        """generate message's field to Pydantic.FieldInfo code"""
        field_info_dict: dict = {}
        rule_type_str: Optional[str] = None
        # TODO Cross-file references are not currently supported
        if field.type == 11:
            # message handle
            message = self._descriptors.messages[field.type_name]

            if message.options.map_entry:
                key_msg, value_msg = message.field
                self._add_import_code("typing")
                type_str: str = (
                    f"typing.Dict["
                    f"{self._get_protobuf_type_str(key_msg)[0]}, "
                    f"{self._get_protobuf_type_str(value_msg)[0]}"
                    f"]"
                )
                field_info_dict["default_factory"] = dict
                rule_type_str = "map"
            elif field.type_name.startswith(".google.protobuf"):
                type_str, rule_type_str = self._get_protobuf_type_str(field)
                if type_str == "datetime.datetime":
                    field_info_dict["default_factory"] = "datetime.datetime.now"
                elif type_str in ("Timedelta", "AnyMessage"):
                    field_info_dict["default_factory"] = type_str
            else:
                type_str = '"' + self._get_protobuf_type_str(field)[0] + '"'
        elif field.type == 14:
            # enum handle
            field_type = field.type_name.split(".")[-1]
            type_str = self._get_value_code(field_type)
            field_info_dict["default"] = 0
        elif field.type not in type_dict:
            logger.error(f"Not found {field.type} in type_dict")
            return None
        else:
            field_info_dict["default"] = python_type_default_value_dict[type_dict[field.type]]
            type_str, rule_type_str = self._get_protobuf_type_str(field)

        if field.label == field.LABEL_REPEATED and not field.type_name.endswith("Entry"):
            # repeated support
            self._add_import_code("typing")
            type_str = f"typing.List[{type_str}]"
            field_info_dict.pop("default", "")
            field_info_dict["default_factory"] = list
            rule_type_str = "repeated"

        if len(field.options.ListFields()) != 0 and rule_type_str:
            # protobuf option support
            field_option_info_dict = MessagePaitModel(
                **self._desc_template.handle_template_var(field_optional_handle(rule_type_str, field.type_name, field))
            ).dict()

            if not field_option_info_dict.pop("skip", False):
                field_param_dict_handle(
                    field_option_info_dict,
                    field_info_dict.get("default", Undefined),
                    field_info_dict.get("default_factory", None),
                )
                field_info_dict = field_option_info_dict

        if "validator" in field_info_dict:
            # validator support
            field_info_dict.pop("validator")
            # logger.info(field_info_dict.pop("validator"))
            # type_str = self.pydantic_con_type_handle(field_info_dict.pop("validator"))

        # type support
        type_: Any = field_info_dict.pop("type_", None)
        map_type_dict: dict = field_info_dict.pop("map_type", {})
        if type_:
            if inspect.isclass(type_) and type_.__mro__[1] in pydantic_con_dict:
                type_str = self.pydantic_con_type_handle(type_)
            else:
                type_str = self._get_value_code(type_)
        elif map_type_dict:
            message = self._descriptors.messages[field.type_name]
            if "keys" in map_type_dict:
                key_type_str = self._get_value_code(map_type_dict["keys"])
            else:
                key_type_str = self._get_protobuf_type_str(message.field[0])[0]
            if "values" in map_type_dict:
                value_type_str = self._get_value_code(map_type_dict["values"])
            else:
                value_type_str = self._get_protobuf_type_str(message.field[1])[0]
            type_str = f"typing.Dict[{key_type_str}, {value_type_str}]"

        # custom field support
        field_class: Optional[FieldInfo] = field_info_dict.pop("field", None)
        if field_class:
            field_name: str = self._get_value_code(field_class)
        else:
            field_name = "FieldInfo"
            self._add_import_code("pydantic.fields", "FieldInfo")

        # arranging  field info parameters
        new_field_info_dict = {}
        for key in FieldInfo.__slots__:
            if key not in field_info_dict:
                continue
            value: Any = field_info_dict.pop(key, None)
            if value is getattr(FieldInfo(), key):
                continue
            new_field_info_dict[key] = value
        if field_info_dict:
            new_field_info_dict["extra"] = field_info_dict

        field_info_dict = new_field_info_dict
        field_info_str: str = " ,".join([f"{k}={self._get_value_code(v)}" for k, v in field_info_dict.items()]) or ""

        return " " * (self.code_indent + indent) + f"{field.name}: {type_str} = {field_name}({field_info_str}) \n"
        # TODO support config
        # TODO support validator

    def _message(self, messages: Iterable[DescriptorProto], scl_prefix: SourceCodeLocation, indent: int = 0) -> str:
        if not messages:
            return ""
        self._add_import_code("google.protobuf.message", "Message")
        self._add_import_code("pydantic", "BaseModel")
        content: str = ""
        for i, desc in enumerate(messages):
            class_name = desc.name if desc.name not in PYTHON_RESERVED else "_r_" + desc.name
            class_content = " " * indent + f"class {class_name}(BaseModel):\n"
            class_head_content = ""
            class_field_content = ""

            if desc.nested_type:
                class_head_content += self._message_nested_type_handle(desc, scl_prefix, indent)
            for idx, field in enumerate(desc.field):
                if field.name in PYTHON_RESERVED:
                    continue
                _field_content: Optional[str] = self._message_field_handle(field, indent)
                if _field_content:
                    class_field_content += _field_content

            content += class_content + class_head_content + class_field_content
            content += "\n" if indent > 0 else "\n\n"
        return content

    def _get_protobuf_type_str(self, field: FieldDescriptorProto) -> Tuple[str, Optional[str]]:
        rule_type_str: Optional[str] = None
        if field.type in type_dict:
            field_type = type_dict[field.type]
            py_type_str: str = self._get_value_code(field_type)
            rule_type_str = protobuf_common_type_dict.get(field.type, None)
            return py_type_str, rule_type_str
        elif field.type_name.startswith(".google.protobuf"):
            _type_str = field.type_name.split(".")[-1]
            if _type_str == "Empty":
                py_type_str = "None"
            elif _type_str == "Timestamp":
                py_type_str = "datetime.datetime"
                rule_type_str = "timestamp"
                self._import_set.add("import datetime")
            elif _type_str == "Duration":
                py_type_str = "Timedelta"
                rule_type_str = "duration"
                self._add_import_code("protobuf_to_pydantic.util", py_type_str)
            elif _type_str == "Any":
                py_type_str = "AnyMessage"
                rule_type_str = "any"
                self._add_import_code("google.protobuf.any_pb2", "Any", " as AnyMessage")
            else:
                logger.error(f"Not support type {field.type_name}")
                py_type_str = ""
            return py_type_str, rule_type_str
        else:
            # TODO Cross-file references are not currently supported
            return field.type_name.split(".")[-1], "message"

    def _parse_field_descriptor(self) -> None:
        self._content_deque.append(self._enum(self._fd.enum_type, [FileDescriptorProto.ENUM_TYPE_FIELD_NUMBER]))
        self._content_deque.append(self._message(self._fd.message_type, [FileDescriptorProto.ENUM_TYPE_FIELD_NUMBER]))
