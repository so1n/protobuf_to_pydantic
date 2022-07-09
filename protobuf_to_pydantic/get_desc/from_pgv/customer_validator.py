from typing import Any, Callable, Dict


def in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["in"]
    if v not in field_value:
        raise ValueError(f"{field_name} not in {field_value}")
    return v


def not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["not_in"]
    if v in field_value:
        raise ValueError(f"{field_name} in {field_value}")
    return v


def len_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["len"]
    if len(v) != field_value:
        raise ValueError(f"{field_name} length does not equal {field_value}")
    return v


def prefix_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["prefix"]
    if not v.startswith(field_value):
        raise ValueError(f"{field_name} does not start with prefix {field_value}")
    return v


def suffix_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["suffix"]
    if not v.startswith(field_value):
        raise ValueError(f"{field_name} does not end with suffix {field_value}")
    return v


def contains_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["contains"]
    if v not in field_value:
        raise ValueError(f"{field_name} not contain {field_value}")
    return v


def not_contains_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["not_contains"]
    if v in field_value:
        raise ValueError(f"{field_name} contain {field_value}")
    return v


validate_validator_dict: Dict[str, Callable] = globals()
