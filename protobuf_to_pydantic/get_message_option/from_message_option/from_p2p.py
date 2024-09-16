from typing import Dict, Type

from protobuf_to_pydantic.grpc_types import Message

from .base import MessageOptionTypedDict, ParseFromPbOption


class _ParseFromPbOption(ParseFromPbOption):
    protobuf_pkg = "p2p_validate"


def get_message_option_dict_from_message_with_p2p(message: Type[Message]) -> Dict[str, MessageOptionTypedDict]:
    return _ParseFromPbOption(message).parse()
