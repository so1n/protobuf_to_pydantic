from datetime import datetime
from typing import Any, Callable, Dict, Tuple, Type, Union

from pydantic import BaseModel, FieldValidationInfo
from pydantic.fields import ModelPrivateAttr

from protobuf_to_pydantic.grpc_types import AnyMessage

from . import rule

from protobuf_to_pydantic.field_info_rule.types import OneOfTypedDict  # isort:skip


################
# requirements #
################
def _get_name_and_value(
    cls: Type[BaseModel], key: str, info: FieldValidationInfo, enable_timestamp_to_datetime: bool = False
) -> Tuple[str, Any]:
    field_name: str = info.field_name
    field_value = cls.model_fields[field_name].json_schema_extra[key]
    if enable_timestamp_to_datetime and not isinstance(field_value, datetime):
        if isinstance(field_value, (list, tuple)):
            field_value = [datetime.fromtimestamp(i) for i in field_value]
        else:
            field_value = datetime.fromtimestamp(field_value)

    return field_name, field_value


#################
# pre validator #
#################
def check_one_of(cls: Type[BaseModel], values: tuple) -> tuple:
    """validatorValidator for supporting protobuf one_of"""
    _one_of_private_attr: Union[ModelPrivateAttr, Dict[str, Any], None] = getattr(cls, "_one_of_dict", None)
    if not _one_of_private_attr:
        return values
    # if model is dynamic gen, _one_of_dict is a dict, else model code run, _one_of_dict is a ModelPrivateAttr
    if isinstance(_one_of_private_attr, ModelPrivateAttr):
        _one_of_private_attr = _one_of_private_attr.default

    for one_of_name, one_of_dict in _one_of_private_attr.items():  # type: str, OneOfTypedDict
        have_value_name = sum([1 for one_of_field_name in one_of_dict["fields"] if one_of_field_name in values])
        if have_value_name >= 2:
            raise ValueError(f"OneOf:{one_of_name} has {have_value_name} value")
        if one_of_dict.get("required", False) and have_value_name == 0:
            raise ValueError(f"OneOf:{one_of_name} must set value (Choose one of :{one_of_dict['fields']})")
    return values


##################
# data validator #
##################
def in_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "in_", info)
    return rule.in_validator(v, field_name, field_value)


def not_in_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "not_in", info)
    return rule.not_in_validator(v, field_name, field_value)


def any_in_validator(cls: Type[BaseModel], v: AnyMessage, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "any_in", info)
    return rule.any_in_validator(v, field_name, field_value)


def any_not_in_validator(cls: Type[BaseModel], v: AnyMessage, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "any_not_in", info)
    return rule.any_not_in_validator(v, field_name, field_value)


def len_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "len", info)
    return rule.len_validator(v, field_name, field_value)


def prefix_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "prefix", info)
    return rule.prefix_validator(v, field_name, field_value)


def suffix_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "suffix", info)
    return rule.suffix_validator(v, field_name, field_value)


def contains_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "contains", info)
    return rule.contains_validator(v, field_name, field_value)


def not_contains_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "not_contains", info)
    return rule.not_contains_validator(v, field_name, field_value)


####################
# duration support #
####################
def duration_lt_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "duration_lt", info)
    return rule.duration_lt_validator(v, field_name, field_value)


def duration_le_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "duration_le", info)
    return rule.duration_le_validator(v, field_name, field_value)


def duration_gt_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "duration_gt", info)
    return rule.duration_gt_validator(v, field_name, field_value)


def duration_ge_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "duration_ge", info)
    return rule.duration_ge_validator(v, field_name, field_value)


def duration_const_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "duration_const", info)
    return rule.duration_const_validator(v, field_name, field_value)


def duration_in_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "duration_in", info)
    return rule.duration_in_validator(v, field_name, field_value)


def duration_not_in_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "duration_not_in", info)
    return rule.duration_not_in_validator(v, field_name, field_value)


#####################
# timestamp support #
#####################
_now_default_factory: Callable[[], datetime] = datetime.now


def set_now_default_factory(now_default_factory: Callable[[], datetime]) -> None:
    global _now_default_factory
    _now_default_factory = now_default_factory


def timestamp_lt_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(
        cls, "timestamp_lt", info, enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    return rule.timestamp_lt_validator(v, field_name, field_value)


def timestamp_lt_now_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "timestamp_lt_now", info)
    return rule.timestamp_lt_now_validator(v, field_name, field_value)


def timestamp_le_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(
        cls, "timestamp_le", info, enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    return rule.timestamp_le_validator(v, field_name, field_value)


def timestamp_gt_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(
        cls, "timestamp_gt", info, enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    return rule.timestamp_gt_validator(v, field_name, field_value)


def timestamp_gt_now_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "timestamp_gt_now", info)
    return rule.timestamp_gt_now_validator(v, field_name, field_value)


def timestamp_within_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "timestamp_within", info)
    return rule.timestamp_within_validator(v, field_name, field_value)


def timestamp_ge_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(
        cls, "timestamp_ge", info, enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    return rule.timestamp_ge_validator(v, field_name, field_value)


def timestamp_const_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(
        cls, "timestamp_const", info, enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    return rule.timestamp_const_validator(v, field_name, field_value)


def timestamp_in_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(
        cls, "timestamp_in", info, enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    return rule.timestamp_in_validator(v, field_name, field_value)


def timestamp_not_in_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(
        cls, "timestamp_not_in", info, enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    return rule.timestamp_not_in_validator(v, field_name, field_value)


###############
# map support #
###############
def map_min_pairs_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "map_min_pairs", info)
    return rule.map_min_pairs_validator(v, field_name, field_value)


def map_max_pairs_validator(cls: Type[BaseModel], v: Any, info: FieldValidationInfo) -> Any:
    field_name, field_value = _get_name_and_value(cls, "map_max_pairs", info)
    return rule.map_max_pairs_validator(v, field_name, field_value)


validate_validator_dict: Dict[str, Callable] = globals()
