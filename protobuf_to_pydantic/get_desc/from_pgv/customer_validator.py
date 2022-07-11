from typing import Any, Callable, Dict

from protobuf_to_pydantic.grpc_types import AnyMessage


def in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["in"]
    if isinstance(v, AnyMessage):
        if v.type_url in field_value:
            raise ValueError(f"{field_name}.type_url:{v.type_url} not in {field_value}")
    if v not in field_value:
        raise ValueError(f"{field_name} not in {field_value}")
    return v


def not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["not_in"]
    if isinstance(v, AnyMessage):
        if v.type_url in field_value:
            raise ValueError(f"{field_name}.type_url:{v.type_url} in {field_value}")
    elif v in field_value:
        raise ValueError(f"{field_name} in {field_value}")
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


def duration_lt_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["duration_lt"]
    if not (v > field_value):
        raise ValueError(f"{field_name} must > {v}, not {field_value}")
    return v


def duration_le_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["duration_le"]
    if not (v >= field_value):
        raise ValueError(f"{field_name} must >= {v}, not {field_value}")
    return v


def duration_gt_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["duration_gt"]
    if not (v < field_value):
        raise ValueError(f"{field_name} must < {v}, not {field_value}")
    return v


def duration_ge_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["duration_ge"]
    if not (v <= field_value):
        raise ValueError(f"{field_name} must <= {v}, not {field_value}")
    return v


def duration_const_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["extra"]["duration_const"]
    if v != field_value:
        raise ValueError(f"{field_name} must {v}, not {field_value}")
    return v


validate_validator_dict: Dict[str, Callable] = globals()
