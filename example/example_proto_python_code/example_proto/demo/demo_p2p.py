# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

import datetime
import typing
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class SexType(IntEnum):
    man = 0
    women = 1

    class UserPayMessage(BaseModel):
        bank_number: str = FieldInfo(default="", extra={})
        exp: datetime.datetime = FieldInfo(default_factory="now", extra={})
        uuid: str = FieldInfo(default="", extra={})


class UserMessage(BaseModel):
    uid: str = FieldInfo(default="", extra={})
    age: int = FieldInfo(default=0, extra={})
    height: float = FieldInfo(default=0.0, extra={})
    sex: "SexType" = FieldInfo(default=0, extra={})
    is_adult: bool = FieldInfo(default=False, extra={})
    user_name: str = FieldInfo(default="", extra={})


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = FieldInfo(default_factory=dict, extra={})
    user_flag: typing.Dict[str, bool] = FieldInfo(default_factory=dict, extra={})


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = FieldInfo(default_factory=list, extra={})
    int_list: typing.List[int] = FieldInfo(default_factory=list, extra={})
    user_list: typing.List["UserMessage"] = FieldInfo(default_factory=list, extra={})


class NestedMessage(BaseModel):
    user_list_map: typing.Dict[str, RepeatedMessage] = FieldInfo(default_factory=dict, extra={})
    user_map: typing.Dict[str, MapMessage] = FieldInfo(default_factory=dict, extra={})
    user_pay: "UserPayMessage" = FieldInfo(extra={})
    not_enable_user_pay: "UserPayMessage" = FieldInfo(extra={})
    empty: None = FieldInfo(extra={})
