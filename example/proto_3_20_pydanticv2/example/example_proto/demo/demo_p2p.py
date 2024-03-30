# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.6](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 2.5.3
import typing
from datetime import datetime
from enum import IntEnum

from google.protobuf.field_mask_pb2 import FieldMask  # type: ignore
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, ConfigDict, Field

from ..common.single_p2p import DemoEnum, DemoMessage


class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = Field(default="")
    age: int = Field(default=0)
    height: float = Field(default=0.0)
    sex: SexType = Field(default=0)
    demo: DemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="")
    demo_message: DemoMessage = Field()


class StructMessage(BaseModel):
    metadata: typing.Dict = Field(default_factory=dict)


class FieldMaskMessage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    field_mask: typing.Optional[FieldMask] = Field(default_factory=FieldMask)


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict)
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict)


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = Field(default_factory=list)
    int_list: typing.List[int] = Field(default_factory=list)
    user_list: typing.List[UserMessage] = Field(default_factory=list)


class AfterReferMessage(BaseModel):
    uid: str = Field(default="")
    age: int = Field(default=0)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: str = Field(default="")
        exp: datetime = Field(default_factory=datetime.now)
        uuid: str = Field(default="")

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    user_list_map: typing.Dict[str, RepeatedMessage] = Field(default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = Field(default_factory=dict)
    user_pay: "NestedMessage.UserPayMessage" = Field()
    include_enum: "NestedMessage.IncludeEnum" = Field(default=0)
    not_enable_user_pay: "NestedMessage.UserPayMessage" = Field()
    empty: None = Field()
    after_refer: AfterReferMessage = Field()


class InvoiceItem(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem"] = Field(default_factory=list)


class EmptyMessage(BaseModel):
    pass


class OptionalMessage(BaseModel):
    name: typing.Optional[str] = Field(default="")
    age: typing.Optional[int] = Field(default=0)
    item: typing.Optional[InvoiceItem] = Field(default=None)
    str_list: typing.List[str] = Field(default_factory=list)
    int_map: typing.Dict[str, int] = Field(default_factory=dict)
