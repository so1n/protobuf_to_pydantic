# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.1.2](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 1.10.7
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field


class DemoEnum(IntEnum):
    zero = 0
    one = 1
    two = 3


class DemoMessage(BaseModel):
    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")
