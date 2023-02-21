from typing import Dict, Type

from protobuf_to_pydantic.grpc_types import Message

from .base import DescFromOptionTypedDict, ParseFromPbOption


class _ParseFromPbOption(ParseFromPbOption):
    protobuf_pkg = "p2p_validate"


def get_desc_from_p2p(message: Type[Message]) -> Dict[str, DescFromOptionTypedDict]:
    """Parse data through Message and return info dict
    Note: The returned dict includes the data of one of
    """
    return _ParseFromPbOption(message).parse()
