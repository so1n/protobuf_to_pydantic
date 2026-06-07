from typing import Dict

from protobuf_to_pydantic.grpc_types import FileDescriptorProto
from protobuf_to_pydantic.plugin.config import ConfigModel
from protobuf_to_pydantic.plugin.field_desc_proto_to_code import FileDescriptorProtoToCode
from protobuf_to_pydantic.template import Template


class _Descriptors:
    messages: Dict[str, object] = {}
    message_to_fd: Dict[str, object] = {}


def _plugin_code_by_config(config: ConfigModel) -> str:
    fd = FileDescriptorProto(name="example/example.proto", package="example", syntax="proto3")
    enum = fd.enum_type.add()
    enum.name = "State"
    inactive = enum.value.add()
    inactive.name = "INACTIVE"
    inactive.number = 0
    active = enum.value.add()
    active.name = "ACTIVE"
    active.number = 1

    return FileDescriptorProtoToCode(fd=fd, descriptors=_Descriptors(), config=config).content


def test_config_model_builds_template_instance() -> None:
    config = ConfigModel(local_dict={"demo": object()}, comment_prefix="custom")

    assert isinstance(config.template_instance, Template)
    assert config.template_instance._comment_prefix == "custom"


def test_enum_name_value_desc_disabled_by_default_in_plugin_mode() -> None:
    content = _plugin_code_by_config(ConfigModel())

    assert "Enumeration State:" not in content
    assert "- INACTIVE = 0" not in content
    assert "- ACTIVE = 1" not in content


def test_enum_name_value_desc_can_be_enabled_in_plugin_mode() -> None:
    content = _plugin_code_by_config(ConfigModel(enable_enum_name_value_desc=True))

    assert "Enumeration State:" in content
    assert "- INACTIVE = 0" in content
    assert "- ACTIVE = 1" in content
