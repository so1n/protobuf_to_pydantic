import time
from datetime import datetime
from typing import Any, Callable, Dict, Tuple

from pydantic.fields import ModelField

from protobuf_to_pydantic.grpc_types import AnyMessage, Timestamp


def _get_name_value_from_kwargs(key: str, field: ModelField) -> Tuple[str, Any]:
    field_name: str = field.name
    if field.field_info.extra:
        field_value: Any = field.field_info.extra["extra"].get(key, None)
    else:
        field_value = getattr(field.type_, key, None)
    return field_name, field_value


def in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("in", kwargs["field"])
    if field_value is not None and v not in field_value:
        raise ValueError(f"{field_name} not in {field_value}")
    return v


def not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name, field_value = _get_name_value_from_kwargs("not_in", kwargs["field"])
    if field_value is not None and v in field_value:
        raise ValueError(f"{field_name} in {field_value}")
    return v


def any_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["any_in"]
    if isinstance(v, AnyMessage):
        if v.type_url in field_value:
            raise ValueError(f"{field_name}.type_url:{v.type_url} not in {field_value}")
    return v


def any_not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["any_in"]
    if isinstance(v, AnyMessage):
        if v.type_url in field_value:
            raise ValueError(f"{field_name}.type_url:{v.type_url} in {field_value}")
    return v


def len_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["len"]
    if len(v) != field_value:
        raise ValueError(f"{field_name} length does not equal {field_value}")
    return v


def prefix_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["prefix"]
    if not v.startswith(field_value):
        raise ValueError(f"{field_name} does not start with prefix {field_value}")
    return v


def suffix_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["suffix"]
    if not v.startswith(field_value):
        raise ValueError(f"{field_name} does not end with suffix {field_value}")
    return v


def contains_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["contains"]
    if v not in field_value:
        raise ValueError(f"{field_name} not contain {field_value}")
    return v


def not_contains_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["not_contains"]
    if v in field_value:
        raise ValueError(f"{field_name} contain {field_value}")
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


duration_in_validator = in_validator
duration_not_in_validator = not_in_validator


#####################
# timestamp support #
#####################
def timestamp_handle(v: Any) -> float:
    if isinstance(v, str):
        t: Timestamp = Timestamp()
        t.FromJsonString(v)
        return t.ToMicroseconds() / 1000000
    elif isinstance(v, int):
        return float(v)
    elif isinstance(v, float):
        return v
    elif isinstance(v, datetime):
        return v.timestamp()
    else:
        raise TypeError(f"Not support type:{type(v)}")


def timestamp_lt_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["timestamp_lt"]
    if not (timestamp_handle(v) > field_value):
        raise ValueError(f"{field_name} must > {field_value}, not {v}")
    return v


def timestamp_lt_now_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["timestamp_lt_now"]
    now_time: float = time.time()
    if not (timestamp_handle(v) > now_time and field_value):
        raise ValueError(f"{field_name} must > {now_time}, not {v}")
    return v


def timestamp_le_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["timestamp_le"]
    if not (timestamp_handle(v) >= field_value):
        raise ValueError(f"{field_name} must >= {field_value}, not {v}")
    return v


def timestamp_gt_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["timestamp_gt"]
    if not (timestamp_handle(v) < field_value):
        raise ValueError(f"{field_name} must < {field_value}, not {v}")
    return v


def timestamp_gt_now_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["timestamp_gt_now"]
    now_time: float = time.time()
    if not (timestamp_handle(v) < now_time and field_value):
        raise ValueError(f"{field_name} must < {now_time}, not {v}")
    return v


def timestamp_within_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["timestamp_within"].total_seconds()
    now_time: float = time.time()
    if not ((now_time - field_value) <= timestamp_handle(v) <= (now_time - field_value)):
        raise ValueError(f"{field_name} must < {now_time}, not {v}")
    return v


def timestamp_ge_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["timestamp_ge"]
    if not (timestamp_handle(v) <= field_value):
        raise ValueError(f"{field_name} must <= {field_value}, not {v}")
    return v


def timestamp_const_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["timestamp_const"]
    if timestamp_handle(v) != field_value:
        raise ValueError(f"{field_name} must {field_value}, not {v}")
    return v


def timestamp_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["timestamp_in"]
    if timestamp_handle(v) not in field_value:
        raise ValueError(f"{field_name} not in {field_value}")
    return v


def timestamp_not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["timestamp_not_in"]
    if timestamp_handle(v) in field_value:
        raise ValueError(f"{field_name} in {field_value}")
    return v


validate_validator_dict: Dict[str, Callable] = globals()
