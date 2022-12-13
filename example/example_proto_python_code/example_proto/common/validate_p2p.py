# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

import datetime
import typing
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from protobuf_to_pydantic.util import Timedelta
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class KnownRegex(IntEnum):
    UNKNOWN = 0
    HTTP_HEADER_NAME = 1
    HTTP_HEADER_VALUE = 2


class FieldRules(BaseModel):
    message: "MessageRules" = FieldInfo(extra={})
    float: "FloatRules" = FieldInfo(extra={})
    double: "DoubleRules" = FieldInfo(extra={})
    int32: "Int32Rules" = FieldInfo(extra={})
    int64: "Int64Rules" = FieldInfo(extra={})
    uint32: "UInt32Rules" = FieldInfo(extra={})
    uint64: "UInt64Rules" = FieldInfo(extra={})
    sint32: "SInt32Rules" = FieldInfo(extra={})
    sint64: "SInt64Rules" = FieldInfo(extra={})
    fixed32: "Fixed32Rules" = FieldInfo(extra={})
    fixed64: "Fixed64Rules" = FieldInfo(extra={})
    sfixed32: "SFixed32Rules" = FieldInfo(extra={})
    sfixed64: "SFixed64Rules" = FieldInfo(extra={})
    bool: "BoolRules" = FieldInfo(extra={})
    string: "StringRules" = FieldInfo(extra={})
    bytes: "BytesRules" = FieldInfo(extra={})
    enum: "EnumRules" = FieldInfo(extra={})
    repeated: "RepeatedRules" = FieldInfo(extra={})
    map: "MapRules" = FieldInfo(extra={})
    any: "AnyRules" = FieldInfo(extra={})
    duration: "DurationRules" = FieldInfo(extra={})
    timestamp: "TimestampRules" = FieldInfo(extra={})


class FloatRules(BaseModel):
    const: float = FieldInfo(default=0.0, extra={})
    lt: float = FieldInfo(default=0.0, extra={})
    lte: float = FieldInfo(default=0.0, extra={})
    gt: float = FieldInfo(default=0.0, extra={})
    gte: float = FieldInfo(default=0.0, extra={})
    not_in: typing.List[float] = FieldInfo(default_factory=list, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class DoubleRules(BaseModel):
    const: float = FieldInfo(default=0.0, extra={})
    lt: float = FieldInfo(default=0.0, extra={})
    lte: float = FieldInfo(default=0.0, extra={})
    gt: float = FieldInfo(default=0.0, extra={})
    gte: float = FieldInfo(default=0.0, extra={})
    not_in: typing.List[float] = FieldInfo(default_factory=list, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class Int32Rules(BaseModel):
    const: int = FieldInfo(default=0, extra={})
    lt: int = FieldInfo(default=0, extra={})
    lte: int = FieldInfo(default=0, extra={})
    gt: int = FieldInfo(default=0, extra={})
    gte: int = FieldInfo(default=0, extra={})
    not_in: typing.List[int] = FieldInfo(default_factory=list, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class Int64Rules(BaseModel):
    const: int = FieldInfo(default=0, extra={})
    lt: int = FieldInfo(default=0, extra={})
    lte: int = FieldInfo(default=0, extra={})
    gt: int = FieldInfo(default=0, extra={})
    gte: int = FieldInfo(default=0, extra={})
    not_in: typing.List[int] = FieldInfo(default_factory=list, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class UInt32Rules(BaseModel):
    const: int = FieldInfo(default=0, extra={})
    lt: int = FieldInfo(default=0, extra={})
    lte: int = FieldInfo(default=0, extra={})
    gt: int = FieldInfo(default=0, extra={})
    gte: int = FieldInfo(default=0, extra={})
    not_in: typing.List[int] = FieldInfo(default_factory=list, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class UInt64Rules(BaseModel):
    const: int = FieldInfo(default=0, extra={})
    lt: int = FieldInfo(default=0, extra={})
    lte: int = FieldInfo(default=0, extra={})
    gt: int = FieldInfo(default=0, extra={})
    gte: int = FieldInfo(default=0, extra={})
    not_in: typing.List[int] = FieldInfo(default_factory=list, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class SInt32Rules(BaseModel):
    const: int = FieldInfo(default=0, extra={})
    lt: int = FieldInfo(default=0, extra={})
    lte: int = FieldInfo(default=0, extra={})
    gt: int = FieldInfo(default=0, extra={})
    gte: int = FieldInfo(default=0, extra={})
    not_in: typing.List[int] = FieldInfo(default_factory=list, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class SInt64Rules(BaseModel):
    const: int = FieldInfo(default=0, extra={})
    lt: int = FieldInfo(default=0, extra={})
    lte: int = FieldInfo(default=0, extra={})
    gt: int = FieldInfo(default=0, extra={})
    gte: int = FieldInfo(default=0, extra={})
    not_in: typing.List[int] = FieldInfo(default_factory=list, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class Fixed32Rules(BaseModel):
    const: float = FieldInfo(default=0.0, extra={})
    lt: float = FieldInfo(default=0.0, extra={})
    lte: float = FieldInfo(default=0.0, extra={})
    gt: float = FieldInfo(default=0.0, extra={})
    gte: float = FieldInfo(default=0.0, extra={})
    not_in: typing.List[float] = FieldInfo(default_factory=list, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class Fixed64Rules(BaseModel):
    const: float = FieldInfo(default=0.0, extra={})
    lt: float = FieldInfo(default=0.0, extra={})
    lte: float = FieldInfo(default=0.0, extra={})
    gt: float = FieldInfo(default=0.0, extra={})
    gte: float = FieldInfo(default=0.0, extra={})
    not_in: typing.List[float] = FieldInfo(default_factory=list, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class SFixed32Rules(BaseModel):
    const: float = FieldInfo(default=0.0, extra={})
    lt: float = FieldInfo(default=0.0, extra={})
    lte: float = FieldInfo(default=0.0, extra={})
    gt: float = FieldInfo(default=0.0, extra={})
    gte: float = FieldInfo(default=0.0, extra={})
    not_in: typing.List[float] = FieldInfo(default_factory=list, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class SFixed64Rules(BaseModel):
    const: float = FieldInfo(default=0.0, extra={})
    lt: float = FieldInfo(default=0.0, extra={})
    lte: float = FieldInfo(default=0.0, extra={})
    gt: float = FieldInfo(default=0.0, extra={})
    gte: float = FieldInfo(default=0.0, extra={})
    not_in: typing.List[float] = FieldInfo(default_factory=list, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class BoolRules(BaseModel):
    const: bool = FieldInfo(default=False, extra={})


class StringRules(BaseModel):
    const: str = FieldInfo(default="", extra={})
    len: int = FieldInfo(default=0, extra={})
    min_len: int = FieldInfo(default=0, extra={})
    max_len: int = FieldInfo(default=0, extra={})
    len_bytes: int = FieldInfo(default=0, extra={})
    min_bytes: int = FieldInfo(default=0, extra={})
    max_bytes: int = FieldInfo(default=0, extra={})
    pattern: str = FieldInfo(default="", extra={})
    prefix: str = FieldInfo(default="", extra={})
    suffix: str = FieldInfo(default="", extra={})
    contains: str = FieldInfo(default="", extra={})
    not_contains: str = FieldInfo(default="", extra={})
    not_in: typing.List[str] = FieldInfo(default_factory=list, extra={})
    email: bool = FieldInfo(default=False, extra={})
    hostname: bool = FieldInfo(default=False, extra={})
    ip: bool = FieldInfo(default=False, extra={})
    ipv4: bool = FieldInfo(default=False, extra={})
    ipv6: bool = FieldInfo(default=False, extra={})
    uri: bool = FieldInfo(default=False, extra={})
    uri_ref: bool = FieldInfo(default=False, extra={})
    address: bool = FieldInfo(default=False, extra={})
    uuid: bool = FieldInfo(default=False, extra={})
    well_known_regex: "KnownRegex" = FieldInfo(default=0, extra={})
    strict: bool = FieldInfo(default=False, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class BytesRules(BaseModel):
    const: bytes = FieldInfo(default=b"", extra={})
    len: int = FieldInfo(default=0, extra={})
    min_len: int = FieldInfo(default=0, extra={})
    max_len: int = FieldInfo(default=0, extra={})
    pattern: str = FieldInfo(default="", extra={})
    prefix: bytes = FieldInfo(default=b"", extra={})
    suffix: bytes = FieldInfo(default=b"", extra={})
    contains: bytes = FieldInfo(default=b"", extra={})
    not_in: typing.List[bytes] = FieldInfo(default_factory=list, extra={})
    ip: bool = FieldInfo(default=False, extra={})
    ipv4: bool = FieldInfo(default=False, extra={})
    ipv6: bool = FieldInfo(default=False, extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class EnumRules(BaseModel):
    const: int = FieldInfo(default=0, extra={})
    defined_only: bool = FieldInfo(default=False, extra={})
    not_in: typing.List[int] = FieldInfo(default_factory=list, extra={})


class MessageRules(BaseModel):
    skip: bool = FieldInfo(default=False, extra={})
    required: bool = FieldInfo(default=False, extra={})


class RepeatedRules(BaseModel):
    min_items: int = FieldInfo(default=0, extra={})
    max_items: int = FieldInfo(default=0, extra={})
    unique: bool = FieldInfo(default=False, extra={})
    items: "FieldRules" = FieldInfo(extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class MapRules(BaseModel):
    min_pairs: int = FieldInfo(default=0, extra={})
    max_pairs: int = FieldInfo(default=0, extra={})
    no_sparse: bool = FieldInfo(default=False, extra={})
    keys: "FieldRules" = FieldInfo(extra={})
    values: "FieldRules" = FieldInfo(extra={})
    ignore_empty: bool = FieldInfo(default=False, extra={})


class AnyRules(BaseModel):
    required: bool = FieldInfo(default=False, extra={})
    not_in: typing.List[str] = FieldInfo(default_factory=list, extra={})


class DurationRules(BaseModel):
    required: bool = FieldInfo(default=False, extra={})
    const: Timedelta = FieldInfo(default_factory="Timedelta", extra={})
    lt: Timedelta = FieldInfo(default_factory="Timedelta", extra={})
    lte: Timedelta = FieldInfo(default_factory="Timedelta", extra={})
    gt: Timedelta = FieldInfo(default_factory="Timedelta", extra={})
    gte: Timedelta = FieldInfo(default_factory="Timedelta", extra={})
    not_in: typing.List[Timedelta] = FieldInfo(default_factory=list, extra={})


class TimestampRules(BaseModel):
    required: bool = FieldInfo(default=False, extra={})
    const: datetime.datetime = FieldInfo(default_factory="now", extra={})
    lt: datetime.datetime = FieldInfo(default_factory="now", extra={})
    lte: datetime.datetime = FieldInfo(default_factory="now", extra={})
    gt: datetime.datetime = FieldInfo(default_factory="now", extra={})
    gte: datetime.datetime = FieldInfo(default_factory="now", extra={})
    lt_now: bool = FieldInfo(default=False, extra={})
    gt_now: bool = FieldInfo(default=False, extra={})
    within: Timedelta = FieldInfo(default_factory="Timedelta", extra={})
