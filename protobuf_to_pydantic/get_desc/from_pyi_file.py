import re
from typing import TYPE_CHECKING, Dict, List, Tuple

from protobuf_to_pydantic.util import gen_dict_from_desc_str

from .utils import one_of_message_dict_handler

if TYPE_CHECKING:
    from protobuf_to_pydantic.types import DescFromOptionTypedDict, FieldInfoTypedDict

_filename_desc_dict: Dict[str, Dict[str, "DescFromOptionTypedDict"]] = {}


def get_desc_from_pyi_file(filename: str, comment_prefix: str) -> Dict[str, "DescFromOptionTypedDict"]:
    """
    For a Protobuf message as follows:
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
    mypy-protobuf will generate the following Python code:
        class UserMessage(google.protobuf.message.Message):
            ```user info```
            DESCRIPTOR: google.protobuf.descriptor.Descriptor
            UID_FIELD_NUMBER: builtins.int
            AGE_FIELD_NUMBER: builtins.int
            HEIGHT_FIELD_NUMBER: builtins.int
            SEX_FIELD_NUMBER: builtins.int
            IS_ADULT_FIELD_NUMBER: builtins.int
            USER_NAME_FIELD_NUMBER: builtins.int
            uid: typing.Text
            ```p2p: {"miss_default": true, "example": "10086", "title": "UID", "description": "user union id"}```

            age: builtins.int
            ```p2p: {"example": 18, "title": "use age", "ge": 0}```

            height: builtins.float
            ```p2p: {"ge": 0, "le": 2.5}```

            sex: global___SexType.ValueType
            is_adult: builtins.bool
            user_name: typing.Text
            ```p2p: {"description": "user name"}
            p2p: {"default": "", "min_length": 1, "max_length": "10", "example": "so1n"}
            ```

    And this function will parse the code and generate the following data
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

    with open(filename, "r") as f:
        pyi_content: str = f.read()
    line_list = pyi_content.split("\n")

    _comment_mode: bool = False  # Whether to enable parsing comment mode
    _doc: str = ""
    _field_name: str = ""
    message_str_stack: List[Tuple[str, int, DescFromOptionTypedDict]] = []
    indent: int = 0

    global_message_field_dict: Dict[str, "DescFromOptionTypedDict"] = {}

    for index, line in enumerate(line_list):
        if "class" in line:
            if not line.endswith("google.protobuf.message.Message):"):
                continue
            match_list = re.findall(r"class (.+)\(google.protobuf.message.Message", line)
            if not match_list:
                continue
            message_str: str = match_list[0]
            new_indent: int = line.index("class")
            if message_str_stack and message_str != message_str_stack[-1][0] and new_indent <= indent:
                # When you encounter the same indentation of different classes,
                # need to pop off the previous one and insert the current one
                message_str_stack.pop()
            message_field_dict: Dict[str, FieldInfoTypedDict] = {}
            global_message_field_dict[message_str] = {
                "message": message_field_dict,
                "one_of": {},
                "nested": {},  # type: ignore
                "metadata": {},
            }
            if message_str_stack:
                parent_message_field_dict = message_str_stack[-1][2]
                parent_message_field_dict["nested"][message_str] = global_message_field_dict[message_str]

            indent = new_indent
            message_str_stack.append((message_str, indent, global_message_field_dict[message_str]))
        elif indent:
            if line and message_str_stack and line[indent] != " ":
                # The current class has been scanned, go back to the previous class
                message_str_stack.pop()

        if message_str_stack:
            message_str, indent, desc_dict = message_str_stack[-1]
            line = line.strip()
            if _comment_mode:
                _doc += "\n" + line

            if not _comment_mode and line.startswith('"""'):
                # start add doc
                if "def " in line_list[index - 1]:
                    _field_name = line_list[index - 1].split("(")[0].replace("def ", "").strip()
                else:
                    _field_name = line_list[index - 1].split(":")[0].strip()
                if line_list[index - 1].startswith("class"):
                    _field_name = ""

                _comment_mode = True
                _doc = line
            if (line.endswith('"""') or line == '"""') and _comment_mode:
                # end add doc
                _comment_mode = False
                gen_desc_dict = gen_dict_from_desc_str(comment_prefix, _doc.replace('"""', ""))
                if _field_name:
                    desc_dict["message"][_field_name] = gen_desc_dict  # type: ignore[assignment]
                else:
                    one_of_message_dict_handler(gen_desc_dict, desc_dict, f"{message_str}")
                    # for key, value in gen_desc_dict.items():
                    #     if key == "ignore":
                    #         desc_dict["metadata"]["ignore"] = value
                    #     elif key.startswith("oneof"):
                    #         # Special support for OneOf
                    #         field_full_name = f"{message_str}.{key.split(':')[1]}"
                    #         if field_full_name not in desc_dict["one_of"]:
                    #             desc_dict["one_of"][field_full_name] = {}
                    #         if "required" in value:
                    #             desc_dict["one_of"][field_full_name]["required"] = value["required"]
                    #         if "optional" in value.get("oneof_extend", {}):
                    #             desc_dict["one_of"][field_full_name]["optional_fields"] = (
                    #                 set(value["oneof_extend"].pop("optional", []))
                    #             )

    _filename_desc_dict[filename] = global_message_field_dict
    return global_message_field_dict
