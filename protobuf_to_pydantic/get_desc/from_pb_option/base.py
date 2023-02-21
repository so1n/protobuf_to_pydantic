import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, Set, Type, Union

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
from protobuf_to_pydantic.grpc_types import Descriptor, FieldDescriptor, FieldDescriptorProto, Message
from protobuf_to_pydantic.types import DescFromOptionTypedDict, FieldInfoTypedDict
from protobuf_to_pydantic.util import replace_protobuf_type_to_python_type

from .types import column_pydantic_type_dict

_logger: logging.Logger = logging.getLogger(__name__)

protobuf_common_type_dict: Dict[Any, str] = {
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

type_not_support_dict: Dict[Any, Set[str]] = {
    FieldDescriptor.TYPE_BYTES: {"pattern"},
    FieldDescriptor.TYPE_STRING: {"min_bytes", "max_bytes", "well_known_regex", "strict"},
    "Any": {"ignore_empty", "defined_only", "no_sparse"},
}

pgv_column_to_pydantic_dict: Dict[str, str] = {
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


def _has_raw_message_field(column: str, message: Message) -> bool:
    """Determine whether the field held by the Message is a field defined by Protobuf"""
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


def option_descriptor_to_desc_dict(
    option_descriptor: Union[Descriptor, FieldDescriptor],
    field: Union[FieldDescriptor, FieldDescriptorProto],
    type_name: str,
    full_name: str,
    desc_dict: FieldInfoTypedDict,
) -> None:
    """Parse the data of option and store it in dict.
    Since array and map are supported, the complexity is relatively high
    """
    if hasattr(option_descriptor, "ListFields"):
        column_list = [column[0].name for column in option_descriptor.ListFields()]  # type: ignore
    else:
        column_list = [
            column
            for column in option_descriptor.__dir__()
            if _has_raw_message_field(column, option_descriptor)  # type: ignore
        ]
    for column in column_list:
        if column in type_not_support_dict.get(field.type, type_not_support_dict["Any"]):
            # Exclude unsupported fields
            _logger.warning(f"{__name__} not support `{column}`, please reset {full_name} `{column}` value")
            continue

        value = getattr(option_descriptor, column)
        if column in pgv_column_to_pydantic_dict:
            # Field Conversion
            column = pgv_column_to_pydantic_dict[column]

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
            # The verification of these parameters is handed over to the validator,
            # see protobuf_to_pydantic/customer_validator for details

            # Types of priority treatment for special cases
            if "validator" not in desc_dict:
                desc_dict["validator"] = {}
            _column: str = f"{type_name}_{column}"
            desc_dict["extra"][_column] = replace_protobuf_type_to_python_type(value)
            desc_dict["validator"][f"{field.name}_{_column}_validator"] = validator(field.name, allow_reuse=True)(
                validate_validator_dict[f"{_column}_validator"]
            )
            continue
        elif column in ("in", "not_in", "len", "prefix", "suffix", "contains", "not_contains"):
            # The verification of these parameters is handed over to the validator,
            # see protobuf_to_pydantic/customer_validator for details

            # Compatible with PGV attributes that are not supported by pydantic
            if "validator" not in desc_dict:
                desc_dict["validator"] = {}
            _column = column + "_" if column in ("in",) else column
            desc_dict["extra"][_column] = replace_protobuf_type_to_python_type(value)
            desc_dict["validator"][f"{field.name}_{column}_validator"] = validator(field.name, allow_reuse=True)(
                validate_validator_dict[f"{column}_validator"]
            )
            continue
        elif column in column_pydantic_type_dict:
            # Support some built-in type judgments of PGV
            desc_dict["type"] = column_pydantic_type_dict[column]
            continue
        elif column in ("keys", "values"):
            # Parse the field data of the key and value in the map
            type_name = value.ListFields()[0][0].full_name.split(".")[-1]
            # Nested types are supported via like constr
            con_type = get_con_type_func_from_type_name(type_name)
            if not con_type:
                # TODO nested message
                _logger.warning(f"{__name__} not support sub type `{type_name}`, please reset {full_name}")
                continue
            # Generate information corresponding to the nested type
            sub_dict: FieldInfoTypedDict = {"extra": {}, "skip": False}
            option_descriptor_to_desc_dict(getattr(value, type_name), field, type_name, full_name, sub_dict)
            if "map_type" not in desc_dict:
                desc_dict["map_type"] = {}
            con_type_param_dict: dict = {}
            for _key in inspect.signature(con_type).parameters.keys():
                param_value = sub_dict.get(_key, None)  # type: ignore
                if param_value is not None:
                    con_type_param_dict[_key] = param_value
                elif "extra" in sub_dict:
                    if sub_dict["extra"].get(_key, None) is not None:
                        con_type_param_dict[_key] = sub_dict["extra"][_key]

            desc_dict["map_type"][column] = con_type(**con_type_param_dict)
            continue
        elif column == "items":
            # Process array data
            type_name = value.ListFields()[0][0].full_name.split(".")[-1]
            # Nested types are supported via like constr
            con_type = get_con_type_func_from_type_name(type_name)
            if not con_type:
                # TODO nested message
                _logger.warning(
                    f"{__name__} not support sub type `{type_name}`, please reset {field.full_name}"  # type: ignore
                )
                desc_dict["type"] = List
                continue
            sub_dict = {"extra": {}, "type": con_type, "skip": False}
            option_descriptor_to_desc_dict(getattr(value, type_name), field, type_name, full_name, sub_dict)
            desc_dict["type"] = conlist
            desc_dict["sub"] = sub_dict
        desc_dict[column] = value  # type: ignore


def field_option_handle(
    type_name: str,
    full_name: str,
    field: Union[FieldDescriptor, FieldDescriptorProto],
    protobuf_pkg: str = "",
) -> FieldInfoTypedDict:
    """Parse the information for each filed"""
    field_dict: FieldInfoTypedDict = {"extra": {}, "skip": False}
    miss_default: bool = False
    if isinstance(field, FieldDescriptor):
        field_list = field.GetOptions().ListFields()
    elif isinstance(field, FieldDescriptorProto):
        field_list = field.options.ListFields()
    else:
        raise RuntimeError(f"Not support type:{field.type}")
    for option_descriptor, option_value in field_list:
        # filter unwanted Option
        if protobuf_pkg:
            if option_descriptor.full_name != f"{protobuf_pkg}.rules":
                continue
        elif not option_descriptor.full_name.endswith("validate.rules"):
            continue

        rule_message: Any = option_value.message
        if rule_message:
            if getattr(rule_message, "skip", None):
                field_dict["skip"] = True
            if getattr(rule_message, "required", None):
                miss_default = True
        type_value: Optional[Descriptor] = getattr(option_value, type_name, None)
        if not type_value:
            _logger.warning(f"{__name__} Can not found {full_name}'s {type_name} from {option_value}")
            continue
        option_descriptor_to_desc_dict(type_value, field, type_name, full_name, field_dict)

    if miss_default:
        field_dict["miss_default"] = miss_default
    return field_dict


_global_desc_dict: Dict[str, Dict[str, DescFromOptionTypedDict]] = {}


class ParseFromPbOption(object):
    protobuf_pkg: str  # Extend the package name of protobuf

    def __init__(self, message: Type[Message]):
        self.message = message
        self._msg_desc_dict: Dict[str, DescFromOptionTypedDict] = {}
        if self.protobuf_pkg not in _global_desc_dict:
            _global_desc_dict[self.protobuf_pkg] = self._msg_desc_dict
        else:
            self._msg_desc_dict = _global_desc_dict[self.protobuf_pkg]

    def parse(self) -> Dict[str, DescFromOptionTypedDict]:
        descriptor: Descriptor = self.message.DESCRIPTOR
        if descriptor.name in self._msg_desc_dict:
            return self._msg_desc_dict

        self._msg_desc_dict[descriptor.name] = self.get_desc_from_options(descriptor)
        return self._msg_desc_dict

    def get_desc_from_options(self, descriptor: Descriptor) -> DescFromOptionTypedDict:
        """Extract the information of each field through the Options of Protobuf Message"""
        if descriptor.name in self._msg_desc_dict:
            return self._msg_desc_dict[descriptor.name]
        message_field_dict: DescFromOptionTypedDict = {"message": {}, "one_of": {}, "nested": {}}

        # Options for processing Messages
        for option_descriptor, option_value in descriptor.GetOptions().ListFields():
            # If parsing is disabled, Options will not continue to be parsed, and empty information will be set
            if (option_descriptor.full_name == f"{self.protobuf_pkg}.disabled" and option_value) or (
                option_descriptor.full_name == f"{self.protobuf_pkg}.ignored" and option_value
            ):
                return message_field_dict
        # Handle one_ofs of Message
        for one_of in descriptor.oneofs:
            for one_of_descriptor, one_ov_value in one_of.GetOptions().ListFields():
                if one_of_descriptor.full_name == f"{self.protobuf_pkg}.required":
                    # if one_of.full_name in self._msg_desc_dict:
                    #     continue
                    # Support one of is required
                    message_field_dict["one_of"] = {one_of.full_name: {"required": True, "fields": set()}}
        # Process all fields of Message
        for field in descriptor.fields:
            type_name: str = ""
            if field.type == FieldDescriptor.TYPE_MESSAGE:
                # Convert some types of Protobuf
                message_type_name: str = field.message_type.name
                if message_type_name in ("Duration", "Any", "Timestamp"):
                    type_name = message_type_name.lower()
                elif message_type_name.endswith("Entry"):
                    type_name = "map"
                elif message_type_name == "Empty":
                    continue
                else:
                    type_name = "message"
            if field.label == FieldDescriptor.LABEL_REPEATED:
                # Support Protobuf.RepeatedXXX
                if not (field.message_type and field.message_type.name.endswith("Entry")):
                    type_name = "repeated"
            if not type_name:
                # Support Protobuf common type
                type_name = protobuf_common_type_dict.get(field.type, "")
            if not type_name:
                _logger.warning(
                    f"{__name__} not support protobuf type id:{field.type} from field name{field.full_name}"
                )
                continue
            field_dict: FieldInfoTypedDict = field_option_handle(type_name, field.full_name, field, self.protobuf_pkg)
            if field_dict["skip"]:
                # If skip is True, the corresponding validation rule is not applied
                continue
            message_field_dict["message"][field.name] = field_dict
            if type_name == "message":
                message_field_dict["nested"][field.message_type.name] = self.get_desc_from_options(field.message_type)
            elif type_name == "map":
                for sub_field in field.message_type.fields:
                    if not sub_field.message_type:
                        continue
                    # keys and values
                    message_field_dict["nested"][sub_field.message_type.name] = self.get_desc_from_options(
                        sub_field.message_type
                    )
        self._msg_desc_dict[descriptor.name] = message_field_dict
        return message_field_dict
