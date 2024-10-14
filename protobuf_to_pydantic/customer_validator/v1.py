from datetime import datetime
from typing import Any, Callable, Dict, Tuple

from pydantic.fields import ModelField

from . import rule

from protobuf_to_pydantic.field_info_rule.types import OneOfTypedDict  # isort:skip


################
# requirements #
################


def _get_name_value_from_kwargs(key: str, field: ModelField) -> Tuple[str, Any]:
    field_name: str = field.name
    if field.field_info.extra:
        field_value: Any = field.field_info.extra.get(key, None)
    else:
        field_value = getattr(field.type_, key, None)
    return field_name, field_value


#################
# pre validator #
#################
def check_one_of(cls: Any, values: tuple) -> tuple:
    """validatorValidator for supporting protobuf one_of"""
    for one_of_name, one_of_dict in getattr(cls, "_one_of_dict", {}).items():  # type: str, OneOfTypedDict
        have_value_name = sum([1 for one_of_field_name in one_of_dict["fields"] if one_of_field_name in values])
        if have_value_name >= 2:
            raise ValueError(f"OneOf:{one_of_name} has {have_value_name} value")
        if one_of_dict.get("required", False) and have_value_name == 0:
            raise ValueError(f"OneOf:{one_of_name} must set value (Choose one of :{one_of_dict['fields']})")
    return values


##################
# data validator #
##################
def in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("in_", kwargs["field"])
    return rule.in_validator(v, field_name, field_value)


def not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("not_in", kwargs["field"])
    return rule.not_in_validator(v, field_name, field_value)


def any_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("any_in", kwargs["field"])
    return rule.any_in_validator(v, field_name, field_value)


def any_not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("any_not_in", kwargs["field"])
    return rule.any_not_in_validator(v, field_name, field_value)


def len_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("len", kwargs["field"])
    return rule.len_validator(v, field_name, field_value)


def prefix_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("prefix", kwargs["field"])
    return rule.prefix_validator(v, field_name, field_value)


def suffix_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("suffix", kwargs["field"])
    return rule.suffix_validator(v, field_name, field_value)


def contains_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("contains", kwargs["field"])
    return rule.contains_validator(v, field_name, field_value)


def not_contains_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("not_contains", kwargs["field"])
    return rule.not_contains_validator(v, field_name, field_value)


####################
# duration support #
####################
def duration_lt_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_lt", kwargs["field"])
    return rule.duration_lt_validator(v, field_name, field_value)


def duration_le_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_le", kwargs["field"])
    return rule.duration_le_validator(v, field_name, field_value)


def duration_gt_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_gt", kwargs["field"])
    return rule.duration_gt_validator(v, field_name, field_value)


def duration_ge_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_ge", kwargs["field"])
    return rule.duration_ge_validator(v, field_name, field_value)


def duration_const_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_const", kwargs["field"])
    return rule.duration_const_validator(v, field_name, field_value)


def duration_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_in", kwargs["field"])
    return rule.duration_in_validator(v, field_name, field_value)


def duration_not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_not_in", kwargs["field"])
    return rule.duration_not_in_validator(v, field_name, field_value)


#####################
# timestamp support #
#####################
_now_default_factory: Callable[[], datetime] = datetime.now


def set_now_default_factory(now_default_factory: Callable[[], datetime]) -> None:
    global _now_default_factory
    _now_default_factory = now_default_factory


def timestamp_lt_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("timestamp_lt", kwargs["field"])
    return rule.timestamp_lt_validator(v, field_name, field_value)


def timestamp_lt_now_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("timestamp_lt_now", kwargs["field"])
    return rule.timestamp_lt_now_validator(v, field_name, field_value)


def timestamp_le_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("timestamp_le", kwargs["field"])
    return rule.timestamp_le_validator(v, field_name, field_value)


def timestamp_gt_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs(
        "timestamp_gt",
        kwargs["field"],
    )
    return rule.timestamp_gt_validator(v, field_name, field_value)


def timestamp_gt_now_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("timestamp_gt_now", kwargs["field"])
    return rule.timestamp_gt_now_validator(v, field_name, field_value)


def timestamp_within_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("timestamp_within", kwargs["field"])
    return rule.timestamp_within_validator(v, field_name, field_value)


def timestamp_ge_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs(
        "timestamp_ge",
        kwargs["field"],
    )
    return rule.timestamp_ge_validator(v, field_name, field_value)


def timestamp_const_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs(
        "timestamp_const",
        kwargs["field"],
    )
    return rule.timestamp_const_validator(v, field_name, field_value)


def timestamp_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs(
        "timestamp_in",
        kwargs["field"],
    )
    return rule.timestamp_in_validator(v, field_name, field_value)


def timestamp_not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs(
        "timestamp_not_in",
        kwargs["field"],
    )
    return rule.timestamp_not_in_validator(v, field_name, field_value)


###############
# map support #
###############
def map_min_pairs_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("map_min_pairs", kwargs["field"])
    return rule.map_min_pairs_validator(v, field_name, field_value)


def map_max_pairs_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("map_max_pairs", kwargs["field"])
    return rule.map_max_pairs_validator(v, field_name, field_value)


validate_validator_dict: Dict[str, Callable] = globals()
