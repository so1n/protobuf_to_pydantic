from typing import Dict, Type

from protobuf_to_pydantic.grpc_types import Message

from .base import DescFromOptionTypedDict, ParseFromPbOption


class _ParseFromPbOption(ParseFromPbOption):
    protobuf_pkg = "validate"


def get_desc_from_pgv(message: Type[Message]) -> Dict[str, DescFromOptionTypedDict]:
    return _ParseFromPbOption(message).parse()
