# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.1.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 4.24.4
# Pydantic Version: 2.5.3
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field

from .diff_pkg_refer_1_p2p import Demo1


class Demo2(BaseModel):
    myField: "typing.Dict[str, Demo1]" = Field(default_factory=dict)
