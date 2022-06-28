import re
from typing import Any, Dict, List, Optional, Tuple

_filename_desc_dict: Dict[str, Dict[str, Dict[str, str]]] = {}


def get_desc_from_pyi_file(filename: str) -> Dict[str, Dict[str, str]]:
    if filename in _filename_desc_dict:
        return _filename_desc_dict[filename]

    with open(filename, "r") as f:
        pyi_content: str = f.read()
    line_list = pyi_content.split("\n")

    _comment_model: bool = False
    _doc: str = ""
    _field_name: str = ""
    message_str_stack: List[Tuple[str, int, dict]] = []
    indent: int = 0

    global_message_field_dict: dict = {}

    for index, line in enumerate(line_list):
        if "class" in line:
            if line.endswith("google.protobuf.message.Message):"):
                match_list = re.findall(r"class (.+)\(google.protobuf.message.Message", line)
                if not match_list:
                    continue
                message_str: str = match_list[0]
                new_indent: int = line.index("class")
                if message_str_stack and message_str != message_str_stack[-1][0] and new_indent <= indent:
                    # When you encounter the same indentation of different classes,
                    # need to pop off the previous one and insert the current one
                    message_str_stack.pop()
                message_field_dict: dict = {}
                if message_str_stack:
                    parent_message_field_dict = message_str_stack[-1][2]
                    parent_message_field_dict[message_str] = message_field_dict
                else:
                    global_message_field_dict[message_str] = message_field_dict

                indent = new_indent
                message_str_stack.append((message_str, indent, message_field_dict))
            continue
        elif indent:
            if line and message_str_stack and line[indent] != " ":
                # The current class has been scanned, go back to the previous class
                message_str_stack.pop()

        if message_str_stack:
            message_str, indent, message_field_dict = message_str_stack[-1]
            line = line.strip()
            if _comment_model:
                _doc += "\n" + line

            if not _comment_model and line.startswith('"""') and not line_list[index - 1].startswith("class"):
                # start add doc
                if "def" in line_list[index - 1]:
                    _field_name = line_list[index - 1].split("(")[0].replace("def", "").strip()
                else:
                    _field_name = line_list[index - 1].split(":")[0].strip()
                _comment_model = True
                _doc = line
            if (line.endswith('"""') or line == '"""') and _comment_model:
                # end add doc
                _comment_model = False
                message_field_dict[_field_name] = _doc.replace('"""', "")

    _filename_desc_dict[filename] = global_message_field_dict
    return global_message_field_dict


def get_desc_from_proto_file(filename: str) -> dict:
    if filename in _filename_desc_dict:
        return _filename_desc_dict[filename]

    from protobuf_to_pydantic.contrib.proto_parser import ProtoFile, parse_from_file

    message_field_dict: dict = {}
    _parse_result: Optional[ProtoFile] = parse_from_file(filename)
    if not _parse_result:
        return message_field_dict
    parse_result: ProtoFile = _parse_result

    def _parse_message_result(message_result: Any, container: dict) -> None:
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
                sub_container: dict = {}
                container[message_name][sub_type_str] = sub_container
                _parse_message_result(sub_message, sub_container)

    for _, _message_result in parse_result.messages.items():
        _parse_message_result(_message_result, message_field_dict)

    _filename_desc_dict[filename] = message_field_dict
    return message_field_dict
