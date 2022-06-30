# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# gen timestamp:1656571164

import typing
from enum import IntEnum

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic.types import PaymentCardNumber

from example.simple_gen_code import exp_time


class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = FieldInfo(default="", title="UID", description="user union id", extra={"example": "10086"})
    age: int = FieldInfo(default=0, title="use age", ge=0, extra={"example": 18})
    height: float = FieldInfo(default=0.0, ge=0, le=2, extra={})
    sex: SexType = FieldInfo(default=0, extra={})
    is_adult: bool = FieldInfo(default=False, extra={})
    user_name: str = FieldInfo(
        default="", description="user name", min_length=1, max_length=10, extra={"example": "so1n"}
    )


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = FieldInfo(min_items=3, max_items=5, extra={})
    int_list: typing.List[int] = FieldInfo(min_items=1, max_items=5, extra={})
    user_list: UserMessage = FieldInfo(extra={})


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = FieldInfo(extra={})
    user_flag: typing.Dict[str, bool] = FieldInfo(extra={})


class UserPayMessage(BaseModel):
    bank_number: PaymentCardNumber = FieldInfo(default="", extra={})
    exp: str = FieldInfo(default_factory=exp_time, extra={})


class NestedMessage(BaseModel):
    user_list_map: typing.Dict[str, RepeatedMessage] = FieldInfo(extra={})
    user_map: typing.Dict[str, MapMessage] = FieldInfo(extra={})
    user_pay: UserPayMessage = FieldInfo(extra={})
    empty: None = FieldInfo(extra={})
