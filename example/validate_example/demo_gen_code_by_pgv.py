# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# gen timestamp:1657275844

import typing
from enum import IntEnum

from pydantic import BaseModel
from pydantic.fields import FieldInfo


class FloatTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True, extra={})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={})
    in_test: float = FieldInfo(default=0.0, extra={})
    not_in_test: float = FieldInfo(default=0.0, extra={})
    ignore_test: float = FieldInfo(default=0.0, extra={})


class DoubleTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True, extra={})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={})
    in_test: float = FieldInfo(default=0.0, extra={})
    not_in_test: float = FieldInfo(default=0.0, extra={})
    ignore_test: float = FieldInfo(default=0.0, extra={})


class Int32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={})
    in_test: int = FieldInfo(default=0, extra={})
    not_in_test: int = FieldInfo(default=0, extra={})
    ignore_test: int = FieldInfo(default=0, extra={})


class Uint32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={})
    in_test: int = FieldInfo(default=0, extra={})
    not_in_test: int = FieldInfo(default=0, extra={})
    ignore_test: int = FieldInfo(default=0, extra={})


class Sfixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True, extra={})
    range_e_test: float = FieldInfo(default=0, ge=1, le=10, extra={})
    range_test: float = FieldInfo(default=0, gt=1, lt=10, extra={})
    in_test: float = FieldInfo(default=0, extra={})
    not_in_test: float = FieldInfo(default=0, extra={})
    ignore_test: float = FieldInfo(default=0, extra={})


class Int64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={})
    in_test: int = FieldInfo(default=0, extra={})
    not_in_test: int = FieldInfo(default=0, extra={})
    ignore_test: int = FieldInfo(default=0, extra={})


class Uint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={})
    in_test: int = FieldInfo(default=0, extra={})
    not_in_test: int = FieldInfo(default=0, extra={})
    ignore_test: int = FieldInfo(default=0, extra={})


class Sfixed64Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True, extra={})
    range_e_test: float = FieldInfo(default=0, ge=1, le=10, extra={})
    range_test: float = FieldInfo(default=0, gt=1, lt=10, extra={})
    in_test: float = FieldInfo(default=0, extra={})
    not_in_test: float = FieldInfo(default=0, extra={})
    ignore_test: float = FieldInfo(default=0, extra={})


class Fixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True, extra={})
    range_e_test: float = FieldInfo(default=0, ge=1, le=10, extra={})
    range_test: float = FieldInfo(default=0, gt=1, lt=10, extra={})
    in_test: float = FieldInfo(default=0, extra={})
    not_in_test: float = FieldInfo(default=0, extra={})
    ignore_test: float = FieldInfo(default=0, extra={})


class Sint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={})
    in_test: int = FieldInfo(default=0, extra={})
    not_in_test: int = FieldInfo(default=0, extra={})
    ignore_test: int = FieldInfo(default=0, extra={})


class BoolTest(BaseModel):
    bool_1_test: bool = FieldInfo(default=True, const=True, extra={})
    bool_2_test: bool = FieldInfo(default=False, const=True, extra={})


class StringTest(BaseModel):
    const_test: str = FieldInfo(default="aaa", const=True, extra={})
    len_test: str = FieldInfo(default="", extra={})
    s_range_len_test: str = FieldInfo(default="", min_length=1, max_length=3, extra={})
    b_range_len_test: str = FieldInfo(default="", extra={})
    pattern_test: str = FieldInfo(default="", regex="^test", extra={})
    prefix_test: str = FieldInfo(default="", extra={})
    suffix_test: str = FieldInfo(default="", extra={})
    contains_test: str = FieldInfo(default="", extra={})
    not_contains_test: str = FieldInfo(default="", extra={})
    in_test: str = FieldInfo(default="", extra={})
    not_in_test: str = FieldInfo(default="", extra={})
    email_test: str = FieldInfo(default="", extra={})
    hostname_test: str = FieldInfo(default="", extra={})
    ip_test: str = FieldInfo(default="", extra={})
    ipv4_test: str = FieldInfo(default="", extra={})
    ipv6_test: str = FieldInfo(default="", extra={})
    uri_test: str = FieldInfo(default="", extra={})
    uri_ref_test: str = FieldInfo(default="", extra={})
    address_test: str = FieldInfo(default="", extra={})
    uuid_test: str = FieldInfo(default="", extra={})
    ignore_test: str = FieldInfo(default="", extra={})


class BytesTest(BaseModel):
    const_test: bytes = FieldInfo(default=b"demo", const=True, extra={})
    len_test: bytes = FieldInfo(default=b"", extra={})
    range_len_test: bytes = FieldInfo(default=b"", min_length=1, max_length=4, extra={})
    pattern_test: bytes = FieldInfo(default=b"", extra={})
    prefix_test: bytes = FieldInfo(default=b"", extra={})
    suffix_test: bytes = FieldInfo(default=b"", extra={})
    contains_test: bytes = FieldInfo(default=b"", extra={})
    in_test: bytes = FieldInfo(default=b"", extra={})
    not_in_test: bytes = FieldInfo(default=b"", extra={})


class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class EnumTest(BaseModel):
    const_test: State = FieldInfo(default=0, extra={})
    defined_only_test: State = FieldInfo(default=0, extra={})
    in_test: State = FieldInfo(default=0, extra={})
    not_in_test: State = FieldInfo(default=0, extra={})


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = FieldInfo(extra={})
    no_parse_test: typing.Dict[str, int] = FieldInfo(extra={})
    keys_test: typing.Dict[str, int] = FieldInfo(extra={})
    values_test: typing.Dict[str, int] = FieldInfo(extra={})
    ignore_test: typing.Dict[str, int] = FieldInfo(extra={})


class MessageTest(BaseModel):
    skip_test: str = FieldInfo(default="", extra={})
    required_test: str = FieldInfo(extra={})


class RepeatedTest(BaseModel):
    range_test: typing.List[str] = FieldInfo(extra={})
    unique_test: typing.List[str] = FieldInfo(extra={})
    items_test: typing.List[str] = FieldInfo(extra={})
    ignore_test: typing.List[str] = FieldInfo(extra={})


class Any(BaseModel):
    type_url: str = FieldInfo(default="", extra={})
    value: bytes = FieldInfo(default=b"", extra={})


class AnyTest(BaseModel):
    required_test: Any = FieldInfo(extra={})
    x: Any = FieldInfo(extra={})


class Duration(BaseModel):
    seconds: int = FieldInfo(default=0, extra={})
    nanos: int = FieldInfo(default=0, extra={})


class DurationTest(BaseModel):
    required_test: Duration = FieldInfo(extra={})
    const_test: Duration = FieldInfo(extra={})
    range_test: Duration = FieldInfo(extra={})
    range_e_test: Duration = FieldInfo(extra={})
    in_test: Duration = FieldInfo(extra={})
    not_in_test: Duration = FieldInfo(extra={})


class TimestampTest(BaseModel):
    required_test: str = FieldInfo(extra={})
    const_test: str = FieldInfo(extra={})
    range_test: str = FieldInfo(extra={})
    range_e_test: str = FieldInfo(extra={})
    lt_now_test: str = FieldInfo(extra={})
    gt_now_test: str = FieldInfo(extra={})
    within_test: str = FieldInfo(extra={})
    within_and_gt_now_test: str = FieldInfo(extra={})


class MessageDisabledTest(BaseModel):
    const_test: int = FieldInfo(default=0, extra={})
    range_e_test: int = FieldInfo(default=0, extra={})
    range_test: int = FieldInfo(default=0, extra={})


class MessageIgnoredTest(BaseModel):
    const_test: int = FieldInfo(default=0, extra={})
    range_e_test: int = FieldInfo(default=0, extra={})
    range_test: int = FieldInfo(default=0, extra={})
