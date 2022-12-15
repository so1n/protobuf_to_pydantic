from datetime import datetime
from typing import Any, Callable, Dict, Tuple

from pydantic.fields import ModelField

from protobuf_to_pydantic.grpc_types import AnyMessage
from protobuf_to_pydantic.types import OneOfTypedDict


################
# requirements #
################
def _get_name_value_from_kwargs(
    key: str, field: ModelField, enable_timestamp_to_datetime: bool = False
) -> Tuple[str, Any]:
    field_name: str = field.name
    if field.field_info.extra:
        field_value: Any = field.field_info.extra.get(key, None)
    else:
        field_value = getattr(field.type_, key, None)
    if enable_timestamp_to_datetime and not isinstance(field_value, datetime):
        if isinstance(field_value, (list, tuple)):
            field_value = [datetime.fromtimestamp(i) for i in field_value]
        else:
            field_value = datetime.fromtimestamp(field_value)

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
            raise ValueError(f"OneOf:{one_of_name} must set value")
    return values


##################
# data validator #
##################
def in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("in_", kwargs["field"])
    if field_value is not None and v not in field_value:
        raise ValueError(f"{field_name}:{v} not in {field_value}")
    return v


def not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("not_in", kwargs["field"])
    if field_value is not None and v in field_value:
        raise ValueError(f"{field_name}:{v} in {field_value}")
    return v


def any_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("any_in", kwargs["field"])
    if field_value is not None and isinstance(v, AnyMessage) and not (v.type_url in field_value or v in field_value):
        raise ValueError(f"{field_name}.type_url:{v.type_url} not in {field_value}")
    return v


def any_not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("any_not_in", kwargs["field"])
    if field_value is not None and isinstance(v, AnyMessage) and (v.type_url in field_value or v in field_value):
        raise ValueError(f"{field_name}.type_url:{v.type_url} in {field_value}")
    return v


def len_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("len", kwargs["field"])
    if field_value is not None and len(v) != field_value:
        raise ValueError(f"{field_name} length does not equal {field_value}")
    return v


def prefix_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("prefix", kwargs["field"])
    if field_value is not None and not v.startswith(field_value):
        raise ValueError(f"{field_name} does not start with prefix {field_value}")
    return v


def suffix_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("suffix", kwargs["field"])
    if field_value is not None and not v.endswith(field_value):
        raise ValueError(f"{field_name} does not end with suffix {field_value}")
    return v


def contains_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("contains", kwargs["field"])
    if field_value is not None and field_value not in v:
        raise ValueError(f"{field_name} value:{v} must contain {field_value}")
    return v


def not_contains_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("not_contains", kwargs["field"])
    if field_value is not None and field_value in v:
        raise ValueError(f"{field_name} value :{v} must not contain {field_value}")
    return v


####################
# duration support #
####################
def duration_lt_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_lt", kwargs["field"])
    if field_value is not None and not (v < field_value):
        raise ValueError(f"{field_name} must < {field_value}, not {v}")
    return v


def duration_le_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_le", kwargs["field"])
    if field_value is not None and not (v <= field_value):
        raise ValueError(f"{field_name} must <= {field_value}, not {v}")
    return v


def duration_gt_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_gt", kwargs["field"])
    if field_value is not None and not (v > field_value):
        raise ValueError(f"{field_name} must > {field_value}, not {v}")
    return v


def duration_ge_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_ge", kwargs["field"])
    if field_value is not None and not (v >= field_value):
        raise ValueError(f"{field_name} must >= {field_value}, not {v}")
    return v


def duration_const_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_const", kwargs["field"])
    if field_value is not None and v != field_value:
        raise ValueError(f"{field_name} must {field_value}, not {v}")
    return v


def duration_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_in", kwargs["field"])
    if field_value is not None and v not in field_value:
        raise ValueError(f"{field_name} not in {field_value}")
    return v


def duration_not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("duration_not_in", kwargs["field"])
    if field_value is not None and v in field_value:
        raise ValueError(f"{field_name} in {field_value}")
    return v


#####################
# timestamp support #
#####################
_now_default_factory: Callable[[], datetime] = datetime.now


def set_now_default_factory(now_default_factory: Callable[[], datetime]) -> None:
    global _now_default_factory
    _now_default_factory = now_default_factory


def timestamp_lt_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs(
        "timestamp_lt", kwargs["field"], enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    if field_value is not None and not (v < field_value):
        raise ValueError(f"{field_name} must < {field_value}, not {v}")
    return v


def timestamp_lt_now_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("timestamp_lt_now", kwargs["field"])
    if field_value is not None:
        if hasattr(field_value, "__call__"):
            now_time: datetime = field_value()
        else:
            now_time = _now_default_factory()
        if not v < now_time:
            raise ValueError(f"{field_name} must < {now_time}, not {v}")
    return v


def timestamp_le_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs(
        "timestamp_le", kwargs["field"], enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    if field_value is not None and not (v <= field_value):
        raise ValueError(f"{field_name} must <= {field_value}, not {v}")
    return v


def timestamp_gt_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs(
        "timestamp_gt", kwargs["field"], enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    if field_value is not None and not (v > field_value):
        raise ValueError(f"{field_name} must > {field_value}, not {v}")
    return v


def timestamp_gt_now_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("timestamp_gt_now", kwargs["field"])
    if field_value is not None:
        if hasattr(field_value, "__call__"):
            now_time: datetime = field_value()
        else:
            now_time = _now_default_factory()
        if not v > now_time:
            raise ValueError(f"{field_name} must > {now_time}, not {v}")
    return v


def timestamp_within_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("timestamp_within", kwargs["field"])
    if field_value is not None:
        if hasattr(field_value, "__call__"):
            now_time: datetime = field_value()
        else:
            now_time = _now_default_factory()
        if not ((now_time - field_value) <= v <= (now_time + field_value)):
            raise ValueError(f"{field_name} must between {now_time -field_value} and {now_time + field_value}, not {v}")
    return v


def timestamp_ge_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs(
        "timestamp_ge", kwargs["field"], enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    if field_value is not None and not (v >= field_value):
        raise ValueError(f"{field_name} must >= {field_value}, not {v}")
    return v


def timestamp_const_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs(
        "timestamp_const", kwargs["field"], enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    if field_value is not None and v != field_value:
        raise ValueError(f"{field_name} must {field_value}, not {v}")
    return v


def timestamp_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs(
        "timestamp_in", kwargs["field"], enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    if field_value is not None and v not in field_value:
        raise ValueError(f"{field_name} not in {field_value}")
    return v


def timestamp_not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs(
        "timestamp_not_in", kwargs["field"], enable_timestamp_to_datetime=isinstance(v, datetime)
    )
    if field_value is not None and v in field_value:
        raise ValueError(f"{field_name} in {field_value}")
    return v


###############
# map support #
###############
def map_min_pairs_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("map_min_pairs", kwargs["field"])
    if field_value is not None and len(v) < field_value:
        raise ValueError(f"{field_name} length must >= {field_value}")
    return v


def map_max_pairs_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("map_max_pairs", kwargs["field"])
    if field_value is not None and len(v) > field_value:
        raise ValueError(f"{field_name} length must <= {field_value}")
    return v


validate_validator_dict: Dict[str, Callable] = globals()
