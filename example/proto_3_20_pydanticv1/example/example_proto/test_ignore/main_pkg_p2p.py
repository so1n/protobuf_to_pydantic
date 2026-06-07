# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 1.10.7
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field


class MainMessage(BaseModel):
    class Config:
        validate_all = True

    normal_field: str = Field(default="")
    # These types should be used but NOT imported due to ignore_pkg_list
    ignored_field: IgnoredMessage = Field(default_factory=IgnoredMessage)
    ignored_enum: IgnoredEnum = Field(default=0)
