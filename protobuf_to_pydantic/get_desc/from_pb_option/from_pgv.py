from typing import Type

from protobuf_to_pydantic.grpc_types import Message

from .base import ParseFromPbOption


class _ParseFromPbOption(ParseFromPbOption):
    protobuf_pkg = "validate"


def get_desc_from_pgv(message: Type[Message]) -> dict:
    return _ParseFromPbOption(message).parse()
