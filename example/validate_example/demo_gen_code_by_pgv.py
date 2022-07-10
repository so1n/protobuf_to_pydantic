# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# gen timestamp:1657445118

import typing
from datetime import timedelta
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID

from pydantic import BaseModel, validator
from pydantic.fields import FieldInfo
from pydantic.networks import AnyUrl, EmailStr, IPvAnyAddress

from protobuf_to_pydantic.get_desc.from_pgv.customer_validator import (
    contains_validator,
    duration_const_validator,
    duration_ge_validator,
    duration_gt_validator,
    duration_le_validator,
    duration_lt_validator,
    in_validator,
    len_validator,
    not_contains_validator,
    not_in_validator,
    prefix_validator,
    suffix_validator,
)
from protobuf_to_pydantic.get_desc.from_pgv.types import HostNameStr, UriRefStr


class FloatTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"not_in": [1.0, 2.0, 3.0]})
    ignore_test: float = FieldInfo(default=0.0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class DoubleTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    ignore_test: float = FieldInfo(default=0.0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


class Int32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


class Uint32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


class Sfixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


class Int64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


class Uint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


class Sfixed64Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


class Fixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


class Sint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


class BoolTest(BaseModel):
    bool_1_test: bool = FieldInfo(default=True, const=True)
    bool_2_test: bool = FieldInfo(default=False, const=True)


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
    email_test: EmailStr = FieldInfo(default="")
    hostname_test: HostNameStr = FieldInfo(default="")
    ip_test: IPvAnyAddress = FieldInfo(default="")
    ipv4_test: IPv4Address = FieldInfo(default="")
    ipv6_test: IPv6Address = FieldInfo(default="")
    uri_test: AnyUrl = FieldInfo(default="")
    uri_ref_test: UriRefStr = FieldInfo(default="")
    address_test: IPvAnyAddress = FieldInfo(default="")
    uuid_test: UUID = FieldInfo(default="")
    ignore_test: str = FieldInfo(default="")

    len_validator_len_test = validator("len_test", allow_reuse=True)(len_validator)
    prefix_validator_prefix_test = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_validator_suffix_test = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_validator_contains_test = validator("contains_test", allow_reuse=True)(contains_validator)
    not_contains_validator_not_contains_test = validator("not_contains_test", allow_reuse=True)(not_contains_validator)
    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


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

    len_validator_len_test = validator("len_test", allow_reuse=True)(len_validator)
    prefix_validator_prefix_test = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_validator_suffix_test = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_validator_contains_test = validator("contains_test", allow_reuse=True)(contains_validator)
    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class EnumTest(BaseModel):
    const_test: State = FieldInfo(default=2, const=True)
    defined_only_test: State = FieldInfo(default=0)
    in_test: State = FieldInfo(default=0, extra={"in": [0, 2]})
    not_in_test: State = FieldInfo(default=0, extra={"in": [0, 2]})

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


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


class DurationTest(BaseModel):
    required_test: timedelta = FieldInfo()
    const_test: timedelta = FieldInfo(extra={"duration_const": 1500000})
    range_test: timedelta = FieldInfo(extra={"duration_lt": 10500000, "duration_gt": 5500000})
    range_e_test: timedelta = FieldInfo(extra={"duration_le": 10500000, "duration_ge": 5500000})
    in_test: timedelta = FieldInfo(
        extra={"in": [timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)]}
    )
    not_in_test: timedelta = FieldInfo(
        extra={"in": [timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)]}
    )

    duration_const_validator_const_test = validator("const_test", allow_reuse=True)(duration_const_validator)
    duration_lt_validator_range_test = validator("range_test", allow_reuse=True)(duration_lt_validator)
    duration_gt_validator_range_test = validator("range_test", allow_reuse=True)(duration_gt_validator)
    duration_le_validator_range_e_test = validator("range_e_test", allow_reuse=True)(duration_le_validator)
    duration_ge_validator_range_e_test = validator("range_e_test", allow_reuse=True)(duration_ge_validator)
    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


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


class UserPayMessage(BaseModel):
    bank_number: str = FieldInfo(default="")
    exp: str = FieldInfo()
    uuid: str = FieldInfo(default="")


class NestedMessage(BaseModel):
    string_in_map_test: typing.Dict[str, StringTest] = FieldInfo()
    map_in_map_test: typing.Dict[str, MapTest] = FieldInfo()
    user_pay: UserPayMessage = FieldInfo()
    empty: None = FieldInfo()
