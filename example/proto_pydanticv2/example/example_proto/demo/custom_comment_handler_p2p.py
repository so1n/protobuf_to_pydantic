# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.1.2](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 4.24.4
# Pydantic Version: 2.5.3
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field


class UserMessage(BaseModel):
    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", description="", ge=0, example=18)
    height: float = Field(default=0.0, description="user_height", ge=0.0, le=2.5)
    is_adult: bool = Field(default=False, description="")
    user_name: str = Field(default="", description="user name", min_length=1, max_length=10, example="so1n")
