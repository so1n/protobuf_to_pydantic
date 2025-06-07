# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.0](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 1.10.7
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field

from .diff_pkg_refer_1_p2p import Demo1


class Demo2(BaseModel):
    myField: "typing.Dict[str, Demo1]" = Field(default_factory=dict)
