from collections import deque
from typing import Any, Deque, Dict, List, Set, Type, TypeVar

from pydantic import BaseModel, Field, root_validator

from protobuf_to_pydantic.gen_model import DescTemplate
from protobuf_to_pydantic.plugin.field_desc_proto_to_code import FileDescriptorProtoToCode

ConfigT = TypeVar("ConfigT", bound="ConfigModel")


class ConfigModel(BaseModel):
    local_dict: dict = Field(default_factory=dict, description="Dict for local variables")
    desc_template: Type[DescTemplate] = Field(
        default=DescTemplate, description="Support more templates by customizing 'Desc Template'"
    )
    comment_prefix: str = Field(default="p2p", description="Comment prefix")
    customer_import_set: Set[str] = Field(default_factory=set, description="customer import code set")
    customer_deque: Deque = Field(default_factory=deque)
    module_path: str = Field(default="")
    pyproject_file_path: str = Field(
        default="",
        description="pyproject file path, In general, pyproject.toml of the project can be found automatically",
    )
    code_indent: int = Field(default=4, description="Code indent")
    ignore_pkg_list: List[str] = Field(default_factory=list, description="Ignore package list")
    base_model_class: Type[BaseModel] = Field(default=BaseModel)
    file_name_suffix: str = Field(
        default="_p2p",
        description=(
            "The file name suffix, but not the file type. "
            "For example, if the name of the proto file is `book`, the generated file name is `book_p2p.py`"
        ),
    )
    file_descriptor_proto_to_code: Type[FileDescriptorProtoToCode] = Field(default=FileDescriptorProtoToCode)

    desc_template_instance: DescTemplate = Field(
        default_factory=lambda: DescTemplate({}, ""),
        description="This variable does not support configuration and will be overwritten even if configured",
    )

    class Config:
        arbitrary_types_allowed = True

    @root_validator
    def after_init(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values["desc_template_instance"] = values["desc_template"](values["local_dict"], values["comment_prefix"])
        return values


def get_config_by_module(module: Any, config_class: Type[ConfigT]) -> ConfigT:
    param_dict: dict = {}
    for key in config_class.__fields__.keys():
        if not hasattr(module, key):
            continue
        param_dict[key] = getattr(module, key)
    return config_class(**param_dict)
