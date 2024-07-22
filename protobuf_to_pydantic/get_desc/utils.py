from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from protobuf_to_pydantic.types import DescFromOptionTypedDict


def one_of_message_dict_handler(
    raw_message_dict: dict, desc_from_option_dict: "DescFromOptionTypedDict", full_name_prefix: str
) -> None:
    for key, value in raw_message_dict.items():
        if key == "ignored":
            desc_from_option_dict["metadata"]["ignored"] = value
        elif key.startswith("oneof"):
            # Special support for OneOf
            field_full_name = f"{full_name_prefix}.{key.split(':')[1]}"
            if field_full_name not in desc_from_option_dict["one_of"]:
                desc_from_option_dict["one_of"][field_full_name] = {}  # type: ignore
            if "required" in value:
                desc_from_option_dict["one_of"][field_full_name]["required"] = value["required"]
            if "optional" in value.get("oneof_extend", {}):
                desc_from_option_dict["one_of"][field_full_name]["optional_fields"] = set(
                    value["oneof_extend"].pop("optional", [])
                )
