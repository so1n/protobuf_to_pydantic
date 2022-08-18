# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

import typing
from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel
from pydantic.fields import FieldInfo


class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = FieldInfo(default="", extra={"miss_default": False})
    age: int = FieldInfo(default=0, extra={"miss_default": False})
    height: float = FieldInfo(default=0.0, extra={"miss_default": False})
    sex: SexType = FieldInfo(default=0, extra={"miss_default": False})
    is_adult: bool = FieldInfo(default=False, extra={"miss_default": False})
    user_name: str = FieldInfo(default="", extra={"miss_default": False})


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = FieldInfo(default_factory=dict, extra={"miss_default": False})
    user_flag: typing.Dict[str, bool] = FieldInfo(default_factory=dict, extra={"miss_default": False})


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = FieldInfo(default_factory=list, extra={"miss_default": False})
    int_list: typing.List[int] = FieldInfo(default_factory=list, extra={"miss_default": False})
    user_list: typing.List[UserMessage] = FieldInfo(default_factory=list, extra={"miss_default": False})


class NestedMessageUserPayMessage(BaseModel):
    bank_number: str = FieldInfo(default="", extra={"miss_default": False})
    exp: datetime = FieldInfo(default_factory=datetime.now, extra={"miss_default": False})
    uuid: str = FieldInfo(default="", extra={"miss_default": False})


class NestedMessage(BaseModel):
    user_list_map: typing.Dict[str, RepeatedMessage] = FieldInfo(default_factory=dict, extra={"miss_default": False})
    user_map: typing.Dict[str, MapMessage] = FieldInfo(default_factory=dict, extra={"miss_default": False})
    user_pay: NestedMessageUserPayMessage = FieldInfo(extra={"miss_default": False})
    not_enable_user_pay: NestedMessageUserPayMessage = FieldInfo(extra={"miss_default": False})
    empty: None = FieldInfo()
