# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

import datetime
import typing
from datetime import timedelta
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID

from google.protobuf.any_pb2 import Any as AnyMessage  # type: ignore
from google.protobuf.message import Message  # type: ignore
from protobuf_to_pydantic.customer_con_type import contimedelta, contimestamp
from protobuf_to_pydantic.get_desc.from_pb_option.types import HostNameStr, UriRefStr
from protobuf_to_pydantic.util import Timedelta
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic.networks import AnyUrl, EmailStr, IPvAnyAddress
from pydantic.types import conbytes, confloat, conint, conlist, constr


class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class FloatTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True, extra={"enable": True})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={"enable": True})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={"enable": True})
    in_test: float = FieldInfo(default=0.0, extra={"enable": True, "in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"enable": True, "not_in": [1.0, 2.0, 3.0]})
    ignore_test: float = FieldInfo(default=0.0, extra={"enable": True})


class DoubleTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True, extra={"enable": True})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={"enable": True})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={"enable": True})
    in_test: float = FieldInfo(default=0.0, extra={"enable": True, "in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"enable": True, "not_in": [1.0, 2.0, 3.0]})
    ignore_test: float = FieldInfo(default=0.0, extra={"enable": True})


class Int32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={"enable": True})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={"enable": True})
    in_test: int = FieldInfo(default=0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"enable": True, "not_in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0, extra={"enable": True})


class Uint32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={"enable": True})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={"enable": True})
    in_test: int = FieldInfo(default=0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"enable": True, "not_in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0, extra={"enable": True})


class Sint32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={"enable": True})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={"enable": True})
    in_test: int = FieldInfo(default=0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"enable": True, "not_in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0, extra={"enable": True})


class Int64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={"enable": True})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={"enable": True})
    in_test: int = FieldInfo(default=0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"enable": True, "not_in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0, extra={"enable": True})


class Uint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={"enable": True})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={"enable": True})
    in_test: int = FieldInfo(default=0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"enable": True, "not_in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0, extra={"enable": True})


class Sint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={"enable": True})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={"enable": True})
    in_test: int = FieldInfo(default=0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"enable": True, "not_in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0, extra={"enable": True})


class Fixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={"enable": True})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={"enable": True})
    in_test: float = FieldInfo(default=0.0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0.0, extra={"enable": True, "not_in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0.0, extra={"enable": True})


class Fixed64Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={"enable": True})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={"enable": True})
    in_test: float = FieldInfo(default=0.0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0.0, extra={"enable": True, "not_in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0.0, extra={"enable": True})


class Sfixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={"enable": True})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={"enable": True})
    in_test: float = FieldInfo(default=0.0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0.0, extra={"enable": True, "not_in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0.0, extra={"enable": True})


class Sfixed64Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={"enable": True})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={"enable": True})
    in_test: float = FieldInfo(default=0.0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0.0, extra={"enable": True, "not_in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0.0, extra={"enable": True})


class BoolTest(BaseModel):
    bool_1_test: bool = FieldInfo(default=True, const=True, extra={"enable": True})
    bool_2_test: bool = FieldInfo(default=False, const=True, extra={"enable": True})


class StringTest(BaseModel):
    const_test: str = FieldInfo(default="aaa", const=True, extra={"enable": True})
    len_test: str = FieldInfo(default="", extra={"enable": True, "len": 3})
    s_range_len_test: str = FieldInfo(default="", min_length=1, max_length=3, extra={"enable": True})
    b_range_len_test: str = FieldInfo(default="", extra={"enable": True})
    pattern_test: str = FieldInfo(default="", regex="^test", extra={"enable": True})
    prefix_test: str = FieldInfo(default="", extra={"enable": True, "prefix": "prefix"})
    suffix_test: str = FieldInfo(default="", extra={"enable": True, "suffix": "suffix"})
    contains_test: str = FieldInfo(default="", extra={"contains": "contains", "enable": True})
    not_contains_test: str = FieldInfo(default="", extra={"enable": True, "not_contains": "not_contains"})
    in_test: str = FieldInfo(default="", extra={"enable": True, "in": ["a", "b", "c"]})
    not_in_test: str = FieldInfo(default="", extra={"enable": True, "not_in": ["a", "b", "c"]})
    email_test: EmailStr = FieldInfo(default="", extra={"enable": True})
    hostname_test: HostNameStr = FieldInfo(default="", extra={"enable": True})
    ip_test: IPvAnyAddress = FieldInfo(default="", extra={"enable": True})
    ipv4_test: IPv4Address = FieldInfo(default="", extra={"enable": True})
    ipv6_test: IPv6Address = FieldInfo(default="", extra={"enable": True})
    uri_test: AnyUrl = FieldInfo(default="", extra={"enable": True})
    uri_ref_test: UriRefStr = FieldInfo(default="", extra={"enable": True})
    address_test: IPvAnyAddress = FieldInfo(default="", extra={"enable": True})
    uuid_test: UUID = FieldInfo(default="", extra={"enable": True})
    ignore_test: str = FieldInfo(default="", extra={"enable": True})


class BytesTest(BaseModel):
    const_test: bytes = FieldInfo(default=b"demo", const=True, extra={"enable": True})
    len_test: bytes = FieldInfo(default=b"", extra={"enable": True, "len": 4})
    range_len_test: bytes = FieldInfo(default=b"", min_length=1, max_length=4, extra={"enable": True})
    pattern_test: bytes = FieldInfo(default=b"", extra={"enable": True})
    prefix_test: bytes = FieldInfo(default=b"", extra={"enable": True, "prefix": b"prefix"})
    suffix_test: bytes = FieldInfo(default=b"", extra={"enable": True, "suffix": b"suffix"})
    contains_test: bytes = FieldInfo(default=b"", extra={"contains": b"contains", "enable": True})
    in_test: bytes = FieldInfo(default=b"", extra={"enable": True, "in": [b"a", b"b", b"c"]})
    not_in_test: bytes = FieldInfo(default=b"", extra={"enable": True, "not_in": [b"a", b"b", b"c"]})


class EnumTest(BaseModel):
    const_test: "State" = FieldInfo(default=0)
    defined_only_test: "State" = FieldInfo(default=0)
    in_test: "State" = FieldInfo(default=0)
    not_in_test: "State" = FieldInfo(default=0)


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = FieldInfo(
        default_factory=dict, extra={"enable": True, "map_max_pairs": 5, "map_min_pairs": 1}
    )
    no_parse_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, extra={"enable": True})
    keys_test: typing.Dict[constr(min_length=1, max_length=5), int] = FieldInfo(
        default_factory=dict, extra={"enable": True}
    )
    values_test: typing.Dict[str, conint(ge=5, le=5)] = FieldInfo(default_factory=dict, extra={"enable": True})
    keys_values_test: typing.Dict[constr(min_length=1, max_length=5), contimestamp(timestamp_gt_now=True)] = FieldInfo(
        default_factory=dict, extra={"enable": True}
    )
    ignore_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, extra={"enable": True})


class MessageTest(BaseModel):
    skip_test: str = FieldInfo(default="", extra={"enable": True})
    required_test: str = FieldInfo(extra={"enable": True})


class RepeatedTest(BaseModel):
    range_test: typing.List[str] = FieldInfo(default_factory=list, min_items=1, max_items=5, extra={"enable": True})
    unique_test: typing.List[str] = FieldInfo(default_factory=list, unique_items=True, extra={"enable": True})
    items_string_test: conlist(item_type=constr(min_length=1, max_length=5), min_items=1, max_items=5) = FieldInfo(
        default_factory=list, extra={"enable": True}
    )
    items_double_test: conlist(item_type=confloat(gt=1, lt=5), min_items=1, max_items=5) = FieldInfo(
        default_factory=list, extra={"enable": True}
    )
    items_int32_test: conlist(item_type=conint(gt=1, lt=5), min_items=1, max_items=5) = FieldInfo(
        default_factory=list, extra={"enable": True}
    )
    items_timestamp_test: conlist(
        item_type=contimestamp(timestamp_gt=1600000000.0, timestamp_lt=1600000010.0), min_items=1, max_items=5
    ) = FieldInfo(default_factory=list, extra={"enable": True})
    items_duration_test: conlist(
        item_type=contimedelta(duration_gt=timedelta(seconds=10), duration_lt=timedelta(seconds=20)),
        min_items=1,
        max_items=5,
    ) = FieldInfo(default_factory=list, extra={"enable": True})
    items_bytes_test: conlist(item_type=conbytes(min_length=1, max_length=5), min_items=1, max_items=5) = FieldInfo(
        default_factory=list, extra={"enable": True}
    )
    ignore_test: typing.List[str] = FieldInfo(default_factory=list, extra={"enable": True})


class AnyTest(BaseModel):
    required_test: AnyMessage = FieldInfo(extra={"enable": True})
    not_in_test: AnyMessage = FieldInfo(
        default_factory="AnyMessage",
        extra={
            "any_not_in": [
                "type.googleapis.com/google.protobuf.Duration",
                "type.googleapis.com/google.protobuf.Timestamp",
            ],
            "enable": True,
        },
    )
    in_test: AnyMessage = FieldInfo(
        default_factory="AnyMessage",
        extra={
            "any_in": ["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
            "enable": True,
        },
    )


class DurationTest(BaseModel):
    required_test: Timedelta = FieldInfo(extra={"enable": True})
    const_test: Timedelta = FieldInfo(
        default_factory="Timedelta", extra={"duration_const": timedelta(seconds=1, microseconds=500000), "enable": True}
    )
    range_test: Timedelta = FieldInfo(
        default_factory="Timedelta",
        extra={
            "duration_gt": timedelta(seconds=5, microseconds=500000),
            "duration_lt": timedelta(seconds=10, microseconds=500000),
            "enable": True,
        },
    )
    range_e_test: Timedelta = FieldInfo(
        default_factory="Timedelta",
        extra={
            "duration_ge": timedelta(seconds=5, microseconds=500000),
            "duration_le": timedelta(seconds=10, microseconds=500000),
            "enable": True,
        },
    )
    in_test: Timedelta = FieldInfo(
        default_factory="Timedelta",
        extra={
            "duration_in": [timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
            "enable": True,
        },
    )
    not_in_test: Timedelta = FieldInfo(
        default_factory="Timedelta",
        extra={
            "duration_not_in": [timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
            "enable": True,
        },
    )


class TimestampTest(BaseModel):
    required_test: datetime.datetime = FieldInfo(extra={"enable": True})
    const_test: datetime.datetime = FieldInfo(
        default_factory="now", extra={"enable": True, "timestamp_const": 1600000000.0}
    )
    range_test: datetime.datetime = FieldInfo(
        default_factory="now", extra={"enable": True, "timestamp_gt": 1600000000.0, "timestamp_lt": 1600000010.0}
    )
    range_e_test: datetime.datetime = FieldInfo(
        default_factory="now", extra={"enable": True, "timestamp_ge": 1600000000.0, "timestamp_le": 1600000010.0}
    )
    lt_now_test: datetime.datetime = FieldInfo(default_factory="now", extra={"enable": True, "timestamp_lt_now": True})
    gt_now_test: datetime.datetime = FieldInfo(default_factory="now", extra={"enable": True, "timestamp_gt_now": True})
    within_test: datetime.datetime = FieldInfo(
        default_factory="now", extra={"enable": True, "timestamp_within": timedelta(seconds=1)}
    )
    within_and_gt_now_test: datetime.datetime = FieldInfo(
        default_factory="now",
        extra={"enable": True, "timestamp_gt_now": True, "timestamp_within": timedelta(seconds=3600)},
    )


class MessageDisabledTest(BaseModel):
    const_test: int = FieldInfo(default=0, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, extra={"enable": True})
    range_test: int = FieldInfo(default=0, extra={"enable": True})


class MessageIgnoredTest(BaseModel):
    const_test: int = FieldInfo(default=0, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, extra={"enable": True})
    range_test: int = FieldInfo(default=0, extra={"enable": True})


class OneOfTest(BaseModel):
    header: str = FieldInfo(default="")
    x: str = FieldInfo(default="")
    y: int = FieldInfo(default=0)


class OneOfNotTest(BaseModel):
    header: str = FieldInfo(default="")
    x: str = FieldInfo(default="")
    y: int = FieldInfo(default=0)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: str = FieldInfo(default="", min_length=13, max_length=19, extra={"enable": True})
        exp: datetime.datetime = FieldInfo(default_factory="now", extra={"enable": True, "timestamp_gt_now": True})
        uuid: UUID = FieldInfo(default="", extra={"enable": True})

    class NotEnableUserPayMessage(BaseModel):
        bank_number: str = FieldInfo(default="", min_length=13, max_length=19, extra={"enable": True})
        exp: datetime.datetime = FieldInfo(default_factory="now", extra={"enable": True, "timestamp_gt_now": True})
        uuid: UUID = FieldInfo(default="", extra={"enable": True})

    string_in_map_test: typing.Dict[str, StringTest] = FieldInfo(default_factory=dict)
    map_in_map_test: typing.Dict[str, MapTest] = FieldInfo(default_factory=dict)
    user_pay: "UserPayMessage" = FieldInfo()
    not_enable_user_pay: "NotEnableUserPayMessage" = FieldInfo()
    empty: None = FieldInfo()
