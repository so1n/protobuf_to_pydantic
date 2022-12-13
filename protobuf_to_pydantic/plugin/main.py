#!/usr/bin/env python
import inspect
import json
import logging
import sys
from collections import deque
from typing import Any, Deque, Iterable, Optional, Set, Tuple

from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest, CodeGeneratorResponse  # type: ignore
from google.protobuf.descriptor_pb2 import (  # type: ignore
    DescriptorProto,
    EnumDescriptorProto,
    FieldDescriptorProto,
    FileDescriptorProto,
)
from google.protobuf.json_format import MessageToDict  # type: ignore
from mypy_protobuf.main import PYTHON_RESERVED, Descriptors, SourceCodeLocation, code_generation
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

# If want to parse option, need to import the corresponding file
#   see details:https://stackoverflow.com/a/59301849
from protobuf_to_pydantic.protos import p2p_validate_pb2  # isort:skip
from protobuf_to_pydantic.protos import validate_pb2  # isort:skip


logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s", datefmt="%y-%m-%d %H:%M:%S", level=logging.INFO)


class FileDescriptorProtoToCode(BaseP2C):
    def __init__(
        self,
        fd: FileDescriptorProto,
        descriptors: Descriptors,
        customer_import_set: Optional[Set[str]] = None,
        customer_deque: Optional[Deque] = None,
        module_path: str = "",
        code_indent: Optional[int] = None,
        desc_template: Optional[DescTemplate] = None,
    ):
        super().__init__(
            customer_import_set=customer_import_set,
            customer_deque=customer_deque,
            module_path=module_path,
            code_indent=code_indent,
        )
        self._fd: FileDescriptorProto = fd
        self._descriptors: Descriptors = descriptors
        self._import_set: Set[str] = set()
        self._content_deque: Deque = deque()
        self.code_indent: int = 4
        self._desc_template: DescTemplate = desc_template or DescTemplate({}, "p2p")
        self._parse_field_descriptor()

    # def _get_value_code(self, type_: Any) -> str:
    #     if type_ and hasattr(type_, "__module__") and type_.__module__ == "builtins" or inspect.isfunction(type_):
    #         type_name = type_.__name__
    #     else:
    #         type_name = repr(type_)
    #     return type_name

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
        self._content_deque.append(content)
        return content

    def _message(self, messages: Iterable[DescriptorProto], scl_prefix: SourceCodeLocation, indent: int = 0) -> str:
        if not messages:
            return ""
        self._add_import_code("google.protobuf.message", "Message")
        self._add_import_code("pydantic", "BaseModel")
        content: str = ""
        for i, desc in enumerate(messages):
            class_name = desc.name if desc.name not in PYTHON_RESERVED else "_r_" + desc.name
            content += " " * indent + f"class {class_name}(BaseModel):\n"

            if desc.nested_type:
                nested_type_list = [
                    nested_message
                    for nested_message in desc.nested_type
                    # Some data of Map Entry in nested type array
                    if not nested_message.options.map_entry
                ]
                self._message(nested_type_list, scl_prefix, indent + self.code_indent)
            for idx, field in enumerate(desc.field):
                field_info_dict: dict = {}
                rule_type_str: Optional[str] = None
                if field.name in PYTHON_RESERVED:
                    continue
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
                    continue
                else:
                    field_info_dict["default"] = python_type_default_value_dict[type_dict[field.type]]
                    type_str, rule_type_str = self._get_protobuf_type_str(field)
                if field.label == field.LABEL_REPEATED and not field.type_name.endswith("Entry"):
                    self._add_import_code("typing")
                    type_str = f"typing.List[{type_str}]"
                    field_info_dict.pop("default", "")
                    field_info_dict["default_factory"] = list
                    rule_type_str = "repeated"

                if len(field.options.ListFields()) != 0 and rule_type_str:
                    field_option_info_dict = MessagePaitModel(
                        **self._desc_template.handle_template_var(
                            field_optional_handle(rule_type_str, field.type_name, field)
                        )
                    ).dict()

                    if not field_option_info_dict.pop("skip", False):
                        field_param_dict_handle(
                            field_option_info_dict,
                            field_info_dict.get("default", Undefined),
                            field_info_dict.get("default_factory", None),
                        )
                        field_info_dict = field_option_info_dict

                if "validator" in field_info_dict:
                    field_info_dict.pop("validator")
                    # logger.info(field_info_dict.pop("validator"))
                    # type_str = self.pydantic_con_type_handle(field_info_dict.pop("validator"))
                type_: Any = field_info_dict.pop("type_", None)
                if type_ and inspect.isclass(type_) and type_.__mro__[1] in pydantic_con_dict:
                    type_str = self.pydantic_con_type_handle(type_)
                field_class: Optional[FieldInfo] = field_info_dict.pop("field", None)
                if field_class:
                    field_name: str = self._get_value_code(field_class)
                else:
                    field_name = "FieldInfo"
                    self._add_import_code("pydantic.fields", "FieldInfo")

                new_field_info_dict = {}
                for key in FieldInfo.__slots__:
                    if key not in field_info_dict:
                        continue
                    value: Any = field_info_dict.pop(key, None)
                    if value is getattr(FieldInfo(), key):
                        continue
                    new_field_info_dict[key] = value
                new_field_info_dict["extra"] = field_info_dict
                field_info_dict = new_field_info_dict
                field_info_str: str = (
                    " ,".join([f"{k}={self._get_value_code(v)}" for k, v in field_info_dict.items()]) or ""
                )

                content += (
                    " " * (self.code_indent + indent) + f"{field.name}: {type_str} = {field_name}({field_info_str}) \n"
                )
                # TODO support config
                # TODO support validator
            if indent > 0:
                content += "\n"
            else:
                content += "\n\n"
        self._content_deque.append(content)
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
        self._enum(self._fd.enum_type, [FileDescriptorProto.ENUM_TYPE_FIELD_NUMBER])
        self._message(self._fd.message_type, [FileDescriptorProto.ENUM_TYPE_FIELD_NUMBER])


def process_file(proto_file: FileDescriptorProto, response: CodeGeneratorResponse) -> None:
    options = str(proto_file.options).strip().replace("\n", ", ").replace('"', "")
    file = response.file.add()
    file.name = proto_file.name + ".json"
    file.content = (
        json.dumps(
            {
                "package": f"{proto_file.package}",
                "filename": f"{proto_file.name}",
                "dependencies": list(proto_file.dependency),
                "message_type": [MessageToDict(i) for i in proto_file.message_type],
                "service": [MessageToDict(i) for i in proto_file.service],
                "public_dependency": list(proto_file.public_dependency),
                "enum_type": [MessageToDict(i) for i in proto_file.enum_type],
                "extension": [MessageToDict(i) for i in proto_file.extension],
                "options": dict(item.split(": ") for item in options.split(", ") if options),  # type: ignore
            },
            indent=2,
        )
        + "\r\n"
    )


def generate_pydantic_model(descriptors: Descriptors, response: CodeGeneratorResponse, config: Any) -> None:
    for name, fd in descriptors.to_generate.items():
        file = response.file.add()
        file.name = fd.name[:-6].replace("-", "_").replace(".", "/") + "_p2p.py"
        file.content = FileDescriptorProtoToCode(
            fd=fd, descriptors=descriptors, desc_template=config.desc_template
        ).content
        logger.info(f"Writing protobuf-to-pydantic code to {file.name}")


def parse_param(request: CodeGeneratorRequest) -> Any:
    param_dict = {}
    try:
        for one_param_str in request.parameter.split(","):
            k, v = one_param_str.split("=")
            param_dict[k] = v
    except Exception as e:
        logger.error(f"parse command-line error:{e}")
    else:
        if "config_path" in param_dict:
            import pathlib

            config_module_str: str = str(pathlib.Path(param_dict["config_path"]).absolute())
            cwd_str: str = str(pathlib.Path().cwd())
            print(f"Load config: {config_module_str}", file=sys.stderr)
            dir_str: str = cwd_str.split("/")[-1]
            logger.debug(f"Cwd: {cwd_str}, dir:{dir_str}")
            if config_module_str.startswith(cwd_str):
                config_module_str = config_module_str.replace(cwd_str, "")
            if config_module_str.startswith("/"):
                config_module_str = config_module_str[1:]
            if config_module_str.endswith(".py"):
                config_module_str = config_module_str[:-3]
            import importlib

            return importlib.import_module(f"{dir_str}.{config_module_str}")


def main() -> None:
    with code_generation() as (request, response):
        # TODO config handle
        generate_pydantic_model(Descriptors(request), response, parse_param(request))
        file_name_set: Set[str] = {i for i in request.file_to_generate}
        for proto_file in request.proto_file:
            if proto_file.name not in file_name_set:
                # Only process .proto files on the command line
                continue
            process_file(proto_file, response)


if __name__ == "__main__":
    main()
