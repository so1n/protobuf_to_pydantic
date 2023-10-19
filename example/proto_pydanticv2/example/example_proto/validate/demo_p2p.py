# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.0.2](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 4.24.4
# Pydantic Version: 2.0.3
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
from protobuf_to_pydantic.get_desc.from_pb_option.types import HostNameStr, UriRefStr
from protobuf_to_pydantic.util import Timedelta


class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class FloatTest(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1.0] = Field(default=0.0, json_schema_extra={})
    range_e_test: float = Field(default=0.0, ge=1.0, le=10.0, json_schema_extra={})
    range_test: float = Field(default=0.0, gt=1.0, lt=10.0, json_schema_extra={})
    in_test: float = Field(default=0.0, json_schema_extra={"in_": [1.0, 2.0, 3.0]})
    not_in_test: float = Field(default=0.0, json_schema_extra={"not_in": [1.0, 2.0, 3.0]})
    ignore_test: float = Field(default=0.0, json_schema_extra={})


class DoubleTest(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1.0] = Field(default=0.0, json_schema_extra={})
    range_e_test: float = Field(default=0.0, ge=1.0, le=10.0, json_schema_extra={})
    range_test: float = Field(default=0.0, gt=1.0, lt=10.0, json_schema_extra={})
    in_test: float = Field(default=0.0, json_schema_extra={"in_": [1.0, 2.0, 3.0]})
    not_in_test: float = Field(default=0.0, json_schema_extra={"not_in": [1.0, 2.0, 3.0]})
    ignore_test: float = Field(default=0.0, json_schema_extra={})


class Int32Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, ge=1, le=10, json_schema_extra={})
    range_test: int = Field(default=0, gt=1, lt=10, json_schema_extra={})
    in_test: int = Field(default=0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: int = Field(default=0, json_schema_extra={"not_in": [1, 2, 3]})
    ignore_test: int = Field(default=0, json_schema_extra={})


class Uint32Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, ge=1, le=10, json_schema_extra={})
    range_test: int = Field(default=0, gt=1, lt=10, json_schema_extra={})
    in_test: int = Field(default=0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: int = Field(default=0, json_schema_extra={"not_in": [1, 2, 3]})
    ignore_test: int = Field(default=0, json_schema_extra={})


class Sint32Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, ge=1, le=10, json_schema_extra={})
    range_test: int = Field(default=0, gt=1, lt=10, json_schema_extra={})
    in_test: int = Field(default=0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: int = Field(default=0, json_schema_extra={"not_in": [1, 2, 3]})
    ignore_test: int = Field(default=0, json_schema_extra={})


class Int64Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, ge=1, le=10, json_schema_extra={})
    range_test: int = Field(default=0, gt=1, lt=10, json_schema_extra={})
    in_test: int = Field(default=0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: int = Field(default=0, json_schema_extra={"not_in": [1, 2, 3]})
    ignore_test: int = Field(default=0, json_schema_extra={})


class Uint64Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, ge=1, le=10, json_schema_extra={})
    range_test: int = Field(default=0, gt=1, lt=10, json_schema_extra={})
    in_test: int = Field(default=0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: int = Field(default=0, json_schema_extra={"not_in": [1, 2, 3]})
    ignore_test: int = Field(default=0, json_schema_extra={})


class Sint64Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, ge=1, le=10, json_schema_extra={})
    range_test: int = Field(default=0, gt=1, lt=10, json_schema_extra={})
    in_test: int = Field(default=0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: int = Field(default=0, json_schema_extra={"not_in": [1, 2, 3]})
    ignore_test: int = Field(default=0, json_schema_extra={})


class Fixed32Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0.0, json_schema_extra={})
    range_e_test: float = Field(default=0.0, ge=1, le=10, json_schema_extra={})
    range_test: float = Field(default=0.0, gt=1, lt=10, json_schema_extra={})
    in_test: float = Field(default=0.0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: float = Field(default=0.0, json_schema_extra={"not_in": [1, 2, 3]})
    ignore_test: float = Field(default=0.0, json_schema_extra={})


class Fixed64Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0.0, json_schema_extra={})
    range_e_test: float = Field(default=0.0, ge=1, le=10, json_schema_extra={})
    range_test: float = Field(default=0.0, gt=1, lt=10, json_schema_extra={})
    in_test: float = Field(default=0.0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: float = Field(default=0.0, json_schema_extra={"not_in": [1, 2, 3]})
    ignore_test: float = Field(default=0.0, json_schema_extra={})


class Sfixed32Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0.0, json_schema_extra={})
    range_e_test: float = Field(default=0.0, ge=1, le=10, json_schema_extra={})
    range_test: float = Field(default=0.0, gt=1, lt=10, json_schema_extra={})
    in_test: float = Field(default=0.0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: float = Field(default=0.0, json_schema_extra={"not_in": [1, 2, 3]})
    ignore_test: float = Field(default=0.0, json_schema_extra={})


class Sfixed64Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0.0, json_schema_extra={})
    range_e_test: float = Field(default=0.0, ge=1, le=10, json_schema_extra={})
    range_test: float = Field(default=0.0, gt=1, lt=10, json_schema_extra={})
    in_test: float = Field(default=0.0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: float = Field(default=0.0, json_schema_extra={"not_in": [1, 2, 3]})
    ignore_test: float = Field(default=0.0, json_schema_extra={})


class BoolTest(BaseModel):
    bool_1_test: typing_extensions.Literal[True] = Field(default=False, json_schema_extra={})
    bool_2_test: typing_extensions.Literal[False] = Field(default=False, json_schema_extra={})


class StringTest(BaseModel):
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

    const_test: typing_extensions.Literal["aaa"] = Field(default="", json_schema_extra={})
    len_test: str = Field(default="", json_schema_extra={"len": 3})
    s_range_len_test: str = Field(default="", min_length=1, max_length=3, json_schema_extra={})
    b_range_len_test: str = Field(default="", json_schema_extra={})
    pattern_test: str = Field(default="", pattern="^test", json_schema_extra={})
    prefix_test: str = Field(default="", json_schema_extra={"prefix": "prefix"})
    suffix_test: str = Field(default="", json_schema_extra={"suffix": "suffix"})
    contains_test: str = Field(default="", json_schema_extra={"contains": "contains"})
    not_contains_test: str = Field(default="", json_schema_extra={"not_contains": "not_contains"})
    in_test: str = Field(default="", json_schema_extra={"in_": ["a", "b", "c"]})
    not_in_test: str = Field(default="", json_schema_extra={"not_in": ["a", "b", "c"]})
    email_test: EmailStr = Field(default="", json_schema_extra={})
    hostname_test: HostNameStr = Field(default="", json_schema_extra={})
    ip_test: IPvAnyAddress = Field(default="", json_schema_extra={})
    ipv4_test: IPv4Address = Field(default="", json_schema_extra={})
    ipv6_test: IPv6Address = Field(default="", json_schema_extra={})
    uri_test: Url = Field(default="", json_schema_extra={})
    uri_ref_test: UriRefStr = Field(default="", json_schema_extra={})
    address_test: IPvAnyAddress = Field(default="", json_schema_extra={})
    uuid_test: UUID = Field(default="", json_schema_extra={})
    ignore_test: str = Field(default="", json_schema_extra={})


class BytesTest(BaseModel):
    len_test_len_validator = field_validator("len_test", mode="after", check_fields=None)(len_validator)
    prefix_test_prefix_validator = field_validator("prefix_test", mode="after", check_fields=None)(prefix_validator)
    suffix_test_suffix_validator = field_validator("suffix_test", mode="after", check_fields=None)(suffix_validator)
    contains_test_contains_validator = field_validator("contains_test", mode="after", check_fields=None)(
        contains_validator
    )
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[b"demo"] = Field(default=b"", json_schema_extra={})
    len_test: bytes = Field(default=b"", json_schema_extra={"len": 4})
    range_len_test: bytes = Field(default=b"", min_length=1, max_length=4, json_schema_extra={})
    pattern_test: bytes = Field(default=b"", json_schema_extra={})
    prefix_test: bytes = Field(default=b"", json_schema_extra={"prefix": b"prefix"})
    suffix_test: bytes = Field(default=b"", json_schema_extra={"suffix": b"suffix"})
    contains_test: bytes = Field(default=b"", json_schema_extra={"contains": b"contains"})
    in_test: bytes = Field(default=b"", json_schema_extra={"in_": [b"a", b"b", b"c"]})
    not_in_test: bytes = Field(default=b"", json_schema_extra={"not_in": [b"a", b"b", b"c"]})


class EnumTest(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[2] = Field(default=0, json_schema_extra={})
    defined_only_test: State = Field(default=0, json_schema_extra={})
    in_test: State = Field(default=0, json_schema_extra={"in_": [0, 2]})
    not_in_test: State = Field(default=0, json_schema_extra={"not_in": [0, 2]})


class MapTest(BaseModel):
    pair_test_map_min_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_min_pairs_validator
    )
    pair_test_map_max_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_max_pairs_validator
    )

    pair_test: typing.Dict[str, int] = Field(
        default_factory=dict, json_schema_extra={"map_max_pairs": 5, "map_min_pairs": 1}
    )
    no_parse_test: typing.Dict[str, int] = Field(default_factory=dict, json_schema_extra={})
    keys_test: typing.Dict[typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)], int] = Field(
        default_factory=dict, json_schema_extra={}
    )
    values_test: typing.Dict[str, typing_extensions.Annotated[int, Ge(ge=5), Le(le=5)]] = Field(
        default_factory=dict, json_schema_extra={}
    )
    keys_values_test: typing.Dict[
        typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)],
        typing_extensions.Annotated[DatetimeType, gt_now(True)],
    ] = Field(default_factory=dict, json_schema_extra={})
    ignore_test: typing.Dict[str, int] = Field(default_factory=dict, json_schema_extra={})


class MessageTest(BaseModel):
    skip_test: str = Field(default="", json_schema_extra={})
    required_test: str = Field(json_schema_extra={})


class RepeatedTest(BaseModel):
    range_test: typing.List[str] = Field(default_factory=list, min_length=1, max_length=5, json_schema_extra={})
    unique_test: typing.Set[str] = Field(default_factory=set, json_schema_extra={})
    items_string_test: typing.List[
        typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)]
    ] = Field(default_factory=list, min_length=1, max_length=5, json_schema_extra={})
    items_double_test: typing.List[typing_extensions.Annotated[float, Gt(gt=1.0), Lt(lt=5.0)]] = Field(
        default_factory=list, min_length=1, max_length=5, json_schema_extra={}
    )
    items_int32_test: typing.List[typing_extensions.Annotated[int, Gt(gt=1), Lt(lt=5)]] = Field(
        default_factory=list, min_length=1, max_length=5, json_schema_extra={}
    )
    items_timestamp_test: typing.List[
        typing_extensions.Annotated[DatetimeType, t_gt(1600000000.0), t_lt(1600000010.0)]
    ] = Field(default_factory=list, min_length=1, max_length=5, json_schema_extra={})
    items_duration_test: typing.List[
        typing_extensions.Annotated[TimedeltaType, Gt(gt=timedelta(seconds=10)), Lt(lt=timedelta(seconds=20))]
    ] = Field(default_factory=list, min_length=1, max_length=5, json_schema_extra={})
    items_bytes_test: typing.List[
        typing_extensions.Annotated[bytes, MinLen(min_length=1), MaxLen(max_length=5)]
    ] = Field(default_factory=list, min_length=1, max_length=5, json_schema_extra={})
    ignore_test: typing.List[str] = Field(default_factory=list, json_schema_extra={})


class AnyTest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    not_in_test_any_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(
        any_not_in_validator
    )
    in_test_any_in_validator = field_validator("in_test", mode="after", check_fields=None)(any_in_validator)

    required_test: Any = Field(json_schema_extra={})
    not_in_test: Any = Field(
        default_factory=Any,
        json_schema_extra={
            "any_not_in": [
                "type.googleapis.com/google.protobuf.Duration",
                "type.googleapis.com/google.protobuf.Timestamp",
            ]
        },
    )
    in_test: Any = Field(
        default_factory=Any,
        json_schema_extra={
            "any_in": ["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"]
        },
    )


class DurationTest(BaseModel):
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

    required_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(json_schema_extra={})
    const_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta, json_schema_extra={"duration_const": timedelta(seconds=1, microseconds=500000)}
    )
    range_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta,
        json_schema_extra={
            "duration_gt": timedelta(seconds=5, microseconds=500000),
            "duration_lt": timedelta(seconds=10, microseconds=500000),
        },
    )
    range_e_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta,
        json_schema_extra={
            "duration_ge": timedelta(seconds=5, microseconds=500000),
            "duration_le": timedelta(seconds=10, microseconds=500000),
        },
    )
    in_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta,
        json_schema_extra={
            "duration_in": [timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)]
        },
    )
    not_in_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta,
        json_schema_extra={
            "duration_not_in": [timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)]
        },
    )


class TimestampTest(BaseModel):
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

    required_test: datetime = Field(json_schema_extra={})
    const_test: datetime = Field(default_factory=datetime.now, json_schema_extra={"timestamp_const": 1600000000.0})
    range_test: datetime = Field(
        default_factory=datetime.now, json_schema_extra={"timestamp_gt": 1600000000.0, "timestamp_lt": 1600000010.0}
    )
    range_e_test: datetime = Field(
        default_factory=datetime.now, json_schema_extra={"timestamp_ge": 1600000000.0, "timestamp_le": 1600000010.0}
    )
    lt_now_test: datetime = Field(default_factory=datetime.now, json_schema_extra={"timestamp_lt_now": True})
    gt_now_test: datetime = Field(default_factory=datetime.now, json_schema_extra={"timestamp_gt_now": True})
    within_test: datetime = Field(
        default_factory=datetime.now, json_schema_extra={"timestamp_within": timedelta(seconds=1)}
    )
    within_and_gt_now_test: datetime = Field(
        default_factory=datetime.now,
        json_schema_extra={"timestamp_gt_now": True, "timestamp_within": timedelta(seconds=3600)},
    )


class MessageDisabledTest(BaseModel):
    const_test: int = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, json_schema_extra={})
    range_test: int = Field(default=0, json_schema_extra={})


class MessageIgnoredTest(BaseModel):
    const_test: int = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, json_schema_extra={})
    range_test: int = Field(default=0, json_schema_extra={})


class OneOfTest(BaseModel):
    _one_of_dict = {"OneOfTest.id": {"fields": {"x", "y"}, "required": True}}
    one_of_validator = model_validator(mode="before")(check_one_of)

    header: str = Field(default="", json_schema_extra={})
    x: str = Field(default="", json_schema_extra={})
    y: int = Field(default=0, json_schema_extra={})


class OneOfNotTest(BaseModel):
    _one_of_dict = {"OneOfNotTest.id": {"fields": {"x", "y"}}}
    one_of_validator = model_validator(mode="before")(check_one_of)

    header: str = Field(default="", json_schema_extra={})
    x: str = Field(default="", json_schema_extra={})
    y: int = Field(default=0, json_schema_extra={})


class AfterReferMessage(BaseModel):
    uid: str = Field(default="", min_length=1, json_schema_extra={})
    age: int = Field(default=0, ge=0, lt=500, json_schema_extra={})


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        exp_timestamp_gt_now_validator = field_validator("exp", mode="after", check_fields=None)(
            timestamp_gt_now_validator
        )

        bank_number: str = Field(default="", min_length=13, max_length=19, json_schema_extra={})
        exp: datetime = Field(default_factory=datetime.now, json_schema_extra={"timestamp_gt_now": True})
        uuid: UUID = Field(default="", json_schema_extra={})

    class NotEnableUserPayMessage(BaseModel):
        bank_number: str = Field(default="", json_schema_extra={})
        exp: datetime = Field(default_factory=datetime.now, json_schema_extra={})
        uuid: str = Field(default="", json_schema_extra={})

    string_in_map_test: typing.Dict[str, StringTest] = Field(default_factory=dict, json_schema_extra={})
    map_in_map_test: typing.Dict[str, MapTest] = Field(default_factory=dict, json_schema_extra={})
    user_pay: UserPayMessage = Field(json_schema_extra={})
    not_enable_user_pay: NotEnableUserPayMessage = Field(json_schema_extra={})
    empty: None = Field(json_schema_extra={})
    after_refer: AfterReferMessage = Field(json_schema_extra={})
