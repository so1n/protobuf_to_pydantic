from typing import Dict, Type

from protobuf_to_pydantic.grpc_types import Message

from .base import MessageOptionTypedDict, ParseFromPbOption


class _ParseFromPbOption(ParseFromPbOption):
    protobuf_pkg = "validate"


def get_message_option_dict_from_message_with_pgv(message: Type[Message]) -> Dict[str, MessageOptionTypedDict]:
    return _ParseFromPbOption(message).parse()
