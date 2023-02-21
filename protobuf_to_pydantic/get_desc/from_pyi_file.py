import re
from typing import TYPE_CHECKING, Dict, List, Tuple

from protobuf_to_pydantic.util import gen_dict_from_desc_str

if TYPE_CHECKING:
    from protobuf_to_pydantic.types import DescFromOptionTypedDict, FieldInfoTypedDict

_filename_desc_dict: Dict[str, Dict[str, "DescFromOptionTypedDict"]] = {}


def get_desc_from_pyi_file(filename: str, comment_prefix: str) -> Dict[str, "DescFromOptionTypedDict"]:
    """
    For a Protobuf message as follows:
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

    with open(filename, "r") as f:
        pyi_content: str = f.read()
    line_list = pyi_content.split("\n")

    _comment_model: bool = False  # Whether to enable parsing comment mode
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
                desc_dict["message"][_field_name] = gen_dict_from_desc_str(comment_prefix, _doc.replace('"""', ""))

    _filename_desc_dict[filename] = global_message_field_dict
    return global_message_field_dict
