from importlib import import_module
from typing import Any, Generator, cast

import pytest
from google.protobuf import __version__
from pydantic import ValidationError

from protobuf_to_pydantic import msg_to_pydantic_model
from protobuf_to_pydantic._pydantic_adapter import is_v1
from protobuf_to_pydantic.gen_model import clear_create_model_cache
from protobuf_to_pydantic.get_message_option.from_message_option import base as message_option_base
from tests.base.base_p2p_validate import local_dict

if __version__ > "4.0.0":
    proto_module = "example.proto_pydanticv1" if is_v1 else "example.proto_pydanticv2"
else:
    proto_module = "example.proto_3_20_pydanticv1" if is_v1 else "example.proto_3_20_pydanticv2"

all_feidl_set_optional_demo_pb2 = cast(
    Any,
    import_module(f"{proto_module}.example.example_proto.demo.all_feidl_set_optional_demo_pb2"),
)
p2p_demo_pb2 = cast(
    Any,
    import_module(f"{proto_module}.example.example_proto.p2p_validate.demo_pb2"),
)
main_pkg_pb2 = cast(
    Any,
    import_module(f"{proto_module}.example.example_proto.test_ignore.main_pkg_pb2"),
)


@pytest.fixture(autouse=True)
def clear_runtime_generation_caches() -> Generator[None, None, None]:
    clear_create_model_cache()
    message_option_base._global_message_option_dict.clear()
    yield
    clear_create_model_cache()
    message_option_base._global_message_option_dict.clear()


def test_proto_file_comments_resolve_fields_with_multi_part_package_name() -> None:
    model = msg_to_pydantic_model(main_pkg_pb2.MainMessage, parse_msg_desc_method=".")

    with pytest.raises(ValidationError):
        model()

    model(normal_field="normal")


def test_p2p_message_option_cache_is_isolated_by_proto_package() -> None:
    msg_to_pydantic_model(
        all_feidl_set_optional_demo_pb2.OptionalMessage,
        local_dict=local_dict,
        all_field_set_optional=True,
    )

    model = msg_to_pydantic_model(p2p_demo_pb2.OptionalMessage, local_dict=local_dict)

    with pytest.raises(ValidationError):
        model()
