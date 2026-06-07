# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 4.24.4
# Pydantic Version: 2.5.3
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, ConfigDict, Field


class MainMessage(BaseModel):
    model_config = ConfigDict(validate_default=True)
    normal_field: str = Field(default="")
    # These types should be used but NOT imported due to ignore_pkg_list
    ignored_field: IgnoredMessage = Field(default_factory=IgnoredMessage)
    ignored_enum: IgnoredEnum = Field(default=0)
