# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# gen timestamp:1657445940

import typing
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


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = FieldInfo(default_factory=list)
    int_list: typing.List[int] = FieldInfo(default_factory=list)
    user_list: UserMessage = FieldInfo()


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = FieldInfo()
    user_flag: typing.Dict[str, bool] = FieldInfo()


class UserPayMessage(BaseModel):
    bank_number: str = FieldInfo(default="")
    exp: str = FieldInfo()
    uuid: str = FieldInfo(default="")


class NestedMessage(BaseModel):
    user_list_map: typing.Dict[str, RepeatedMessage] = FieldInfo()
    user_map: typing.Dict[str, MapMessage] = FieldInfo()
    user_pay: UserPayMessage = FieldInfo()
    not_enable_user_pay: UserPayMessage = FieldInfo()
    empty: None = FieldInfo()
