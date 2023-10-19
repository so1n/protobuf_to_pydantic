# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.0.2](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 4.24.4
# Pydantic Version: 2.0.3
import typing
from datetime import datetime, timedelta
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID, uuid4

import typing_extensions
from annotated_types import Ge, Gt, Interval, Le, Len, Lt, MaxLen, MinLen
from google.protobuf.any_pb2 import Any  # type: ignore
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_validator, model_validator
from pydantic._internal._fields import PydanticGeneralMetadata
from pydantic.networks import EmailStr, IPvAnyAddress
from pydantic_core._pydantic_core import Url
from typing_extensions import Annotated

from example.plugin_config import CustomerField, customer_any
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
    default_test: float = Field(default=1.0, json_schema_extra={})
    default_template_test: float = Field(default=1600000000, json_schema_extra={})
    default_factory_test: float = Field(default_factory=float, json_schema_extra={})
    miss_default_test: float = Field(json_schema_extra={})
    required_test: float = Field(json_schema_extra={})
    alias_test: float = Field(default=0.0, alias="alias", json_schema_extra={})
    desc_test: float = Field(default=0.0, description="test desc", json_schema_extra={})
    multiple_of_test: float = Field(default=0.0, multiple_of=3, json_schema_extra={})
    example_test: float = Field(default=0.0, json_schema_extra={"example": 1.0})
    example_factory: float = Field(default=0.0, json_schema_extra={"example": float})
    field_test: float = CustomerField(default=0.0, json_schema_extra={})
    type_test: typing_extensions.Annotated[
        float, None, Interval(gt=None, ge=None, lt=None, le=None), None, None
    ] = Field(default=0.0, json_schema_extra={})
    title_test: float = Field(default=0.0, title="title_test", json_schema_extra={})
    extra_test: float = Field(default=0.0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class DoubleTest(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1.0] = Field(default=0.0, json_schema_extra={})
    range_e_test: float = Field(default=0.0, ge=1.0, le=10.0, json_schema_extra={})
    range_test: float = Field(default=0.0, gt=1.0, lt=10.0, json_schema_extra={})
    in_test: float = Field(default=0.0, json_schema_extra={"in_": [1.0, 2.0, 3.0]})
    not_in_test: float = Field(default=0.0, json_schema_extra={"not_in": [1.0, 2.0, 3.0]})
    default_test: float = Field(default=1.0, json_schema_extra={})
    default_template_test: float = Field(default=1600000000, json_schema_extra={})
    default_factory_test: float = Field(default_factory=float, json_schema_extra={})
    miss_default_test: float = Field(json_schema_extra={})
    required_test: float = Field(json_schema_extra={})
    alias_test: float = Field(default=0.0, alias="alias", json_schema_extra={})
    desc_test: float = Field(default=0.0, description="test desc", json_schema_extra={})
    multiple_of_test: float = Field(default=0.0, multiple_of=3, json_schema_extra={})
    example_test: float = Field(default=0.0, json_schema_extra={"example": 1.0})
    example_factory: float = Field(default=0.0, json_schema_extra={"example": float})
    field_test: float = CustomerField(default=0.0, json_schema_extra={})
    type_test: typing_extensions.Annotated[
        float, None, Interval(gt=None, ge=None, lt=None, le=None), None, None
    ] = Field(default=0.0, json_schema_extra={})
    title_test: float = Field(default=0.0, title="title_test", json_schema_extra={})
    extra_test: float = Field(default=0.0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class Int32Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, ge=1, le=10, json_schema_extra={})
    range_test: int = Field(default=0, gt=1, lt=10, json_schema_extra={})
    in_test: int = Field(default=0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: int = Field(default=0, json_schema_extra={"not_in": [1, 2, 3]})
    default_test: int = Field(default=1.0, json_schema_extra={})
    default_template_test: int = Field(default=1600000000, json_schema_extra={})
    default_factory_test: int = Field(default_factory=int, json_schema_extra={})
    miss_default_test: int = Field(json_schema_extra={})
    required_test: int = Field(json_schema_extra={})
    alias_test: int = Field(default=0, alias="alias", json_schema_extra={})
    desc_test: int = Field(default=0, description="test desc", json_schema_extra={})
    multiple_of_test: int = Field(default=0, multiple_of=3, json_schema_extra={})
    example_test: int = Field(default=0, json_schema_extra={"example": 1.0})
    example_factory: int = Field(default=0, json_schema_extra={"example": int})
    field_test: int = CustomerField(default=0, json_schema_extra={})
    type_test: typing_extensions.Annotated[
        float, None, Interval(gt=None, ge=None, lt=None, le=None), None, None
    ] = Field(default=0, json_schema_extra={})
    title_test: int = Field(default=0, title="title_test", json_schema_extra={})
    extra_test: int = Field(default=0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class Int64Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, ge=1, le=10, json_schema_extra={})
    range_test: int = Field(default=0, gt=1, lt=10, json_schema_extra={})
    in_test: int = Field(default=0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: int = Field(default=0, json_schema_extra={"not_in": [1, 2, 3]})
    default_test: int = Field(default=1.0, json_schema_extra={})
    default_template_test: int = Field(default=1600000000, json_schema_extra={})
    default_factory_test: int = Field(default_factory=int, json_schema_extra={})
    miss_default_test: int = Field(json_schema_extra={})
    required_test: int = Field(json_schema_extra={})
    alias_test: int = Field(default=0, alias="alias", json_schema_extra={})
    desc_test: int = Field(default=0, description="test desc", json_schema_extra={})
    multiple_of_test: int = Field(default=0, multiple_of=3, json_schema_extra={})
    example_test: int = Field(default=0, json_schema_extra={"example": 1.0})
    example_factory: int = Field(default=0, json_schema_extra={"example": int})
    field_test: int = CustomerField(default=0, json_schema_extra={})
    type_test: typing_extensions.Annotated[
        float, None, Interval(gt=None, ge=None, lt=None, le=None), None, None
    ] = Field(default=0, json_schema_extra={})
    title_test: int = Field(default=0, title="title_test", json_schema_extra={})
    extra_test: int = Field(default=0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class Uint32Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, ge=1, le=10, json_schema_extra={})
    range_test: int = Field(default=0, gt=1, lt=10, json_schema_extra={})
    in_test: int = Field(default=0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: int = Field(default=0, json_schema_extra={"not_in": [1, 2, 3]})
    default_test: int = Field(default=1.0, json_schema_extra={})
    default_template_test: int = Field(default=1600000000, json_schema_extra={})
    default_factory_test: int = Field(default_factory=int, json_schema_extra={})
    miss_default_test: int = Field(json_schema_extra={})
    required_test: int = Field(json_schema_extra={})
    alias_test: int = Field(default=0, alias="alias", json_schema_extra={})
    desc_test: int = Field(default=0, description="test desc", json_schema_extra={})
    multiple_of_test: int = Field(default=0, multiple_of=3, json_schema_extra={})
    example_test: int = Field(default=0, json_schema_extra={"example": 1.0})
    example_factory: int = Field(default=0, json_schema_extra={"example": int})
    field_test: int = CustomerField(default=0, json_schema_extra={})
    type_test: typing_extensions.Annotated[int, None, Interval(gt=None, ge=None, lt=None, le=None), None] = Field(
        default=0, json_schema_extra={}
    )
    title_test: int = Field(default=0, title="title_test", json_schema_extra={})
    extra_test: int = Field(default=0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class Sint32Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, ge=1, le=10, json_schema_extra={})
    range_test: int = Field(default=0, gt=1, lt=10, json_schema_extra={})
    in_test: int = Field(default=0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: int = Field(default=0, json_schema_extra={"not_in": [1, 2, 3]})
    default_test: int = Field(default=1.0, json_schema_extra={})
    default_template_test: int = Field(default=1600000000, json_schema_extra={})
    default_factory_test: int = Field(default_factory=int, json_schema_extra={})
    miss_default_test: int = Field(json_schema_extra={})
    required_test: int = Field(json_schema_extra={})
    alias_test: int = Field(default=0, alias="alias", json_schema_extra={})
    desc_test: int = Field(default=0, description="test desc", json_schema_extra={})
    multiple_of_test: int = Field(default=0, multiple_of=3, json_schema_extra={})
    example_test: int = Field(default=0, json_schema_extra={"example": 1.0})
    example_factory: int = Field(default=0, json_schema_extra={"example": int})
    field_test: int = CustomerField(default=0, json_schema_extra={})
    type_test: typing_extensions.Annotated[int, None, Interval(gt=None, ge=None, lt=None, le=None), None] = Field(
        default=0, json_schema_extra={}
    )
    title_test: int = Field(default=0, title="title_test", json_schema_extra={})
    extra_test: int = Field(default=0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class Uint64Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, ge=1, le=10, json_schema_extra={})
    range_test: int = Field(default=0, gt=1, lt=10, json_schema_extra={})
    in_test: int = Field(default=0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: int = Field(default=0, json_schema_extra={"not_in": [1, 2, 3]})
    default_test: int = Field(default=1.0, json_schema_extra={})
    default_template_test: int = Field(default=1600000000, json_schema_extra={})
    default_factory_test: int = Field(default_factory=int, json_schema_extra={})
    miss_default_test: int = Field(json_schema_extra={})
    required_test: int = Field(json_schema_extra={})
    alias_test: int = Field(default=0, alias="alias", json_schema_extra={})
    desc_test: int = Field(default=0, description="test desc", json_schema_extra={})
    multiple_of_test: int = Field(default=0, multiple_of=3, json_schema_extra={})
    example_test: int = Field(default=0, json_schema_extra={"example": 1.0})
    example_factory: int = Field(default=0, json_schema_extra={"example": int})
    field_test: int = CustomerField(default=0, json_schema_extra={})
    type_test: typing_extensions.Annotated[int, None, Interval(gt=None, ge=None, lt=None, le=None), None] = Field(
        default=0, json_schema_extra={}
    )
    title_test: int = Field(default=0, title="title_test", json_schema_extra={})
    extra_test: int = Field(default=0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class Sint64Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0, json_schema_extra={})
    range_e_test: int = Field(default=0, ge=1, le=10, json_schema_extra={})
    range_test: int = Field(default=0, gt=1, lt=10, json_schema_extra={})
    in_test: int = Field(default=0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: int = Field(default=0, json_schema_extra={"not_in": [1, 2, 3]})
    default_test: int = Field(default=1.0, json_schema_extra={})
    default_template_test: int = Field(default=1600000000, json_schema_extra={})
    default_factory_test: int = Field(default_factory=int, json_schema_extra={})
    miss_default_test: int = Field(json_schema_extra={})
    required_test: int = Field(json_schema_extra={})
    alias_test: int = Field(default=0, alias="alias", json_schema_extra={})
    desc_test: int = Field(default=0, description="test desc", json_schema_extra={})
    multiple_of_test: int = Field(default=0, multiple_of=3, json_schema_extra={})
    example_test: int = Field(default=0, json_schema_extra={"example": 1.0})
    example_factory: int = Field(default=0, json_schema_extra={"example": int})
    field_test: int = CustomerField(default=0, json_schema_extra={})
    type_test: typing_extensions.Annotated[int, None, Interval(gt=None, ge=None, lt=None, le=None), None] = Field(
        default=0, json_schema_extra={}
    )
    title_test: int = Field(default=0, title="title_test", json_schema_extra={})
    extra_test: int = Field(default=0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class Fixed32Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[1] = Field(default=0.0, json_schema_extra={})
    range_e_test: float = Field(default=0.0, ge=1, le=10, json_schema_extra={})
    range_test: float = Field(default=0.0, gt=1, lt=10, json_schema_extra={})
    in_test: float = Field(default=0.0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: float = Field(default=0.0, json_schema_extra={"not_in": [1, 2, 3]})
    default_test: float = Field(default=1.0, json_schema_extra={})
    default_template_test: float = Field(default=1600000000, json_schema_extra={})
    default_factory_test: float = Field(default_factory=float, json_schema_extra={})
    miss_default_test: float = Field(json_schema_extra={})
    required_test: float = Field(json_schema_extra={})
    alias_test: float = Field(default=0.0, alias="alias", json_schema_extra={})
    desc_test: float = Field(default=0.0, description="test desc", json_schema_extra={})
    multiple_of_test: float = Field(default=0.0, multiple_of=3, json_schema_extra={})
    example_test: float = Field(default=0.0, json_schema_extra={"example": 1.0})
    example_factory: float = Field(default=0.0, json_schema_extra={"example": float})
    field_test: float = CustomerField(default=0.0, json_schema_extra={})
    type_test: typing_extensions.Annotated[
        float, None, Interval(gt=None, ge=None, lt=None, le=None), None, None
    ] = Field(default=0.0, json_schema_extra={})
    title_test: float = Field(default=0.0, title="title_test", json_schema_extra={})
    extra_test: float = Field(default=0.0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class Fixed64Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: float = Field(default=0.0, json_schema_extra={})
    range_e_test: float = Field(default=0.0, ge=1, le=10, json_schema_extra={})
    range_test: float = Field(default=0.0, gt=1, lt=10, json_schema_extra={})
    in_test: float = Field(default=0.0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: float = Field(default=0.0, json_schema_extra={"not_in": [1, 2, 3]})
    default_test: float = Field(default=1.0, json_schema_extra={})
    default_template_test: float = Field(default=1600000000, json_schema_extra={})
    default_factory_test: float = Field(default_factory=float, json_schema_extra={})
    miss_default_test: float = Field(json_schema_extra={})
    required_test: float = Field(json_schema_extra={})
    alias_test: float = Field(default=0.0, alias="alias", json_schema_extra={})
    desc_test: float = Field(default=0.0, description="test desc", json_schema_extra={})
    multiple_of_test: float = Field(default=0.0, multiple_of=3, json_schema_extra={})
    example_test: float = Field(default=0.0, json_schema_extra={"example": 1.0})
    example_factory: float = Field(default=0.0, json_schema_extra={"example": float})
    field_test: float = CustomerField(default=0.0, json_schema_extra={})
    type_test: typing_extensions.Annotated[
        float, None, Interval(gt=None, ge=None, lt=None, le=None), None, None
    ] = Field(default=0.0, json_schema_extra={})
    title_test: float = Field(default=0.0, title="title_test", json_schema_extra={})
    extra_test: float = Field(default=0.0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class Sfixed32Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: float = Field(default=0.0, json_schema_extra={})
    range_e_test: float = Field(default=0.0, ge=1, le=10, json_schema_extra={})
    range_test: float = Field(default=0.0, gt=1, lt=10, json_schema_extra={})
    in_test: float = Field(default=0.0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: float = Field(default=0.0, json_schema_extra={"not_in": [1, 2, 3]})
    default_test: float = Field(default=1.0, json_schema_extra={})
    default_template_test: float = Field(default=1600000000, json_schema_extra={})
    default_factory_test: float = Field(default_factory=float, json_schema_extra={})
    miss_default_test: float = Field(json_schema_extra={})
    required_test: float = Field(json_schema_extra={})
    alias_test: float = Field(default=0.0, alias="alias", json_schema_extra={})
    desc_test: float = Field(default=0.0, description="test desc", json_schema_extra={})
    multiple_of_test: float = Field(default=0.0, multiple_of=3, json_schema_extra={})
    example_test: float = Field(default=0.0, json_schema_extra={"example": 1.0})
    example_factory: float = Field(default=0.0, json_schema_extra={"example": float})
    field_test: float = CustomerField(default=0.0, json_schema_extra={})
    type_test: typing_extensions.Annotated[
        float, None, Interval(gt=None, ge=None, lt=None, le=None), None, None
    ] = Field(default=0.0, json_schema_extra={})
    title_test: float = Field(default=0.0, title="title_test", json_schema_extra={})
    extra_test: float = Field(default=0.0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class Sfixed64Test(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: float = Field(default=0.0, json_schema_extra={})
    range_e_test: float = Field(default=0.0, ge=1, le=10, json_schema_extra={})
    range_test: float = Field(default=0.0, gt=1, lt=10, json_schema_extra={})
    in_test: float = Field(default=0.0, json_schema_extra={"in_": [1, 2, 3]})
    not_in_test: float = Field(default=0.0, json_schema_extra={"not_in": [1, 2, 3]})
    default_test: float = Field(default=1.0, json_schema_extra={})
    default_template_test: float = Field(default=1600000000, json_schema_extra={})
    default_factory_test: float = Field(default_factory=float, json_schema_extra={})
    miss_default_test: float = Field(json_schema_extra={})
    required_test: float = Field(json_schema_extra={})
    alias_test: float = Field(default=0.0, alias="alias", json_schema_extra={})
    desc_test: float = Field(default=0.0, description="test desc", json_schema_extra={})
    multiple_of_test: float = Field(default=0.0, multiple_of=3, json_schema_extra={})
    example_test: float = Field(default=0.0, json_schema_extra={"example": 1.0})
    example_factory: float = Field(default=0.0, json_schema_extra={"example": float})
    field_test: float = CustomerField(default=0.0, json_schema_extra={})
    type_test: typing_extensions.Annotated[
        float, None, Interval(gt=None, ge=None, lt=None, le=None), None, None
    ] = Field(default=0.0, json_schema_extra={})
    title_test: float = Field(default=0.0, title="title_test", json_schema_extra={})
    extra_test: float = Field(default=0.0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class BoolTest(BaseModel):
    bool_1_test: typing_extensions.Literal[True] = Field(default=False, json_schema_extra={})
    bool_2_test: typing_extensions.Literal[False] = Field(default=False, json_schema_extra={})
    default_test: bool = Field(default=True, json_schema_extra={})
    miss_default_test: bool = Field(json_schema_extra={})
    required_test: bool = Field(json_schema_extra={})
    alias_test: bool = Field(default=False, alias="alias", json_schema_extra={})
    desc_test: bool = Field(default=False, description="test desc", json_schema_extra={})
    example_test: bool = Field(default=False, json_schema_extra={"example": True})
    field_test: bool = CustomerField(default=False, json_schema_extra={})
    title_test: bool = Field(default=False, title="title_test", json_schema_extra={})
    extra_test: bool = Field(default=False, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


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
    pydantic_type_test: str = Field(default="", json_schema_extra={})
    default_test: str = Field(default="default", json_schema_extra={})
    default_factory_test: str = Field(default_factory=uuid4, json_schema_extra={})
    miss_default_test: str = Field(json_schema_extra={})
    required_test: str = Field(json_schema_extra={})
    alias_test: str = Field(default="", alias="alias", json_schema_extra={})
    desc_test: str = Field(default="", description="test desc", json_schema_extra={})
    example_test: str = Field(default="", json_schema_extra={"example": "example"})
    example_factory_test: str = Field(default="", json_schema_extra={"example": uuid4})
    field_test: str = CustomerField(default="", json_schema_extra={})
    title_test: str = Field(default="", title="title_test", json_schema_extra={})
    type_test: typing_extensions.Annotated[
        str, None, Len(min_length=0, max_length=None), PydanticGeneralMetadata()
    ] = Field(default="", json_schema_extra={})
    extra_test: str = Field(default="", json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class BytesTest(BaseModel):
    prefix_test_prefix_validator = field_validator("prefix_test", mode="after", check_fields=None)(prefix_validator)
    suffix_test_suffix_validator = field_validator("suffix_test", mode="after", check_fields=None)(suffix_validator)
    contains_test_contains_validator = field_validator("contains_test", mode="after", check_fields=None)(
        contains_validator
    )
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[b"demo"] = Field(default=b"", json_schema_extra={})
    range_len_test: bytes = Field(default=b"", min_length=1, max_length=4, json_schema_extra={})
    prefix_test: bytes = Field(default=b"", json_schema_extra={"prefix": b"prefix"})
    suffix_test: bytes = Field(default=b"", json_schema_extra={"suffix": b"suffix"})
    contains_test: bytes = Field(default=b"", json_schema_extra={"contains": b"contains"})
    in_test: bytes = Field(default=b"", json_schema_extra={"in_": [b"a", b"b", b"c"]})
    not_in_test: bytes = Field(default=b"", json_schema_extra={"not_in": [b"a", b"b", b"c"]})
    default_test: bytes = Field(default=b"default", json_schema_extra={})
    default_factory_test: bytes = Field(default_factory=bytes, json_schema_extra={})
    miss_default_test: bytes = Field(json_schema_extra={})
    required_test: bytes = Field(json_schema_extra={})
    alias_test: bytes = Field(default=b"", alias="alias", json_schema_extra={})
    desc_test: bytes = Field(default=b"", description="test desc", json_schema_extra={})
    example_test: bytes = Field(default=b"", json_schema_extra={"example": b"example"})
    example_factory_test: bytes = Field(default=b"", json_schema_extra={"example": bytes})
    field_test: bytes = CustomerField(default=b"", json_schema_extra={})
    title_test: bytes = Field(default=b"", title="title_test", json_schema_extra={})
    type_test: typing_extensions.Annotated[
        str, None, Len(min_length=0, max_length=None), PydanticGeneralMetadata()
    ] = Field(default=b"", json_schema_extra={})
    extra_test: bytes = Field(default=b"", json_schema_extra={"customer_int": 1, "customer_string": "c1"})


class EnumTest(BaseModel):
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)

    const_test: typing_extensions.Literal[2] = Field(default=0, json_schema_extra={})
    in_test: State = Field(default=0, json_schema_extra={"in_": [0, 2]})
    not_in_test: State = Field(default=0, json_schema_extra={"not_in": [0, 2]})
    default_test: State = Field(default=1, json_schema_extra={})
    miss_default_test: State = Field(json_schema_extra={})
    required_test: State = Field(json_schema_extra={})
    alias_test: State = Field(default=0, alias="alias", json_schema_extra={})
    desc_test: State = Field(default=0, description="test desc", json_schema_extra={})
    example_test: State = Field(default=0, json_schema_extra={"example": 2})
    field_test: State = CustomerField(default=0, json_schema_extra={})
    title_test: State = Field(default=0, title="title_test", json_schema_extra={})
    extra_test: State = Field(default=0, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


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
    default_factory_test: typing.Dict[str, int] = Field(default_factory=dict, json_schema_extra={})
    miss_default_test: typing.Dict[str, int] = Field(json_schema_extra={})
    required_test: typing.Dict[str, int] = Field(json_schema_extra={})
    alias_test: typing.Dict[str, int] = Field(default_factory=dict, alias="alias", json_schema_extra={})
    desc_test: typing.Dict[str, int] = Field(default_factory=dict, description="test desc", json_schema_extra={})
    example_factory_test: typing.Dict[str, int] = Field(default_factory=dict, json_schema_extra={"example": dict})
    field_test: typing.Dict[str, int] = CustomerField(default_factory=dict, json_schema_extra={})
    title_test: typing.Dict[str, int] = Field(default_factory=dict, title="title_test", json_schema_extra={})
    type_test: dict = Field(default_factory=dict, json_schema_extra={})
    extra_test: typing.Dict[str, int] = Field(
        default_factory=dict, json_schema_extra={"customer_int": 1, "customer_string": "c1"}
    )


class MessageTest(BaseModel):
    skip_test: str = Field(default="", json_schema_extra={})
    required_test: str = Field(json_schema_extra={})
    extra_test: str = Field(default="", json_schema_extra={})


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
        typing_extensions.Annotated[TimedeltaType, Ge(ge=timedelta(seconds=10)), Le(le=timedelta(seconds=10))]
    ] = Field(default_factory=list, min_length=1, max_length=5, json_schema_extra={})
    items_bytes_test: typing.List[
        typing_extensions.Annotated[bytes, MinLen(min_length=1), MaxLen(max_length=5)]
    ] = Field(default_factory=list, min_length=1, max_length=5, json_schema_extra={})
    default_factory_test: typing.List[str] = Field(default_factory=list, json_schema_extra={})
    miss_default_test: typing.List[str] = Field(json_schema_extra={})
    required_test: typing.List[str] = Field(json_schema_extra={})
    alias_test: typing.List[str] = Field(default_factory=list, alias="alias", json_schema_extra={})
    desc_test: typing.List[str] = Field(default_factory=list, description="test desc", json_schema_extra={})
    example_factory_test: typing.List[str] = Field(default_factory=list, json_schema_extra={"example": list})
    field_test: typing.List[str] = CustomerField(default_factory=list, json_schema_extra={})
    title_test: typing.List[str] = Field(default_factory=list, title="title_test", json_schema_extra={})
    type_test: list = Field(default_factory=list, json_schema_extra={})
    extra_test: typing.List[str] = Field(
        default_factory=list, json_schema_extra={"customer_int": 1, "customer_string": "c1"}
    )


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
            "any_in": [
                Any(type_url="type.googleapis.com/google.protobuf.Duration"),
                "type.googleapis.com/google.protobuf.Timestamp",
            ]
        },
    )
    default_test: Any = Field(
        default=Any(type_url="type.googleapis.com/google.protobuf.Duration"), json_schema_extra={}
    )
    default_factory_test: Any = Field(default_factory=customer_any, json_schema_extra={})
    miss_default_test: Any = Field(json_schema_extra={})
    alias_test: Any = Field(default_factory=Any, alias="alias", json_schema_extra={})
    desc_test: Any = Field(default_factory=Any, description="test desc", json_schema_extra={})
    example_test: Any = Field(
        default_factory=Any, json_schema_extra={"example": "type.googleapis.com/google.protobuf.Duration"}
    )
    example_factory_test: Any = Field(default_factory=Any, json_schema_extra={"example": customer_any})
    field_test: Any = CustomerField(default_factory=Any, json_schema_extra={})
    title_test: Any = Field(default_factory=Any, title="title_test", json_schema_extra={})
    extra_test: Any = Field(default_factory=Any, json_schema_extra={"customer_int": 1, "customer_string": "c1"})


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
    default_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default=timedelta(seconds=1, microseconds=500000), json_schema_extra={}
    )
    default_factory_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta, json_schema_extra={}
    )
    miss_default_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(json_schema_extra={})
    required_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(json_schema_extra={})
    alias_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta, alias="alias", json_schema_extra={}
    )
    desc_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta, description="test desc", json_schema_extra={}
    )
    example_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta, json_schema_extra={"example": timedelta(seconds=1, microseconds=500000)}
    )
    example_factory_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta, json_schema_extra={"example": timedelta}
    )
    field_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = CustomerField(
        default_factory=timedelta, json_schema_extra={}
    )
    title_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta, title="title_test", json_schema_extra={}
    )
    type_test: timedelta = Field(default_factory=timedelta, json_schema_extra={})
    extra_test: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(
        default_factory=timedelta, json_schema_extra={"customer_int": 1, "customer_string": "c1"}
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
    default_test: datetime = Field(default=1.5, json_schema_extra={})
    default_factory_test: datetime = Field(default_factory=datetime.now, json_schema_extra={})
    miss_default_test: datetime = Field(json_schema_extra={})
    required_test: datetime = Field(json_schema_extra={})
    alias_test: datetime = Field(default_factory=datetime.now, alias="alias", json_schema_extra={})
    desc_test: datetime = Field(default_factory=datetime.now, description="test desc", json_schema_extra={})
    example_test: datetime = Field(default_factory=datetime.now, json_schema_extra={"example": 1.5})
    example_factory_test: datetime = Field(default_factory=datetime.now, json_schema_extra={"example": datetime.now})
    field_test: datetime = CustomerField(default_factory=datetime.now, json_schema_extra={})
    title_test: datetime = Field(default_factory=datetime.now, title="title_test", json_schema_extra={})
    type_test: datetime = Field(default_factory=datetime.now, json_schema_extra={})
    extra_test: datetime = Field(
        default_factory=datetime.now, json_schema_extra={"customer_int": 1, "customer_string": "c1"}
    )


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
    uid: str = Field(title="UID", description="user union id", json_schema_extra={"example": "10086"})
    age: int = Field(default=0, title="use age", ge=0, json_schema_extra={"example": 18.0})


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
