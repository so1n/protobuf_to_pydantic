import inspect
import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

from protobuf_to_pydantic import _pydantic_adapter
from protobuf_to_pydantic.customer_con_type import (
    conbytes,
    confloat,
    conint,
    conlist,
    constr,
    contimedelta,
    contimestamp,
)
from protobuf_to_pydantic.customer_validator import validate_validator_dict
from protobuf_to_pydantic.grpc_types import Descriptor, FieldDescriptor, FieldDescriptorProto, Message, Timestamp
from protobuf_to_pydantic.types import DescFromOptionTypedDict, FieldInfoTypedDict, OneOfTypedDict
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
    "miss_default": "required",
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


def get_type_hints_from_type_name(type_name: str) -> Optional[Type]:
    if type_name == "string":
        return str
    elif "double" in type_name or "float" in type_name:
        return float
    elif "int" in type_name:
        return int
    elif type_name == "duration":
        return timedelta
    elif type_name == "timestamp":
        return datetime
    elif type_name == "bytes":
        return bytes
    else:
        return None


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


def field_dict_handler(
    field_dict: Dict[str, Any],
    *,
    field_name: str,
    field_type: int,
    type_name: str,
    full_name: str,
    sub_value_handler: Callable[[Any], Dict[str, Any]],
    sub_type_name_handler: Callable[[Any], str],
    rule_value_to_field_value_handler: Callable[[str, str, Any], str],
    value_type_conversion_handler: Optional[Callable[[str, str, Any], Tuple[bool, Any]]] = None,
) -> FieldInfoTypedDict:
    """
    Adapt some Field verification information to convert it into verification information that is compatible with
     Protobuf's special type of pydantic
    """
    field_info_type_dict: FieldInfoTypedDict = {"extra": {}, "skip": False}
    for column, column_value in field_dict.items():
        if column in type_not_support_dict.get(field_type, type_not_support_dict["Any"]):
            # Exclude unsupported fields
            rule_name = column
            if field_type in protobuf_common_type_dict:
                rule_name = f"{protobuf_common_type_dict[field_type]}.{rule_name}"
            elif field_type == 1:
                rule_name = f"Message.{rule_name}"

            msg: str = f"{__name__} not support `{rule_name}` rule."
            if full_name:
                msg = msg + f"(field:{full_name})"
            _logger.warning(msg)
            continue
        if value_type_conversion_handler:
            is_change, new_column_value = value_type_conversion_handler(type_name, column, column_value)
            if is_change:
                column_value = new_column_value
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
            if "validator" not in field_info_type_dict:
                field_info_type_dict["validator"] = {}

            _column: str = f"{type_name}_{column}"
            field_info_type_dict["extra"][_column] = rule_value_to_field_value_handler(type_name, column, column_value)
            field_info_type_dict["validator"][f"{field_name}_{_column}_validator"] = _pydantic_adapter.field_validator(
                field_name, allow_reuse=True
            )(validate_validator_dict[f"{_column}_validator"])
            continue
        elif column in ("in", "not_in", "len", "prefix", "suffix", "contains", "not_contains"):
            # The verification of these parameters is handed over to the validator,
            # see protobuf_to_pydantic/customer_validator for details

            # Compatible with PGV attributes that are not supported by pydantic
            if "validator" not in field_info_type_dict:
                field_info_type_dict["validator"] = {}
            _column = column + "_" if column in ("in",) else column
            field_info_type_dict["extra"][_column] = rule_value_to_field_value_handler(type_name, column, column_value)
            field_info_type_dict["validator"][f"{field_name}_{column}_validator"] = _pydantic_adapter.field_validator(
                field_name, allow_reuse=True
            )(validate_validator_dict[f"{column}_validator"])
            continue
        elif column in column_pydantic_type_dict:
            # Support some built-in type judgments of PGV
            field_info_type_dict["type"] = column_pydantic_type_dict[column]
            continue
        elif column in ("keys", "values"):
            # Parse the field data of the key and value in the map
            type_name = sub_type_name_handler(column_value)
            # Nested types are supported via like constr

            # Generate information corresponding to the nested type
            sub_dict = field_dict_handler(
                sub_value_handler(column_value),
                field_name=field_name,
                field_type=field_type,
                type_name=type_name,
                full_name=full_name,
                sub_value_handler=sub_value_handler,
                sub_type_name_handler=sub_type_name_handler,
                rule_value_to_field_value_handler=rule_value_to_field_value_handler,
            )
            con_type = get_con_type_func_from_type_name(type_name)
            if not con_type:
                # TODO nested message
                _logger.warning(f"{__name__} not support sub type `{type_name}`, please reset {full_name}")
                continue
            if "map_type" not in field_info_type_dict:
                field_info_type_dict["map_type"] = {}
            con_type_param_dict: dict = {}
            for _key in inspect.signature(con_type).parameters.keys():
                param_value = sub_dict.get(_key, None)  # type: ignore
                if param_value is not None:
                    con_type_param_dict[_key] = param_value
                elif "extra" in sub_dict:
                    if sub_dict["extra"].get(_key, None) is not None:
                        con_type_param_dict[_key] = sub_dict["extra"][_key]

            field_info_type_dict["map_type"][column] = con_type(**con_type_param_dict)
            # if _pydantic_adapter.is_v1:
            #     con_type = get_con_type_func_from_type_name(type_name)
            #     if not con_type:
            #         # TODO nested message
            #         _logger.warning(f"{__name__} not support sub type `{type_name}`, please reset {full_name}")
            #         continue
            #     if "map_type" not in field_info_type_dict:
            #         field_info_type_dict["map_type"] = {}
            #     con_type_param_dict: dict = {}
            #     for _key in inspect.signature(con_type).parameters.keys():
            #         param_value = sub_dict.get(_key, None)  # type: ignore
            #         if param_value is not None:
            #             con_type_param_dict[_key] = param_value
            #         elif "extra" in sub_dict:
            #             if sub_dict["extra"].get(_key, None) is not None:
            #                 con_type_param_dict[_key] = sub_dict["extra"][_key]
            #
            #     field_info_type_dict["map_type"][column] = con_type(**con_type_param_dict)
            # else:
            #     _type = get_type_hints_from_type_name(type_name)
            #     if not _type:
            #         # TODO nested message
            #         _logger.warning(f"{__name__} not support sub type `{type_name}`, please reset {full_name}")
            #         continue
            #     if "map_type" not in field_info_type_dict:
            #         field_info_type_dict["map_type"] = {}
            #
            #     from pydantic import Field
            #
            #     with_validator_param_field = Field(**sub_dict)
            #     if not with_validator_param_field.metadata:
            #         field_info_type_dict["map_type"][column] = _type
            #     else:
            #         field_info_type_dict["map_type"][column] = Annotated.__class_getitem__(
            #             (_type, *with_validator_param_field.metadata)
            #         )
            # TODO extra handler
            #
            # con_type_param_dict: dict = {}
            # for _key in inspect.signature(con_type).parameters.keys():
            #     param_value = sub_dict.get(_key, None)  # type: ignore
            #     if param_value is not None:
            #         con_type_param_dict[_key] = param_value
            #     elif "extra" in sub_dict:
            #         if sub_dict["extra"].get(_key, None) is not None:
            #             con_type_param_dict[_key] = sub_dict["extra"][_key]
            #
            # field_info_type_dict["map_type"][column] = con_type(**con_type_param_dict)
        elif column == "items":
            # Process array data
            type_name = sub_type_name_handler(column_value)
            # Nested types are supported via like constr
            # TODO pydantic v2
            con_type = get_con_type_func_from_type_name(type_name)
            # if _pydantic_adapter.is_v1:
            #     con_type = get_con_type_func_from_type_name(type_name)
            # else:
            #     con_type = get_type_hints_from_type_name(type_name)
            if not con_type:
                # TODO nested message
                _logger.warning(f"{__name__} not support sub type `{type_name}`, please reset {full_name}")
                field_info_type_dict["type"] = List
                continue
            # sub_dict = {"extra": {}, "type": con_type, "skip": False}
            sub_dict = field_dict_handler(
                sub_value_handler(column_value),
                field_name=field_name,
                field_type=field_type,
                type_name=type_name,
                full_name=full_name,
                sub_value_handler=sub_value_handler,
                sub_type_name_handler=sub_type_name_handler,
                rule_value_to_field_value_handler=rule_value_to_field_value_handler,
            )
            if "type" not in sub_dict:
                sub_dict["type"] = con_type

            field_info_type_dict["type"] = conlist
            field_info_type_dict["sub"] = sub_dict

        field_info_type_dict[column] = column_value  # type: ignore
    return field_info_type_dict


def field_comment_handler(  # noqa: C901
    field_dict: Dict[str, Any],
    field: Union[FieldDescriptor, FieldDescriptorProto],
    type_name: str,
    full_name: str,
) -> FieldInfoTypedDict:
    """Parse the data of option and store it in dict.
    Since array and map are supported, the complexity is relatively high

    The field names used by validator need to be prefixed with type_name, such as timestamp_gt,
    while the built-in validation of Pydantic V2 does not require type_name prefix, such as gt
    """

    def _duration_handler(_value: Any) -> Optional[timedelta]:
        if isinstance(_value, timedelta):
            return _value
        elif not isinstance(_value, dict):
            return _value
        seconds = _value.get("seconds", 0)
        nanos = _value.get("nanos", 0)
        if nanos:
            nanos = nanos / 1000
        if not seconds and not nanos:
            return None
        return timedelta(seconds=seconds, microseconds=nanos)

    def sub_value_handler(column_value: Any) -> Dict[str, Any]:
        sub_type_name = sub_type_name_handler(column_value)
        return column_value[sub_type_name]

    def sub_type_name_handler(column_value: Any) -> str:
        sub_type_name = list(column_value.keys())[0]
        return sub_type_name

    def value_type_conversion_handler(column_type_name: str, column_name: str, column_value: Any) -> Tuple[bool, Any]:
        if type_name in ("double", "float") and isinstance(column_value, (float, int)):
            return True, float(column_value)
        elif type_name == "bytes" and isinstance(column_value, str):
            return True, column_value.encode("utf-8")
        elif isinstance(column_value, list):
            new_value = []
            is_change: bool = False
            for i in column_value:
                _is_change, i = value_type_conversion_handler(column_type_name, column_name, i)
                new_value.append(i)
                if _is_change:
                    is_change = _is_change
            if is_change:
                return is_change, new_value
            return is_change, column_value
        elif column_name not in (
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
            if type_name == "duration" and isinstance(column_value, dict):
                new_column_value = _duration_handler(column_value)
                if new_column_value:
                    return True, new_column_value
                return False, column_value
            elif type_name == "timestamp" and isinstance(column_value, dict):
                if "seconds" in column_value or "nanos" in column_value:
                    return True, Timestamp(**column_value)
                else:
                    return False, column_value
        return False, column_value

    def rule_value_to_field_value_handler(column_type_name: str, column_name: str, column_value: Any) -> Any:
        if isinstance(column_value, list):
            return [rule_value_to_field_value_handler(column_type_name, column_name, i) for i in column_value]
        elif column_type_name == "duration":
            return _duration_handler(column_value)
        elif column_type_name == "timestamp":
            if column_name in ("const", "gt", "lt", "ge", "le") and isinstance(column_value, dict):
                return Timestamp(**column_value)
            elif column_name in ("within",):
                return _duration_handler(column_value)
        return column_value

    return field_dict_handler(
        field_dict,
        field_name=field.name,
        field_type=field.type,
        type_name=type_name,
        full_name=full_name,
        sub_value_handler=sub_value_handler,
        sub_type_name_handler=sub_type_name_handler,
        rule_value_to_field_value_handler=rule_value_to_field_value_handler,
        value_type_conversion_handler=value_type_conversion_handler,
    )


def option_descriptor_to_desc_dict(
    option_descriptor: Union[Descriptor, FieldDescriptor],
    field: Union[FieldDescriptor, FieldDescriptorProto],
    type_name: str,
    full_name: str,
) -> FieldInfoTypedDict:
    """Parse the data of option and store it in dict.
    Since array and map are supported, the complexity is relatively high

    The field names used by validator need to be prefixed with type_name, such as timestamp_gt,
    while the built-in validation of Pydantic V2 does not require type_name prefix, such as gt
    """

    def get_column_list(column_descriptor: Union[Descriptor, FieldDescriptor]) -> List[str]:
        if hasattr(column_descriptor, "ListFields"):
            column_list = [column[0].name for column in column_descriptor.ListFields()]  # type: ignore
        else:
            column_list = [
                column
                for column in column_descriptor.__dir__()
                if _has_raw_message_field(column, column_descriptor)  # type: ignore
            ]
        return column_list

    def get_field_dict(column_list: List[str], field_descriptor: Union[Descriptor, FieldDescriptor]) -> Dict[str, Any]:
        field_dict = {}
        for column in column_list:
            value = getattr(field_descriptor, column)
            field_dict[column] = value
        return field_dict

    def sub_value_handler(column_value: Any) -> Dict[str, Any]:
        sub_type_name = sub_type_name_handler(column_value)
        _descriptor = getattr(column_value, sub_type_name)
        return get_field_dict(get_column_list(_descriptor), _descriptor)

    def sub_type_name_handler(column_value: Any) -> str:
        sub_type_name = column_value.ListFields()[0][0].full_name.split(".")[-1]
        return sub_type_name

    def rule_value_to_field_value_handler(column_type_name: str, column_name: str, column_value: Any) -> Any:
        return replace_protobuf_type_to_python_type(column_value)

    # print(get_column_list(option_descriptor), file=sys.stderr)
    # print(get_field_dict(get_column_list(option_descriptor), option_descriptor), file=sys.stderr)
    return field_dict_handler(
        get_field_dict(get_column_list(option_descriptor), option_descriptor),
        field_name=field.name,
        field_type=field.type,
        type_name=type_name,
        full_name=full_name,
        sub_value_handler=sub_value_handler,
        sub_type_name_handler=sub_type_name_handler,
        rule_value_to_field_value_handler=rule_value_to_field_value_handler,
    )


def field_option_handle(
    type_name: str,
    full_name: str,
    field: Union[FieldDescriptor, FieldDescriptorProto],
    protobuf_pkg: str = "",
) -> FieldInfoTypedDict:
    """Parse the information for each filed"""
    field_dict: FieldInfoTypedDict = {"extra": {}, "skip": False}
    required: bool = False
    skip: bool = False
    if isinstance(field, FieldDescriptor):
        field_list = field.GetOptions().ListFields()
    elif isinstance(field, FieldDescriptorProto):
        field_list = field.options.ListFields()
    else:
        raise RuntimeError(f"Not support type:{field.type}")
    for option_descriptor, option_value in field_list:
        # filter unwanted Option
        if protobuf_pkg:
            if not option_descriptor.full_name.endswith(f"{protobuf_pkg}.rules"):
                continue
        elif not option_descriptor.full_name.endswith("validate.rules"):
            continue

        rule_message: Any = option_value.message
        if rule_message:
            if getattr(rule_message, "skip", None):
                skip = True
            if getattr(rule_message, "required", None):
                required = True
        type_value: Optional[Descriptor] = getattr(option_value, type_name, None)
        if not type_value:
            continue
        if not type_value.ListFields():  # type: ignore
            type_value = getattr(option_value, "message", None)
            if not type_value or not type_value.ListFields():  # type: ignore
                _logger.warning(f"{__name__} Can not found {full_name}'s {type_name} from {option_value}")

        field_dict.update(
            option_descriptor_to_desc_dict(type_value, field, type_name, full_name)  # type:ignore
        )

    if required:
        field_dict["required"] = required
    if skip:
        field_dict["skip"] = skip
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

    def get_desc_from_options(self, descriptor: Descriptor) -> DescFromOptionTypedDict:  # noqa:C901
        """Extract the information of each field through the Options of Protobuf Message"""
        if descriptor.name in self._msg_desc_dict:
            return self._msg_desc_dict[descriptor.name]
        message_field_dict: DescFromOptionTypedDict = {"message": {}, "one_of": {}, "nested": {}, "metadata": {}}

        # Options for processing Messages
        for option_descriptor, option_value in descriptor.GetOptions().ListFields():
            # If parsing is disabled, Options will not continue to be parsed, and empty information will be set
            if (option_descriptor.full_name == f"{self.protobuf_pkg}.disabled" and option_value) or (
                option_descriptor.full_name == f"{self.protobuf_pkg}.ignored" and option_value
            ):
                return message_field_dict
        # Handle one_ofs of Message
        one_of_dict: Dict[str, OneOfTypedDict] = {}
        for one_of in descriptor.oneofs:
            required: bool = False
            optional_fields: Set[str] = set()
            for one_of_descriptor, one_ov_value in one_of.GetOptions().ListFields():
                if one_of_descriptor.full_name == f"{self.protobuf_pkg}.required":
                    required = True
                    # if one_of.full_name in self._msg_desc_dict:
                    #     continue
                    # Support one of is required
                elif one_of_descriptor.full_name == f"{self.protobuf_pkg}.oneof_extend":
                    # Support one of is optional
                    for one_of_extend_field_descriptor, result in one_ov_value.ListFields():
                        for one_of_optional_name in result:
                            optional_fields.add(one_of_optional_name)

            if required or optional_fields:
                one_of_dict[one_of.full_name] = {
                    "required": required,
                    "optional_fields": optional_fields,
                    # optional cannot get the value of the current one of,
                    # so it needs to be processed in subsequent processing
                    "fields": set(),
                }
        if one_of_dict:
            message_field_dict["one_of"] = one_of_dict
        # Process all fields of Message
        for field in descriptor.fields:
            type_name: str = ""
            if field.type == FieldDescriptor.TYPE_MESSAGE:
                # Convert some types of Protobuf
                message_type_name: str = field.message_type.name
                if message_type_name in ("Duration", "Any", "Timestamp", "Struct"):
                    type_name = message_type_name.lower()
                elif message_type_name.endswith("Entry"):
                    type_name = "map"
                elif message_type_name == "Empty":
                    continue
                else:
                    type_name = "message"
            if field.label == FieldDescriptor.LABEL_REPEATED and not (
                field.message_type and field.message_type.name.endswith("Entry")
            ):
                # Support Protobuf.RepeatedXXX
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
