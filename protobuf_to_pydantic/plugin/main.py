#!/usr/bin/env python
import json
import logging
import sys
from typing import Set

from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest, CodeGeneratorResponse  # type: ignore
from google.protobuf.descriptor_pb2 import (  # type: ignore
    DescriptorProto,
    EnumDescriptorProto,
    FieldDescriptorProto,
    FileDescriptorProto,
)
from google.protobuf.json_format import MessageToDict  # type: ignore
from mypy_protobuf.main import Descriptors, code_generation

from protobuf_to_pydantic.plugin.config import Config, get_config_by_module
from protobuf_to_pydantic.plugin.field_desc_proto_to_code import FileDescriptorProtoToCode

# If want to parse option, need to import the corresponding file
#   see details:https://stackoverflow.com/a/59301849
from protobuf_to_pydantic.protos import p2p_validate_pb2  # isort:skip
from protobuf_to_pydantic.protos import validate_pb2  # isort:skip


logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s", datefmt="%y-%m-%d %H:%M:%S", level=logging.INFO)


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


def generate_pydantic_model(descriptors: Descriptors, response: CodeGeneratorResponse, config: Config) -> None:
    for name, fd in descriptors.to_generate.items():
        if fd.package in config.ignore_pkg_list:
            continue
        file = response.file.add()
        file.name = fd.name[:-6].replace("-", "_").replace(".", "/") + "_p2p.py"
        file.content = FileDescriptorProtoToCode(fd=fd, descriptors=descriptors, config=config).content
        logger.info(f"Writing protobuf-to-pydantic code to {file.name}")


def parse_param(request: CodeGeneratorRequest) -> Config:
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

            return get_config_by_module(importlib.import_module(f"{dir_str}.{config_module_str}"))
    return Config()


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
