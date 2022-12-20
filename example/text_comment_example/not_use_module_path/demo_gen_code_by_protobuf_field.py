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
from text_comment_example.gen_code import exp_time


class SexType(IntEnum):
    man = 0
    women = 1


class ExampleProtoCommonSingleDemoEnum(IntEnum):
    """Note: The current class does not belong to the package
    ExampleProtoCommonSingleDemoEnum protobuf path:example_proto/common/single.proto"""

    zero = 0
    one = 1
    two = 3


class ExampleProtoCommonSingleDemoMessage(BaseModel):
    """Note: The current class does not belong to the package
    ExampleProtoCommonSingleDemoMessage protobuf path:example_proto/common/single.proto"""

    earth: str = FieldInfo(default="")
    mercury: str = FieldInfo(default="")
    mars: str = FieldInfo(default="")


class UserMessage(BaseModel):
    uid: str = FieldInfo(title="UID", description="user union id", example="10086")
    age: int = FieldInfo(default=0, title="use age", ge=0, example=18)
    height: float = FieldInfo(default=0.0, ge=0, le=2)
    sex: SexType = FieldInfo(default=0)
    demo: ExampleProtoCommonSingleDemoEnum = FieldInfo(default=0)
    is_adult: bool = FieldInfo(default=False)
    user_name: str = FieldInfo(default="", description="user name", min_length=1, max_length=10, example="so1n")
    demo_message: ExampleProtoCommonSingleDemoMessage = FieldInfo()


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = FieldInfo(default_factory=dict)
    user_flag: typing.Dict[str, bool] = FieldInfo(default_factory=dict)


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = FieldInfo(default_factory=list, min_items=3, max_items=5)
    int_list: typing.List[int] = FieldInfo(default_factory=list, min_items=1, max_items=5, unique_items=True)
    user_list: typing.List[UserMessage] = FieldInfo(default_factory=list)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: PaymentCardNumber = FieldInfo(default="")
        exp: datetime = FieldInfo(default_factory=exp_time)
        uuid: str = FieldInfo(default_factory=uuid4)

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    user_list_map: typing.Dict[str, RepeatedMessage] = FieldInfo(default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = FieldInfo(default_factory=dict)
    user_pay: UserPayMessage = FieldInfo()
    include_enum: IncludeEnum = FieldInfo(default=0)
    empty: None = FieldInfo()
