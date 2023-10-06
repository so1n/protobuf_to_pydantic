# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.0.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 4.24.0
# Pydantic Version: 2.0.3
import typing
from datetime import datetime
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field

from ..common.single_p2p import DemoEnum, DemoMessage


class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = Field(default="", json_schema_extra={})
    age: int = Field(default=0, json_schema_extra={})
    height: float = Field(default=0.0, json_schema_extra={})
    sex: SexType = Field(default=0, json_schema_extra={})
    demo: DemoEnum = Field(default=0, json_schema_extra={})
    is_adult: bool = Field(default=False, json_schema_extra={})
    user_name: str = Field(default="", json_schema_extra={})
    demo_message: DemoMessage = Field(json_schema_extra={})


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict, json_schema_extra={})
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict, json_schema_extra={})


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = Field(default_factory=list, json_schema_extra={})
    int_list: typing.List[int] = Field(default_factory=list, json_schema_extra={})
    user_list: typing.List[UserMessage] = Field(default_factory=list, json_schema_extra={})


class AfterReferMessage(BaseModel):
    uid: str = Field(default="", json_schema_extra={})
    age: int = Field(default=0, json_schema_extra={})


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: str = Field(default="", json_schema_extra={})
        exp: datetime = Field(default_factory=datetime.now, json_schema_extra={})
        uuid: str = Field(default="", json_schema_extra={})

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    user_list_map: typing.Dict[str, RepeatedMessage] = Field(default_factory=dict, json_schema_extra={})
    user_map: typing.Dict[str, MapMessage] = Field(default_factory=dict, json_schema_extra={})
    user_pay: UserPayMessage = Field(json_schema_extra={})
    include_enum: IncludeEnum = Field(default=0, json_schema_extra={})
    not_enable_user_pay: UserPayMessage = Field(json_schema_extra={})
    empty: None = Field(json_schema_extra={})
    after_refer: AfterReferMessage = Field(json_schema_extra={})


class InvoiceItem(BaseModel):
    name: str = Field(default="", json_schema_extra={})
    amount: int = Field(default=0, json_schema_extra={})
    quantity: int = Field(default=0, json_schema_extra={})
    items: typing.List["InvoiceItem"] = Field(default_factory=list, json_schema_extra={})


class EmptyMessage(BaseModel):
    pass


class OptionalMessage(BaseModel):
    name: typing.Optional[str] = Field(default="", json_schema_extra={})
    age: typing.Optional[int] = Field(default=0, json_schema_extra={})
    item: typing.Optional[InvoiceItem] = Field(json_schema_extra={}, default=None)
    str_list: typing.List[str] = Field(default_factory=list, json_schema_extra={})
    int_map: typing.Dict[str, int] = Field(default_factory=dict, json_schema_extra={})
