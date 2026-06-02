from protobuf_to_pydantic.plugin.config import ConfigModel
from protobuf_to_pydantic.template import Template


def test_config_model_builds_template_instance() -> None:
    config = ConfigModel(local_dict={"demo": object()}, comment_prefix="custom")

    assert isinstance(config.template_instance, Template)
    assert config.template_instance._comment_prefix == "custom"
