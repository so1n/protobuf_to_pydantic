# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class DemoEnum(IntEnum):
    zero = 0
    one = 1
    two = 3


class DemoMessage(BaseModel):

    earth: str = FieldInfo(default="")
    mercury: str = FieldInfo(default="")
    mars: str = FieldInfo(default="")
