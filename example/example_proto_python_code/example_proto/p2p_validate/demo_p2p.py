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
    default_test: float = FieldInfo(default=0.0)
    not_enable_test: float = FieldInfo(default=0.0)
    default_factory_test: float = FieldInfo(default=0.0)
    miss_default_test: float = FieldInfo(default=0.0)
    alias_test: float = FieldInfo(default=0.0)
    desc_test: float = FieldInfo(default=0.0)
    multiple_of_test: float = FieldInfo(default=0.0)
    example_test: float = FieldInfo(default=0.0)
    example_factory: float = FieldInfo(default=0.0)
    field_test: float = FieldInfo(default=0.0)
    type_test: float = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0)


class DoubleTest(BaseModel):
    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0)
    range_test: float = FieldInfo(default=0.0)
    in_test: float = FieldInfo(default=0.0)
    not_in_test: float = FieldInfo(default=0.0)
    default_test: float = FieldInfo(default=0.0)
    not_enable_test: float = FieldInfo(default=0.0)
    default_factory_test: float = FieldInfo(default=0.0)
    miss_default_test: float = FieldInfo(default=0.0)
    alias_test: float = FieldInfo(default=0.0)
    desc_test: float = FieldInfo(default=0.0)
    multiple_of_test: float = FieldInfo(default=0.0)
    example_test: float = FieldInfo(default=0.0)
    example_factory: float = FieldInfo(default=0.0)
    field_test: float = FieldInfo(default=0.0)
    type_test: float = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0)


class Int32Test(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
    in_test: int = FieldInfo(default=0)
    not_in_test: int = FieldInfo(default=0)
    default_test: int = FieldInfo(default=0)
    not_enable_test: int = FieldInfo(default=0)
    default_factory_test: int = FieldInfo(default=0)
    miss_default_test: int = FieldInfo(default=0)
    alias_test: int = FieldInfo(default=0)
    desc_test: int = FieldInfo(default=0)
    multiple_of_test: int = FieldInfo(default=0)
    example_test: int = FieldInfo(default=0)
    example_factory: int = FieldInfo(default=0)
    field_test: int = FieldInfo(default=0)
    type_test: int = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0)


class Int64Test(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
    in_test: int = FieldInfo(default=0)
    not_in_test: int = FieldInfo(default=0)
    default_test: int = FieldInfo(default=0)
    not_enable_test: int = FieldInfo(default=0)
    default_factory_test: int = FieldInfo(default=0)
    miss_default_test: int = FieldInfo(default=0)
    alias_test: int = FieldInfo(default=0)
    desc_test: int = FieldInfo(default=0)
    multiple_of_test: int = FieldInfo(default=0)
    example_test: int = FieldInfo(default=0)
    example_factory: int = FieldInfo(default=0)
    field_test: int = FieldInfo(default=0)
    type_test: int = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0)


class Uint32Test(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
    in_test: int = FieldInfo(default=0)
    not_in_test: int = FieldInfo(default=0)
    default_test: int = FieldInfo(default=0)
    not_enable_test: int = FieldInfo(default=0)
    default_factory_test: int = FieldInfo(default=0)
    miss_default_test: int = FieldInfo(default=0)
    alias_test: int = FieldInfo(default=0)
    desc_test: int = FieldInfo(default=0)
    multiple_of_test: int = FieldInfo(default=0)
    example_test: int = FieldInfo(default=0)
    example_factory: int = FieldInfo(default=0)
    field_test: int = FieldInfo(default=0)
    type_test: int = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0)


class Sint32Test(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
    in_test: int = FieldInfo(default=0)
    not_in_test: int = FieldInfo(default=0)
    default_test: int = FieldInfo(default=0)
    not_enable_test: int = FieldInfo(default=0)
    default_factory_test: int = FieldInfo(default=0)
    miss_default_test: int = FieldInfo(default=0)
    alias_test: int = FieldInfo(default=0)
    desc_test: int = FieldInfo(default=0)
    multiple_of_test: int = FieldInfo(default=0)
    example_test: int = FieldInfo(default=0)
    example_factory: int = FieldInfo(default=0)
    field_test: int = FieldInfo(default=0)
    type_test: int = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0)


class Uint64Test(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
    in_test: int = FieldInfo(default=0)
    not_in_test: int = FieldInfo(default=0)
    default_test: int = FieldInfo(default=0)
    not_enable_test: int = FieldInfo(default=0)
    default_factory_test: int = FieldInfo(default=0)
    miss_default_test: int = FieldInfo(default=0)
    alias_test: int = FieldInfo(default=0)
    desc_test: int = FieldInfo(default=0)
    multiple_of_test: int = FieldInfo(default=0)
    example_test: int = FieldInfo(default=0)
    example_factory: int = FieldInfo(default=0)
    field_test: int = FieldInfo(default=0)
    type_test: int = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0)


class Sint64Test(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)
    in_test: int = FieldInfo(default=0)
    not_in_test: int = FieldInfo(default=0)
    default_test: int = FieldInfo(default=0)
    not_enable_test: int = FieldInfo(default=0)
    default_factory_test: int = FieldInfo(default=0)
    miss_default_test: int = FieldInfo(default=0)
    alias_test: int = FieldInfo(default=0)
    desc_test: int = FieldInfo(default=0)
    multiple_of_test: int = FieldInfo(default=0)
    example_test: int = FieldInfo(default=0)
    example_factory: int = FieldInfo(default=0)
    field_test: int = FieldInfo(default=0)
    type_test: int = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0)


class Fixed32Test(BaseModel):
    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0)
    range_test: float = FieldInfo(default=0.0)
    in_test: float = FieldInfo(default=0.0)
    not_in_test: float = FieldInfo(default=0.0)
    default_test: float = FieldInfo(default=0.0)
    not_enable_test: float = FieldInfo(default=0.0)
    default_factory_test: float = FieldInfo(default=0.0)
    miss_default_test: float = FieldInfo(default=0.0)
    alias_test: float = FieldInfo(default=0.0)
    desc_test: float = FieldInfo(default=0.0)
    multiple_of_test: float = FieldInfo(default=0.0)
    example_test: float = FieldInfo(default=0.0)
    example_factory: float = FieldInfo(default=0.0)
    field_test: float = FieldInfo(default=0.0)
    type_test: float = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0)


class Fixed64Test(BaseModel):
    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0)
    range_test: float = FieldInfo(default=0.0)
    in_test: float = FieldInfo(default=0.0)
    not_in_test: float = FieldInfo(default=0.0)
    default_test: float = FieldInfo(default=0.0)
    not_enable_test: float = FieldInfo(default=0.0)
    default_factory_test: float = FieldInfo(default=0.0)
    miss_default_test: float = FieldInfo(default=0.0)
    alias_test: float = FieldInfo(default=0.0)
    desc_test: float = FieldInfo(default=0.0)
    multiple_of_test: float = FieldInfo(default=0.0)
    example_test: float = FieldInfo(default=0.0)
    example_factory: float = FieldInfo(default=0.0)
    field_test: float = FieldInfo(default=0.0)
    type_test: float = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0)


class Sfixed32Test(BaseModel):
    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0)
    range_test: float = FieldInfo(default=0.0)
    in_test: float = FieldInfo(default=0.0)
    not_in_test: float = FieldInfo(default=0.0)
    default_test: float = FieldInfo(default=0.0)
    not_enable_test: float = FieldInfo(default=0.0)
    default_factory_test: float = FieldInfo(default=0.0)
    miss_default_test: float = FieldInfo(default=0.0)
    alias_test: float = FieldInfo(default=0.0)
    desc_test: float = FieldInfo(default=0.0)
    multiple_of_test: float = FieldInfo(default=0.0)
    example_test: float = FieldInfo(default=0.0)
    example_factory: float = FieldInfo(default=0.0)
    field_test: float = FieldInfo(default=0.0)
    type_test: float = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0)


class Sfixed64Test(BaseModel):
    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0)
    range_test: float = FieldInfo(default=0.0)
    in_test: float = FieldInfo(default=0.0)
    not_in_test: float = FieldInfo(default=0.0)
    default_test: float = FieldInfo(default=0.0)
    not_enable_test: float = FieldInfo(default=0.0)
    default_factory_test: float = FieldInfo(default=0.0)
    miss_default_test: float = FieldInfo(default=0.0)
    alias_test: float = FieldInfo(default=0.0)
    desc_test: float = FieldInfo(default=0.0)
    multiple_of_test: float = FieldInfo(default=0.0)
    example_test: float = FieldInfo(default=0.0)
    example_factory: float = FieldInfo(default=0.0)
    field_test: float = FieldInfo(default=0.0)
    type_test: float = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0)


class BoolTest(BaseModel):
    bool_1_test: bool = FieldInfo(default=False)
    bool_2_test: bool = FieldInfo(default=False)
    enable_test: bool = FieldInfo(default=False)
    default_test: bool = FieldInfo(default=False)
    miss_default_test: bool = FieldInfo(default=False)
    alias_test: bool = FieldInfo(default=False)
    desc_test: bool = FieldInfo(default=False)
    example_test: bool = FieldInfo(default=False)
    field_test: bool = FieldInfo(default=False)
    title_test: bool = FieldInfo(default=False)


class StringTest(BaseModel):
    const_test: str = FieldInfo(default='')
    len_test: str = FieldInfo(default='')
    s_range_len_test: str = FieldInfo(default='')
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
    pydantic_type_test: str = FieldInfo(default='')
    enable_test: str = FieldInfo(default='')
    default_test: str = FieldInfo(default='')
    default_factory_test: str = FieldInfo(default='')
    miss_default_test: str = FieldInfo(default='')
    alias_test: str = FieldInfo(default='')
    desc_test: str = FieldInfo(default='')
    example_test: str = FieldInfo(default='')
    example_factory_test: str = FieldInfo(default='')
    field_test: str = FieldInfo(default='')
    title_test: str = FieldInfo(default='')
    type_test: str = FieldInfo(default='')


class BytesTest(BaseModel):
    const_test: bytes = FieldInfo(default=b'')
    range_len_test: bytes = FieldInfo(default=b'')
    prefix_test: bytes = FieldInfo(default=b'')
    suffix_test: bytes = FieldInfo(default=b'')
    contains_test: bytes = FieldInfo(default=b'')
    in_test: bytes = FieldInfo(default=b'')
    not_in_test: bytes = FieldInfo(default=b'')
    enable_test: bytes = FieldInfo(default=b'')
    default_test: bytes = FieldInfo(default=b'')
    default_factory_test: bytes = FieldInfo(default=b'')
    miss_default_test: bytes = FieldInfo(default=b'')
    alias_test: bytes = FieldInfo(default=b'')
    desc_test: bytes = FieldInfo(default=b'')
    example_test: bytes = FieldInfo(default=b'')
    example_factory_test: bytes = FieldInfo(default=b'')
    field_test: bytes = FieldInfo(default=b'')
    title_test: bytes = FieldInfo(default=b'')
    type_test: bytes = FieldInfo(default=b'')


class EnumTest(BaseModel):
    const_test: 'State' = FieldInfo(default=0)
    in_test: 'State' = FieldInfo(default=0)
    not_in_test: 'State' = FieldInfo(default=0)
    enable_test: 'State' = FieldInfo(default=0)
    default_test: 'State' = FieldInfo(default=0)
    miss_default_test: 'State' = FieldInfo(default=0)
    alias_test: 'State' = FieldInfo(default=0)
    desc_test: 'State' = FieldInfo(default=0)
    example_test: 'State' = FieldInfo(default=0)
    field_test: 'State' = FieldInfo(default=0)
    title_test: 'State' = FieldInfo(default=0)


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    keys_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    values_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    keys_values_test: typing.Dict[str, datetime.datetime] = FieldInfo(default_factory=dict)
    enable_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    default_factory_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    miss_default_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    alias_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    desc_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    example_factory_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    field_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    title_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    type_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)


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
    enable_test: typing.List[str] = FieldInfo(default_factory=list)
    default_factory_test: typing.List[str] = FieldInfo(default_factory=list)
    miss_default_test: typing.List[str] = FieldInfo(default_factory=list)
    alias_test: typing.List[str] = FieldInfo(default_factory=list)
    desc_test: typing.List[str] = FieldInfo(default_factory=list)
    example_factory_test: typing.List[str] = FieldInfo(default_factory=list)
    field_test: typing.List[str] = FieldInfo(default_factory=list)
    title_test: typing.List[str] = FieldInfo(default_factory=list)
    type_test: typing.List[str] = FieldInfo(default_factory=list)


class AnyTest(BaseModel):
    required_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    not_in_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    in_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    enable_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    default_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    default_factory_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    miss_default_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    alias_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    desc_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    example_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    example_factory_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    field_test: AnyMessage = FieldInfo(default_factory=AnyMessage)
    title_test: AnyMessage = FieldInfo(default_factory=AnyMessage)


class DurationTest(BaseModel):
    const_test: Timedelta = FieldInfo(default_factory=Timedelta)
    range_test: Timedelta = FieldInfo(default_factory=Timedelta)
    range_e_test: Timedelta = FieldInfo(default_factory=Timedelta)
    in_test: Timedelta = FieldInfo(default_factory=Timedelta)
    not_in_test: Timedelta = FieldInfo(default_factory=Timedelta)
    enable_test: Timedelta = FieldInfo(default_factory=Timedelta)
    default_test: Timedelta = FieldInfo(default_factory=Timedelta)
    default_factory_test: Timedelta = FieldInfo(default_factory=Timedelta)
    miss_default_test: Timedelta = FieldInfo(default_factory=Timedelta)
    alias_test: Timedelta = FieldInfo(default_factory=Timedelta)
    desc_test: Timedelta = FieldInfo(default_factory=Timedelta)
    example_test: Timedelta = FieldInfo(default_factory=Timedelta)
    example_factory_test: Timedelta = FieldInfo(default_factory=Timedelta)
    field_test: Timedelta = FieldInfo(default_factory=Timedelta)
    title_test: Timedelta = FieldInfo(default_factory=Timedelta)
    type_test: Timedelta = FieldInfo(default_factory=Timedelta)


class TimestampTest(BaseModel):
    const_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    range_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    range_e_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    lt_now_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    gt_now_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    within_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    within_and_gt_now_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    enable_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    default_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    default_factory_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    miss_default_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    alias_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    desc_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    example_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    example_factory_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    field_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    title_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)
    type_test: datetime.datetime = FieldInfo(default_factory=datetime.datetime.now)


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
