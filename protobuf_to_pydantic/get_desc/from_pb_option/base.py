import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, Set, Type

from protobuf_to_pydantic.customer_con_type import (
    conbytes,
    confloat,
    conint,
    conlist,
    constr,
    contimedelta,
    contimestamp,
    validator,
)
from protobuf_to_pydantic.customer_validator import validate_validator_dict
from protobuf_to_pydantic.grpc_types import Descriptor, FieldDescriptor, Message
from protobuf_to_pydantic.util import replace_protobuf_type_to_python_type

from .types import column_pydantic_type_dict

_logger: logging.Logger = logging.getLogger(__name__)

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
    FieldDescriptor.TYPE_ENUM: "enum",
    FieldDescriptor.TYPE_SFIXED32: "sfixed32",
    FieldDescriptor.TYPE_SFIXED64: "sfixed64",
    FieldDescriptor.TYPE_SINT32: "sint32",
    FieldDescriptor.TYPE_SINT64: "sint64",
}

type_not_support_dict: Dict[str, Set[str]] = {
    FieldDescriptor.TYPE_BYTES: {"pattern"},
    FieldDescriptor.TYPE_STRING: {"min_bytes", "max_bytes", "well_known_regex", "strict"},
    "Any": {"ignore_empty", "defined_only", "no_sparse"},
}

column_pydantic_dict: Dict[str, str] = {
    "min_len": "min_length",
    "min_bytes": "min_length",
    "max_len": "max_length",
    "max_bytes": "max_length",
    "pattern": "regex",
    "unique": "unique_items",
    "gte": "ge",
    "lte": "le",
    "len_bytes": "len",
    "required": "miss_default",
}


def _has_field(column: str, message: Message) -> bool:
    if column.startswith("_"):
        return False
    if getattr(Message, column, None):
        return False
    try:
        if not message.HasField(column):
            return False
    except ValueError:
        if not getattr(message, column, None) or column[0].lower() != column[0]:
            return False
    return True


def get_con_type_func_from_type_name(type_name: str) -> Optional[Callable]:
    if type_name == "string":
        return constr
    elif "double" in type_name or "float" in type_name:
        return confloat
    elif "int" in type_name:
        return conint
    elif type_name == "duration":
        return contimedelta
    elif type_name == "timestamp":
        return contimestamp
    elif type_name == "bytes":
        return conbytes
    else:
        return None


def option_descriptor_to_desc_dict(option_descriptor: Descriptor, field: Any, desc_dict: dict, type_name: str) -> None:

    for column in option_descriptor.__dir__():
        # Removing internal methods
        if not _has_field(column, option_descriptor):  # type: ignore
            continue

        # Exclude unsupported fields
        if column in type_not_support_dict.get(field.type, type_not_support_dict["Any"]):
            _logger.warning(f"{__name__} not support `{column}`, please reset {field.full_name} `{column}` value")
            continue

        value = getattr(option_descriptor, column)
        if column in column_pydantic_dict:
            # Field Conversion
            column = column_pydantic_dict[column]

        if type_name in ("duration", "any", "timestamp", "map") and column in (
            "lt",
            "le",
            "gt",
            "ge",
            "const",
            "in",
            "not_in",
            "lt_now",
            "gt_now",
            "within",
            "min_pairs",
            "max_pairs",
        ):
            # Types of priority treatment for special cases
            if "validator" not in desc_dict:
                desc_dict["validator"] = {}
            desc_dict["extra"][f"{type_name}_{column}"] = replace_protobuf_type_to_python_type(value)
            desc_dict["validator"][f"{field.name}_{type_name}_{column}_validator"] = validator(
                field.name, allow_reuse=True
            )(validate_validator_dict[f"{type_name}_{column}_validator"])
            continue
        elif column in ("in", "not_in", "len", "prefix", "suffix", "contains", "not_contains"):
            # Compatible with PGV attributes that are not supported by pydantic
            if "validator" not in desc_dict:
                desc_dict["validator"] = {}
            desc_dict["extra"][column] = replace_protobuf_type_to_python_type(value)
            desc_dict["validator"][f"{field.name}_{column}_validator"] = validator(field.name, allow_reuse=True)(
                validate_validator_dict[f"{column}_validator"]
            )
            continue
        elif column in column_pydantic_type_dict:
            desc_dict["type"] = column_pydantic_type_dict[column]
            continue
        elif column in ("keys", "values"):
            type_name = value.ListFields()[0][0].full_name.split(".")[-1]
            con_type = get_con_type_func_from_type_name(type_name)
            if not con_type:
                # TODO nested message
                _logger.warning(f"{__name__} not support sub type `{type_name}`, please reset {field.full_name}")
                continue
            sub_dict: dict = {"extra": {}}
            option_descriptor_to_desc_dict(getattr(value, type_name), field, sub_dict, type_name)
            if "map_type" not in desc_dict:
                desc_dict["map_type"] = {}
            con_type_param_dict: dict = {}
            for _key in inspect.signature(con_type).parameters.keys():
                if sub_dict.get(_key, None) is not None:
                    con_type_param_dict[_key] = sub_dict[_key]
                elif "extra" in sub_dict:
                    if sub_dict["extra"].get(_key, None) is not None:
                        con_type_param_dict[_key] = sub_dict["extra"][_key]

            desc_dict["map_type"][column] = con_type(**con_type_param_dict)
            continue
        elif column == "items":
            type_name = value.ListFields()[0][0].full_name.split(".")[-1]
            con_type = get_con_type_func_from_type_name(type_name)
            if not con_type:
                # TODO nested message
                _logger.warning(f"{__name__} not support sub type `{type_name}`, please reset {field.full_name}")
                desc_dict["type"] = List
                continue
            sub_dict = {"extra": {}, "type": con_type}
            option_descriptor_to_desc_dict(getattr(value, type_name), field, sub_dict, type_name)
            desc_dict["type"] = conlist
            desc_dict["sub"] = sub_dict
        desc_dict[column] = value


_global_desc_dict: Dict[str, Dict[str, Any]] = {}


class ParseFromPbOption(object):
    protobuf_pkg: str

    def __init__(self, message: Type[Message]):
        self.message = message
        self._msg_desc_dict: Dict[str, Any] = {}
        if self.protobuf_pkg not in _global_desc_dict:
            _global_desc_dict[self.protobuf_pkg] = self._msg_desc_dict
        else:
            self._msg_desc_dict = _global_desc_dict[self.protobuf_pkg]

    def parse(self) -> Dict[str, Any]:
        descriptor: Descriptor = self.message.DESCRIPTOR
        if descriptor.name in self._msg_desc_dict:
            return self._msg_desc_dict

        self._msg_desc_dict[descriptor.name] = self.get_desc_from_options(descriptor)
        return self._msg_desc_dict

    def get_desc_from_options(self, descriptor: Descriptor) -> dict:
        if descriptor.name in self._msg_desc_dict:
            return self._msg_desc_dict[descriptor.name]
        message_field_dict: dict = {}

        for option_descriptor, option_value in descriptor.GetOptions().ListFields():
            if (option_descriptor.full_name == f"{self.protobuf_pkg}.disabled" and option_value) or (
                option_descriptor.full_name == f"{self.protobuf_pkg}.ignored" and option_value
            ):
                self._msg_desc_dict[descriptor.name] = message_field_dict
                return message_field_dict
        for one_of in descriptor.oneofs:
            for one_of_descriptor, one_ov_value in one_of.GetOptions().ListFields():
                if one_of_descriptor.full_name == f"{self.protobuf_pkg}.required":
                    if one_of.full_name in self._msg_desc_dict:
                        continue
                    self._msg_desc_dict[one_of.full_name] = {"required": True}
        for field in descriptor.fields:
            type_name: str = ""
            if field.type == FieldDescriptor.TYPE_MESSAGE:
                message_type_name: str = field.message_type.name
                if message_type_name == "Duration":
                    type_name = "duration"
                elif message_type_name == "Any":
                    type_name = "any"
                elif message_type_name == "Timestamp":
                    type_name = "timestamp"
                elif message_type_name.endswith("Entry"):
                    type_name = "map"
                elif message_type_name == "Empty":
                    continue
                else:
                    type_name = "message"
            if field.label == FieldDescriptor.LABEL_REPEATED:
                if not (field.message_type and field.message_type.name.endswith("Entry")):
                    type_name = "repeated"
            if not type_name:
                type_name = type_dict.get(field.type, "")
            if not type_name:
                _logger.warning(
                    f"{__name__} not support protobuf type id:{field.type} from field name{field.full_name}"
                )
                continue
            field_dict: dict = self.field_optional_handle(type_name, field)
            if not field_dict["skip"]:
                # If skip is True, the corresponding validation rule is not applied
                message_field_dict[field.name] = field_dict
                if type_name == "message":
                    message_field_dict[field.message_type.name] = self.get_desc_from_options(field.message_type)
                elif type_name == "map":
                    for sub_field in field.message_type.fields:
                        if not sub_field.message_type:
                            continue
                        # keys and values
                        message_field_dict[sub_field.message_type.name] = self.get_desc_from_options(
                            sub_field.message_type
                        )
        self._msg_desc_dict[descriptor.name] = message_field_dict
        return message_field_dict

    def field_optional_handle(self, type_name: str, field: FieldDescriptor) -> dict:
        field_dict: dict = {"extra": {}, "skip": False}
        miss_default: bool = False
        for option_descriptor, option_value in field.GetOptions().ListFields():
            if option_descriptor.full_name != f"{self.protobuf_pkg}.rules":
                continue
            rule_message: Any = option_value.message
            if rule_message:
                if getattr(rule_message, "skip", None):
                    field_dict["skip"] = True
                if getattr(rule_message, "required", None):
                    miss_default = True
            type_value: Optional[Descriptor] = getattr(option_value, type_name, None)
            if not type_value:
                _logger.warning(f"{__name__} Can not found {field.full_name}'s {type_name} from {option_value}")
                continue
            option_descriptor_to_desc_dict(type_value, field, field_dict, type_name)

        if miss_default:
            field_dict["miss_default"] = miss_default
        return field_dict
