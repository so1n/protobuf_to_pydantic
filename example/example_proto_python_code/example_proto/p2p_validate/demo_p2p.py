# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

import datetime
import typing
from datetime import datetime, timedelta
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID, uuid4

from google.protobuf.any_pb2 import Any  # type: ignore
from google.protobuf.any_pb2 import Any as AnyMessage
from google.protobuf.message import Message  # type: ignore
from protobuf_to_pydantic.customer_con_type import contimedelta, contimestamp
from protobuf_to_pydantic.get_desc.from_pb_option.types import HostNameStr, UriRefStr
from protobuf_to_pydantic.util import Timedelta
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic.networks import AnyUrl, EmailStr, IPvAnyAddress
from pydantic.types import conbytes, confloat, conint, conlist, constr

from example.plugin_config import CustomerField, customer_any


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
    default_test: float = FieldInfo(default=1.0, extra={"enable": True})
    not_enable_test: float = FieldInfo(default=0.0, extra={"enable": False})
    default_factory_test: float = FieldInfo(default_factory=float, extra={"enable": True})
    miss_default_test: float = FieldInfo(extra={"enable": True})
    alias_test: float = FieldInfo(default=0.0, alias="alias", extra={"enable": True})
    desc_test: float = FieldInfo(default=0.0, description="test desc", extra={"enable": True})
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3, extra={"enable": True})
    example_test: float = FieldInfo(default=0.0, extra={"enable": True, "example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"enable": True, "example": float})
    field_test: float = CustomerField(default=0.0, extra={"enable": True})
    type_test: confloat() = FieldInfo(default=0.0, extra={"enable": True})
    title_test: float = FieldInfo(default=0.0, title="title_test", extra={"enable": True})


class DoubleTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True, extra={"enable": True})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={"enable": True})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={"enable": True})
    in_test: float = FieldInfo(default=0.0, extra={"enable": True, "in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"enable": True, "not_in": [1.0, 2.0, 3.0]})
    default_test: float = FieldInfo(default=1.0, extra={"enable": True})
    not_enable_test: float = FieldInfo(default=0.0, extra={"enable": False})
    default_factory_test: float = FieldInfo(default_factory=float, extra={"enable": True})
    miss_default_test: float = FieldInfo(extra={"enable": True})
    alias_test: float = FieldInfo(default=0.0, alias="alias", extra={"enable": True})
    desc_test: float = FieldInfo(default=0.0, description="test desc", extra={"enable": True})
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3, extra={"enable": True})
    example_test: float = FieldInfo(default=0.0, extra={"enable": True, "example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"enable": True, "example": float})
    field_test: float = CustomerField(default=0.0, extra={"enable": True})
    type_test: confloat() = FieldInfo(default=0.0, extra={"enable": True})
    title_test: float = FieldInfo(default=0.0, title="title_test", extra={"enable": True})


class Int32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={"enable": True})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={"enable": True})
    in_test: int = FieldInfo(default=0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"enable": True, "not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0, extra={"enable": True})
    not_enable_test: int = FieldInfo(default=0, extra={"enable": False})
    default_factory_test: int = FieldInfo(default_factory=int, extra={"enable": True})
    miss_default_test: int = FieldInfo(extra={"enable": True})
    alias_test: int = FieldInfo(default=0, alias="alias", extra={"enable": True})
    desc_test: int = FieldInfo(default=0, description="test desc", extra={"enable": True})
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3, extra={"enable": True})
    example_test: int = FieldInfo(default=0, extra={"enable": True, "example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"enable": True, "example": int})
    field_test: int = CustomerField(default=0, extra={"enable": True})
    type_test: confloat() = FieldInfo(default=0, extra={"enable": True})
    title_test: int = FieldInfo(default=0, title="title_test", extra={"enable": True})


class Int64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={"enable": True})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={"enable": True})
    in_test: int = FieldInfo(default=0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"enable": True, "not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0, extra={"enable": True})
    not_enable_test: int = FieldInfo(default=0, extra={"enable": False})
    default_factory_test: int = FieldInfo(default_factory=int, extra={"enable": True})
    miss_default_test: int = FieldInfo(extra={"enable": True})
    alias_test: int = FieldInfo(default=0, alias="alias", extra={"enable": True})
    desc_test: int = FieldInfo(default=0, description="test desc", extra={"enable": True})
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3, extra={"enable": True})
    example_test: int = FieldInfo(default=0, extra={"enable": True, "example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"enable": True, "example": int})
    field_test: int = CustomerField(default=0, extra={"enable": True})
    type_test: confloat() = FieldInfo(default=0, extra={"enable": True})
    title_test: int = FieldInfo(default=0, title="title_test", extra={"enable": True})


class Uint32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={"enable": True})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={"enable": True})
    in_test: int = FieldInfo(default=0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"enable": True, "not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0, extra={"enable": True})
    not_enable_test: int = FieldInfo(default=0, extra={"enable": False})
    default_factory_test: int = FieldInfo(default_factory=int, extra={"enable": True})
    miss_default_test: int = FieldInfo(extra={"enable": True})
    alias_test: int = FieldInfo(default=0, alias="alias", extra={"enable": True})
    desc_test: int = FieldInfo(default=0, description="test desc", extra={"enable": True})
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3, extra={"enable": True})
    example_test: int = FieldInfo(default=0, extra={"enable": True, "example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"enable": True, "example": int})
    field_test: int = CustomerField(default=0, extra={"enable": True})
    type_test: conint() = FieldInfo(default=0, extra={"enable": True})
    title_test: int = FieldInfo(default=0, title="title_test", extra={"enable": True})


class Sint32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={"enable": True})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={"enable": True})
    in_test: int = FieldInfo(default=0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"enable": True, "not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0, extra={"enable": True})
    not_enable_test: int = FieldInfo(default=0, extra={"enable": False})
    default_factory_test: int = FieldInfo(default_factory=int, extra={"enable": True})
    miss_default_test: int = FieldInfo(extra={"enable": True})
    alias_test: int = FieldInfo(default=0, alias="alias", extra={"enable": True})
    desc_test: int = FieldInfo(default=0, description="test desc", extra={"enable": True})
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3, extra={"enable": True})
    example_test: int = FieldInfo(default=0, extra={"enable": True, "example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"enable": True, "example": int})
    field_test: int = CustomerField(default=0, extra={"enable": True})
    type_test: conint() = FieldInfo(default=0, extra={"enable": True})
    title_test: int = FieldInfo(default=0, title="title_test", extra={"enable": True})


class Uint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={"enable": True})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={"enable": True})
    in_test: int = FieldInfo(default=0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"enable": True, "not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0, extra={"enable": True})
    not_enable_test: int = FieldInfo(default=0, extra={"enable": False})
    default_factory_test: int = FieldInfo(default_factory=int, extra={"enable": True})
    miss_default_test: int = FieldInfo(extra={"enable": True})
    alias_test: int = FieldInfo(default=0, alias="alias", extra={"enable": True})
    desc_test: int = FieldInfo(default=0, description="test desc", extra={"enable": True})
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3, extra={"enable": True})
    example_test: int = FieldInfo(default=0, extra={"enable": True, "example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"enable": True, "example": int})
    field_test: int = CustomerField(default=0, extra={"enable": True})
    type_test: conint() = FieldInfo(default=0, extra={"enable": True})
    title_test: int = FieldInfo(default=0, title="title_test", extra={"enable": True})


class Sint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: int = FieldInfo(default=0, ge=1, le=10, extra={"enable": True})
    range_test: int = FieldInfo(default=0, gt=1, lt=10, extra={"enable": True})
    in_test: int = FieldInfo(default=0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"enable": True, "not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0, extra={"enable": True})
    not_enable_test: int = FieldInfo(default=0, extra={"enable": False})
    default_factory_test: int = FieldInfo(default_factory=int, extra={"enable": True})
    miss_default_test: int = FieldInfo(extra={"enable": True})
    alias_test: int = FieldInfo(default=0, alias="alias", extra={"enable": True})
    desc_test: int = FieldInfo(default=0, description="test desc", extra={"enable": True})
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3, extra={"enable": True})
    example_test: int = FieldInfo(default=0, extra={"enable": True, "example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"enable": True, "example": int})
    field_test: int = CustomerField(default=0, extra={"enable": True})
    type_test: conint() = FieldInfo(default=0, extra={"enable": True})
    title_test: int = FieldInfo(default=0, title="title_test", extra={"enable": True})


class Fixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True, extra={"enable": True})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={"enable": True})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={"enable": True})
    in_test: float = FieldInfo(default=0.0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0.0, extra={"enable": True, "not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0, extra={"enable": True})
    not_enable_test: float = FieldInfo(default=0.0, extra={"enable": False})
    default_factory_test: float = FieldInfo(default_factory=float, extra={"enable": True})
    miss_default_test: float = FieldInfo(extra={"enable": True})
    alias_test: float = FieldInfo(default=0.0, alias="alias", extra={"enable": True})
    desc_test: float = FieldInfo(default=0.0, description="test desc", extra={"enable": True})
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3, extra={"enable": True})
    example_test: float = FieldInfo(default=0.0, extra={"enable": True, "example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"enable": True, "example": float})
    field_test: float = CustomerField(default=0.0, extra={"enable": True})
    type_test: confloat() = FieldInfo(default=0.0, extra={"enable": True})
    title_test: float = FieldInfo(default=0.0, title="title_test", extra={"enable": True})


class Fixed64Test(BaseModel):
    const_test: float = FieldInfo(default=0.0, extra={"enable": True})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={"enable": True})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={"enable": True})
    in_test: float = FieldInfo(default=0.0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0.0, extra={"enable": True, "not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0, extra={"enable": True})
    not_enable_test: float = FieldInfo(default=0.0, extra={"enable": False})
    default_factory_test: float = FieldInfo(default_factory=float, extra={"enable": True})
    miss_default_test: float = FieldInfo(extra={"enable": True})
    alias_test: float = FieldInfo(default=0.0, alias="alias", extra={"enable": True})
    desc_test: float = FieldInfo(default=0.0, description="test desc", extra={"enable": True})
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3, extra={"enable": True})
    example_test: float = FieldInfo(default=0.0, extra={"enable": True, "example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"enable": True, "example": float})
    field_test: float = CustomerField(default=0.0, extra={"enable": True})
    type_test: confloat() = FieldInfo(default=0.0, extra={"enable": True})
    title_test: float = FieldInfo(default=0.0, title="title_test", extra={"enable": True})


class Sfixed32Test(BaseModel):
    const_test: float = FieldInfo(default=0.0, extra={"enable": True})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={"enable": True})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={"enable": True})
    in_test: float = FieldInfo(default=0.0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0.0, extra={"enable": True, "not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0, extra={"enable": True})
    not_enable_test: float = FieldInfo(default=0.0, extra={"enable": False})
    default_factory_test: float = FieldInfo(default_factory=float, extra={"enable": True})
    miss_default_test: float = FieldInfo(extra={"enable": True})
    alias_test: float = FieldInfo(default=0.0, alias="alias", extra={"enable": True})
    desc_test: float = FieldInfo(default=0.0, description="test desc", extra={"enable": True})
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3, extra={"enable": True})
    example_test: float = FieldInfo(default=0.0, extra={"enable": True, "example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"enable": True, "example": float})
    field_test: float = CustomerField(default=0.0, extra={"enable": True})
    type_test: confloat() = FieldInfo(default=0.0, extra={"enable": True})
    title_test: float = FieldInfo(default=0.0, title="title_test", extra={"enable": True})


class Sfixed64Test(BaseModel):
    const_test: float = FieldInfo(default=0.0, extra={"enable": True})
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10, extra={"enable": True})
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10, extra={"enable": True})
    in_test: float = FieldInfo(default=0.0, extra={"enable": True, "in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0.0, extra={"enable": True, "not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0, extra={"enable": True})
    not_enable_test: float = FieldInfo(default=0.0, extra={"enable": False})
    default_factory_test: float = FieldInfo(default_factory=float, extra={"enable": True})
    miss_default_test: float = FieldInfo(extra={"enable": True})
    alias_test: float = FieldInfo(default=0.0, alias="alias", extra={"enable": True})
    desc_test: float = FieldInfo(default=0.0, description="test desc", extra={"enable": True})
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3, extra={"enable": True})
    example_test: float = FieldInfo(default=0.0, extra={"enable": True, "example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"enable": True, "example": float})
    field_test: float = CustomerField(default=0.0, extra={"enable": True})
    type_test: confloat() = FieldInfo(default=0.0, extra={"enable": True})
    title_test: float = FieldInfo(default=0.0, title="title_test", extra={"enable": True})


class BoolTest(BaseModel):
    bool_1_test: bool = FieldInfo(default=True, const=True, extra={"enable": True})
    bool_2_test: bool = FieldInfo(default=False, const=True, extra={"enable": True})
    enable_test: bool = FieldInfo(default=False, extra={"enable": False})
    default_test: bool = FieldInfo(default=True, extra={"enable": True})
    miss_default_test: bool = FieldInfo(extra={"enable": True})
    alias_test: bool = FieldInfo(default=False, alias="alias", extra={"enable": True})
    desc_test: bool = FieldInfo(default=False, description="test desc", extra={"enable": True})
    example_test: bool = FieldInfo(default=False, extra={"enable": True, "example": True})
    field_test: bool = CustomerField(default=False, extra={"enable": True})
    title_test: bool = FieldInfo(default=False, title="title_test", extra={"enable": True})


class StringTest(BaseModel):
    const_test: str = FieldInfo(default="aaa", const=True, extra={"enable": True})
    len_test: str = FieldInfo(default="", extra={"enable": True, "len": 3})
    s_range_len_test: str = FieldInfo(default="", min_length=1, max_length=3, extra={"enable": True})
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
    pydantic_type_test: str = FieldInfo(default="", extra={"enable": True})
    enable_test: str = FieldInfo(default="", extra={"enable": False})
    default_test: str = FieldInfo(default="default", extra={"enable": True})
    default_factory_test: str = FieldInfo(default_factory=uuid4, extra={"enable": True})
    miss_default_test: str = FieldInfo(extra={"enable": True})
    alias_test: str = FieldInfo(default="", alias="alias", extra={"enable": True})
    desc_test: str = FieldInfo(default="", description="test desc", extra={"enable": True})
    example_test: str = FieldInfo(default="", extra={"enable": True, "example": "example"})
    example_factory_test: str = FieldInfo(default="", extra={"enable": True, "example": uuid4})
    field_test: str = CustomerField(default="", extra={"enable": True})
    title_test: str = FieldInfo(default="", title="title_test", extra={"enable": True})
    type_test: constr() = FieldInfo(default="", extra={"enable": True})


class BytesTest(BaseModel):
    const_test: bytes = FieldInfo(default=b"demo", const=True, extra={"enable": True})
    range_len_test: bytes = FieldInfo(default=b"", min_length=1, max_length=4, extra={"enable": True})
    prefix_test: bytes = FieldInfo(default=b"", extra={"enable": True, "prefix": b"prefix"})
    suffix_test: bytes = FieldInfo(default=b"", extra={"enable": True, "suffix": b"suffix"})
    contains_test: bytes = FieldInfo(default=b"", extra={"contains": b"contains", "enable": True})
    in_test: bytes = FieldInfo(default=b"", extra={"enable": True, "in": [b"a", b"b", b"c"]})
    not_in_test: bytes = FieldInfo(default=b"", extra={"enable": True, "not_in": [b"a", b"b", b"c"]})
    enable_test: bytes = FieldInfo(default=b"", extra={"enable": False})
    default_test: bytes = FieldInfo(default=b"default", extra={"enable": True})
    default_factory_test: bytes = FieldInfo(default_factory=bytes, extra={"enable": True})
    miss_default_test: bytes = FieldInfo(extra={"enable": True})
    alias_test: bytes = FieldInfo(default=b"", alias="alias", extra={"enable": True})
    desc_test: bytes = FieldInfo(default=b"", description="test desc", extra={"enable": True})
    example_test: bytes = FieldInfo(default=b"", extra={"enable": True, "example": b"example"})
    example_factory_test: bytes = FieldInfo(default=b"", extra={"enable": True, "example": bytes})
    field_test: bytes = CustomerField(default=b"", extra={"enable": True})
    title_test: bytes = FieldInfo(default=b"", title="title_test", extra={"enable": True})
    type_test: constr() = FieldInfo(default=b"", extra={"enable": True})


class EnumTest(BaseModel):
    const_test: "State" = FieldInfo(default=0)
    in_test: "State" = FieldInfo(default=0)
    not_in_test: "State" = FieldInfo(default=0)
    enable_test: "State" = FieldInfo(default=0)
    default_test: "State" = FieldInfo(default=0)
    miss_default_test: "State" = FieldInfo(default=0)
    alias_test: "State" = FieldInfo(default=0)
    desc_test: "State" = FieldInfo(default=0)
    example_test: "State" = FieldInfo(default=0)
    field_test: "State" = FieldInfo(default=0)
    title_test: "State" = FieldInfo(default=0)


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = FieldInfo(
        default_factory=dict, extra={"enable": True, "map_max_pairs": 5, "map_min_pairs": 1}
    )
    keys_test: typing.Dict[constr(min_length=1, max_length=5), int] = FieldInfo(
        default_factory=dict, extra={"enable": True}
    )
    values_test: typing.Dict[str, conint(ge=5, le=5)] = FieldInfo(default_factory=dict, extra={"enable": True})
    keys_values_test: typing.Dict[constr(min_length=1, max_length=5), contimestamp(timestamp_gt_now=True)] = FieldInfo(
        default_factory=dict, extra={"enable": True}
    )
    enable_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, extra={"enable": False})
    default_factory_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, extra={"enable": True})
    miss_default_test: typing.Dict[str, int] = FieldInfo(extra={"enable": True})
    alias_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, alias="alias", extra={"enable": True})
    desc_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, description="test desc", extra={"enable": True})
    example_factory_test: typing.Dict[str, int] = FieldInfo(
        default_factory=dict, extra={"enable": True, "example": dict}
    )
    field_test: typing.Dict[str, int] = CustomerField(default_factory=dict, extra={"enable": True})
    title_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, title="title_test", extra={"enable": True})
    type_test: dict = FieldInfo(default_factory=dict, extra={"enable": True})


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
        item_type=contimedelta(duration_ge=timedelta(seconds=10), duration_le=timedelta(seconds=10)),
        min_items=1,
        max_items=5,
    ) = FieldInfo(default_factory=list, extra={"enable": True})
    items_bytes_test: conlist(item_type=conbytes(min_length=1, max_length=5), min_items=1, max_items=5) = FieldInfo(
        default_factory=list, extra={"enable": True}
    )
    enable_test: typing.List[str] = FieldInfo(default_factory=list, extra={"enable": False})
    default_factory_test: typing.List[str] = FieldInfo(default_factory=list, extra={"enable": True})
    miss_default_test: typing.List[str] = FieldInfo(extra={"enable": True})
    alias_test: typing.List[str] = FieldInfo(default_factory=list, alias="alias", extra={"enable": True})
    desc_test: typing.List[str] = FieldInfo(default_factory=list, description="test desc", extra={"enable": True})
    example_factory_test: typing.List[str] = FieldInfo(default_factory=list, extra={"enable": True, "example": list})
    field_test: typing.List[str] = CustomerField(default_factory=list, extra={"enable": True})
    title_test: typing.List[str] = FieldInfo(default_factory=list, title="title_test", extra={"enable": True})
    type_test: list = FieldInfo(default_factory=list, extra={"enable": True})


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
            "any_in": [
                "type.googleapis.com/google.protobuf.Timestamp",
                Any(type_url="type.googleapis.com/google.protobuf.Duration"),
            ],
            "enable": True,
        },
    )
    enable_test: AnyMessage = FieldInfo(default_factory="AnyMessage", extra={"enable": False})
    default_test: AnyMessage = FieldInfo(
        default=Any(type_url="type.googleapis.com/google.protobuf.Duration"), extra={"enable": True}
    )
    default_factory_test: AnyMessage = FieldInfo(default_factory=customer_any, extra={"enable": True})
    miss_default_test: AnyMessage = FieldInfo(extra={"enable": True})
    alias_test: AnyMessage = FieldInfo(default_factory="AnyMessage", alias="alias", extra={"enable": True})
    desc_test: AnyMessage = FieldInfo(default_factory="AnyMessage", description="test desc", extra={"enable": True})
    example_test: AnyMessage = FieldInfo(
        default_factory="AnyMessage", extra={"enable": True, "example": "type.googleapis.com/google.protobuf.Duration"}
    )
    example_factory_test: AnyMessage = FieldInfo(
        default_factory="AnyMessage", extra={"enable": True, "example": customer_any}
    )
    field_test: AnyMessage = CustomerField(default_factory="AnyMessage", extra={"enable": True})
    title_test: AnyMessage = FieldInfo(default_factory="AnyMessage", title="title_test", extra={"enable": True})


class DurationTest(BaseModel):
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
    enable_test: Timedelta = FieldInfo(default_factory="Timedelta", extra={"enable": False})
    default_test: Timedelta = FieldInfo(default=timedelta(seconds=1, microseconds=500000), extra={"enable": True})
    default_factory_test: Timedelta = FieldInfo(default_factory=timedelta, extra={"enable": True})
    miss_default_test: Timedelta = FieldInfo(extra={"enable": True})
    alias_test: Timedelta = FieldInfo(default_factory="Timedelta", alias="alias", extra={"enable": True})
    desc_test: Timedelta = FieldInfo(default_factory="Timedelta", description="test desc", extra={"enable": True})
    example_test: Timedelta = FieldInfo(
        default_factory="Timedelta", extra={"enable": True, "example": timedelta(seconds=1, microseconds=500000)}
    )
    example_factory_test: Timedelta = FieldInfo(
        default_factory="Timedelta", extra={"enable": True, "example": timedelta}
    )
    field_test: Timedelta = CustomerField(default_factory="Timedelta", extra={"enable": True})
    title_test: Timedelta = FieldInfo(default_factory="Timedelta", title="title_test", extra={"enable": True})
    type_test: timedelta = FieldInfo(default_factory="Timedelta", extra={"enable": True})


class TimestampTest(BaseModel):
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
    enable_test: datetime.datetime = FieldInfo(default_factory="now", extra={"enable": False})
    default_test: datetime.datetime = FieldInfo(default=1.5, extra={"enable": True})
    default_factory_test: datetime.datetime = FieldInfo(default_factory=datetime.now, extra={"enable": True})
    miss_default_test: datetime.datetime = FieldInfo(extra={"enable": True})
    alias_test: datetime.datetime = FieldInfo(default_factory="now", alias="alias", extra={"enable": True})
    desc_test: datetime.datetime = FieldInfo(default_factory="now", description="test desc", extra={"enable": True})
    example_test: datetime.datetime = FieldInfo(default_factory="now", extra={"enable": True, "example": 1.5})
    example_factory_test: datetime.datetime = FieldInfo(
        default_factory="now", extra={"enable": True, "example": datetime.now}
    )
    field_test: datetime.datetime = CustomerField(default_factory="now", extra={"enable": True})
    title_test: datetime.datetime = FieldInfo(default_factory="now", title="title_test", extra={"enable": True})
    type_test: datetime = FieldInfo(default_factory="now", extra={"enable": True})


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
