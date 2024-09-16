from datetime import timedelta
from typing import Any, Dict, Optional, Tuple, Union

from protobuf_to_pydantic.field_info_rule.protobuf_option_to_field_info.base import (
    BaseProtobufOptionToFieldInfo,
    special_type_rule_name_set,
)
from protobuf_to_pydantic.field_info_rule.types import FieldInfoTypedDict
from protobuf_to_pydantic.grpc_types import FieldDescriptor, FieldDescriptorProto, Timestamp


class ProtobufOptionToFieldInfoWithCommentDict(BaseProtobufOptionToFieldInfo):
    """Parse the data of option and store it in dict.
    Since array and map are supported, the complexity is relatively high

    The field names used by validator need to be prefixed with type_name, such as timestamp_gt,
    while the built-in validation of Pydantic V2 does not require type_name prefix, such as gt
    """

    def __init__(
        self,
        rule_dict: Dict[str, Any],
        field: Union[FieldDescriptor, FieldDescriptorProto],
        type_name: str,
        full_name: str,
    ):
        self._rule_dict = self._core_handler(
            rule_dict=rule_dict,
            field_name=field.name,
            field_type=field.type,
            type_name=type_name,
            full_name=full_name,
        )

    @property
    def rule_dict(self) -> FieldInfoTypedDict:
        return self._rule_dict

    @staticmethod
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

    def sub_value_handler(self, rule_value: Any) -> Dict[str, Any]:
        sub_type_name = self.sub_type_name_handler(rule_value)
        return rule_value[sub_type_name]

    def sub_type_name_handler(self, rule_value: Any) -> str:
        sub_type_name = list(rule_value.keys())[0]
        return sub_type_name

    def rule_value_to_field_value_handler(self, field_type_name: str, rule_name: str, rule_value: Any) -> Any:
        if isinstance(rule_value, list):
            return [self.rule_value_to_field_value_handler(field_type_name, rule_name, i) for i in rule_value]
        elif field_type_name == "duration":
            return self._duration_handler(rule_value)
        elif field_type_name == "timestamp":
            if rule_name in ("const", "gt", "lt", "ge", "le") and isinstance(rule_value, dict):
                return Timestamp(**rule_value)
            elif rule_name in ("within",):
                return self._duration_handler(rule_value)
        return rule_value

    def value_type_conversion_handler(self, field_type_name: str, rule_name: str, rule_value: Any) -> Tuple[bool, Any]:
        if field_type_name in ("double", "float") and isinstance(rule_value, (float, int)):
            return True, float(rule_value)
        elif field_type_name == "bytes" and isinstance(rule_value, str):
            return True, rule_value.encode("utf-8")
        elif isinstance(rule_value, list):
            new_value = []
            is_change: bool = False
            for i in rule_value:
                _is_change, i = self.value_type_conversion_handler(field_type_name, rule_name, i)
                new_value.append(i)
                if _is_change:
                    is_change = _is_change
            if is_change:
                return is_change, new_value
            return is_change, rule_value
        elif rule_name not in special_type_rule_name_set:
            if field_type_name == "duration" and isinstance(rule_value, dict):
                new_column_value = self._duration_handler(rule_value)
                if new_column_value:
                    return True, new_column_value
                return False, rule_value
            elif field_type_name == "timestamp" and isinstance(rule_value, dict):
                if "seconds" in rule_value or "nanos" in rule_value:
                    return True, Timestamp(**rule_value)
                else:
                    return False, rule_value
        return False, rule_value


def gen_field_rule_info_dict_from_field_comment_dict(  # noqa: C901
    rule_dict: Dict[str, Any],
    field: Union[FieldDescriptor, FieldDescriptorProto],
    type_name: str,
    full_name: str,
) -> FieldInfoTypedDict:
    return ProtobufOptionToFieldInfoWithCommentDict(
        rule_dict=rule_dict, field=field, type_name=type_name, full_name=full_name
    ).rule_dict
