from typing import Type

from protobuf_to_pydantic.grpc_types import Message

from .base import ParseFromPbOption


class _ParseFromPbOption(ParseFromPbOption):
    protobuf_pkg = "p2p_validate"


def get_desc_from_p2p(message: Type[Message]) -> dict:
    return _ParseFromPbOption(message).parse()
