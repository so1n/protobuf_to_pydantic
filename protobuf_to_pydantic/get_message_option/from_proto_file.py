from typing import TYPE_CHECKING, Dict, Optional

from protobuf_to_pydantic.util import get_dict_from_comment

from .utils import rule_dict_handler

if TYPE_CHECKING:
    from protobuf_to_pydantic.contrib.proto_parser import Message, ProtoFile
    from protobuf_to_pydantic.field_info_rule.types import MessageOptionTypedDict

_filename_desc_dict: Dict[str, Dict[str, "MessageOptionTypedDict"]] = {}


def _protobuf_msg_handler(
    protobuf_msg: "Message",
    proto_file: "ProtoFile",
    container: Dict[str, "MessageOptionTypedDict"],
    comment_prefix: str,
    msg_cache: Dict[str, "MessageOptionTypedDict"],
) -> None:
    message_name: str = protobuf_msg.name
    if message_name in msg_cache:
        return
    new_container: "MessageOptionTypedDict" = {"message": {}, "one_of": {}, "nested": {}, "metadata": {}}
    container[message_name] = new_container
    msg_cache[message_name] = new_container

    if protobuf_msg.comment:
        message_dict = get_dict_from_comment(  # type: ignore[assignment]
            comment_prefix, protobuf_msg.comment.content.replace("//", "")
        )
        rule_dict_handler(message_dict, new_container, f"{proto_file.package}.{message_name}")

    for field in protobuf_msg.fields:
        new_container["message"][field.name] = get_dict_from_comment(  # type: ignore[assignment]
            comment_prefix, field.comment.content.replace("//", "") if field.comment else ""
        )
        # parse nested message by map
        for sub_type_str in [field.type, field.key_type, field.val_type]:
            if sub_type_str in proto_file.messages:
                sub_message = proto_file.messages[sub_type_str]
            elif sub_type_str in protobuf_msg.messages:
                sub_message = protobuf_msg.messages[sub_type_str]
            else:
                continue
            if sub_message is protobuf_msg:
                continue
            _protobuf_msg_handler(sub_message, proto_file, new_container["nested"], comment_prefix, msg_cache)


def get_message_option_dict_from_proto_file(filename: str, comment_prefix: str) -> Dict[str, "MessageOptionTypedDict"]:
    """Obtain corresponding information through protobuf file

    protobuf file name: demo.proto, message e.g:
    ```protobuf
    message UserMessage {
      // p2p: {"required": true, "example": "10086", "title": "UID", "description": "user union id"}
      string uid=1;
      // p2p: {"example": 18, "title": "use age", "ge": 0}
      int32 age=2;
      // p2p: {"ge": 0, "le": 2.5}
      float height=3;
      SexType sex=4;
      single.DemoEnum demo =6;
      bool is_adult=7;
      // p2p: {"description": "user name"}
      // p2p: {"default": "", "min_length": 1, "max_length": "10", "example": "so1n"}
      string user_name=8;
    }
    ```

    return data:
    {
        "path/demo.pyi": {
            "UserMessage": {
                # field info like `protobuf_to_pydantic.gen_model.FieldParamModel`,
                "uid": {"miss_default": True, "example": "10086", "title": "UID", "description": "user union id"},
                "age": {"example": 18, "title": "use age", "ge": 0},
                "height": {"ge": 0, "le": 2.5},
                "sex": {},
                "is_adult": {},
                "user_name": {
                    "description": "user name", "default": "", "min_length": 1, "max_length": "10", "example": "so1n"
                },
            }
        }
    }
    """
    if filename in _filename_desc_dict:
        # get protobuf message info by cache
        return _filename_desc_dict[filename]

    try:
        from protobuf_to_pydantic.contrib.proto_parser import ProtoFile, parse_from_file
    except ImportError:
        raise ImportError("Can not parse protobuf file, please install lark")

    message_field_dict: Dict[str, "MessageOptionTypedDict"] = {}
    _proto_file: Optional[ProtoFile] = parse_from_file(filename)
    if _proto_file:
        # Currently only used protobuf file message
        for _, protobuf_msg in _proto_file.messages.items():
            msg_cache: Dict[str, "MessageOptionTypedDict"] = {}
            _protobuf_msg_handler(protobuf_msg, _proto_file, message_field_dict, comment_prefix, msg_cache)
    # cache data and return
    _filename_desc_dict[filename] = message_field_dict
    return message_field_dict
