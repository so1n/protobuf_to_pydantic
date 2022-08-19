# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

import typing
from datetime import datetime
from enum import IntEnum
from uuid import uuid4

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic.types import PaymentCardNumber

from example.text_comment_example.gen_code import exp_time


class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = FieldInfo(title="UID", description="user union id", extra={"example": "10086"})
    age: int = FieldInfo(default=0, title="use age", ge=0, extra={"example": 18})
    height: float = FieldInfo(default=0.0, ge=0, le=2)
    sex: SexType = FieldInfo(default=0)
    is_adult: bool = FieldInfo(default=False)
    user_name: str = FieldInfo(
        default="", description="user name", min_length=1, max_length=10, extra={"example": "so1n"}
    )


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = FieldInfo(default_factory=dict)
    user_flag: typing.Dict[str, bool] = FieldInfo(default_factory=dict)


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = FieldInfo(default_factory=list, min_items=3, max_items=5)
    int_list: typing.List[int] = FieldInfo(default_factory=list, min_items=1, max_items=5, unique_items=True)
    user_list: typing.List[UserMessage] = FieldInfo(default_factory=list)


class NestedMessageUserPayMessage(BaseModel):
    bank_number: PaymentCardNumber = FieldInfo(default="")
    exp: datetime = FieldInfo(default_factory=exp_time)
    uuid: str = FieldInfo(default_factory=uuid4)


class NestedMessage(BaseModel):
    user_list_map: typing.Dict[str, RepeatedMessage] = FieldInfo(default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = FieldInfo(default_factory=dict)
    user_pay: NestedMessageUserPayMessage = FieldInfo()
    empty: None = FieldInfo()
