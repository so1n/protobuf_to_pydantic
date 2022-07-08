import logging
from typing import Any, Callable, Dict, List, Optional, Set, Type

from pydantic import validator

from protobuf_to_pydantic.grpc_types import Descriptor, FieldDescriptor, Message

_logger: logging.Logger = logging.getLogger(__name__)
_message_desc_dict: Dict[str, Dict[str, Dict[str, str]]] = {}

type_dict: Dict[str, str] = {
    FieldDescriptor.TYPE_DOUBLE: "double",
    FieldDescriptor.TYPE_FLOAT: "float",
    FieldDescriptor.TYPE_INT64: "int64",
    FieldDescriptor.TYPE_UINT64: "uint64",
    FieldDescriptor.TYPE_INT32: "int32",
    FieldDescriptor.TYPE_FIXED64: "fixed64",
    FieldDescriptor.TYPE_FIXED32: "fixed32",
    FieldDescriptor.TYPE_BOOL: "bool",
    FieldDescriptor.TYPE_STRING: "string",
    FieldDescriptor.TYPE_BYTES: "bytes",
    FieldDescriptor.TYPE_UINT32: "uint32",
    FieldDescriptor.TYPE_SFIXED32: "sfixed32",
    FieldDescriptor.TYPE_SFIXED64: "sfixed64",
    FieldDescriptor.TYPE_SINT32: "sint32",
    FieldDescriptor.TYPE_SINT64: "sint64",
}

type_not_support_dict: Dict[str, Set[str]] = {
    FieldDescriptor.TYPE_BYTES: {"pattern"},
    FieldDescriptor.TYPE_STRING: {"min_bytes", "max_bytes"},
}


def has_validate(field: Any) -> bool:
    if field.GetOptions() is None:
        return False
    for option_descriptor, option_value in field.GetOptions().ListFields():
        if option_descriptor.full_name == "validate.rules":
            return True
    return False


# flake8: noqa: C901
def option_descriptor_to_desc_dict(option_descriptor_list: list, field: Any) -> dict:
    desc_dict: dict = {}
    validator_fn_list: List[Callable[[Any], Any]] = []
    for option_descriptor in option_descriptor_list:
        for column in option_descriptor.__dir__():
            if column.startswith("_"):
                continue
            if column[0] != column[0].lower():
                continue
            try:
                if not option_descriptor.HasField(column):
                    continue
            except ValueError:
                if not getattr(option_descriptor, column):
                    continue

            if column in type_not_support_dict.get(field.type, set()):
                _logger.warning(f"P2p not support `{column}`, please reset {field.full_name} `{column}` value")
                continue

            value = getattr(option_descriptor, column)
            if column in ("ignore_empty", "defined_only"):
                _logger.warning(f"P2p not support `{column}`, please reset {field.full_name} `{column}` value")
                continue
            # elif column == "const":
            #     # const: this argument must be the same as the field's default value if present.
            #     column = "default"
            #     desc_dict["const"] = True
            elif column == "in":

                def _in_validator(v: Any) -> Any:
                    if v not in value:
                        raise ValueError(f"{field.name} not in {value}")
                    return v

                validator_fn_list.append(_in_validator)
                continue
            elif column == "not_in":

                def _in_validator(v: Any) -> Any:
                    if v in value:
                        raise ValueError(f"{field.name} in {value}")
                    return v

                validator_fn_list.append(_in_validator)
                continue
            elif column in ("len", "len_bytes"):

                def _len_validator(v: Any) -> Any:
                    if len(v) != value:
                        raise ValueError(f"{field.name} length does not equal {value}")
                    return v

                validator_fn_list.append(_len_validator)
                continue
            elif column in ("min_len", "min_bytes"):
                column = "min_length"
            elif column in ("max_len", "max_bytes"):
                column = "max_length"
            elif column == "pattern":
                column = "regex"
            elif column == "unique":
                column = "unique_items"
            elif column == "gte":
                column = "ge"
            elif column == "lte":
                column = "le"
            elif column == "prefix":

                def _prefix_validator(v: Any) -> Any:
                    if not v.startswith(value):
                        raise ValueError(f"{field.name} does not start with prefix {value}")
                    return v

                validator_fn_list.append(_prefix_validator)
                continue
            elif column == "suffix":

                def _suffix_validator(v: Any) -> Any:
                    if not v.startswith(value):
                        raise ValueError(f"{field.name} does not end with suffix {value}")
                    return v

                validator_fn_list.append(_suffix_validator)
                continue
            elif column == "contains":

                def _contain_validator(v: Any) -> Any:
                    if v not in value:
                        raise ValueError(f"{field.name} not contain {value}")
                    return v

                validator_fn_list.append(_contain_validator)
                continue
            elif column == "not_contains":

                def _contain_validator(v: Any) -> Any:
                    if v in value:
                        raise ValueError(f"{field.name} contain {value}")
                    return v

                validator_fn_list.append(_contain_validator)
                continue
            # TODO
            # support strging rule well know
            # support Repeated items
            # support MapRules
            # support TimestampRules

            desc_dict[column] = value
    if validator_fn_list:

        @validator(field.name, allow_reuse=True)
        def auto_validator_fn(cls: Any, v: Any) -> Any:
            for fn in validator_fn_list:
                v = fn(v)
            return v

        desc_dict["validator"] = auto_validator_fn
    return desc_dict


def get_desc_from_pgv(message: Type[Message]) -> dict:
    if message in _message_desc_dict:
        return _message_desc_dict[message.__name__]

    message_field_dict: dict = {}
    _message_desc_dict[message.__name__] = message_field_dict

    for option_descriptor, option_value in message.DESCRIPTOR.GetOptions().ListFields():
        if (option_descriptor.full_name == "validate.disabled" and option_value) or (
            option_descriptor.full_name == "validate.ignored" and option_value
        ):
            return message_field_dict
    for field in message.DESCRIPTOR.fields:
        if field.type not in type_dict:
            print(field.type, "ignore")
            continue
        type_name: str = type_dict[field.type]
        option_value_list: List = []
        miss_default: bool = False
        if has_validate(field) and field.message_type is None:
            for option_descriptor, option_value in field.GetOptions().ListFields():
                if option_descriptor.full_name == "validate.rules":
                    rule_message: Any = option_value.message
                    if rule_message:
                        if getattr(rule_message, "skip", None):
                            _logger.warning(f"P2p not support `skip`, please reset {field.full_name} `skip` value")
                        if getattr(rule_message, "required", None):
                            miss_default = True
                    type_value: Optional[Descriptor] = getattr(option_value, type_name, None)
                    if not type_value:
                        _logger.warning(f"Can not found {field.full_name}'s {type_name} from {option_value}")
                        continue
                    option_value_list.append(type_value)
        field_dict = option_descriptor_to_desc_dict(option_value_list, field)
        field_dict["miss_default"] = miss_default
        message_field_dict[field.name] = field_dict
        _message_desc_dict[message.__name__] = message_field_dict
    return _message_desc_dict
