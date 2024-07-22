from collections import deque
from typing import Any, Deque, Dict, List, Set, Type, TypeVar

from pydantic import BaseModel, Field

from protobuf_to_pydantic import _pydantic_adapter
from protobuf_to_pydantic.desc_template import DescTemplate
from protobuf_to_pydantic.plugin.field_desc_proto_to_code import FileDescriptorProtoToCode

ConfigT = TypeVar("ConfigT", bound="ConfigModel")


class ProtobufTypeConfigModel(BaseModel):
    module_name: str = Field(description="Python module name")
    message_name: str = Field(description="Python message name")
    is_custom: bool = Field(
        default=False,
        description="Whether it is a custom message, if true, model config arbitrary_types_allowed = True",
    )


class ConfigModel(BaseModel):
    local_dict: dict = Field(default_factory=dict, description="Dict for local variables")
    desc_template: Type[DescTemplate] = Field(
        default=DescTemplate, description="Support more templates by customizing 'Desc Template'"
    )
    comment_prefix: str = Field(default="p2p", description="Comment prefix")
    parse_comment: bool = Field(
        default=True,
        description="If true, the annotation is parsed and the validation rule data is extracted from the annotation",
    )
    customer_import_set: Set[str] = Field(default_factory=set, description="customer import code set")
    customer_deque: Deque = Field(default_factory=deque)
    module_path: str = Field(default="")
    pyproject_file_path: str = Field(
        default="",
        description="pyproject file path, In general, pyproject.toml of the project can be found automatically",
    )
    code_indent: int = Field(default=4, description="Code indent")
    ignore_pkg_list: List[str] = Field(
        default_factory=lambda: ["validate", "p2p_validate"], description="Ignore the specified pkg file"
    )
    base_model_class: Type[BaseModel] = Field(default=BaseModel)
    file_name_suffix: str = Field(
        default="_p2p",
        description=(
            "The file name suffix, but not the file type. "
            "For example, if the name of the proto file is `book`, the generated file name is `book_p2p.py`"
        ),
    )
    file_descriptor_proto_to_code: Type[FileDescriptorProtoToCode] = Field(default=FileDescriptorProtoToCode)
    protobuf_type_config: Dict[str, ProtobufTypeConfigModel] = Field(
        default_factory=dict,
        description="""
        Fixed the issue that some protobuf message names are inconsistent with Python module names

        use template: {"{protobuf message name}": ("{python module name}", "{python message name}")}

        The configuration of the protobuf type, for example protobuf:
        ```protobuf
        syntax = "proto3";

        import "google/protobuf/wrappers.proto";

        message CalculatedValue {
            google.protobuf.DoubleValue myValue = 1;
        }
        ```
        In order for `protobuf_to_pydantic` to find google.protobuf.DoubleValue module - google/protobuf/wrappers.proto,
        need to enter the configuration information:
        ```Python
        {
            "google.protobuf.DoubleValue": ProtobufTypeConfigModel(
                module_name="builtins",
                message_name="float",
                is_custom=False
            ),
        }
        ```
        """,
    )
    desc_template_instance: DescTemplate = Field(
        default_factory=lambda: DescTemplate({}, ""),
        description="This variable does not support configuration and will be overwritten even if configured",
    )

    class Config:
        arbitrary_types_allowed = True

    @_pydantic_adapter.model_validator(mode="after")
    def after_init(cls, values: Any) -> Any:
        if _pydantic_adapter.is_v1:
            # values: Dict[str, Any]
            values["desc_template_instance"] = values["desc_template"](values["local_dict"], values["comment_prefix"])
            return values
        else:
            # values: "ConfigModel"
            values.desc_template_instance = values.desc_template(values.local_dict, values.comment_prefix)


def get_config_by_module(module: Any, config_class: Type[ConfigT]) -> ConfigT:
    param_dict: dict = {}
    for key in _pydantic_adapter.model_fields(config_class).keys():
        if not hasattr(module, key):
            continue
        param_dict[key] = getattr(module, key)
    return config_class(**param_dict)
