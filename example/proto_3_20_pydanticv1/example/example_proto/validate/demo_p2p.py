# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.0.2](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 1.10.7
import typing
from datetime import datetime, timedelta
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID

from google.protobuf.any_pb2 import Any  # type: ignore
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field, root_validator, validator
from pydantic.networks import AnyUrl, EmailStr, IPvAnyAddress
from pydantic.types import conbytes, confloat, conint, conlist, constr

from protobuf_to_pydantic.customer_con_type.v1 import contimedelta, contimestamp
from protobuf_to_pydantic.customer_validator import check_one_of
from protobuf_to_pydantic.customer_validator.v1 import (
    any_in_validator,
    any_not_in_validator,
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


class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class FloatTest(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = Field(default=1.0, const=True)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    ignore_test: float = Field(default=0.0)


class DoubleTest(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = Field(default=1.0, const=True)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    ignore_test: float = Field(default=0.0)


class Int32Test(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)


class Uint32Test(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)


class Sint32Test(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)


class Int64Test(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)


class Uint64Test(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)


class Sint64Test(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)


class Fixed32Test(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = Field(default=1, const=True)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0.0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0.0)


class Fixed64Test(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = Field(default=1, const=True)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0.0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0.0)


class Sfixed32Test(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = Field(default=1, const=True)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0.0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0.0)


class Sfixed64Test(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = Field(default=1, const=True)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0.0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0.0)


class BoolTest(BaseModel):
    bool_1_test: bool = Field(default=True, const=True)
    bool_2_test: bool = Field(default=False, const=True)


class StringTest(BaseModel):
    len_test_len_validator = validator("len_test", allow_reuse=True)(len_validator)
    prefix_test_prefix_validator = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_test_suffix_validator = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_test_contains_validator = validator("contains_test", allow_reuse=True)(contains_validator)
    not_contains_test_not_contains_validator = validator("not_contains_test", allow_reuse=True)(not_contains_validator)
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: str = Field(default="aaa", const=True)
    len_test: str = Field(default="", len=3)
    s_range_len_test: str = Field(default="", min_length=1, max_length=3)
    b_range_len_test: str = Field(default="")
    pattern_test: str = Field(default="", regex="^test")
    prefix_test: str = Field(default="", prefix="prefix")
    suffix_test: str = Field(default="", suffix="suffix")
    contains_test: str = Field(default="", contains="contains")
    not_contains_test: str = Field(default="", not_contains="not_contains")
    in_test: str = Field(default="", in_=["a", "b", "c"])
    not_in_test: str = Field(default="", not_in=["a", "b", "c"])
    email_test: EmailStr = Field(default="")
    hostname_test: HostNameStr = Field(default="")
    ip_test: IPvAnyAddress = Field(default="")
    ipv4_test: IPv4Address = Field(default="")
    ipv6_test: IPv6Address = Field(default="")
    uri_test: AnyUrl = Field(default="")
    uri_ref_test: UriRefStr = Field(default="")
    address_test: IPvAnyAddress = Field(default="")
    uuid_test: UUID = Field(default="")
    ignore_test: str = Field(default="")


class BytesTest(BaseModel):
    len_test_len_validator = validator("len_test", allow_reuse=True)(len_validator)
    prefix_test_prefix_validator = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_test_suffix_validator = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_test_contains_validator = validator("contains_test", allow_reuse=True)(contains_validator)
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: bytes = Field(default=b"demo", const=True)
    len_test: bytes = Field(default=b"", len=4)
    range_len_test: bytes = Field(default=b"", min_length=1, max_length=4)
    pattern_test: bytes = Field(default=b"")
    prefix_test: bytes = Field(default=b"", prefix=b"prefix")
    suffix_test: bytes = Field(default=b"", suffix=b"suffix")
    contains_test: bytes = Field(default=b"", contains=b"contains")
    in_test: bytes = Field(default=b"", in_=[b"a", b"b", b"c"])
    not_in_test: bytes = Field(default=b"", not_in=[b"a", b"b", b"c"])


class EnumTest(BaseModel):
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: State = Field(default=2, const=True)
    defined_only_test: State = Field(default=0)
    in_test: State = Field(default=0, in_=[0, 2])
    not_in_test: State = Field(default=0, not_in=[0, 2])


class MapTest(BaseModel):
    pair_test_map_min_pairs_validator = validator("pair_test", allow_reuse=True)(map_min_pairs_validator)
    pair_test_map_max_pairs_validator = validator("pair_test", allow_reuse=True)(map_max_pairs_validator)

    pair_test: typing.Dict[str, int] = Field(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    no_parse_test: typing.Dict[str, int] = Field(default_factory=dict)
    keys_test: typing.Dict[constr(min_length=1, max_length=5), int] = Field(default_factory=dict)
    values_test: typing.Dict[str, conint(ge=5, le=5)] = Field(default_factory=dict)
    keys_values_test: typing.Dict[constr(min_length=1, max_length=5), contimestamp(timestamp_gt_now=True)] = Field(
        default_factory=dict
    )
    ignore_test: typing.Dict[str, int] = Field(default_factory=dict)


class MessageTest(BaseModel):
    skip_test: str = Field(default="")
    required_test: str = Field()


class RepeatedTest(BaseModel):
    range_test: typing.List[str] = Field(default_factory=list, min_items=1, max_items=5)
    unique_test: typing.List[str] = Field(default_factory=list, unique_items=True)
    items_string_test: conlist(item_type=constr(min_length=1, max_length=5), min_items=1, max_items=5) = Field(
        default_factory=list
    )
    items_double_test: conlist(item_type=confloat(gt=1, lt=5), min_items=1, max_items=5) = Field(default_factory=list)
    items_int32_test: conlist(item_type=conint(gt=1, lt=5), min_items=1, max_items=5) = Field(default_factory=list)
    items_timestamp_test: conlist(
        item_type=contimestamp(timestamp_gt=1600000000.0, timestamp_lt=1600000010.0), min_items=1, max_items=5
    ) = Field(default_factory=list)
    items_duration_test: conlist(
        item_type=contimedelta(duration_gt=timedelta(seconds=10), duration_lt=timedelta(seconds=20)),
        min_items=1,
        max_items=5,
    ) = Field(default_factory=list)
    items_bytes_test: conlist(item_type=conbytes(min_length=1, max_length=5), min_items=1, max_items=5) = Field(
        default_factory=list
    )
    ignore_test: typing.List[str] = Field(default_factory=list)


class AnyTest(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    not_in_test_any_not_in_validator = validator("not_in_test", allow_reuse=True)(any_not_in_validator)
    in_test_any_in_validator = validator("in_test", allow_reuse=True)(any_in_validator)

    required_test: Any = Field()
    not_in_test: Any = Field(
        default_factory=Any,
        any_not_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )
    in_test: Any = Field(
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

    required_test: Timedelta = Field()
    const_test: Timedelta = Field(default_factory=timedelta, duration_const=timedelta(seconds=1, microseconds=500000))
    range_test: Timedelta = Field(
        default_factory=timedelta,
        duration_lt=timedelta(seconds=10, microseconds=500000),
        duration_gt=timedelta(seconds=5, microseconds=500000),
    )
    range_e_test: Timedelta = Field(
        default_factory=timedelta,
        duration_le=timedelta(seconds=10, microseconds=500000),
        duration_ge=timedelta(seconds=5, microseconds=500000),
    )
    in_test: Timedelta = Field(
        default_factory=timedelta,
        duration_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    not_in_test: Timedelta = Field(
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

    required_test: datetime = Field()
    const_test: datetime = Field(default_factory=datetime.now, timestamp_const=1600000000.0)
    range_test: datetime = Field(default_factory=datetime.now, timestamp_lt=1600000010.0, timestamp_gt=1600000000.0)
    range_e_test: datetime = Field(default_factory=datetime.now, timestamp_le=1600000010.0, timestamp_ge=1600000000.0)
    lt_now_test: datetime = Field(default_factory=datetime.now, timestamp_lt_now=True)
    gt_now_test: datetime = Field(default_factory=datetime.now, timestamp_gt_now=True)
    within_test: datetime = Field(default_factory=datetime.now, timestamp_within=timedelta(seconds=1))
    within_and_gt_now_test: datetime = Field(
        default_factory=datetime.now, timestamp_gt_now=True, timestamp_within=timedelta(seconds=3600)
    )


class MessageDisabledTest(BaseModel):
    const_test: int = Field(default=0)
    range_e_test: int = Field(default=0)
    range_test: int = Field(default=0)


class MessageIgnoredTest(BaseModel):
    const_test: int = Field(default=0)
    range_e_test: int = Field(default=0)
    range_test: int = Field(default=0)


class OneOfTest(BaseModel):
    _one_of_dict = {"OneOfTest.id": {"fields": {"x", "y"}, "required": True}}
    one_of_validator = root_validator(pre=True, allow_reuse=True)(check_one_of)

    header: str = Field(default="")
    x: str = Field(default="")
    y: int = Field(default=0)


class OneOfNotTest(BaseModel):
    _one_of_dict = {"OneOfNotTest.id": {"fields": {"x", "y"}}}
    one_of_validator = root_validator(pre=True, allow_reuse=True)(check_one_of)

    header: str = Field(default="")
    x: str = Field(default="")
    y: int = Field(default=0)


class AfterReferMessage(BaseModel):
    uid: str = Field(default="", min_length=1)
    age: int = Field(default=0, ge=0, lt=500)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        exp_timestamp_gt_now_validator = validator("exp", allow_reuse=True)(timestamp_gt_now_validator)

        bank_number: str = Field(default="", min_length=13, max_length=19)
        exp: datetime = Field(default_factory=datetime.now, timestamp_gt_now=True)
        uuid: UUID = Field(default="")

    class NotEnableUserPayMessage(BaseModel):
        bank_number: str = Field(default="")
        exp: datetime = Field(default_factory=datetime.now)
        uuid: str = Field(default="")

    string_in_map_test: typing.Dict[str, StringTest] = Field(default_factory=dict)
    map_in_map_test: typing.Dict[str, MapTest] = Field(default_factory=dict)
    user_pay: UserPayMessage = Field()
    not_enable_user_pay: NotEnableUserPayMessage = Field()
    empty: None = Field()
    after_refer: AfterReferMessage = Field()
