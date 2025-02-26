# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[0.0.0](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 4.24.4
# Pydantic Version: 2.9.2
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field


class MyMessage1(BaseModel):
    content: typing.Optional[str] = Field(default="")


class MyMessage2(BaseModel):
    my_message1: typing.Optional[MyMessage1] = Field()
    my_message2: typing.Optional[MyMessage1] = Field(default_factory=MyMessage1)
    my_message3: MyMessage1 = Field()
    my_message4: MyMessage1 = Field(default_factory=MyMessage1)


class MyMessage3(BaseModel):
    my_message1: typing.Optional[MyMessage1] = Field()
    my_message2: typing.Optional[MyMessage1] = Field(default_factory=MyMessage1)
    my_message3: MyMessage1 = Field()
    my_message4: MyMessage1 = Field(default_factory=MyMessage1)
