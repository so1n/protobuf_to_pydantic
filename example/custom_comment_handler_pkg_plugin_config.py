from typing import TYPE_CHECKING, List, Tuple

from protobuf_to_pydantic.util import get_dict_from_comment

if TYPE_CHECKING:
    from protobuf_to_pydantic.plugin.config import ConfigModel


def comment_handler(
    leading_comments: str,
    trailing_comments: str,
    config_model: "ConfigModel",
) -> Tuple[dict, str, str]:
    comment_info_dict: dict = {}
    leading_comments_list: List[str] = []
    trailing_comments_list: List[str] = []
    for container, comments in (
        (leading_comments_list, leading_comments),
        (trailing_comments_list, trailing_comments),
    ):
        for line in comments.split("\n"):
            field_dict = get_dict_from_comment("aha", line)
            if not field_dict:
                if line.startswith("#"):
                    line = line[1:]
                line = line.strip()
                if "description" not in comment_info_dict:
                    comment_info_dict["description"] = ""
                comment_info_dict["description"] += line
            else:
                comment_info_dict.update(field_dict)
    leading_comments = "\n".join(leading_comments_list)
    trailing_comments = "\n".join(trailing_comments_list)
    return comment_info_dict, leading_comments, trailing_comments
