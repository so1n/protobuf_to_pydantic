# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.1.0](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 2.5.3
import typing
from datetime import datetime
from enum import IntEnum
from uuid import uuid4

from google.protobuf.field_mask_pb2 import FieldMask  # type: ignore
from google.protobuf.message import Message  # type: ignore
from google.protobuf.wrappers_pb2 import DoubleValue  # type: ignore
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.types import PaymentCardNumber

from example.plugin_config import exp_time
from protobuf_to_pydantic.customer_validator import check_one_of

from ..common.single_p2p import DemoEnum, DemoMessage


class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    """
    user info
    """

    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", ge=0, example=18)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: DemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", description="user name", min_length=1, max_length=10, example="so1n")
    demo_message: DemoMessage = Field(default_factory=DemoMessage, customer_string="c1", customer_int=1)


class OtherMessage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
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

    str_list: typing.List[str] = Field(default_factory=list, min_length=3, max_length=5)
    int_list: typing.Set[int] = Field(default_factory=set, min_length=1, max_length=5)
    user_list: typing.List[UserMessage] = Field(default_factory=list)


class AfterReferMessage(BaseModel):
    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", ge=0, example=18)


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
    user_pay: "NestedMessage.UserPayMessage" = Field(default_factory=lambda: NestedMessage.UserPayMessage())
    include_enum: "NestedMessage.IncludeEnum" = Field(default=0)
    empty: None = Field()
    after_refer: AfterReferMessage = Field(default_factory=AfterReferMessage)


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
    _one_of_dict = {"OptionalMessage.a": {"fields": {"x", "yy"}, "required": True}}
    one_of_validator = model_validator(mode="before")(check_one_of)
    x: str = Field(default="")
    y: int = Field(default=0, alias="yy", title="use age", ge=0, example=18)
    name: typing.Optional[str] = Field(default="")
    age: typing.Optional[int] = Field(default=0)
    item: typing.Optional[InvoiceItem] = Field(default_factory=InvoiceItem)
    str_list: typing.List[str] = Field(default_factory=list)
    int_map: typing.Dict[str, int] = Field(default_factory=dict)
    default_template_test: float = Field(default=1600000000.0)


class Invoice3(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem2"] = Field(default_factory=list)


class InvoiceItem2(BaseModel):
    """
        Test Circular references
    from: https://github.com/so1n/protobuf_to_pydantic/issues/57
    """

    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem2"] = Field(default_factory=list)
    invoice: Invoice3 = Field(default_factory=Invoice3)


class AnOtherMessage(BaseModel):
    class SubMessage(BaseModel):
        text: str = Field(default="")

    field1: str = Field(default="")
    field2: SubMessage = Field(default_factory=SubMessage)


class RootMessage(BaseModel):
    """
        Test Message references
    from: https://github.com/so1n/protobuf_to_pydantic/issues/64
    """

    field1: str = Field(default="")
    field2: AnOtherMessage = Field(default_factory=AnOtherMessage)


class TestSameName0(BaseModel):
    """
        Test inline structure of the same name
    from: https://github.com/so1n/protobuf_to_pydantic/issues/76
    """

    class Body(BaseModel):
        input_model: str = Field(default="")
        input_info: typing.Dict[str, str] = Field(default_factory=dict)

    body: "TestSameName0.Body" = Field(default_factory=lambda: TestSameName0.Body())


class TestSameName1(BaseModel):
    class Body(BaseModel):
        output_model: str = Field(default="")
        output_info: typing.Dict[str, str] = Field(default_factory=dict)

    body: "TestSameName1.Body" = Field(default_factory=lambda: TestSameName1.Body())
