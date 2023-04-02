# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
import typing
from datetime import datetime
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from ..common.single_p2p import DemoEnum, DemoMessage


class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = FieldInfo(default="")
    age: int = FieldInfo(default=0)
    height: float = FieldInfo(default=0.0)
    sex: SexType = FieldInfo(default=0)
    demo: DemoEnum = FieldInfo(default=0)
    is_adult: bool = FieldInfo(default=False)
    user_name: str = FieldInfo(default="")
    demo_message: DemoMessage = FieldInfo()


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = FieldInfo(default_factory=dict)
    user_flag: typing.Dict[str, bool] = FieldInfo(default_factory=dict)


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = FieldInfo(default_factory=list)
    int_list: typing.List[int] = FieldInfo(default_factory=list)
    user_list: typing.List[UserMessage] = FieldInfo(default_factory=list)


class AfterReferMessage(BaseModel):
    uid: str = FieldInfo(default="")
    age: int = FieldInfo(default=0)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: str = FieldInfo(default="")
        exp: datetime = FieldInfo(default_factory=datetime.now)
        uuid: str = FieldInfo(default="")

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    user_list_map: typing.Dict[str, RepeatedMessage] = FieldInfo(default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = FieldInfo(default_factory=dict)
    user_pay: UserPayMessage = FieldInfo()
    include_enum: IncludeEnum = FieldInfo(default=0)
    not_enable_user_pay: UserPayMessage = FieldInfo()
    empty: None = FieldInfo()
    after_refer: AfterReferMessage = FieldInfo()


class InvoiceItem(BaseModel):
    name: str = FieldInfo(default="")
    amount: int = FieldInfo(default=0)
    quantity: int = FieldInfo(default=0)
    items: typing.List["InvoiceItem"] = FieldInfo(default_factory=list)
