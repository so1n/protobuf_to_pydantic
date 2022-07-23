from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from protobuf_to_pydantic.contrib.proto_parser import ProtoFile

_filename_desc_dict: Dict[str, Dict[str, Dict[str, str]]] = {}


def _parse_message_result(message_result: Any, container: dict, parse_result: "ProtoFile") -> None:
    message_name: str = message_result.name
    container[message_name] = {}
    for field in message_result.fields:
        container[message_name][field.name] = field.comment.content.replace("//", "") if field.comment else ""
        for sub_type_str in [field.type, field.key_type, field.val_type]:
            if sub_type_str in parse_result.messages:
                sub_message = parse_result.messages[sub_type_str]
            elif sub_type_str in message_result.messages:
                sub_message = message_result.messages[sub_type_str]
            else:
                continue
            _parse_message_result(sub_message, container[message_name], parse_result)


def get_desc_from_proto_file(filename: str) -> dict:
    if filename in _filename_desc_dict:
        return _filename_desc_dict[filename]

    from protobuf_to_pydantic.contrib.proto_parser import ProtoFile, parse_from_file

    message_field_dict: dict = {}
    _parse_result: Optional[ProtoFile] = parse_from_file(filename)
    if not _parse_result:
        _filename_desc_dict[filename] = message_field_dict
        return message_field_dict

    parse_result: ProtoFile = _parse_result
    for _, _message_result in parse_result.messages.items():
        _parse_message_result(_message_result, message_field_dict, parse_result)

    _filename_desc_dict[filename] = message_field_dict
    return message_field_dict
