from typing import TYPE_CHECKING, Any, Dict
from warnings import warn

if TYPE_CHECKING:
    from protobuf_to_pydantic.field_info_rule.types import MessageOptionTypedDict


def rule_dict_handler(
    rule_dict: Dict[str, Any], message_option_dict: "MessageOptionTypedDict", field_full_name_prefix: str
) -> None:
    """
    parse message_rule_dict data and save to message_option_dict
    """
    for key, value in rule_dict.items():
        if key == "ignored":
            message_option_dict["metadata"]["ignored"] = value
        elif key.startswith("oneof"):
            # Special support for OneOf
            field_full_name = f"{field_full_name_prefix}.{key.split(':')[1]}"
            if field_full_name not in message_option_dict["one_of"]:
                message_option_dict["one_of"][field_full_name] = {}  # type: ignore
            if "required" in value:
                message_option_dict["one_of"][field_full_name]["required"] = value["required"]
            if "optional" in value.get("oneof_extend", {}):
                message_option_dict["one_of"][field_full_name]["optional_fields"] = set(
                    value["oneof_extend"].pop("optional", [])
                )
        else:
            warn(f"Message rule not support key:{key}")
