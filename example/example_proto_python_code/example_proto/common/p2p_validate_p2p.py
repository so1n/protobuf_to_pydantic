# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

import datetime
import typing

from google.protobuf.message import Message  # type: ignore
from protobuf_to_pydantic.customer_validator import check_one_of
from protobuf_to_pydantic.util import Timedelta
from pydantic import BaseModel, root_validator
from pydantic.fields import FieldInfo


class FieldRules(BaseModel):

    _one_of_dict = {
        "FieldRules._message": {"fields": {"message"}},
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
        },
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    message: "MessageRules" = FieldInfo()
    float: "FloatRules" = FieldInfo()
    double: "DoubleRules" = FieldInfo()
    int32: "Int32Rules" = FieldInfo()
    int64: "Int64Rules" = FieldInfo()
    uint32: "UInt32Rules" = FieldInfo()
    uint64: "UInt64Rules" = FieldInfo()
    sint32: "SInt32Rules" = FieldInfo()
    sint64: "SInt64Rules" = FieldInfo()
    fixed32: "Fixed32Rules" = FieldInfo()
    fixed64: "Fixed64Rules" = FieldInfo()
    sfixed32: "SFixed32Rules" = FieldInfo()
    sfixed64: "SFixed64Rules" = FieldInfo()
    bool: "BoolRules" = FieldInfo()
    string: "StringRules" = FieldInfo()
    bytes: "BytesRules" = FieldInfo()
    enum: "EnumRules" = FieldInfo()
    repeated: "RepeatedRules" = FieldInfo()
    map: "MapRules" = FieldInfo()
    any: "AnyRules" = FieldInfo()
    duration: "DurationRules" = FieldInfo()
    timestamp: "TimestampRules" = FieldInfo()


class FloatRules(BaseModel):

    _one_of_dict = {
        "FloatRules._alias": {"fields": {"alias"}},
        "FloatRules._const": {"fields": {"const"}},
        "FloatRules._description": {"fields": {"description"}},
        "FloatRules._enable": {"fields": {"enable"}},
        "FloatRules._field": {"fields": {"field"}},
        "FloatRules._ge": {"fields": {"ge"}},
        "FloatRules._gt": {"fields": {"gt"}},
        "FloatRules._le": {"fields": {"le"}},
        "FloatRules._lt": {"fields": {"lt"}},
        "FloatRules._multiple_of": {"fields": {"multiple_of"}},
        "FloatRules._title": {"fields": {"title"}},
        "FloatRules._type": {"fields": {"type"}},
        "FloatRules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "FloatRules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: float = FieldInfo(default=0.0)
    lt: float = FieldInfo(default=0.0)
    le: float = FieldInfo(default=0.0)
    gt: float = FieldInfo(default=0.0)
    ge: float = FieldInfo(default=0.0)
    not_in: typing.List[float] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class DoubleRules(BaseModel):

    _one_of_dict = {
        "DoubleRules._alias": {"fields": {"alias"}},
        "DoubleRules._const": {"fields": {"const"}},
        "DoubleRules._description": {"fields": {"description"}},
        "DoubleRules._enable": {"fields": {"enable"}},
        "DoubleRules._field": {"fields": {"field"}},
        "DoubleRules._ge": {"fields": {"ge"}},
        "DoubleRules._gt": {"fields": {"gt"}},
        "DoubleRules._le": {"fields": {"le"}},
        "DoubleRules._lt": {"fields": {"lt"}},
        "DoubleRules._multiple_of": {"fields": {"multiple_of"}},
        "DoubleRules._title": {"fields": {"title"}},
        "DoubleRules._type": {"fields": {"type"}},
        "DoubleRules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "DoubleRules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: float = FieldInfo(default=0.0)
    lt: float = FieldInfo(default=0.0)
    le: float = FieldInfo(default=0.0)
    gt: float = FieldInfo(default=0.0)
    ge: float = FieldInfo(default=0.0)
    not_in: typing.List[float] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class Int32Rules(BaseModel):

    _one_of_dict = {
        "Int32Rules._alias": {"fields": {"alias"}},
        "Int32Rules._const": {"fields": {"const"}},
        "Int32Rules._description": {"fields": {"description"}},
        "Int32Rules._enable": {"fields": {"enable"}},
        "Int32Rules._field": {"fields": {"field"}},
        "Int32Rules._ge": {"fields": {"ge"}},
        "Int32Rules._gt": {"fields": {"gt"}},
        "Int32Rules._le": {"fields": {"le"}},
        "Int32Rules._lt": {"fields": {"lt"}},
        "Int32Rules._multiple_of": {"fields": {"multiple_of"}},
        "Int32Rules._title": {"fields": {"title"}},
        "Int32Rules._type": {"fields": {"type"}},
        "Int32Rules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "Int32Rules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: int = FieldInfo(default=0)
    lt: int = FieldInfo(default=0)
    le: int = FieldInfo(default=0)
    gt: int = FieldInfo(default=0)
    ge: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class Int64Rules(BaseModel):

    _one_of_dict = {
        "Int64Rules._alias": {"fields": {"alias"}},
        "Int64Rules._const": {"fields": {"const"}},
        "Int64Rules._description": {"fields": {"description"}},
        "Int64Rules._enable": {"fields": {"enable"}},
        "Int64Rules._field": {"fields": {"field"}},
        "Int64Rules._ge": {"fields": {"ge"}},
        "Int64Rules._gt": {"fields": {"gt"}},
        "Int64Rules._le": {"fields": {"le"}},
        "Int64Rules._lt": {"fields": {"lt"}},
        "Int64Rules._multiple_of": {"fields": {"multiple_of"}},
        "Int64Rules._title": {"fields": {"title"}},
        "Int64Rules._type": {"fields": {"type"}},
        "Int64Rules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "Int64Rules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: int = FieldInfo(default=0)
    lt: int = FieldInfo(default=0)
    le: int = FieldInfo(default=0)
    gt: int = FieldInfo(default=0)
    ge: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class UInt32Rules(BaseModel):

    _one_of_dict = {
        "UInt32Rules._alias": {"fields": {"alias"}},
        "UInt32Rules._const": {"fields": {"const"}},
        "UInt32Rules._description": {"fields": {"description"}},
        "UInt32Rules._enable": {"fields": {"enable"}},
        "UInt32Rules._field": {"fields": {"field"}},
        "UInt32Rules._ge": {"fields": {"ge"}},
        "UInt32Rules._gt": {"fields": {"gt"}},
        "UInt32Rules._le": {"fields": {"le"}},
        "UInt32Rules._lt": {"fields": {"lt"}},
        "UInt32Rules._multiple_of": {"fields": {"multiple_of"}},
        "UInt32Rules._title": {"fields": {"title"}},
        "UInt32Rules._type": {"fields": {"type"}},
        "UInt32Rules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "UInt32Rules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: int = FieldInfo(default=0)
    lt: int = FieldInfo(default=0)
    le: int = FieldInfo(default=0)
    gt: int = FieldInfo(default=0)
    ge: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class UInt64Rules(BaseModel):

    _one_of_dict = {
        "UInt64Rules._alias": {"fields": {"alias"}},
        "UInt64Rules._const": {"fields": {"const"}},
        "UInt64Rules._description": {"fields": {"description"}},
        "UInt64Rules._enable": {"fields": {"enable"}},
        "UInt64Rules._field": {"fields": {"field"}},
        "UInt64Rules._ge": {"fields": {"ge"}},
        "UInt64Rules._gt": {"fields": {"gt"}},
        "UInt64Rules._le": {"fields": {"le"}},
        "UInt64Rules._lt": {"fields": {"lt"}},
        "UInt64Rules._multiple_of": {"fields": {"multiple_of"}},
        "UInt64Rules._title": {"fields": {"title"}},
        "UInt64Rules._type": {"fields": {"type"}},
        "UInt64Rules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "UInt64Rules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: int = FieldInfo(default=0)
    lt: int = FieldInfo(default=0)
    le: int = FieldInfo(default=0)
    gt: int = FieldInfo(default=0)
    ge: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class SInt32Rules(BaseModel):

    _one_of_dict = {
        "SInt32Rules._alias": {"fields": {"alias"}},
        "SInt32Rules._const": {"fields": {"const"}},
        "SInt32Rules._description": {"fields": {"description"}},
        "SInt32Rules._enable": {"fields": {"enable"}},
        "SInt32Rules._field": {"fields": {"field"}},
        "SInt32Rules._ge": {"fields": {"ge"}},
        "SInt32Rules._gt": {"fields": {"gt"}},
        "SInt32Rules._le": {"fields": {"le"}},
        "SInt32Rules._lt": {"fields": {"lt"}},
        "SInt32Rules._multiple_of": {"fields": {"multiple_of"}},
        "SInt32Rules._title": {"fields": {"title"}},
        "SInt32Rules._type": {"fields": {"type"}},
        "SInt32Rules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "SInt32Rules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: int = FieldInfo(default=0)
    lt: int = FieldInfo(default=0)
    le: int = FieldInfo(default=0)
    gt: int = FieldInfo(default=0)
    ge: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class SInt64Rules(BaseModel):

    _one_of_dict = {
        "SInt64Rules._alias": {"fields": {"alias"}},
        "SInt64Rules._const": {"fields": {"const"}},
        "SInt64Rules._description": {"fields": {"description"}},
        "SInt64Rules._enable": {"fields": {"enable"}},
        "SInt64Rules._field": {"fields": {"field"}},
        "SInt64Rules._ge": {"fields": {"ge"}},
        "SInt64Rules._gt": {"fields": {"gt"}},
        "SInt64Rules._le": {"fields": {"le"}},
        "SInt64Rules._lt": {"fields": {"lt"}},
        "SInt64Rules._multiple_of": {"fields": {"multiple_of"}},
        "SInt64Rules._title": {"fields": {"title"}},
        "SInt64Rules._type": {"fields": {"type"}},
        "SInt64Rules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "SInt64Rules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: int = FieldInfo(default=0)
    lt: int = FieldInfo(default=0)
    le: int = FieldInfo(default=0)
    gt: int = FieldInfo(default=0)
    ge: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class Fixed32Rules(BaseModel):

    _one_of_dict = {
        "Fixed32Rules._alias": {"fields": {"alias"}},
        "Fixed32Rules._const": {"fields": {"const"}},
        "Fixed32Rules._description": {"fields": {"description"}},
        "Fixed32Rules._enable": {"fields": {"enable"}},
        "Fixed32Rules._field": {"fields": {"field"}},
        "Fixed32Rules._ge": {"fields": {"ge"}},
        "Fixed32Rules._gt": {"fields": {"gt"}},
        "Fixed32Rules._le": {"fields": {"le"}},
        "Fixed32Rules._lt": {"fields": {"lt"}},
        "Fixed32Rules._multiple_of": {"fields": {"multiple_of"}},
        "Fixed32Rules._title": {"fields": {"title"}},
        "Fixed32Rules._type": {"fields": {"type"}},
        "Fixed32Rules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "Fixed32Rules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: float = FieldInfo(default=0.0)
    lt: float = FieldInfo(default=0.0)
    le: float = FieldInfo(default=0.0)
    gt: float = FieldInfo(default=0.0)
    ge: float = FieldInfo(default=0.0)
    not_in: typing.List[float] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class Fixed64Rules(BaseModel):

    _one_of_dict = {
        "Fixed64Rules._alias": {"fields": {"alias"}},
        "Fixed64Rules._const": {"fields": {"const"}},
        "Fixed64Rules._description": {"fields": {"description"}},
        "Fixed64Rules._enable": {"fields": {"enable"}},
        "Fixed64Rules._field": {"fields": {"field"}},
        "Fixed64Rules._ge": {"fields": {"ge"}},
        "Fixed64Rules._gt": {"fields": {"gt"}},
        "Fixed64Rules._le": {"fields": {"le"}},
        "Fixed64Rules._lt": {"fields": {"lt"}},
        "Fixed64Rules._multiple_of": {"fields": {"multiple_of"}},
        "Fixed64Rules._title": {"fields": {"title"}},
        "Fixed64Rules._type": {"fields": {"type"}},
        "Fixed64Rules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "Fixed64Rules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: float = FieldInfo(default=0.0)
    lt: float = FieldInfo(default=0.0)
    le: float = FieldInfo(default=0.0)
    gt: float = FieldInfo(default=0.0)
    ge: float = FieldInfo(default=0.0)
    not_in: typing.List[float] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class SFixed32Rules(BaseModel):

    _one_of_dict = {
        "SFixed32Rules._alias": {"fields": {"alias"}},
        "SFixed32Rules._const": {"fields": {"const"}},
        "SFixed32Rules._description": {"fields": {"description"}},
        "SFixed32Rules._enable": {"fields": {"enable"}},
        "SFixed32Rules._field": {"fields": {"field"}},
        "SFixed32Rules._ge": {"fields": {"ge"}},
        "SFixed32Rules._gt": {"fields": {"gt"}},
        "SFixed32Rules._le": {"fields": {"le"}},
        "SFixed32Rules._lt": {"fields": {"lt"}},
        "SFixed32Rules._multiple_of": {"fields": {"multiple_of"}},
        "SFixed32Rules._title": {"fields": {"title"}},
        "SFixed32Rules._type": {"fields": {"type"}},
        "SFixed32Rules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "SFixed32Rules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: float = FieldInfo(default=0.0)
    lt: float = FieldInfo(default=0.0)
    le: float = FieldInfo(default=0.0)
    gt: float = FieldInfo(default=0.0)
    ge: float = FieldInfo(default=0.0)
    not_in: typing.List[float] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class SFixed64Rules(BaseModel):

    _one_of_dict = {
        "SFixed64Rules._alias": {"fields": {"alias"}},
        "SFixed64Rules._const": {"fields": {"const"}},
        "SFixed64Rules._description": {"fields": {"description"}},
        "SFixed64Rules._enable": {"fields": {"enable"}},
        "SFixed64Rules._field": {"fields": {"field"}},
        "SFixed64Rules._ge": {"fields": {"ge"}},
        "SFixed64Rules._gt": {"fields": {"gt"}},
        "SFixed64Rules._le": {"fields": {"le"}},
        "SFixed64Rules._lt": {"fields": {"lt"}},
        "SFixed64Rules._multiple_of": {"fields": {"multiple_of"}},
        "SFixed64Rules._title": {"fields": {"title"}},
        "SFixed64Rules._type": {"fields": {"type"}},
        "SFixed64Rules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "SFixed64Rules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: float = FieldInfo(default=0.0)
    lt: float = FieldInfo(default=0.0)
    le: float = FieldInfo(default=0.0)
    gt: float = FieldInfo(default=0.0)
    ge: float = FieldInfo(default=0.0)
    not_in: typing.List[float] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class BoolRules(BaseModel):

    _one_of_dict = {
        "BoolRules._alias": {"fields": {"alias"}},
        "BoolRules._const": {"fields": {"const"}},
        "BoolRules._description": {"fields": {"description"}},
        "BoolRules._enable": {"fields": {"enable"}},
        "BoolRules._example": {"fields": {"example"}},
        "BoolRules._field": {"fields": {"field"}},
        "BoolRules._title": {"fields": {"title"}},
        "BoolRules._type": {"fields": {"type"}},
        "BoolRules.default_config": {"fields": {"default", "miss_default"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: bool = FieldInfo(default=False)
    enable: bool = FieldInfo(default=False)
    default: bool = FieldInfo(default=False)
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    example: bool = FieldInfo(default=False)
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class StringRules(BaseModel):

    _one_of_dict = {
        "StringRules._alias": {"fields": {"alias"}},
        "StringRules._const": {"fields": {"const"}},
        "StringRules._contains": {"fields": {"contains"}},
        "StringRules._description": {"fields": {"description"}},
        "StringRules._enable": {"fields": {"enable"}},
        "StringRules._field": {"fields": {"field"}},
        "StringRules._len": {"fields": {"len"}},
        "StringRules._max_length": {"fields": {"max_length"}},
        "StringRules._min_length": {"fields": {"min_length"}},
        "StringRules._not_contains": {"fields": {"not_contains"}},
        "StringRules._pattern": {"fields": {"pattern"}},
        "StringRules._prefix": {"fields": {"prefix"}},
        "StringRules._suffix": {"fields": {"suffix"}},
        "StringRules._title": {"fields": {"title"}},
        "StringRules._type": {"fields": {"type"}},
        "StringRules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "StringRules.example_config": {"fields": {"example", "example_factory"}},
        "StringRules.well_known": {
            "fields": {"address", "email", "hostname", "ip", "ipv4", "ipv6", "pydantic_type", "uri", "uri_ref", "uuid"}
        },
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: str = FieldInfo(default="")
    len: int = FieldInfo(default=0)
    min_length: int = FieldInfo(default=0)
    max_length: int = FieldInfo(default=0)
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
    pydantic_type: str = FieldInfo(default="")
    enable: bool = FieldInfo(default=False)
    default: str = FieldInfo(default="")
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    example: str = FieldInfo(default="")
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class BytesRules(BaseModel):

    _one_of_dict = {
        "BytesRules._alias": {"fields": {"alias"}},
        "BytesRules._const": {"fields": {"const"}},
        "BytesRules._contains": {"fields": {"contains"}},
        "BytesRules._description": {"fields": {"description"}},
        "BytesRules._enable": {"fields": {"enable"}},
        "BytesRules._field": {"fields": {"field"}},
        "BytesRules._max_length": {"fields": {"max_length"}},
        "BytesRules._min_length": {"fields": {"min_length"}},
        "BytesRules._multiple_of": {"fields": {"multiple_of"}},
        "BytesRules._prefix": {"fields": {"prefix"}},
        "BytesRules._suffix": {"fields": {"suffix"}},
        "BytesRules._title": {"fields": {"title"}},
        "BytesRules._type": {"fields": {"type"}},
        "BytesRules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "BytesRules.example_config": {"fields": {"example", "example_factory"}},
        "BytesRules.well_known": {"fields": {"ip", "ipv4", "ipv6"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: bytes = FieldInfo(default=b"")
    min_length: int = FieldInfo(default=0)
    max_length: int = FieldInfo(default=0)
    prefix: bytes = FieldInfo(default=b"")
    suffix: bytes = FieldInfo(default=b"")
    contains: bytes = FieldInfo(default=b"")
    not_in: typing.List[bytes] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: bytes = FieldInfo(default=b"")
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    multiple_of: float = FieldInfo(default=0.0)
    example: bytes = FieldInfo(default=b"")
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    ip: bool = FieldInfo(default=False)
    ipv4: bool = FieldInfo(default=False)
    ipv6: bool = FieldInfo(default=False)
    title: str = FieldInfo(default="")


class EnumRules(BaseModel):

    _one_of_dict = {
        "EnumRules._alias": {"fields": {"alias"}},
        "EnumRules._const": {"fields": {"const"}},
        "EnumRules._description": {"fields": {"description"}},
        "EnumRules._enable": {"fields": {"enable"}},
        "EnumRules._field": {"fields": {"field"}},
        "EnumRules._title": {"fields": {"title"}},
        "EnumRules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "EnumRules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: int = FieldInfo(default=0)
    not_in: typing.List[int] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: int = FieldInfo(default=0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    example: int = FieldInfo(default=0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class MessageRules(BaseModel):

    _one_of_dict = {
        "MessageRules._alias": {"fields": {"alias"}},
        "MessageRules._description": {"fields": {"description"}},
        "MessageRules._enable": {"fields": {"enable"}},
        "MessageRules._field": {"fields": {"field"}},
        "MessageRules._required": {"fields": {"required"}},
        "MessageRules._skip": {"fields": {"skip"}},
        "MessageRules._title": {"fields": {"title"}},
        "MessageRules._type": {"fields": {"type"}},
        "MessageRules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "MessageRules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    skip: bool = FieldInfo(default=False)
    required: bool = FieldInfo(default=False)
    enable: bool = FieldInfo(default=False)
    default: float = FieldInfo(default=0.0)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    example: float = FieldInfo(default=0.0)
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class RepeatedRules(BaseModel):

    _one_of_dict = {
        "RepeatedRules._alias": {"fields": {"alias"}},
        "RepeatedRules._description": {"fields": {"description"}},
        "RepeatedRules._enable": {"fields": {"enable"}},
        "RepeatedRules._field": {"fields": {"field"}},
        "RepeatedRules._items": {"fields": {"items"}},
        "RepeatedRules._max_items": {"fields": {"max_items"}},
        "RepeatedRules._min_items": {"fields": {"min_items"}},
        "RepeatedRules._title": {"fields": {"title"}},
        "RepeatedRules._type": {"fields": {"type"}},
        "RepeatedRules._unique": {"fields": {"unique"}},
        "RepeatedRules.default_config": {"fields": {"default_factory", "miss_default"}},
        "RepeatedRules.example_config": {"fields": {"example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    min_items: int = FieldInfo(default=0)
    max_items: int = FieldInfo(default=0)
    unique: bool = FieldInfo(default=False)
    items: "FieldRules" = FieldInfo()
    enable: bool = FieldInfo(default=False)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class MapRules(BaseModel):

    _one_of_dict = {
        "MapRules._alias": {"fields": {"alias"}},
        "MapRules._description": {"fields": {"description"}},
        "MapRules._enable": {"fields": {"enable"}},
        "MapRules._field": {"fields": {"field"}},
        "MapRules._keys": {"fields": {"keys"}},
        "MapRules._max_pairs": {"fields": {"max_pairs"}},
        "MapRules._min_pairs": {"fields": {"min_pairs"}},
        "MapRules._title": {"fields": {"title"}},
        "MapRules._type": {"fields": {"type"}},
        "MapRules._values": {"fields": {"values"}},
        "MapRules.default_config": {"fields": {"default_factory", "miss_default"}},
        "MapRules.example_config": {"fields": {"example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    min_pairs: int = FieldInfo(default=0)
    max_pairs: int = FieldInfo(default=0)
    keys: "FieldRules" = FieldInfo()
    values: "FieldRules" = FieldInfo()
    enable: bool = FieldInfo(default=False)
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class AnyRules(BaseModel):

    _one_of_dict = {
        "AnyRules._alias": {"fields": {"alias"}},
        "AnyRules._description": {"fields": {"description"}},
        "AnyRules._enable": {"fields": {"enable"}},
        "AnyRules._field": {"fields": {"field"}},
        "AnyRules._required": {"fields": {"required"}},
        "AnyRules._title": {"fields": {"title"}},
        "AnyRules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "AnyRules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    required: bool = FieldInfo(default=False)
    not_in: typing.List[str] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: str = FieldInfo(default="")
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    example: str = FieldInfo(default="")
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class DurationRules(BaseModel):

    _one_of_dict = {
        "DurationRules._alias": {"fields": {"alias"}},
        "DurationRules._const": {"fields": {"const"}},
        "DurationRules._description": {"fields": {"description"}},
        "DurationRules._enable": {"fields": {"enable"}},
        "DurationRules._field": {"fields": {"field"}},
        "DurationRules._ge": {"fields": {"ge"}},
        "DurationRules._gt": {"fields": {"gt"}},
        "DurationRules._le": {"fields": {"le"}},
        "DurationRules._lt": {"fields": {"lt"}},
        "DurationRules._title": {"fields": {"title"}},
        "DurationRules._type": {"fields": {"type"}},
        "DurationRules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "DurationRules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: Timedelta = FieldInfo(default_factory="Timedelta")
    lt: Timedelta = FieldInfo(default_factory="Timedelta")
    le: Timedelta = FieldInfo(default_factory="Timedelta")
    gt: Timedelta = FieldInfo(default_factory="Timedelta")
    ge: Timedelta = FieldInfo(default_factory="Timedelta")
    not_in: typing.List[Timedelta] = FieldInfo(default_factory=list)
    enable: bool = FieldInfo(default=False)
    default: Timedelta = FieldInfo(default_factory="Timedelta")
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    example: Timedelta = FieldInfo(default_factory="Timedelta")
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")


class TimestampRules(BaseModel):

    _one_of_dict = {
        "TimestampRules._alias": {"fields": {"alias"}},
        "TimestampRules._const": {"fields": {"const"}},
        "TimestampRules._description": {"fields": {"description"}},
        "TimestampRules._enable": {"fields": {"enable"}},
        "TimestampRules._field": {"fields": {"field"}},
        "TimestampRules._ge": {"fields": {"ge"}},
        "TimestampRules._gt": {"fields": {"gt"}},
        "TimestampRules._gt_now": {"fields": {"gt_now"}},
        "TimestampRules._le": {"fields": {"le"}},
        "TimestampRules._lt": {"fields": {"lt"}},
        "TimestampRules._lt_now": {"fields": {"lt_now"}},
        "TimestampRules._title": {"fields": {"title"}},
        "TimestampRules._type": {"fields": {"type"}},
        "TimestampRules._within": {"fields": {"within"}},
        "TimestampRules.default_config": {"fields": {"default", "default_factory", "miss_default"}},
        "TimestampRules.example_config": {"fields": {"example", "example_factory"}},
    }
    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)

    const: datetime.datetime = FieldInfo(default_factory="now")
    lt: datetime.datetime = FieldInfo(default_factory="now")
    le: datetime.datetime = FieldInfo(default_factory="now")
    gt: datetime.datetime = FieldInfo(default_factory="now")
    ge: datetime.datetime = FieldInfo(default_factory="now")
    lt_now: bool = FieldInfo(default=False)
    gt_now: bool = FieldInfo(default=False)
    within: Timedelta = FieldInfo(default_factory="Timedelta")
    enable: bool = FieldInfo(default=False)
    default: datetime.datetime = FieldInfo(default_factory="now")
    default_factory: str = FieldInfo(default="")
    miss_default: bool = FieldInfo(default=False)
    alias: str = FieldInfo(default="")
    description: str = FieldInfo(default="")
    example: datetime.datetime = FieldInfo(default_factory="now")
    example_factory: str = FieldInfo(default="")
    field: str = FieldInfo(default="")
    type: str = FieldInfo(default="")
    title: str = FieldInfo(default="")
