# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

import typing
from datetime import datetime, timedelta
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from protobuf_to_pydantic.customer_validator import check_one_of
from protobuf_to_pydantic.util import Timedelta
from pydantic import BaseModel, root_validator
from pydantic.fields import FieldInfo


class KnownRegex(IntEnum):
    UNKNOWN = 0
    HTTP_HEADER_NAME = 1
    HTTP_HEADER_VALUE = 2


class FieldRules(BaseModel):

    _one_of_dict = {
        "FieldRules.type": {
            "fields": {
                "any",
                "bool",
                "bytes",
                "double",
                "duration",
                "enum",
                "fixed32",
                "fixed64",
                "float",
                "int32",
                "int64",
                "map",
                "repeated",
                "sfixed32",
                "sfixed64",
                "sint32",
                "sint64",
                "string",
                "timestamp",
                "uint32",
                "uint64",
            }
        }
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    message: MessageRules = FieldInfo()
    float: FloatRules = FieldInfo()
    double: DoubleRules = FieldInfo()
    int32: Int32Rules = FieldInfo()
    int64: Int64Rules = FieldInfo()
    uint32: UInt32Rules = FieldInfo()
    uint64: UInt64Rules = FieldInfo()
    sint32: SInt32Rules = FieldInfo()
    sint64: SInt64Rules = FieldInfo()
    fixed32: Fixed32Rules = FieldInfo()
    fixed64: Fixed64Rules = FieldInfo()
    sfixed32: SFixed32Rules = FieldInfo()
    sfixed64: SFixed64Rules = FieldInfo()
    bool: BoolRules = FieldInfo()
    string: StringRules = FieldInfo()
    bytes: BytesRules = FieldInfo()
    enum: EnumRules = FieldInfo()
    repeated: RepeatedRules = FieldInfo()
    map: MapRules = FieldInfo()
    any: AnyRules = FieldInfo()
    duration: DurationRules = FieldInfo()
    timestamp: TimestampRules = FieldInfo()


class FloatRules(BaseModel):

    const: float = FieldInfo(default=0.0)
    lt: float = FieldInfo(default=0.0)
    lte: float = FieldInfo(default=0.0)
    gt: float = FieldInfo(default=0.0)
    gte: float = FieldInfo(default=0.0)
    not_in: typing.List[float] = FieldInfo(default_factory=list)
    ignore_empty: bool = FieldInfo(default=False)


class DoubleRules(BaseModel):

    const: float = FieldInfo(default=0.0)
    lt: float = FieldInfo(default=0.0)
    lte: float = FieldInfo(default=0.0)
    gt: float = FieldInfo(default=0.0)
    gte: float = FieldInfo(default=0.0)
    not_in: typing.List[float] = FieldInfo(default_factory=list)
    ignore_empty: bool = FieldInfo(default=False)


class Int32Rules(BaseModel):

    const: int = FieldInfo(default=0)
    lt: int = FieldInfo(default=0)
    lte: int = FieldInfo(default=0)
    gt: int = FieldInfo(default=0)
    gte: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    ignore_empty: bool = FieldInfo(default=False)


class Int64Rules(BaseModel):

    const: int = FieldInfo(default=0)
    lt: int = FieldInfo(default=0)
    lte: int = FieldInfo(default=0)
    gt: int = FieldInfo(default=0)
    gte: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    ignore_empty: bool = FieldInfo(default=False)


class UInt32Rules(BaseModel):

    const: int = FieldInfo(default=0)
    lt: int = FieldInfo(default=0)
    lte: int = FieldInfo(default=0)
    gt: int = FieldInfo(default=0)
    gte: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    ignore_empty: bool = FieldInfo(default=False)


class UInt64Rules(BaseModel):

    const: int = FieldInfo(default=0)
    lt: int = FieldInfo(default=0)
    lte: int = FieldInfo(default=0)
    gt: int = FieldInfo(default=0)
    gte: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    ignore_empty: bool = FieldInfo(default=False)


class SInt32Rules(BaseModel):

    const: int = FieldInfo(default=0)
    lt: int = FieldInfo(default=0)
    lte: int = FieldInfo(default=0)
    gt: int = FieldInfo(default=0)
    gte: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    ignore_empty: bool = FieldInfo(default=False)


class SInt64Rules(BaseModel):

    const: int = FieldInfo(default=0)
    lt: int = FieldInfo(default=0)
    lte: int = FieldInfo(default=0)
    gt: int = FieldInfo(default=0)
    gte: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    ignore_empty: bool = FieldInfo(default=False)


class Fixed32Rules(BaseModel):

    const: float = FieldInfo(default=0.0)
    lt: float = FieldInfo(default=0.0)
    lte: float = FieldInfo(default=0.0)
    gt: float = FieldInfo(default=0.0)
    gte: float = FieldInfo(default=0.0)
    not_in: typing.List[float] = FieldInfo(default_factory=list)
    ignore_empty: bool = FieldInfo(default=False)


class Fixed64Rules(BaseModel):

    const: float = FieldInfo(default=0.0)
    lt: float = FieldInfo(default=0.0)
    lte: float = FieldInfo(default=0.0)
    gt: float = FieldInfo(default=0.0)
    gte: float = FieldInfo(default=0.0)
    not_in: typing.List[float] = FieldInfo(default_factory=list)
    ignore_empty: bool = FieldInfo(default=False)


class SFixed32Rules(BaseModel):

    const: float = FieldInfo(default=0.0)
    lt: float = FieldInfo(default=0.0)
    lte: float = FieldInfo(default=0.0)
    gt: float = FieldInfo(default=0.0)
    gte: float = FieldInfo(default=0.0)
    not_in: typing.List[float] = FieldInfo(default_factory=list)
    ignore_empty: bool = FieldInfo(default=False)


class SFixed64Rules(BaseModel):

    const: float = FieldInfo(default=0.0)
    lt: float = FieldInfo(default=0.0)
    lte: float = FieldInfo(default=0.0)
    gt: float = FieldInfo(default=0.0)
    gte: float = FieldInfo(default=0.0)
    not_in: typing.List[float] = FieldInfo(default_factory=list)
    ignore_empty: bool = FieldInfo(default=False)


class BoolRules(BaseModel):

    const: bool = FieldInfo(default=False)


class StringRules(BaseModel):

    _one_of_dict = {
        "StringRules.well_known": {
            "fields": {
                "address",
                "email",
                "hostname",
                "ip",
                "ipv4",
                "ipv6",
                "uri",
                "uri_ref",
                "uuid",
                "well_known_regex",
            }
        }
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: str = FieldInfo(default="")
    len: int = FieldInfo(default=0)
    min_len: int = FieldInfo(default=0)
    max_len: int = FieldInfo(default=0)
    len_bytes: int = FieldInfo(default=0)
    min_bytes: int = FieldInfo(default=0)
    max_bytes: int = FieldInfo(default=0)
    pattern: str = FieldInfo(default="")
    prefix: str = FieldInfo(default="")
    suffix: str = FieldInfo(default="")
    contains: str = FieldInfo(default="")
    not_contains: str = FieldInfo(default="")
    not_in: typing.List[str] = FieldInfo(default_factory=list)
    email: bool = FieldInfo(default=False)
    hostname: bool = FieldInfo(default=False)
    ip: bool = FieldInfo(default=False)
    ipv4: bool = FieldInfo(default=False)
    ipv6: bool = FieldInfo(default=False)
    uri: bool = FieldInfo(default=False)
    uri_ref: bool = FieldInfo(default=False)
    address: bool = FieldInfo(default=False)
    uuid: bool = FieldInfo(default=False)
    well_known_regex: KnownRegex = FieldInfo(default=0)
    strict: bool = FieldInfo(default=False)
    ignore_empty: bool = FieldInfo(default=False)


class BytesRules(BaseModel):

    _one_of_dict = {"BytesRules.well_known": {"fields": {"ip", "ipv4", "ipv6"}}}
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: bytes = FieldInfo(default=b"")
    len: int = FieldInfo(default=0)
    min_len: int = FieldInfo(default=0)
    max_len: int = FieldInfo(default=0)
    pattern: str = FieldInfo(default="")
    prefix: bytes = FieldInfo(default=b"")
    suffix: bytes = FieldInfo(default=b"")
    contains: bytes = FieldInfo(default=b"")
    not_in: typing.List[bytes] = FieldInfo(default_factory=list)
    ip: bool = FieldInfo(default=False)
    ipv4: bool = FieldInfo(default=False)
    ipv6: bool = FieldInfo(default=False)
    ignore_empty: bool = FieldInfo(default=False)


class EnumRules(BaseModel):

    const: int = FieldInfo(default=0)
    defined_only: bool = FieldInfo(default=False)
    not_in: typing.List[int] = FieldInfo(default_factory=list)


class MessageRules(BaseModel):

    skip: bool = FieldInfo(default=False)
    required: bool = FieldInfo(default=False)


class RepeatedRules(BaseModel):

    min_items: int = FieldInfo(default=0)
    max_items: int = FieldInfo(default=0)
    unique: bool = FieldInfo(default=False)
    items: FieldRules = FieldInfo()
    ignore_empty: bool = FieldInfo(default=False)


class MapRules(BaseModel):

    min_pairs: int = FieldInfo(default=0)
    max_pairs: int = FieldInfo(default=0)
    no_sparse: bool = FieldInfo(default=False)
    keys: FieldRules = FieldInfo()
    values: FieldRules = FieldInfo()
    ignore_empty: bool = FieldInfo(default=False)


class AnyRules(BaseModel):

    required: bool = FieldInfo(default=False)
    not_in: typing.List[str] = FieldInfo(default_factory=list)


class DurationRules(BaseModel):

    required: bool = FieldInfo(default=False)
    const: Timedelta = FieldInfo(default_factory=timedelta)
    lt: Timedelta = FieldInfo(default_factory=timedelta)
    lte: Timedelta = FieldInfo(default_factory=timedelta)
    gt: Timedelta = FieldInfo(default_factory=timedelta)
    gte: Timedelta = FieldInfo(default_factory=timedelta)
    not_in: typing.List[Timedelta] = FieldInfo(default_factory=list)


class TimestampRules(BaseModel):

    required: bool = FieldInfo(default=False)
    const: datetime = FieldInfo(default_factory=datetime.now)
    lt: datetime = FieldInfo(default_factory=datetime.now)
    lte: datetime = FieldInfo(default_factory=datetime.now)
    gt: datetime = FieldInfo(default_factory=datetime.now)
    gte: datetime = FieldInfo(default_factory=datetime.now)
    lt_now: bool = FieldInfo(default=False)
    gt_now: bool = FieldInfo(default=False)
    within: Timedelta = FieldInfo(default_factory=timedelta)
