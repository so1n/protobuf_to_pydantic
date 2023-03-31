from typing import TYPE_CHECKING, Dict, Optional

from protobuf_to_pydantic.util import gen_dict_from_desc_str

if TYPE_CHECKING:
    from protobuf_to_pydantic.contrib.proto_parser import Message, ProtoFile
    from protobuf_to_pydantic.types import DescFromOptionTypedDict

_filename_desc_dict: Dict[str, Dict[str, "DescFromOptionTypedDict"]] = {}


def _parse_message_result_dict(
    protobuf_msg: "Message",
    parse_result: "ProtoFile",
    container: Dict[str, "DescFromOptionTypedDict"],
    comment_prefix: str,
) -> None:
    message_name: str = protobuf_msg.name
    container[message_name] = {"message": {}, "one_of": {}, "nested": {}}  # type: ignore
    for field in protobuf_msg.fields:
        container[message_name]["message"][field.name] = gen_dict_from_desc_str(
            comment_prefix, field.comment.content.replace("//", "") if field.comment else ""
        )
        # parse nested message by map
        for sub_type_str in [field.type, field.key_type, field.val_type]:
            if sub_type_str in parse_result.messages:
                sub_message = parse_result.messages[sub_type_str]
            elif sub_type_str in protobuf_msg.messages:
                sub_message = protobuf_msg.messages[sub_type_str]
            else:
                continue
            if sub_message is protobuf_msg:
                continue
            _parse_message_result_dict(sub_message, parse_result, container[message_name]["nested"], comment_prefix)


def get_desc_from_proto_file(filename: str, comment_prefix: str) -> Dict[str, "DescFromOptionTypedDict"]:
    """Obtain corresponding information through protobuf file

    protobuf file name: demo.proto, message e.g:
    ```protobuf
    message UserMessage {
        string uid=1;
        int32 age=2;
        float height=3;
        SexType sex=4;
        bool is_adult=5;
        string user_name=6;
    }
    ```

    return data:
    {
        "path/demo.proto": {
            "UserMessage": {
                "uid": {}        # field info like `protobuf_to_pydantic.gen_model.MessagePaitModel`,
                "age": {}        # field info like `protobuf_to_pydantic.gen_model.MessagePaitModel`,
                "height": {}     # field info like `protobuf_to_pydantic.gen_model.MessagePaitModel`,
                "sex": {}        # field info like `protobuf_to_pydantic.gen_model.MessagePaitModel`,
                "is_adult": {}   # field info like `protobuf_to_pydantic.gen_model.MessagePaitModel`,
                "user_name": {}  # field info like `protobuf_to_pydantic.gen_model.MessagePaitModel`,
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
        raise RuntimeError("Can not parse protobuf file, please install lark")

    message_field_dict: Dict[str, "DescFromOptionTypedDict"] = {}
    _proto_file: Optional[ProtoFile] = parse_from_file(filename)
    if not _proto_file:
        # Even if there is no data, it should be cached, and it will take time to parse the protobuf file
        _filename_desc_dict[filename] = message_field_dict
        return message_field_dict

    # Currently only used protobuf file message
    proto_file: ProtoFile = _proto_file
    for _, protobuf_msg in proto_file.messages.items():
        _parse_message_result_dict(protobuf_msg, proto_file, message_field_dict, comment_prefix)

    # cache data and return
    _filename_desc_dict[filename] = message_field_dict
    return message_field_dict
