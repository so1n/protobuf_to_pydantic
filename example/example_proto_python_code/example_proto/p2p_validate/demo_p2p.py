# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

import typing
from datetime import datetime, timedelta
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID, uuid4

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

from example.plugin_config import CustomerField, customer_any


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
    in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"not_in": [1.0, 2.0, 3.0]})
    default_test: float = FieldInfo(default=1.0)
    not_enable_test: float = FieldInfo(default=0.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0.0, alias="alias")
    desc_test: float = FieldInfo(default=0.0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3)
    example_test: float = FieldInfo(default=0.0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"example": float})
    field_test: float = CustomerField(default=0.0)
    type_test: confloat() = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0, title="title_test")


class DoubleTest(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"not_in": [1.0, 2.0, 3.0]})
    default_test: float = FieldInfo(default=1.0)
    not_enable_test: float = FieldInfo(default=0.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0.0, alias="alias")
    desc_test: float = FieldInfo(default=0.0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3)
    example_test: float = FieldInfo(default=0.0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"example": float})
    field_test: float = CustomerField(default=0.0)
    type_test: confloat() = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0, title="title_test")


class Int32Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    not_enable_test: int = FieldInfo(default=0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias")
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: confloat() = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0, title="title_test")


class Int64Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    not_enable_test: int = FieldInfo(default=0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias")
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: confloat() = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0, title="title_test")


class Uint32Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    not_enable_test: int = FieldInfo(default=0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias")
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: conint() = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0, title="title_test")


class Sint32Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    not_enable_test: int = FieldInfo(default=0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias")
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: conint() = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0, title="title_test")


class Uint64Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    not_enable_test: int = FieldInfo(default=0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias")
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: conint() = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0, title="title_test")


class Sint64Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    not_enable_test: int = FieldInfo(default=0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias")
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: conint() = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0, title="title_test")


class Fixed32Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0.0, extra={"not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0)
    not_enable_test: float = FieldInfo(default=0.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0.0, alias="alias")
    desc_test: float = FieldInfo(default=0.0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3)
    example_test: float = FieldInfo(default=0.0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"example": float})
    field_test: float = CustomerField(default=0.0)
    type_test: confloat() = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0, title="title_test")


class Fixed64Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0.0, extra={"not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0)
    not_enable_test: float = FieldInfo(default=0.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0.0, alias="alias")
    desc_test: float = FieldInfo(default=0.0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3)
    example_test: float = FieldInfo(default=0.0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"example": float})
    field_test: float = CustomerField(default=0.0)
    type_test: confloat() = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0, title="title_test")


class Sfixed32Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0.0, extra={"not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0)
    not_enable_test: float = FieldInfo(default=0.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0.0, alias="alias")
    desc_test: float = FieldInfo(default=0.0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3)
    example_test: float = FieldInfo(default=0.0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"example": float})
    field_test: float = CustomerField(default=0.0)
    type_test: confloat() = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0, title="title_test")


class Sfixed64Test(BaseModel):

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: float = FieldInfo(default=0.0)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0.0, extra={"not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0)
    not_enable_test: float = FieldInfo(default=0.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0.0, alias="alias")
    desc_test: float = FieldInfo(default=0.0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3)
    example_test: float = FieldInfo(default=0.0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"example": float})
    field_test: float = CustomerField(default=0.0)
    type_test: confloat() = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0, title="title_test")


class BoolTest(BaseModel):

    bool_1_test: bool = FieldInfo(default=True, const=True)
    bool_2_test: bool = FieldInfo(default=False, const=True)
    enable_test: bool = FieldInfo(default=False)
    default_test: bool = FieldInfo(default=True)
    miss_default_test: bool = FieldInfo()
    alias_test: bool = FieldInfo(default=False, alias="alias")
    desc_test: bool = FieldInfo(default=False, description="test desc")
    example_test: bool = FieldInfo(default=False, extra={"example": True})
    field_test: bool = CustomerField(default=False)
    title_test: bool = FieldInfo(default=False, title="title_test")


class StringTest(BaseModel):

    len_test_len_validator = validator("len_test", allow_reuse=True)(len_validator)
    prefix_test_prefix_validator = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_test_suffix_validator = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_test_contains_validator = validator("contains_test", allow_reuse=True)(contains_validator)
    not_contains_test_not_contains_validator = validator("not_contains_test", allow_reuse=True)(not_contains_validator)
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: str = FieldInfo(default="aaa", const=True)
    len_test: str = FieldInfo(default="", extra={"len": 3})
    s_range_len_test: str = FieldInfo(default="", min_length=1, max_length=3)
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
    pydantic_type_test: str = FieldInfo(default="")
    enable_test: str = FieldInfo(default="")
    default_test: str = FieldInfo(default="default")
    default_factory_test: str = FieldInfo(default_factory=uuid4)
    miss_default_test: str = FieldInfo()
    alias_test: str = FieldInfo(default="", alias="alias")
    desc_test: str = FieldInfo(default="", description="test desc")
    example_test: str = FieldInfo(default="", extra={"example": "example"})
    example_factory_test: str = FieldInfo(default="", extra={"example": uuid4})
    field_test: str = CustomerField(default="")
    title_test: str = FieldInfo(default="", title="title_test")
    type_test: constr() = FieldInfo(default="")


class BytesTest(BaseModel):

    prefix_test_prefix_validator = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_test_suffix_validator = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_test_contains_validator = validator("contains_test", allow_reuse=True)(contains_validator)
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)

    const_test: bytes = FieldInfo(default=b"demo", const=True)
    range_len_test: bytes = FieldInfo(default=b"", min_length=1, max_length=4)
    prefix_test: bytes = FieldInfo(default=b"", extra={"prefix": b"prefix"})
    suffix_test: bytes = FieldInfo(default=b"", extra={"suffix": b"suffix"})
    contains_test: bytes = FieldInfo(default=b"", extra={"contains": b"contains"})
    in_test: bytes = FieldInfo(default=b"", extra={"in": [b"a", b"b", b"c"]})
    not_in_test: bytes = FieldInfo(default=b"", extra={"not_in": [b"a", b"b", b"c"]})
    enable_test: bytes = FieldInfo(default=b"")
    default_test: bytes = FieldInfo(default=b"default")
    default_factory_test: bytes = FieldInfo(default_factory=bytes)
    miss_default_test: bytes = FieldInfo()
    alias_test: bytes = FieldInfo(default=b"", alias="alias")
    desc_test: bytes = FieldInfo(default=b"", description="test desc")
    example_test: bytes = FieldInfo(default=b"", extra={"example": b"example"})
    example_factory_test: bytes = FieldInfo(default=b"", extra={"example": bytes})
    field_test: bytes = CustomerField(default=b"")
    title_test: bytes = FieldInfo(default=b"", title="title_test")
    type_test: constr() = FieldInfo(default=b"")


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

    pair_test_map_min_pairs_validator = validator("pair_test", allow_reuse=True)(map_min_pairs_validator)
    pair_test_map_max_pairs_validator = validator("pair_test", allow_reuse=True)(map_max_pairs_validator)

    pair_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, extra={"map_max_pairs": 5, "map_min_pairs": 1})
    keys_test: typing.Dict[constr(min_length=1, max_length=5), int] = FieldInfo(default_factory=dict)
    values_test: typing.Dict[str, conint(ge=5, le=5)] = FieldInfo(default_factory=dict)
    keys_values_test: typing.Dict[constr(min_length=1, max_length=5), contimestamp(timestamp_gt_now=True)] = FieldInfo(
        default_factory=dict
    )
    enable_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    default_factory_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    miss_default_test: typing.Dict[str, int] = FieldInfo()
    alias_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, alias="alias")
    desc_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, description="test desc")
    example_factory_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, extra={"example": dict})
    field_test: typing.Dict[str, int] = CustomerField(default_factory=dict)
    title_test: typing.Dict[str, int] = FieldInfo(default_factory=dict, title="title_test")
    type_test: dict = FieldInfo(default_factory=dict)


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
        item_type=contimedelta(duration_ge=timedelta(seconds=10), duration_le=timedelta(seconds=10)),
        min_items=1,
        max_items=5,
    ) = FieldInfo(default_factory=list)
    items_bytes_test: conlist(item_type=conbytes(min_length=1, max_length=5), min_items=1, max_items=5) = FieldInfo(
        default_factory=list
    )
    enable_test: typing.List[str] = FieldInfo(default_factory=list)
    default_factory_test: typing.List[str] = FieldInfo(default_factory=list)
    miss_default_test: typing.List[str] = FieldInfo()
    alias_test: typing.List[str] = FieldInfo(default_factory=list, alias="alias")
    desc_test: typing.List[str] = FieldInfo(default_factory=list, description="test desc")
    example_factory_test: typing.List[str] = FieldInfo(default_factory=list, extra={"example": list})
    field_test: typing.List[str] = CustomerField(default_factory=list)
    title_test: typing.List[str] = FieldInfo(default_factory=list, title="title_test")
    type_test: list = FieldInfo(default_factory=list)


class AnyTest(BaseModel):

    not_in_test_any_not_in_validator = validator("not_in_test", allow_reuse=True)(any_not_in_validator)
    in_test_any_in_validator = validator("in_test", allow_reuse=True)(any_in_validator)

    required_test: Any = FieldInfo()
    not_in_test: Any = FieldInfo(
        default_factory=Any,
        extra={
            "any_not_in": [
                "type.googleapis.com/google.protobuf.Duration",
                "type.googleapis.com/google.protobuf.Timestamp",
            ]
        },
    )
    in_test: Any = FieldInfo(
        default_factory=Any,
        extra={
            "any_in": [
                "type.googleapis.com/google.protobuf.Timestamp",
                Any(type_url="type.googleapis.com/google.protobuf.Duration"),
            ]
        },
    )
    enable_test: Any = FieldInfo(default_factory=Any)
    default_test: Any = FieldInfo(default=Any(type_url="type.googleapis.com/google.protobuf.Duration"))
    default_factory_test: Any = FieldInfo(default_factory=customer_any)
    miss_default_test: Any = FieldInfo()
    alias_test: Any = FieldInfo(default_factory=Any, alias="alias")
    desc_test: Any = FieldInfo(default_factory=Any, description="test desc")
    example_test: Any = FieldInfo(
        default_factory=Any, extra={"example": "type.googleapis.com/google.protobuf.Duration"}
    )
    example_factory_test: Any = FieldInfo(default_factory=Any, extra={"example": customer_any})
    field_test: Any = CustomerField(default_factory=Any)
    title_test: Any = FieldInfo(default_factory=Any, title="title_test")


class DurationTest(BaseModel):

    const_test_duration_const_validator = validator("const_test", allow_reuse=True)(duration_const_validator)
    range_test_duration_lt_validator = validator("range_test", allow_reuse=True)(duration_lt_validator)
    range_test_duration_gt_validator = validator("range_test", allow_reuse=True)(duration_gt_validator)
    range_e_test_duration_le_validator = validator("range_e_test", allow_reuse=True)(duration_le_validator)
    range_e_test_duration_ge_validator = validator("range_e_test", allow_reuse=True)(duration_ge_validator)
    in_test_duration_in_validator = validator("in_test", allow_reuse=True)(duration_in_validator)
    not_in_test_duration_not_in_validator = validator("not_in_test", allow_reuse=True)(duration_not_in_validator)

    const_test: Timedelta = FieldInfo(
        default_factory=timedelta, extra={"duration_const": timedelta(seconds=1, microseconds=500000)}
    )
    range_test: Timedelta = FieldInfo(
        default_factory=timedelta,
        extra={
            "duration_gt": timedelta(seconds=5, microseconds=500000),
            "duration_lt": timedelta(seconds=10, microseconds=500000),
        },
    )
    range_e_test: Timedelta = FieldInfo(
        default_factory=timedelta,
        extra={
            "duration_ge": timedelta(seconds=5, microseconds=500000),
            "duration_le": timedelta(seconds=10, microseconds=500000),
        },
    )
    in_test: Timedelta = FieldInfo(
        default_factory=timedelta,
        extra={"duration_in": [timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)]},
    )
    not_in_test: Timedelta = FieldInfo(
        default_factory=timedelta,
        extra={
            "duration_not_in": [timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)]
        },
    )
    enable_test: Timedelta = FieldInfo(default_factory=timedelta)
    default_test: Timedelta = FieldInfo(default=timedelta(seconds=1, microseconds=500000))
    default_factory_test: Timedelta = FieldInfo(default_factory=timedelta)
    miss_default_test: Timedelta = FieldInfo()
    alias_test: Timedelta = FieldInfo(default_factory=timedelta, alias="alias")
    desc_test: Timedelta = FieldInfo(default_factory=timedelta, description="test desc")
    example_test: Timedelta = FieldInfo(
        default_factory=timedelta, extra={"example": timedelta(seconds=1, microseconds=500000)}
    )
    example_factory_test: Timedelta = FieldInfo(default_factory=timedelta, extra={"example": timedelta})
    field_test: Timedelta = CustomerField(default_factory=timedelta)
    title_test: Timedelta = FieldInfo(default_factory=timedelta, title="title_test")
    type_test: timedelta = FieldInfo(default_factory=timedelta)


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

    const_test: datetime = FieldInfo(default_factory=datetime.now, extra={"timestamp_const": 1600000000.0})
    range_test: datetime = FieldInfo(
        default_factory=datetime.now, extra={"timestamp_gt": 1600000000.0, "timestamp_lt": 1600000010.0}
    )
    range_e_test: datetime = FieldInfo(
        default_factory=datetime.now, extra={"timestamp_ge": 1600000000.0, "timestamp_le": 1600000010.0}
    )
    lt_now_test: datetime = FieldInfo(default_factory=datetime.now, extra={"timestamp_lt_now": True})
    gt_now_test: datetime = FieldInfo(default_factory=datetime.now, extra={"timestamp_gt_now": True})
    within_test: datetime = FieldInfo(default_factory=datetime.now, extra={"timestamp_within": timedelta(seconds=1)})
    within_and_gt_now_test: datetime = FieldInfo(
        default_factory=datetime.now, extra={"timestamp_gt_now": True, "timestamp_within": timedelta(seconds=3600)}
    )
    enable_test: datetime = FieldInfo(default_factory=datetime.now)
    default_test: datetime = FieldInfo(default=1.5)
    default_factory_test: datetime = FieldInfo(default_factory=datetime.now)
    miss_default_test: datetime = FieldInfo()
    alias_test: datetime = FieldInfo(default_factory=datetime.now, alias="alias")
    desc_test: datetime = FieldInfo(default_factory=datetime.now, description="test desc")
    example_test: datetime = FieldInfo(default_factory=datetime.now, extra={"example": 1.5})
    example_factory_test: datetime = FieldInfo(default_factory=datetime.now, extra={"example": datetime.now})
    field_test: datetime = CustomerField(default_factory=datetime.now)
    title_test: datetime = FieldInfo(default_factory=datetime.now, title="title_test")
    type_test: datetime = FieldInfo(default_factory=datetime.now)


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
        exp: datetime = FieldInfo(default_factory=datetime.now, extra={"timestamp_gt_now": True})
        uuid: UUID = FieldInfo(default="")

    class NotEnableUserPayMessage(BaseModel):

        exp_timestamp_gt_now_validator = validator("exp", allow_reuse=True)(timestamp_gt_now_validator)

        bank_number: str = FieldInfo(default="", min_length=13, max_length=19)
        exp: datetime = FieldInfo(default_factory=datetime.now, extra={"timestamp_gt_now": True})
        uuid: UUID = FieldInfo(default="")

    string_in_map_test: typing.Dict[str, StringTest] = FieldInfo(default_factory=dict)
    map_in_map_test: typing.Dict[str, MapTest] = FieldInfo(default_factory=dict)
    user_pay: "UserPayMessage" = FieldInfo()
    not_enable_user_pay: "NotEnableUserPayMessage" = FieldInfo()
    empty: None = FieldInfo()
