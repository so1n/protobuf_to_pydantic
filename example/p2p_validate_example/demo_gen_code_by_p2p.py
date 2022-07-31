# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

import typing
from datetime import datetime, timedelta
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID, uuid4

from google.protobuf.any_pb2 import Any  # type: ignore
from google.protobuf.duration_pb2 import Duration  # type: ignore
from google.protobuf.timestamp_pb2 import Timestamp  # type: ignore
from pydantic import BaseModel, root_validator, validator
from pydantic.fields import FieldInfo
from pydantic.networks import AnyUrl, EmailStr, IPvAnyAddress
from pydantic.types import conbytes, confloat, conint, conlist, constr

from example.p2p_validate_example.gen_code import CustomerField, customer_any
from protobuf_to_pydantic.customer_con_type import contimedelta, contimestamp
from protobuf_to_pydantic.customer_validator import (
    any_in_validator,
    any_not_in_validator,
    check_one_of,
    contains_validator,
    duration_const_validator,
    duration_ge_validator,
    duration_gt_validator,
    duration_le_validator,
    duration_lt_validator,
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
    in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"not_in": [1.0, 2.0, 3.0]})
    default_test: float = FieldInfo(default=1.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0.0, alias="alias", alias_priority=2)
    desc_test: float = FieldInfo(default=0.0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3)
    example_test: float = FieldInfo(default=0.0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"example": float})
    field_test: float = CustomerField(default=0.0)
    type_test: confloat() = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0, title="title_test")

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class DoubleTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"not_in": [1.0, 2.0, 3.0]})
    default_test: float = FieldInfo(default=1.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0.0, alias="alias", alias_priority=2)
    desc_test: float = FieldInfo(default=0.0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3)
    example_test: float = FieldInfo(default=0.0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"example": float})
    field_test: float = CustomerField(default=0.0)
    type_test: confloat() = FieldInfo(default=0.0)
    title_test: float = FieldInfo(default=0.0, title="title_test")

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Int32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: confloat() = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0, title="title_test")

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Uint32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: conint() = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0, title="title_test")

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Sfixed32Test(BaseModel):
    const_test: float = FieldInfo(default=0)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: float = FieldInfo(default=0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0, multiple_of=3)
    example_test: float = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0, extra={"example": float})
    field_test: float = CustomerField(default=0)
    type_test: confloat() = FieldInfo(default=0)
    title_test: float = FieldInfo(default=0, title="title_test")

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Int64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: confloat() = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0, title="title_test")

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Sint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: conint() = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0, title="title_test")

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Uint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: conint() = FieldInfo(default=0)
    title_test: int = FieldInfo(default=0, title="title_test")

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Sfixed64Test(BaseModel):
    const_test: float = FieldInfo(default=0)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: float = FieldInfo(default=0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0, multiple_of=3)
    example_test: float = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0, extra={"example": float})
    field_test: float = CustomerField(default=0)
    type_test: confloat() = FieldInfo(default=0)
    title_test: float = FieldInfo(default=0, title="title_test")

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Fixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: float = FieldInfo(default=0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0, multiple_of=3)
    example_test: float = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0, extra={"example": float})
    field_test: float = CustomerField(default=0)
    type_test: confloat() = FieldInfo(default=0)
    title_test: float = FieldInfo(default=0, title="title_test")

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class BoolTest(BaseModel):
    bool_1_test: bool = FieldInfo(default=True, const=True)
    bool_2_test: bool = FieldInfo(default=False, const=True)
    default_test: bool = FieldInfo(default=True)
    miss_default_test: bool = FieldInfo()
    alias_test: bool = FieldInfo(default=False, alias="alias", alias_priority=2)
    desc_test: bool = FieldInfo(default=False, description="test desc")
    example_test: bool = FieldInfo(default=False, extra={"example": True})
    field_test: bool = CustomerField(default=False)
    title_test: bool = FieldInfo(default=False, title="title_test")


class StringTest(BaseModel):
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
    default_test: str = FieldInfo(default="default")
    default_factory_test: str = FieldInfo(default_factory=uuid4)
    miss_default_test: str = FieldInfo()
    alias_test: str = FieldInfo(default="", alias="alias", alias_priority=2)
    desc_test: str = FieldInfo(default="", description="test desc")
    example_test: str = FieldInfo(default="", extra={"example": "example"})
    example_factory_test: str = FieldInfo(default="", extra={"example": uuid4})
    field_test: str = CustomerField(default="")
    title_test: str = FieldInfo(default="", title="title_test")
    type_test: constr() = FieldInfo(default="")

    len_validator_len_test = validator("len_test", allow_reuse=True)(len_validator)
    prefix_validator_prefix_test = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_validator_suffix_test = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_validator_contains_test = validator("contains_test", allow_reuse=True)(contains_validator)
    not_contains_validator_not_contains_test = validator("not_contains_test", allow_reuse=True)(not_contains_validator)
    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class BytesTest(BaseModel):
    const_test: bytes = FieldInfo(default=b"demo", const=True)
    range_len_test: bytes = FieldInfo(default=b"", min_length=1, max_length=4)
    prefix_test: bytes = FieldInfo(default=b"", extra={"prefix": b"prefix"})
    suffix_test: bytes = FieldInfo(default=b"", extra={"suffix": b"suffix"})
    contains_test: bytes = FieldInfo(default=b"", extra={"contains": b"contains"})
    in_test: bytes = FieldInfo(default=b"", extra={"in": [b"a", b"b", b"c"]})
    not_in_test: bytes = FieldInfo(default=b"", extra={"not_in": [b"a", b"b", b"c"]})
    default_test: bytes = FieldInfo(default=b"default")
    default_factory_test: bytes = FieldInfo(default_factory=bytes)
    miss_default_test: bytes = FieldInfo()
    alias_test: bytes = FieldInfo(default=b"", alias="alias", alias_priority=2)
    desc_test: bytes = FieldInfo(default=b"", description="test desc")
    example_test: bytes = FieldInfo(default=b"", extra={"example": b"example"})
    example_factory_test: bytes = FieldInfo(default=b"", extra={"example": bytes})
    field_test: bytes = CustomerField(default=b"")
    title_test: bytes = FieldInfo(default=b"", title="title_test")
    type_test: constr() = FieldInfo(default=b"")

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
    in_test: State = FieldInfo(default=0, extra={"in": [0, 2]})
    not_in_test: State = FieldInfo(default=0, extra={"in": [0, 2]})
    default_test: State = FieldInfo(default=1)
    miss_default_test: State = FieldInfo()
    alias_test: State = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: State = FieldInfo(default=0, description="test desc")
    example_test: State = FieldInfo(default=0, extra={"example": 2})
    field_test: State = CustomerField(default=0)
    title_test: State = FieldInfo(default=0, title="title_test")

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = FieldInfo(extra={"map_max_pairs": 5, "map_min_pairs": 1})
    keys_test: typing.Dict[constr(), int] = FieldInfo()
    values_test: typing.Dict[str, conint()] = FieldInfo()
    keys_values_test: typing.Dict[constr(), contimestamp(timestamp_gt_now=True)] = FieldInfo()
    default_factory_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    miss_default_test: typing.Dict[str, int] = FieldInfo()
    alias_test: typing.Dict[str, int] = FieldInfo(alias="alias", alias_priority=2)
    desc_test: typing.Dict[str, int] = FieldInfo(description="test desc")
    example_factory_test: typing.Dict[str, int] = FieldInfo(extra={"example": dict})
    field_test: typing.Dict[str, int] = CustomerField()
    title_test: typing.Dict[str, int] = FieldInfo(title="title_test")
    type_test: dict = FieldInfo()

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
        item_type=contimestamp(
            timestamp_gt=datetime(2020, 9, 13, 12, 26, 40), timestamp_lt=datetime(2020, 9, 13, 12, 26, 50)
        ),
        min_items=1,
        max_items=5,
    ) = FieldInfo(default_factory=list)
    items_duration_test: conlist(
        item_type=contimedelta(duration_gt=timedelta(seconds=10), duration_lt=timedelta(seconds=10)),
        min_items=1,
        max_items=5,
    ) = FieldInfo(default_factory=list)
    items_bytes_test: conlist(item_type=conbytes(min_length=1, max_length=5), min_items=1, max_items=5) = FieldInfo(
        default_factory=list
    )
    default_factory_test: typing.List[str] = FieldInfo(default_factory=list)
    miss_default_test: typing.List[str] = FieldInfo()
    alias_test: typing.List[str] = FieldInfo(default_factory=list, alias="alias", alias_priority=2)
    desc_test: typing.List[str] = FieldInfo(default_factory=list, description="test desc")
    example_factory_test: typing.List[str] = FieldInfo(default_factory=list, extra={"example": list})
    field_test: typing.List[str] = CustomerField(default_factory=list)
    title_test: typing.List[str] = FieldInfo(default_factory=list, title="title_test")
    type_test: list = FieldInfo(default_factory=list)


class AnyTest(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    required_test: Any = FieldInfo()
    not_in_test: Any = FieldInfo(
        extra={
            "any_not_in": [
                "type.googleapis.com/google.protobuf.Duration",
                "type.googleapis.com/google.protobuf.Timestamp",
            ]
        }
    )
    in_test: Any = FieldInfo(
        extra={
            "any_in": ["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"]
        }
    )
    default_test: Any = FieldInfo(default="type.googleapis.com/google.protobuf.Duration")
    default_factory_test: Any = FieldInfo(default_factory=customer_any)
    miss_default_test: Any = FieldInfo()
    alias_test: Any = FieldInfo(alias="alias", alias_priority=2)
    desc_test: Any = FieldInfo(description="test desc")
    example_test: Any = FieldInfo(extra={"example": "type.googleapis.com/google.protobuf.Duration"})
    example_factory_test: Any = FieldInfo(extra={"example": customer_any})
    field_test: Any = CustomerField()
    title_test: Any = FieldInfo(title="title_test")

    any_not_in_validator_default_test = validator("default_test", allow_reuse=True)(any_not_in_validator)
    any_not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(any_not_in_validator)
    any_in_validator_in_test = validator("in_test", allow_reuse=True)(any_in_validator)


class DurationTest(BaseModel):
    const_test: Timedelta = FieldInfo(extra={"duration_const": timedelta(seconds=1, microseconds=500000)})
    range_test: Timedelta = FieldInfo(
        extra={
            "duration_gt": timedelta(seconds=5, microseconds=500000),
            "duration_lt": timedelta(seconds=10, microseconds=500000),
        }
    )
    range_e_test: Timedelta = FieldInfo(
        extra={
            "duration_ge": timedelta(seconds=5, microseconds=500000),
            "duration_le": timedelta(seconds=10, microseconds=500000),
        }
    )
    in_test: Timedelta = FieldInfo(
        extra={"duration_in": [timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)]}
    )
    not_in_test: Timedelta = FieldInfo(
        extra={"duration_in": [timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)]}
    )
    default_test: Timedelta = FieldInfo(default=timedelta(seconds=1, microseconds=500000))
    default_factory_test: Timedelta = FieldInfo(default_factory=timedelta)
    miss_default_test: Timedelta = FieldInfo()
    alias_test: Timedelta = FieldInfo(alias="alias", alias_priority=2)
    desc_test: Timedelta = FieldInfo(description="test desc")
    example_test: Timedelta = FieldInfo(extra={"example": timedelta(seconds=1, microseconds=500000)})
    example_factory_test: Timedelta = FieldInfo(extra={"example": timedelta})
    field_test: Timedelta = CustomerField()
    title_test: Timedelta = FieldInfo(title="title_test")
    type_test: timedelta = FieldInfo()

    duration_const_validator_const_test = validator("const_test", allow_reuse=True)(duration_const_validator)
    duration_lt_validator_range_test = validator("range_test", allow_reuse=True)(duration_lt_validator)
    duration_gt_validator_range_test = validator("range_test", allow_reuse=True)(duration_gt_validator)
    duration_le_validator_range_e_test = validator("range_e_test", allow_reuse=True)(duration_le_validator)
    duration_ge_validator_range_e_test = validator("range_e_test", allow_reuse=True)(duration_ge_validator)
    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(in_validator)


class TimestampTest(BaseModel):
    const_test: datetime = FieldInfo(extra={"timestamp_const": datetime(2020, 9, 13, 12, 26, 40)})
    range_test: datetime = FieldInfo(
        extra={"timestamp_gt": datetime(2020, 9, 13, 12, 26, 40), "timestamp_lt": datetime(2020, 9, 13, 12, 26, 50)}
    )
    range_e_test: datetime = FieldInfo(
        extra={"timestamp_ge": datetime(2020, 9, 13, 12, 26, 40), "timestamp_le": datetime(2020, 9, 13, 12, 26, 50)}
    )
    lt_now_test: datetime = FieldInfo(extra={"timestamp_lt_now": True})
    gt_now_test: datetime = FieldInfo(extra={"timestamp_gt_now": True})
    within_test: datetime = FieldInfo(extra={"timestamp_within": timedelta(seconds=1)})
    within_and_gt_now_test: datetime = FieldInfo(
        extra={"timestamp_gt_now": True, "timestamp_within": timedelta(seconds=3600)}
    )
    default_test: datetime = FieldInfo(default=datetime(1970, 1, 1, 0, 0, 1, 500000))
    default_factory_test: datetime = FieldInfo(default_factory=datetime)
    miss_default_test: datetime = FieldInfo()
    alias_test: datetime = FieldInfo(alias="alias", alias_priority=2)
    desc_test: datetime = FieldInfo(description="test desc")
    example_test: datetime = FieldInfo(extra={"example": datetime(1970, 1, 1, 0, 0, 1, 500000)})
    example_factory_test: datetime = FieldInfo(extra={"example": datetime})
    field_test: datetime = CustomerField()
    title_test: datetime = FieldInfo(title="title_test")
    type_test: datetime = FieldInfo(extra={"example": datetime})

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


class MessageIgnoredTest(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)


class NestedMessageUserPayMessage(BaseModel):
    bank_number: str = FieldInfo(default="", min_length=13, max_length=19)
    exp: datetime = FieldInfo(extra={"timestamp_gt_now": True})
    uuid: UUID = FieldInfo(default="")

    timestamp_gt_now_validator_exp = validator("exp", allow_reuse=True)(timestamp_gt_now_validator)


class NestedMessageNotEnableUserPayMessage(BaseModel):
    bank_number: str = FieldInfo(default="")
    exp: datetime = FieldInfo()
    uuid: str = FieldInfo(default="")


class NestedMessage(BaseModel):
    string_in_map_test: typing.Dict[str, StringTest] = FieldInfo()
    map_in_map_test: typing.Dict[str, MapTest] = FieldInfo()
    user_pay: NestedMessageUserPayMessage = FieldInfo()
    not_enable_user_pay: NestedMessageNotEnableUserPayMessage = FieldInfo()
    empty: None = FieldInfo()


class OneOfTest(BaseModel):
    _one_of_dict = {"p2p_validate_test.OneOfTest.id": {"fields": {"x", "y"}, "required": True}}

    header: str = FieldInfo(default="")
    x: str = FieldInfo(default="")
    y: int = FieldInfo(default=0)

    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)


class OneOfNotTest(BaseModel):
    _one_of_dict = {"p2p_validate_test.OneOfNotTest.id": {"fields": {"x", "y"}, "required": False}}

    header: str = FieldInfo(default="")
    x: str = FieldInfo(default="")
    y: int = FieldInfo(default=0)

    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)
