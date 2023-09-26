# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.2.0.0](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 2.0.3
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field


class DemoEnum(IntEnum):
    zero = 0
    one = 1
    two = 3


class DemoMessage(BaseModel):
    earth: str = Field(default="", json_schema_extra={})
    mercury: str = Field(default="", json_schema_extra={})
    mars: str = Field(default="", json_schema_extra={})
