import copy
from collections import deque
from typing import Any, Callable, Deque, Dict, List, Optional, Set, Tuple, Type, TypeVar
from warnings import warn

from pydantic import BaseModel, Field

from protobuf_to_pydantic import _pydantic_adapter
from protobuf_to_pydantic.plugin.field_desc_proto_to_code import FileDescriptorProtoToCode
from protobuf_to_pydantic.template import Template
from protobuf_to_pydantic.util import get_dict_from_comment

ConfigT = TypeVar("ConfigT", bound="ConfigModel")


class ProtobufTypeConfigModel(BaseModel):
    module_name: str = Field(description="Python module name")
    message_name: str = Field(description="Python message name")
    is_custom: bool = Field(
        default=False,
        description="Whether it is a custom message, if true, model config arbitrary_types_allowed = True",
    )


class SubConfigModel(BaseModel):
    module: Any
    use_root_config: bool = Field(default=False, description="If True, the root configuration will be inherited")


def default_comment_handler(
    leading_comments: str, trailing_comments: str, config_model: "ConfigModel"
) -> Tuple[dict, str, str]:
    comment_info_dict: dict = {}
    if config_model.parse_comment:
        leading_comments_list: List[str] = []
        trailing_comments_list: List[str] = []
        for container, comments in (
            (leading_comments_list, leading_comments),
            (trailing_comments_list, trailing_comments),
        ):
            for line in comments.split("\n"):
                field_dict = get_dict_from_comment(config_model.comment_prefix, line)
                if not field_dict:
                    container.append(line)
                else:
                    comment_info_dict.update(field_dict)
        leading_comments = "\n".join(leading_comments_list)
        trailing_comments = "\n".join(trailing_comments_list)
    return comment_info_dict, leading_comments, trailing_comments


class ConfigModel(BaseModel):
    # output code config
    customer_import_set: Set[str] = Field(default_factory=set, description="customer import code set")
    customer_deque: Deque = Field(default_factory=deque, description="customer file content")
    code_indent: int = Field(default=4, description="Code indent")
    module_path: str = Field(default="", description="protobuf project path")
    pyproject_file_path: str = Field(
        default="",
        description="pyproject file path, In general, pyproject.toml of the project can be found automatically",
    )
    file_name_suffix: str = Field(
        default="_p2p",
        description=(
            "The file name suffix, but not the file type. "
            "For example, if the name of the proto file is `book`, the generated file name is `book_p2p.py`"
        ),
    )

    # gen message config
    local_dict: dict = Field(default_factory=dict, description="Dict for local variables")
    template: Type[Template] = Field(default=Template, description="Support more templates by customizing 'Template'")
    comment_handler: Optional[Callable[[str, str, "ConfigModel"], Tuple[dict, str, str]]] = Field(
        default=default_comment_handler,
        description="Customize the comment parsing function. if None, not parse the comment",
    )
    comment_prefix: str = Field(default="p2p", description="Comment prefix")
    parse_comment: bool = Field(
        default=True,
        description="If true, the annotation is parsed and the validation rule data is extracted from the annotation",
    )
    ignore_pkg_list: List[str] = Field(
        default_factory=lambda: ["validate", "p2p_validate"], description="Ignore the specified pkg file"
    )
    base_model_class: Type[BaseModel] = Field(default=BaseModel, description="Inherited base pydantic model")
    all_field_set_optional: bool = Field(
        default=False,
        description="If true, all fields become optional, see: https://github.com/so1n/protobuf_to_pydantic/issues/60",
    )

    # other config
    file_descriptor_proto_to_code: Type[FileDescriptorProtoToCode] = Field(
        default=FileDescriptorProtoToCode,
        description="If you have modified the resolution rules, then you can customize FileDescriptorProtoToCode",
    )
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
    pkg_config: Dict[str, "ConfigModel"] = Field(
        default_factory=dict, description="Customize the configuration of different pkgs"
    )
    template_instance: Template = Field(
        default_factory=lambda: Template({}, ""),
        description="This variable does not support configuration and will be overwritten even if configured",
    )

    class Config:
        arbitrary_types_allowed = True

    @_pydantic_adapter.model_validator(mode="after")
    def after_init(cls, values: Any) -> Any:
        if _pydantic_adapter.is_v1:
            # values: Dict[str, Any]
            values["template_instance"] = values["template"](values["local_dict"], values["comment_prefix"])
            return values
        else:
            # values: "ConfigModel"
            values.template_instance = values.template(values.local_dict, values.comment_prefix)
        return values

    @_pydantic_adapter.model_validator(mode="before")
    def before_init(cls, values: Any) -> Any:
        def _validator(_values: Any) -> dict:
            if not isinstance(_values, SubConfigModel):
                raise ValueError("values must be a SubConfigModel")
            if _values.use_root_config:
                root_dict = {k: v for k, v in values.items() if k != "pkg_config"}
            else:
                root_dict = None
            return get_config_by_module(_values.module, ConfigModel, root_dict).dict()

        if "pkg_config" in values:
            values["pkg_config"] = {k: _validator(v) for k, v in values.get("pkg_config", {}).items()}
        if "parse_comment" in values or "comment_handler" in values:
            warning_msg = (
                "The 'parse_comment' and 'comment_handler' configuration items are deprecated, "
                "please use the 'comment_handler' configuration item instead"
            )
            warn(warning_msg, DeprecationWarning)
        return values


def get_config_by_module(module: Any, config_class: Type[ConfigT], root_dict: Optional[dict] = None) -> ConfigT:
    if root_dict:
        param_dict: dict = copy.deepcopy(root_dict)
    else:
        param_dict = {}
    for key in _pydantic_adapter.model_fields(config_class).keys():
        if not hasattr(module, key):
            continue
        param_dict[key] = getattr(module, key)
    return config_class(**param_dict)
