# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.0](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 2.5.3
import typing
from datetime import datetime, timedelta
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID

import typing_extensions
from annotated_types import Ge, Gt, Le, Lt, MaxLen, MinLen
from google.protobuf.any_pb2 import Any  # type: ignore
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_validator, model_validator
from pydantic.networks import EmailStr, IPvAnyAddress
from pydantic_core._pydantic_core import Url
from typing_extensions import Annotated

from protobuf_to_pydantic.customer_con_type.v2 import DatetimeType, TimedeltaType, gt_now, t_gt, t_lt
from protobuf_to_pydantic.customer_validator import check_one_of
from protobuf_to_pydantic.customer_validator.v2 import (
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
from protobuf_to_pydantic.field_info_rule.protobuf_option_to_field_info.types import HostNameStr, UriRefStr
from protobuf_to_pydantic.util import Timedelta


class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class FloatTest(BaseModel):
    const_test: typing_extensions.Literal[1.0] = Field(default=0.0)
    range_e_test: float = Field(default=0.0, ge=1.0, le=10.0)
    range_test: float = Field(default=0.0, gt=1.0, lt=10.0)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    ignore_test: float = Field(default=0.0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class DoubleTest(BaseModel):
    const_test: typing_extensions.Literal[1.0] = Field(default=0.0)
    range_e_test: float = Field(default=0.0, ge=1.0, le=10.0)
    range_test: float = Field(default=0.0, gt=1.0, lt=10.0)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    ignore_test: float = Field(default=0.0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Int32Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Uint32Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Sint32Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Int64Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Uint64Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Sint64Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Fixed32Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0.0)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0.0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0.0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Fixed64Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0.0)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0.0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0.0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Sfixed32Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0.0)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0.0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0.0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Sfixed64Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0.0)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0.0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0.0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class BoolTest(BaseModel):
    bool_1_test: typing_extensions.Literal[True] = Field(default=False)
    bool_2_test: typing_extensions.Literal[False] = Field(default=False)


class StringTest(BaseModel):
    const_test: typing_extensions.Literal["aaa"] = Field(default="")
    len_test: str = Field(default="", len=3)
    s_range_len_test: str = Field(default="", min_length=1, max_length=3)
    b_range_len_test: str = Field(default="")
    pattern_test: str = Field(default="", pattern="^test")
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
    uri_test: Url = Field(default="")
    uri_ref_test: UriRefStr = Field(default="")
    address_test: IPvAnyAddress = Field(default="")
    uuid_test: UUID = Field(default="")
    ignore_test: str = Field(default="")

    len_test_len_validator = field_validator("len_test", mode="after", check_fields=None)(len_validator)
    prefix_test_prefix_validator = field_validator("prefix_test", mode="after", check_fields=None)(prefix_validator)
    suffix_test_suffix_validator = field_validator("suffix_test", mode="after", check_fields=None)(suffix_validator)
    contains_test_contains_validator = field_validator("contains_test", mode="after", check_fields=None)(
        contains_validator
    )
    not_contains_test_not_contains_validator = field_validator("not_contains_test", mode="after", check_fields=None)(
        not_contains_validator
    )
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class BytesTest(BaseModel):
    const_test: typing_extensions.Literal[b"demo"] = Field(default=b"")
    len_test: bytes = Field(default=b"", len=4)
    range_len_test: bytes = Field(default=b"", min_length=1, max_length=4)
    pattern_test: bytes = Field(default=b"")
    prefix_test: bytes = Field(default=b"", prefix=b"prefix")
    suffix_test: bytes = Field(default=b"", suffix=b"suffix")
    contains_test: bytes = Field(default=b"", contains=b"contains")
    in_test: bytes = Field(default=b"", in_=[b"a", b"b", b"c"])
    not_in_test: bytes = Field(default=b"", not_in=[b"a", b"b", b"c"])

    len_test_len_validator = field_validator("len_test", mode="after", check_fields=None)(len_validator)
    prefix_test_prefix_validator = field_validator("prefix_test", mode="after", check_fields=None)(prefix_validator)
    suffix_test_suffix_validator = field_validator("suffix_test", mode="after", check_fields=None)(suffix_validator)
    contains_test_contains_validator = field_validator("contains_test", mode="after", check_fields=None)(
        contains_validator
    )
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class EnumTest(BaseModel):
    model_config = ConfigDict(validate_default=True)
    const_test: typing_extensions.Literal[2] = Field(default=0)
    defined_only_test: State = Field(default=0)
    in_test: State = Field(default=0, in_=[0, 2])
    not_in_test: State = Field(default=0, not_in=[0, 2])

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class MapTest(BaseModel):
    pair_test: "typing.Dict[str, int]" = Field(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    no_parse_test: "typing.Dict[str, int]" = Field(default_factory=dict)
    keys_test: typing.Dict[typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)], int] = Field(
        default_factory=dict
    )
    values_test: typing.Dict[str, typing_extensions.Annotated[int, Ge(ge=5), Le(le=5)]] = Field(default_factory=dict)
    keys_values_test: typing.Dict[
        typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)],
        typing_extensions.Annotated[DatetimeType, gt_now(True)],
    ] = Field(default_factory=dict)
    ignore_test: "typing.Dict[str, int]" = Field(default_factory=dict)

    pair_test_map_min_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_min_pairs_validator
    )
    pair_test_map_max_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_max_pairs_validator
    )


class MessageTest(BaseModel):
    skip_test: str = Field(default="")
    required_test: str = Field()


class RepeatedTest(BaseModel):
    range_test: typing.List[str] = Field(default_factory=list, min_length=1, max_length=5)
    unique_test: typing.Set[str] = Field(default_factory=set)
    items_string_test: typing.List[
        typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)]
    ] = Field(default_factory=list, min_length=1, max_length=5)
    items_double_test: typing.List[typing_extensions.Annotated[float, Gt(gt=1.0), Lt(lt=5.0)]] = Field(
        default_factory=list, min_length=1, max_length=5
    )
    items_int32_test: typing.List[typing_extensions.Annotated[int, Gt(gt=1), Lt(lt=5)]] = Field(
        default_factory=list, min_length=1, max_length=5
    )
    items_timestamp_test: typing.List[
        typing_extensions.Annotated[DatetimeType, t_gt(1600000000.0), t_lt(1600000010.0)]
    ] = Field(default_factory=list, min_length=1, max_length=5)
    items_duration_test: typing.List[
        typing_extensions.Annotated[TimedeltaType, Gt(gt=timedelta(seconds=10)), Lt(lt=timedelta(seconds=20))]
    ] = Field(default_factory=list, min_length=1, max_length=5)
    items_bytes_test: typing.List[
        typing_extensions.Annotated[bytes, MinLen(min_length=1), MaxLen(max_length=5)]
    ] = Field(default_factory=list, min_length=1, max_length=5)
    ignore_test: typing.List[str] = Field(default_factory=list)


class AnyTest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    required_test: Any = Field()
    not_in_test: Any = Field(
        default_factory=Any,
        any_not_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )
    in_test: Any = Field(
        default_factory=Any,
        any_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )

    not_in_test_any_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(
        any_not_in_validator
    )
    in_test_any_in_validator = field_validator("in_test", mode="after", check_fields=None)(any_in_validator)


class DurationTest(BaseModel):
    required_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field()
    const_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta, duration_const=timedelta(seconds=1, microseconds=500000)
    )
    range_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta,
        duration_lt=timedelta(seconds=10, microseconds=500000),
        duration_gt=timedelta(seconds=5, microseconds=500000),
    )
    range_e_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta,
        duration_le=timedelta(seconds=10, microseconds=500000),
        duration_ge=timedelta(seconds=5, microseconds=500000),
    )
    in_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta,
        duration_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    not_in_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta,
        duration_not_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )

    const_test_duration_const_validator = field_validator("const_test", mode="after", check_fields=None)(
        duration_const_validator
    )
    range_test_duration_lt_validator = field_validator("range_test", mode="after", check_fields=None)(
        duration_lt_validator
    )
    range_test_duration_gt_validator = field_validator("range_test", mode="after", check_fields=None)(
        duration_gt_validator
    )
    range_e_test_duration_le_validator = field_validator("range_e_test", mode="after", check_fields=None)(
        duration_le_validator
    )
    range_e_test_duration_ge_validator = field_validator("range_e_test", mode="after", check_fields=None)(
        duration_ge_validator
    )
    in_test_duration_in_validator = field_validator("in_test", mode="after", check_fields=None)(duration_in_validator)
    not_in_test_duration_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(
        duration_not_in_validator
    )


class TimestampTest(BaseModel):
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

    const_test_timestamp_const_validator = field_validator("const_test", mode="after", check_fields=None)(
        timestamp_const_validator
    )
    range_test_timestamp_lt_validator = field_validator("range_test", mode="after", check_fields=None)(
        timestamp_lt_validator
    )
    range_test_timestamp_gt_validator = field_validator("range_test", mode="after", check_fields=None)(
        timestamp_gt_validator
    )
    range_e_test_timestamp_le_validator = field_validator("range_e_test", mode="after", check_fields=None)(
        timestamp_le_validator
    )
    range_e_test_timestamp_ge_validator = field_validator("range_e_test", mode="after", check_fields=None)(
        timestamp_ge_validator
    )
    lt_now_test_timestamp_lt_now_validator = field_validator("lt_now_test", mode="after", check_fields=None)(
        timestamp_lt_now_validator
    )
    gt_now_test_timestamp_gt_now_validator = field_validator("gt_now_test", mode="after", check_fields=None)(
        timestamp_gt_now_validator
    )
    within_test_timestamp_within_validator = field_validator("within_test", mode="after", check_fields=None)(
        timestamp_within_validator
    )
    within_and_gt_now_test_timestamp_gt_now_validator = field_validator(
        "within_and_gt_now_test", mode="after", check_fields=None
    )(timestamp_gt_now_validator)
    within_and_gt_now_test_timestamp_within_validator = field_validator(
        "within_and_gt_now_test", mode="after", check_fields=None
    )(timestamp_within_validator)


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
    one_of_validator = model_validator(mode="before")(check_one_of)
    header: str = Field(default="")
    x: str = Field(default="")
    y: int = Field(default=0)


class OneOfNotTest(BaseModel):
    _one_of_dict = {"OneOfNotTest.id": {"fields": {"x", "y"}}}
    one_of_validator = model_validator(mode="before")(check_one_of)
    header: str = Field(default="")
    x: str = Field(default="")
    y: int = Field(default=0)


class AfterReferMessage(BaseModel):
    uid: str = Field(default="", min_length=1)
    age: int = Field(default=0, ge=0, lt=500)


class NestedMessage(BaseModel):
    """
    test nested message
    """

    class UserPayMessage(BaseModel):
        bank_number: str = Field(default="", min_length=13, max_length=19)
        exp: datetime = Field(default_factory=datetime.now, timestamp_gt_now=True)
        uuid: UUID = Field(default="")

        exp_timestamp_gt_now_validator = field_validator("exp", mode="after", check_fields=None)(
            timestamp_gt_now_validator
        )

    class NotEnableUserPayMessage(BaseModel):
        bank_number: str = Field(default="")
        exp: datetime = Field(default_factory=datetime.now)
        uuid: str = Field(default="")

    string_in_map_test: "typing.Dict[str, StringTest]" = Field(default_factory=dict)
    map_in_map_test: "typing.Dict[str, MapTest]" = Field(default_factory=dict)
    user_pay: "NestedMessage.UserPayMessage" = Field(default_factory=lambda: NestedMessage.UserPayMessage())
    not_enable_user_pay: "NestedMessage.NotEnableUserPayMessage" = Field(
        default_factory=lambda: NestedMessage.NotEnableUserPayMessage()
    )
    empty: None = Field()
    after_refer: AfterReferMessage = Field(default_factory=AfterReferMessage)
