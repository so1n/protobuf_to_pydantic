# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.6.2](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 1.10.7
import typing
from datetime import datetime
from enum import IntEnum
from uuid import uuid4

from google.protobuf.field_mask_pb2 import FieldMask  # type: ignore
from google.protobuf.message import Message  # type: ignore
from google.protobuf.wrappers_pb2 import DoubleValue  # type: ignore
from pydantic import BaseModel, Field
from pydantic.types import PaymentCardNumber

from example.plugin_config import exp_time

from ..common.single_p2p import DemoEnum, DemoMessage


class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    """
    user info
    """

    uid: str = Field(example="10086", title="UID", description="user union id")
    age: int = Field(default=0, example=18, title="use age", ge=0.0)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: DemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", example="so1n", description="user name", min_length=1, max_length=10)
    demo_message: DemoMessage = Field(customer_string="c1", customer_int=1)


class OtherMessage(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    metadata: typing.Dict[str, typing.Any] = Field(default_factory=dict)
    double_value: DoubleValue = Field(default_factory=DoubleValue)
    field_mask: typing.Optional[FieldMask] = Field(default_factory=FieldMask)


class MapMessage(BaseModel):
    """
    test map message and bad message
    """

    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict)
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict)


class RepeatedMessage(BaseModel):
    """
    test repeated msg
    """

    str_list: typing.List[str] = Field(default_factory=list, min_items=3, max_items=5)
    int_list: typing.List[int] = Field(default_factory=list, min_items=1, max_items=5, unique_items=True)
    user_list: typing.List[UserMessage] = Field(default_factory=list)


class AfterReferMessage(BaseModel):
    uid: str = Field(example="10086", title="UID", description="user union id")
    age: int = Field(default=0, example=18, title="use age", ge=0.0)


class NestedMessage(BaseModel):
    """
    test nested message
    """

    class UserPayMessage(BaseModel):
        bank_number: PaymentCardNumber = Field(default="")
        exp: datetime = Field(default_factory=exp_time)
        uuid: str = Field(default_factory=uuid4)

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    user_list_map: typing.Dict[str, RepeatedMessage] = Field(default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = Field(default_factory=dict)
    user_pay: "NestedMessage.UserPayMessage" = Field()
    include_enum: "NestedMessage.IncludeEnum" = Field(default=0)
    empty: None = Field()
    after_refer: AfterReferMessage = Field()


class InvoiceItem(BaseModel):
    """
        Test self-referencing Messages
    from: https://github.com/so1n/protobuf_to_pydantic/issues/7#issuecomment-1490705932
    """

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
