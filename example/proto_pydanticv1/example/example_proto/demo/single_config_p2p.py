# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.2.0](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 4.24.4
# Pydantic Version: 1.10.7
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field


class UserMessage(BaseModel):
    """
    user info
    """

    uid: str = Field(example="10086", title="UID", description="user union id")
    age: int = Field(default=0, example=18, title="use age", ge=0.0)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", example="so1n", description="user name", min_length=1, max_length=10)
