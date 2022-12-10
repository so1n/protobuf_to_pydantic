# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

from enum import IntEnum
from google.protobuf.any_pb2 import Any as AnyMessage  # type: ignore
from google.protobuf.message import Message  # type: ignore
from protobuf_to_pydantic.util import Timedelta
from pydantic import BaseModel
from pydantic.fields import FieldInfo
import datetime
import typing


class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class FloatTest(BaseModel):
    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0)
    range_test: float = FieldInfo(default=0.0)
    in_test: float = FieldInfo(default=0.0)
    not_in_test: float = FieldInfo(default=0.0)
    ignore_test: float = FieldInfo(default=0.0)


class DoubleTest(BaseModel):
    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0)
    range_test: float = FieldInfo(default=0.0)
    in_test: float = FieldInfo(default=0.0)
    not_in_test: float = FieldInfo(default=0.0)
    ignore_test: float = FieldInfo(default=0.0)


class Int32Test(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
    in_test: int = FieldInfo(default=0)
    not_in_test: int = FieldInfo(default=0)
    ignore_test: int = FieldInfo(default=0)


class Uint32Test(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
    in_test: int = FieldInfo(default=0)
    not_in_test: int = FieldInfo(default=0)
    ignore_test: int = FieldInfo(default=0)


class Sint32Test(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
    in_test: int = FieldInfo(default=0)
    not_in_test: int = FieldInfo(default=0)
    ignore_test: int = FieldInfo(default=0)


class Int64Test(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
    in_test: int = FieldInfo(default=0)
    not_in_test: int = FieldInfo(default=0)
    ignore_test: int = FieldInfo(default=0)


class Uint64Test(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
    in_test: int = FieldInfo(default=0)
    not_in_test: int = FieldInfo(default=0)
    ignore_test: int = FieldInfo(default=0)


class Sint64Test(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
    in_test: int = FieldInfo(default=0)
    not_in_test: int = FieldInfo(default=0)
    ignore_test: int = FieldInfo(default=0)


class Fixed32Test(BaseModel):
    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0)
    range_test: float = FieldInfo(default=0.0)
    in_test: float = FieldInfo(default=0.0)
    not_in_test: float = FieldInfo(default=0.0)
    ignore_test: float = FieldInfo(default=0.0)


class Fixed64Test(BaseModel):
    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0)
    range_test: float = FieldInfo(default=0.0)
    in_test: float = FieldInfo(default=0.0)
    not_in_test: float = FieldInfo(default=0.0)
    ignore_test: float = FieldInfo(default=0.0)


class Sfixed32Test(BaseModel):
    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0)
    range_test: float = FieldInfo(default=0.0)
    in_test: float = FieldInfo(default=0.0)
    not_in_test: float = FieldInfo(default=0.0)
    ignore_test: float = FieldInfo(default=0.0)


class Sfixed64Test(BaseModel):
    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0)
    range_test: float = FieldInfo(default=0.0)
    in_test: float = FieldInfo(default=0.0)
    not_in_test: float = FieldInfo(default=0.0)
    ignore_test: float = FieldInfo(default=0.0)


class BoolTest(BaseModel):
    bool_1_test: bool = FieldInfo(default=False)
    bool_2_test: bool = FieldInfo(default=False)


class StringTest(BaseModel):
    const_test: str = FieldInfo(default='')
    len_test: str = FieldInfo(default='')
    s_range_len_test: str = FieldInfo(default='')
    b_range_len_test: str = FieldInfo(default='')
    pattern_test: str = FieldInfo(default='')
    prefix_test: str = FieldInfo(default='')
    suffix_test: str = FieldInfo(default='')
    contains_test: str = FieldInfo(default='')
    not_contains_test: str = FieldInfo(default='')
    in_test: str = FieldInfo(default='')
    not_in_test: str = FieldInfo(default='')
    email_test: str = FieldInfo(default='')
    hostname_test: str = FieldInfo(default='')
    ip_test: str = FieldInfo(default='')
    ipv4_test: str = FieldInfo(default='')
    ipv6_test: str = FieldInfo(default='')
    uri_test: str = FieldInfo(default='')
    uri_ref_test: str = FieldInfo(default='')
    address_test: str = FieldInfo(default='')
    uuid_test: str = FieldInfo(default='')
    ignore_test: str = FieldInfo(default='')


class BytesTest(BaseModel):
    const_test: bytes = FieldInfo(default=b'')
    len_test: bytes = FieldInfo(default=b'')
    range_len_test: bytes = FieldInfo(default=b'')
    pattern_test: bytes = FieldInfo(default=b'')
    prefix_test: bytes = FieldInfo(default=b'')
    suffix_test: bytes = FieldInfo(default=b'')
    contains_test: bytes = FieldInfo(default=b'')
    in_test: bytes = FieldInfo(default=b'')
    not_in_test: bytes = FieldInfo(default=b'')


class EnumTest(BaseModel):
    const_test: 'State' = FieldInfo(default=0)
    defined_only_test: 'State' = FieldInfo(default=0)
    in_test: 'State' = FieldInfo(default=0)
    not_in_test: 'State' = FieldInfo(default=0)


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    no_parse_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    keys_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    values_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    keys_values_test: typing.Dict[str, datetime.datetime] = FieldInfo(default_factory=dict)
    ignore_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)


class MessageTest(BaseModel):
    skip_test: str = FieldInfo(default='')
    required_test: str = FieldInfo(default='')


class RepeatedTest(BaseModel):
    range_test: typing.List[str] = FieldInfo(default_factory=list)
    unique_test: typing.List[str] = FieldInfo(default_factory=list)
    items_string_test: typing.List[str] = FieldInfo(default_factory=list)
    items_double_test: typing.List[float] = FieldInfo(default_factory=list)
    items_int32_test: typing.List[int] = FieldInfo(default_factory=list)
    items_timestamp_test: typing.List[datetime.datetime] = FieldInfo(default_factory=list)
    items_duration_test: typing.List[Timedelta] = FieldInfo(default_factory=list)
    items_bytes_test: typing.List[bytes] = FieldInfo(default_factory=list)
    ignore_test: typing.List[str] = FieldInfo(default_factory=list)


class AnyTest(BaseModel):
    required_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    not_in_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    in_test: AnyMessage = FieldInfo(default_factory=AnyMessage)


class DurationTest(BaseModel):
    required_test: Timedelta = FieldInfo(default_factory=Timedelta)
    const_test: Timedelta = FieldInfo(default_factory=Timedelta)
    range_test: Timedelta = FieldInfo(default_factory=Timedelta)
    range_e_test: Timedelta = FieldInfo(default_factory=Timedelta)
    in_test: Timedelta = FieldInfo(default_factory=Timedelta)
    not_in_test: Timedelta = FieldInfo(default_factory=Timedelta)


class TimestampTest(BaseModel):
    required_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    const_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    range_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    range_e_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    lt_now_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    gt_now_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    within_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    within_and_gt_now_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)


class MessageDisabledTest(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)


class MessageIgnoredTest(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)


class OneOfTest(BaseModel):
    header: str = FieldInfo(default='')
    x: str = FieldInfo(default='')
    y: int = FieldInfo(default=0)


class OneOfNotTest(BaseModel):
    header: str = FieldInfo(default='')
    x: str = FieldInfo(default='')
    y: int = FieldInfo(default=0)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: str = FieldInfo(default='')
        exp: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
        uuid: str = FieldInfo(default='')

    class NotEnableUserPayMessage(BaseModel):
        bank_number: str = FieldInfo(default='')
        exp: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
        uuid: str = FieldInfo(default='')

    string_in_map_test: typing.Dict[str, StringTest] = FieldInfo(default_factory=dict)
    map_in_map_test: typing.Dict[str, MapTest] = FieldInfo(default_factory=dict)
    user_pay: "UserPayMessage" = FieldInfo()
    not_enable_user_pay: "NotEnableUserPayMessage" = FieldInfo()
    empty: None = FieldInfo()
