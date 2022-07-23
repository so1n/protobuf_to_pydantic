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
    uid: str = FieldInfo(default="")
    age: int = FieldInfo(default=0)
    height: float = FieldInfo(default=0.0)
    sex: SexType = FieldInfo(default=0)
    is_adult: bool = FieldInfo(default=False)
    user_name: str = FieldInfo(default="")


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = FieldInfo()
    user_flag: typing.Dict[str, bool] = FieldInfo()


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = FieldInfo(default_factory=list)
    int_list: typing.List[int] = FieldInfo(default_factory=list)
    user_list: typing.List[UserMessage] = FieldInfo(default_factory=list)


class NestedMessageUserPayMessage(BaseModel):
    bank_number: str = FieldInfo(default="")
    exp: datetime = FieldInfo()
    uuid: str = FieldInfo(default="")


class NestedMessage(BaseModel):
    user_list_map: typing.Dict[str, RepeatedMessage] = FieldInfo()
    user_map: typing.Dict[str, MapMessage] = FieldInfo()
    user_pay: NestedMessageUserPayMessage = FieldInfo()
    not_enable_user_pay: NestedMessageUserPayMessage = FieldInfo()
    empty: None = FieldInfo()
