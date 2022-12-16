# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

import typing
from datetime import datetime, timedelta
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID

from google.protobuf.any_pb2 import Any  # type: ignore
from pydantic import BaseModel, root_validator, validator
from pydantic.fields import FieldInfo
from pydantic.networks import AnyUrl, EmailStr, IPvAnyAddress
from pydantic.types import conbytes, confloat, conint, conlist, constr

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


class FloatTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = FieldInfo(default=0.0, not_in=[1.0, 2.0, 3.0])
    ignore_test: float = FieldInfo(default=0.0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class DoubleTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = FieldInfo(default=0.0, not_in=[1.0, 2.0, 3.0])
    ignore_test: float = FieldInfo(default=0.0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Int32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: int = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Uint32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: int = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Sfixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: float = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: float = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Int64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: int = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Sint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: int = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Uint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: int = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Sfixed64Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: float = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: float = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Fixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: float = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: float = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Fixed64Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, in_=[1, 2, 3])
    not_in_test: float = FieldInfo(default=0, not_in=[1, 2, 3])
    ignore_test: float = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class BoolTest(BaseModel):
    bool_1_test: bool = FieldInfo(default=True, const=True)
    bool_2_test: bool = FieldInfo(default=False, const=True)


class StringTest(BaseModel):
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

    len_validator_len_test = validator("len_test", allow_reuse=True)(len_validator)
    prefix_validator_prefix_test = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_validator_suffix_test = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_validator_contains_test = validator("contains_test", allow_reuse=True)(contains_validator)
    not_contains_validator_not_contains_test = validator("not_contains_test", allow_reuse=True)(not_contains_validator)
    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class BytesTest(BaseModel):
    const_test: bytes = FieldInfo(default=b"demo", const=True)
    len_test: bytes = FieldInfo(default=b"", len=4)
    range_len_test: bytes = FieldInfo(default=b"", min_length=1, max_length=4)
    pattern_test: bytes = FieldInfo(default=b"")
    prefix_test: bytes = FieldInfo(default=b"", prefix=b"prefix")
    suffix_test: bytes = FieldInfo(default=b"", suffix=b"suffix")
    contains_test: bytes = FieldInfo(default=b"", contains=b"contains")
    in_test: bytes = FieldInfo(default=b"", in_=[b"a", b"b", b"c"])
    not_in_test: bytes = FieldInfo(default=b"", not_in=[b"a", b"b", b"c"])

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
    in_test: State = FieldInfo(default=0, in_=[0, 2])
    not_in_test: State = FieldInfo(default=0, not_in=[0, 2])

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    no_parse_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    keys_test: typing.Dict[constr(min_length=1, max_length=5), int] = FieldInfo(default_factory=dict)
    values_test: typing.Dict[str, conint(ge=5, le=5)] = FieldInfo(default_factory=dict)
    keys_values_test: typing.Dict[constr(min_length=1, max_length=5), contimestamp(timestamp_gt_now=True)] = FieldInfo(
        default_factory=dict
    )
    ignore_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)

    map_min_pairs_validator_pair_test = validator("pair_test", allow_reuse=True)(map_min_pairs_validator)
    map_max_pairs_validator_pair_test = validator("pair_test", allow_reuse=True)(map_max_pairs_validator)


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

    required_test: Any = FieldInfo()
    not_in_test: Any = FieldInfo(
        default_factory=Any,
        any_not_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )
    in_test: Any = FieldInfo(
        default_factory=Any,
        any_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )

    any_not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(any_not_in_validator)
    any_in_validator_in_test = validator("in_test", allow_reuse=True)(any_in_validator)


class DurationTest(BaseModel):
    required_test: Timedelta = FieldInfo()
    const_test: Timedelta = FieldInfo(
        default_factory=Timedelta, duration_const=timedelta(seconds=1, microseconds=500000)
    )
    range_test: Timedelta = FieldInfo(
        default_factory=Timedelta,
        duration_lt=timedelta(seconds=10, microseconds=500000),
        duration_gt=timedelta(seconds=5, microseconds=500000),
    )
    range_e_test: Timedelta = FieldInfo(
        default_factory=Timedelta,
        duration_le=timedelta(seconds=10, microseconds=500000),
        duration_ge=timedelta(seconds=5, microseconds=500000),
    )
    in_test: Timedelta = FieldInfo(
        default_factory=Timedelta,
        duration_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    not_in_test: Timedelta = FieldInfo(
        default_factory=Timedelta,
        duration_not_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )

    duration_const_validator_const_test = validator("const_test", allow_reuse=True)(duration_const_validator)
    duration_lt_validator_range_test = validator("range_test", allow_reuse=True)(duration_lt_validator)
    duration_gt_validator_range_test = validator("range_test", allow_reuse=True)(duration_gt_validator)
    duration_le_validator_range_e_test = validator("range_e_test", allow_reuse=True)(duration_le_validator)
    duration_ge_validator_range_e_test = validator("range_e_test", allow_reuse=True)(duration_ge_validator)
    duration_in_validator_in_test = validator("in_test", allow_reuse=True)(duration_in_validator)
    duration_not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(duration_not_in_validator)


class TimestampTest(BaseModel):
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

    timestamp_const_validator_const_test = validator("const_test", allow_reuse=True)(timestamp_const_validator)
    timestamp_lt_validator_range_test = validator("range_test", allow_reuse=True)(timestamp_lt_validator)
    timestamp_gt_validator_range_test = validator("range_test", allow_reuse=True)(timestamp_gt_validator)
    timestamp_le_validator_range_e_test = validator("range_e_test", allow_reuse=True)(timestamp_le_validator)
    timestamp_ge_validator_range_e_test = validator("range_e_test", allow_reuse=True)(timestamp_ge_validator)
    timestamp_lt_now_validator_lt_now_test = validator("lt_now_test", allow_reuse=True)(timestamp_lt_now_validator)
    timestamp_gt_now_validator_gt_now_test = validator("gt_now_test", allow_reuse=True)(timestamp_gt_now_validator)
    timestamp_within_validator_within_test = validator("within_test", allow_reuse=True)(timestamp_within_validator)
    timestamp_gt_now_validator_within_and_gt_now_test = validator("within_and_gt_now_test", allow_reuse=True)(
        timestamp_gt_now_validator
    )
    timestamp_within_validator_within_and_gt_now_test = validator("within_and_gt_now_test", allow_reuse=True)(
        timestamp_within_validator
    )


class MessageDisabledTest(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)


class MessageIgnoredTest(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)


class NestedMessageUserPayMessage(BaseModel):
    bank_number: str = FieldInfo(default="", min_length=13, max_length=19)
    exp: datetime = FieldInfo(default_factory=datetime.now, timestamp_gt_now=True)
    uuid: UUID = FieldInfo(default="")

    timestamp_gt_now_validator_exp = validator("exp", allow_reuse=True)(timestamp_gt_now_validator)


class NestedMessageNotEnableUserPayMessage(BaseModel):
    bank_number: str = FieldInfo(default="")
    exp: datetime = FieldInfo(default_factory=datetime.now)
    uuid: str = FieldInfo(default="")


class NestedMessage(BaseModel):
    string_in_map_test: typing.Dict[str, StringTest] = FieldInfo(default_factory=dict)
    map_in_map_test: typing.Dict[str, MapTest] = FieldInfo(default_factory=dict)
    user_pay: NestedMessageUserPayMessage = FieldInfo()
    not_enable_user_pay: NestedMessageNotEnableUserPayMessage = FieldInfo()
    empty: None = FieldInfo()


class OneOfTest(BaseModel):
    _one_of_dict = {"validate_test.OneOfTest.id": {"fields": {"x", "y"}, "required": True}}

    header: str = FieldInfo(default="")
    x: str = FieldInfo(default="")
    y: int = FieldInfo(default=0)

    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)


class OneOfNotTest(BaseModel):
    _one_of_dict = {"validate_test.OneOfNotTest.id": {"fields": {"x", "y"}, "required": False}}

    header: str = FieldInfo(default="")
    x: str = FieldInfo(default="")
    y: int = FieldInfo(default=0)

    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)
