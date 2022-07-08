# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# gen timestamp:1657310807

import typing
from enum import IntEnum
from typing import Any

from pydantic import BaseModel, validator
from pydantic.fields import FieldInfo


def _in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["in"]
    if v not in field_value:
        raise ValueError(f"{field_name} not in {field_value}")
    return v


def _not_in_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["not_in"]
    if v in field_value:
        raise ValueError(f"{field_name} in {field_value}")
    return v


class FloatTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"not_in": [1.0, 2.0, 3.0]})
    ignore_test: float = FieldInfo(default=0.0)

    _in_validator_in_test = validator("in_test", allow_reuse=True)(_in_validator)
    _not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(_not_in_validator)


class DoubleTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    ignore_test: float = FieldInfo(default=0.0)

    _in_validator_in_test = validator("in_test", allow_reuse=True)(_in_validator)
    _in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(_in_validator)


class Int32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    _in_validator_in_test = validator("in_test", allow_reuse=True)(_in_validator)
    _in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(_in_validator)


class Uint32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    _in_validator_in_test = validator("in_test", allow_reuse=True)(_in_validator)
    _in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(_in_validator)


class Sfixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0)

    _in_validator_in_test = validator("in_test", allow_reuse=True)(_in_validator)
    _in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(_in_validator)


class Int64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    _in_validator_in_test = validator("in_test", allow_reuse=True)(_in_validator)
    _in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(_in_validator)


class Uint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    _in_validator_in_test = validator("in_test", allow_reuse=True)(_in_validator)
    _in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(_in_validator)


class Sfixed64Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0)

    _in_validator_in_test = validator("in_test", allow_reuse=True)(_in_validator)
    _in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(_in_validator)


class Fixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0)

    _in_validator_in_test = validator("in_test", allow_reuse=True)(_in_validator)
    _in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(_in_validator)


class Sint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    _in_validator_in_test = validator("in_test", allow_reuse=True)(_in_validator)
    _in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(_in_validator)


class BoolTest(BaseModel):
    bool_1_test: bool = FieldInfo(default=True, const=True)
    bool_2_test: bool = FieldInfo(default=False, const=True)


def _len_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["len"]
    if len(v) != field_value:
        raise ValueError(f"{field_name} length does not equal {field_value}")
    return v


def _prefix_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["prefix"]
    if not v.startswith(field_value):
        raise ValueError(f"{field_name} does not start with prefix {field_value}")
    return v


def _suffix_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["suffix"]
    if not v.startswith(field_value):
        raise ValueError(f"{field_name} does not end with suffix {field_value}")
    return v


def _contains_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["contains"]
    if v not in field_value:
        raise ValueError(f"{field_name} not contain {field_value}")
    return v


def _not_contains_validator(cls: Any, v: Any, **kwargs: Any) -> Any:
    field_name: str = kwargs["field"].name
    field_value: Any = kwargs["field"].field_info.extra["not_contains"]
    if v in field_value:
        raise ValueError(f"{field_name} contain {field_value}")
    return v


class StringTest(BaseModel):
    const_test: str = FieldInfo(default="aaa", const=True)
    len_test: str = FieldInfo(default="", extra={"len": 3})
    s_range_len_test: str = FieldInfo(default="", min_length=1, max_length=3)
    b_range_len_test: str = FieldInfo(default="")
    pattern_test: str = FieldInfo(default="", regex="^test")
    prefix_test: str = FieldInfo(default="", extra={"prefix": "prefix"})
    suffix_test: str = FieldInfo(default="", extra={"suffix": "suffix"})
    contains_test: str = FieldInfo(default="", extra={"contains": "contains"})
    not_contains_test: str = FieldInfo(default="", extra={"not_contains": "not_contains"})
    in_test: str = FieldInfo(default="", extra={"in": ["a", "b", "c"]})
    not_in_test: str = FieldInfo(default="", extra={"not_in": ["a", "b", "c"]})
    email_test: str = FieldInfo(default="")
    hostname_test: str = FieldInfo(default="")
    ip_test: str = FieldInfo(default="")
    ipv4_test: str = FieldInfo(default="")
    ipv6_test: str = FieldInfo(default="")
    uri_test: str = FieldInfo(default="")
    uri_ref_test: str = FieldInfo(default="")
    address_test: str = FieldInfo(default="")
    uuid_test: str = FieldInfo(default="")
    ignore_test: str = FieldInfo(default="")

    _len_validator_len_test = validator("len_test", allow_reuse=True)(_len_validator)
    _prefix_validator_prefix_test = validator("prefix_test", allow_reuse=True)(_prefix_validator)
    _suffix_validator_suffix_test = validator("suffix_test", allow_reuse=True)(_suffix_validator)
    _contains_validator_contains_test = validator("contains_test", allow_reuse=True)(_contains_validator)
    _not_contains_validator_not_contains_test = validator("not_contains_test", allow_reuse=True)(
        _not_contains_validator
    )
    _in_validator_in_test = validator("in_test", allow_reuse=True)(_in_validator)
    _not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(_not_in_validator)


class BytesTest(BaseModel):
    const_test: bytes = FieldInfo(default=b"demo", const=True)
    len_test: bytes = FieldInfo(default=b"", extra={"len": 4})
    range_len_test: bytes = FieldInfo(default=b"", min_length=1, max_length=4)
    pattern_test: bytes = FieldInfo(default=b"")
    prefix_test: bytes = FieldInfo(default=b"", extra={"prefix": b"prefix"})
    suffix_test: bytes = FieldInfo(default=b"", extra={"suffix": b"suffix"})
    contains_test: bytes = FieldInfo(default=b"", extra={"contains": b"contains"})
    in_test: bytes = FieldInfo(default=b"", extra={"in": [b"a", b"b", b"c"]})
    not_in_test: bytes = FieldInfo(default=b"", extra={"not_in": [b"a", b"b", b"c"]})

    _len_validator_len_test = validator("len_test", allow_reuse=True)(_len_validator)
    _prefix_validator_prefix_test = validator("prefix_test", allow_reuse=True)(_prefix_validator)
    _suffix_validator_suffix_test = validator("suffix_test", allow_reuse=True)(_suffix_validator)
    _contains_validator_contains_test = validator("contains_test", allow_reuse=True)(_contains_validator)
    _in_validator_in_test = validator("in_test", allow_reuse=True)(_in_validator)
    _not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(_not_in_validator)


class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class EnumTest(BaseModel):
    const_test: State = FieldInfo(default=0)
    defined_only_test: State = FieldInfo(default=0)
    in_test: State = FieldInfo(default=0)
    not_in_test: State = FieldInfo(default=0)


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = FieldInfo()
    no_parse_test: typing.Dict[str, int] = FieldInfo()
    keys_test: typing.Dict[str, int] = FieldInfo()
    values_test: typing.Dict[str, int] = FieldInfo()
    ignore_test: typing.Dict[str, int] = FieldInfo()


class MessageTest(BaseModel):
    skip_test: str = FieldInfo(default="")
    required_test: str = FieldInfo()


class RepeatedTest(BaseModel):
    range_test: typing.List[str] = FieldInfo()
    unique_test: typing.List[str] = FieldInfo()
    items_test: typing.List[str] = FieldInfo()
    ignore_test: typing.List[str] = FieldInfo()


class AnyMessage(BaseModel):
    type_url: str = FieldInfo(default="")
    value: bytes = FieldInfo(default=b"")


class AnyTest(BaseModel):
    required_test: AnyMessage = FieldInfo()
    x: AnyMessage = FieldInfo()


class Duration(BaseModel):
    seconds: int = FieldInfo(default=0)
    nanos: int = FieldInfo(default=0)


class DurationTest(BaseModel):
    required_test: Duration = FieldInfo()
    const_test: Duration = FieldInfo()
    range_test: Duration = FieldInfo()
    range_e_test: Duration = FieldInfo()
    in_test: Duration = FieldInfo()
    not_in_test: Duration = FieldInfo()


class TimestampTest(BaseModel):
    required_test: str = FieldInfo()
    const_test: str = FieldInfo()
    range_test: str = FieldInfo()
    range_e_test: str = FieldInfo()
    lt_now_test: str = FieldInfo()
    gt_now_test: str = FieldInfo()
    within_test: str = FieldInfo()
    within_and_gt_now_test: str = FieldInfo()


class MessageDisabledTest(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)


class MessageIgnoredTest(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
