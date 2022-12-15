# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

import typing
from datetime import datetime, timedelta
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID

from google.protobuf.any_pb2 import Any  # type: ignore
from google.protobuf.message import Message  # type: ignore
from protobuf_to_pydantic.customer_con_type import contimedelta, contimestamp
from protobuf_to_pydantic.customer_validator import (
    any_in_validator,
    any_not_in_validator,
    check_one_of,
    contains_validator,
    duration_const_validator,
    duration_ge_validator,
    duration_gt_validator,
    duration_in_validator,
    duration_le_validator,
    duration_lt_validator,
    duration_not_in_validator,
    in_validator,
    len_validator,
    map_max_pairs_validator,
    map_min_pairs_validator,
    not_contains_validator,
    not_in_validator,
    prefix_validator,
    suffix_validator,
    timestamp_const_validator,
    timestamp_ge_validator,
    timestamp_gt_now_validator,
    timestamp_gt_validator,
    timestamp_le_validator,
    timestamp_lt_now_validator,
    timestamp_lt_validator,
    timestamp_within_validator,
)
from protobuf_to_pydantic.get_desc.from_pb_option.types import HostNameStr, UriRefStr
from protobuf_to_pydantic.util import Timedelta
from pydantic import BaseModel, root_validator, validator
from pydantic.fields import FieldInfo
from pydantic.networks import AnyUrl, EmailStr, IPvAnyAddress
from pydantic.types import conbytes, confloat, conint, conlist, constr


class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class FloatTest(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = FieldInfo(default=0.0, not_in=[1.0, 2.0, 3.0])
    ignore_test: float = FieldInfo(default=0.0)


class DoubleTest(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = FieldInfo(default=0.0, not_in=[1.0, 2.0, 3.0])
    ignore_test: float = FieldInfo(default=0.0)


class Int32Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: int = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: int = FieldInfo(default=0)


class Uint32Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: int = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: int = FieldInfo(default=0)


class Sint32Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: int = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: int = FieldInfo(default=0)


class Int64Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: int = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: int = FieldInfo(default=0)


class Uint64Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: int = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: int = FieldInfo(default=0)


class Sint64Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: int = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: int = FieldInfo(default=0)


class Fixed32Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, in_=[1, 2, 3])
    not_in_test: float = FieldInfo(default=0.0, not_in=[1, 2, 3])
    ignore_test: float = FieldInfo(default=0.0)


class Fixed64Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, in_=[1, 2, 3])
    not_in_test: float = FieldInfo(default=0.0, not_in=[1, 2, 3])
    ignore_test: float = FieldInfo(default=0.0)


class Sfixed32Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, in_=[1, 2, 3])
    not_in_test: float = FieldInfo(default=0.0, not_in=[1, 2, 3])
    ignore_test: float = FieldInfo(default=0.0)


class Sfixed64Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, in_=[1, 2, 3])
    not_in_test: float = FieldInfo(default=0.0, not_in=[1, 2, 3])
    ignore_test: float = FieldInfo(default=0.0)


class BoolTest(BaseModel):

    bool_1_test: bool = FieldInfo(default=True, const=True)
    bool_2_test: bool = FieldInfo(default=False, const=True)


class StringTest(BaseModel):

    len_test_len_validator = validator("len_test", allow_reuse=True)(len_validator)
    prefix_test_prefix_validator = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_test_suffix_validator = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_test_contains_validator = validator("contains_test", allow_reuse=True)(contains_validator)
    not_contains_test_not_contains_validator = validator("not_contains_test", allow_reuse=True)(not_contains_validator)
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: str = FieldInfo(default="aaa", const=True)
    len_test: str = FieldInfo(default="", len=3)
    s_range_len_test: str = FieldInfo(default="", min_length=1, max_length=3)
    b_range_len_test: str = FieldInfo(default="")
    pattern_test: str = FieldInfo(default="", regex="^test")
    prefix_test: str = FieldInfo(default="", prefix="prefix")
    suffix_test: str = FieldInfo(default="", suffix="suffix")
    contains_test: str = FieldInfo(default="", contains="contains")
    not_contains_test: str = FieldInfo(default="", not_contains="not_contains")
    in_test: str = FieldInfo(default="", in_=["a", "b", "c"])
    not_in_test: str = FieldInfo(default="", not_in=["a", "b", "c"])
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


class BytesTest(BaseModel):

    len_test_len_validator = validator("len_test", allow_reuse=True)(len_validator)
    prefix_test_prefix_validator = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_test_suffix_validator = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_test_contains_validator = validator("contains_test", allow_reuse=True)(contains_validator)
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: bytes = FieldInfo(default=b"demo", const=True)
    len_test: bytes = FieldInfo(default=b"", len=4)
    range_len_test: bytes = FieldInfo(default=b"", min_length=1, max_length=4)
    pattern_test: bytes = FieldInfo(default=b"")
    prefix_test: bytes = FieldInfo(default=b"", prefix=b"prefix")
    suffix_test: bytes = FieldInfo(default=b"", suffix=b"suffix")
    contains_test: bytes = FieldInfo(default=b"", contains=b"contains")
    in_test: bytes = FieldInfo(default=b"", in_=[b"a", b"b", b"c"])
    not_in_test: bytes = FieldInfo(default=b"", not_in=[b"a", b"b", b"c"])


class EnumTest(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: "State" = FieldInfo(default=2, const=True)
    defined_only_test: "State" = FieldInfo(default=0)
    in_test: "State" = FieldInfo(default=0, in_=[0, 2])
    not_in_test: "State" = FieldInfo(default=0, not_in=[0, 2])


class MapTest(BaseModel):

    pair_test_map_min_pairs_validator = validator("pair_test", allow_reuse=True)(map_min_pairs_validator)
    pair_test_map_max_pairs_validator = validator("pair_test", allow_reuse=True)(map_max_pairs_validator)

    pair_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    no_parse_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    keys_test: typing.Dict[constr(min_length=1, max_length=5), int] = FieldInfo(default_factory=dict)
    values_test: typing.Dict[str, conint(ge=5, le=5)] = FieldInfo(default_factory=dict)
    keys_values_test: typing.Dict[constr(min_length=1, max_length=5), contimestamp(timestamp_gt_now=True)] = FieldInfo(
        default_factory=dict
    )
    ignore_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)


class MessageTest(BaseModel):

    skip_test: str = FieldInfo(default="")
    required_test: str = FieldInfo()


class RepeatedTest(BaseModel):

    range_test: typing.List[str] = FieldInfo(default_factory=list, min_items=1, max_items=5)
    unique_test: typing.List[str] = FieldInfo(default_factory=list, unique_items=True)
    items_string_test: conlist(item_type=constr(min_length=1, max_length=5), min_items=1, max_items=5) = FieldInfo(
        default_factory=list
    )
    items_double_test: conlist(item_type=confloat(gt=1, lt=5), min_items=1, max_items=5) = FieldInfo(
        default_factory=list
    )
    items_int32_test: conlist(item_type=conint(gt=1, lt=5), min_items=1, max_items=5) = FieldInfo(default_factory=list)
    items_timestamp_test: conlist(
        item_type=contimestamp(timestamp_gt=1600000000.0, timestamp_lt=1600000010.0), min_items=1, max_items=5
    ) = FieldInfo(default_factory=list)
    items_duration_test: conlist(
        item_type=contimedelta(duration_gt=timedelta(seconds=10), duration_lt=timedelta(seconds=20)),
        min_items=1,
        max_items=5,
    ) = FieldInfo(default_factory=list)
    items_bytes_test: conlist(item_type=conbytes(min_length=1, max_length=5), min_items=1, max_items=5) = FieldInfo(
        default_factory=list
    )
    ignore_test: typing.List[str] = FieldInfo(default_factory=list)


class AnyTest(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    not_in_test_any_not_in_validator = validator("not_in_test", allow_reuse=True)(any_not_in_validator)
    in_test_any_in_validator = validator("in_test", allow_reuse=True)(any_in_validator)

    required_test: Any = FieldInfo()
    not_in_test: Any = FieldInfo(
        default_factory=Any,
        any_not_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )
    in_test: Any = FieldInfo(
        default_factory=Any,
        any_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )


class DurationTest(BaseModel):

    const_test_duration_const_validator = validator("const_test", allow_reuse=True)(duration_const_validator)
    range_test_duration_lt_validator = validator("range_test", allow_reuse=True)(duration_lt_validator)
    range_test_duration_gt_validator = validator("range_test", allow_reuse=True)(duration_gt_validator)
    range_e_test_duration_le_validator = validator("range_e_test", allow_reuse=True)(duration_le_validator)
    range_e_test_duration_ge_validator = validator("range_e_test", allow_reuse=True)(duration_ge_validator)
    in_test_duration_in_validator = validator("in_test", allow_reuse=True)(duration_in_validator)
    not_in_test_duration_not_in_validator = validator("not_in_test", allow_reuse=True)(duration_not_in_validator)

    required_test: Timedelta = FieldInfo()
    const_test: Timedelta = FieldInfo(
        default_factory=timedelta, duration_const=timedelta(seconds=1, microseconds=500000)
    )
    range_test: Timedelta = FieldInfo(
        default_factory=timedelta,
        duration_lt=timedelta(seconds=10, microseconds=500000),
        duration_gt=timedelta(seconds=5, microseconds=500000),
    )
    range_e_test: Timedelta = FieldInfo(
        default_factory=timedelta,
        duration_le=timedelta(seconds=10, microseconds=500000),
        duration_ge=timedelta(seconds=5, microseconds=500000),
    )
    in_test: Timedelta = FieldInfo(
        default_factory=timedelta,
        duration_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    not_in_test: Timedelta = FieldInfo(
        default_factory=timedelta,
        duration_not_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )


class TimestampTest(BaseModel):

    const_test_timestamp_const_validator = validator("const_test", allow_reuse=True)(timestamp_const_validator)
    range_test_timestamp_lt_validator = validator("range_test", allow_reuse=True)(timestamp_lt_validator)
    range_test_timestamp_gt_validator = validator("range_test", allow_reuse=True)(timestamp_gt_validator)
    range_e_test_timestamp_le_validator = validator("range_e_test", allow_reuse=True)(timestamp_le_validator)
    range_e_test_timestamp_ge_validator = validator("range_e_test", allow_reuse=True)(timestamp_ge_validator)
    lt_now_test_timestamp_lt_now_validator = validator("lt_now_test", allow_reuse=True)(timestamp_lt_now_validator)
    gt_now_test_timestamp_gt_now_validator = validator("gt_now_test", allow_reuse=True)(timestamp_gt_now_validator)
    within_test_timestamp_within_validator = validator("within_test", allow_reuse=True)(timestamp_within_validator)
    within_and_gt_now_test_timestamp_gt_now_validator = validator("within_and_gt_now_test", allow_reuse=True)(
        timestamp_gt_now_validator
    )
    within_and_gt_now_test_timestamp_within_validator = validator("within_and_gt_now_test", allow_reuse=True)(
        timestamp_within_validator
    )

    required_test: datetime = FieldInfo()
    const_test: datetime = FieldInfo(default_factory=datetime.now, timestamp_const=1600000000.0)
    range_test: datetime = FieldInfo(default_factory=datetime.now, timestamp_lt=1600000010.0, timestamp_gt=1600000000.0)
    range_e_test: datetime = FieldInfo(
        default_factory=datetime.now, timestamp_le=1600000010.0, timestamp_ge=1600000000.0
    )
    lt_now_test: datetime = FieldInfo(default_factory=datetime.now, timestamp_lt_now=True)
    gt_now_test: datetime = FieldInfo(default_factory=datetime.now, timestamp_gt_now=True)
    within_test: datetime = FieldInfo(default_factory=datetime.now, timestamp_within=timedelta(seconds=1))
    within_and_gt_now_test: datetime = FieldInfo(
        default_factory=datetime.now, timestamp_gt_now=True, timestamp_within=timedelta(seconds=3600)
    )


class MessageDisabledTest(BaseModel):

    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)


class MessageIgnoredTest(BaseModel):

    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)


class OneOfTest(BaseModel):

    _one_of_dict = {"OneOfTest.id": {"fields": {"x", "y"}, "required": True}}
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    header: str = FieldInfo(default="")
    x: str = FieldInfo(default="")
    y: int = FieldInfo(default=0)


class OneOfNotTest(BaseModel):

    _one_of_dict = {"OneOfNotTest.id": {"fields": {"x", "y"}}}
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    header: str = FieldInfo(default="")
    x: str = FieldInfo(default="")
    y: int = FieldInfo(default=0)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):

        exp_timestamp_gt_now_validator = validator("exp", allow_reuse=True)(timestamp_gt_now_validator)

        bank_number: str = FieldInfo(default="", min_length=13, max_length=19)
        exp: datetime = FieldInfo(default_factory=datetime.now, timestamp_gt_now=True)
        uuid: UUID = FieldInfo(default="")

    class NotEnableUserPayMessage(BaseModel):

        bank_number: str = FieldInfo(default="")
        exp: datetime = FieldInfo(default_factory=datetime.now)
        uuid: str = FieldInfo(default="")

    string_in_map_test: typing.Dict[str, StringTest] = FieldInfo(default_factory=dict)
    map_in_map_test: typing.Dict[str, MapTest] = FieldInfo(default_factory=dict)
    user_pay: UserPayMessage = FieldInfo()
    not_enable_user_pay: NotEnableUserPayMessage = FieldInfo()
    empty: None = FieldInfo()
