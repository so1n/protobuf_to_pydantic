import re
from typing import Dict, List, Tuple

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


def get_desc_from_proto_file(filename: str) -> Dict[str, Dict[str, str]]:
    if filename in _filename_desc_dict:
        return _filename_desc_dict[filename]

    with open(filename, "r") as f:
        protobuf_content: str = f.read()
    message_stack: List[str] = []
    message_field_dict: Dict[str, Dict[str, str]] = {}
    _field: str = ""
    _doc: str = ""
    _comment_model: bool = False

    for line in protobuf_content.split("\n"):
        _comment_model = False
        line_list: List[str] = line.split()
        for index, column in enumerate(line_list):
            if _comment_model:
                _doc += column + " "
                continue

            if column == "message" and line_list[index + 2] == "{":
                # message parse start
                message_stack.append(line_list[index + 1])
                continue
            if message_stack:
                if column == "}":
                    # message parse end
                    message_stack.pop()
                elif column == "//":
                    # comment start
                    _comment_model = True
                    _doc += "\n"
                elif column == "=":
                    # get field name
                    _field = line_list[index - 1]
                elif column[-1] == ";":
                    # field parse end
                    if _doc:
                        message_str: str = message_stack[-1]
                        if message_str not in message_field_dict:
                            message_field_dict[message_str] = {}

                        message_field_dict[message_str][_field] = _doc
                    _field = ""
                    _doc = ""
    _filename_desc_dict[filename] = message_field_dict
    return message_field_dict
