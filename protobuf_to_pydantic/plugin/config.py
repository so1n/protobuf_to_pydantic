from collections import deque
from typing import Any, Deque, Dict, List, Set, Type

from pydantic import BaseModel, Field, root_validator

from protobuf_to_pydantic.gen_model import DescTemplate
from protobuf_to_pydantic.plugin.field_desc_proto_to_code import FileDescriptorProtoToCode


class ConfigModel(BaseModel):
    local_dict: dict = Field(default_factory=dict)
    desc_template: Type[DescTemplate] = Field(default=DescTemplate)
    comment_prefix: str = Field(default="p2p")
    customer_import_set: Set[str] = Field(default_factory=set)
    customer_deque: Deque = Field(default_factory=deque)
    module_path: str = Field(default="")
    code_indent: int = Field(default=4)
    ignore_pkg_list: List[str] = Field(default_factory=list)
    base_model_class: Type[BaseModel] = Field(default=BaseModel)
    file_descriptor_proto_to_code: Type[FileDescriptorProtoToCode] = Field(default=FileDescriptorProtoToCode)

    desc_template_instance: DescTemplate = Field(default_factory=lambda: DescTemplate({}, ""))

    class Config:
        arbitrary_types_allowed = True

    @root_validator
    def after_init(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values["desc_template_instance"] = values["desc_template"](values["local_dict"], values["comment_prefix"])
        return values


def get_config_by_module(module: Any) -> ConfigModel:
    param_dict: dict = {}
    for key in ConfigModel.__fields__.keys():
        if not hasattr(module, key):
            continue
        param_dict[key] = getattr(module, key)
    return ConfigModel(**param_dict)
