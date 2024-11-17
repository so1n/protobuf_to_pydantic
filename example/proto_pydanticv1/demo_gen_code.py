# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.0](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 4.24.4
# Pydantic Version: 1.10.7
import typing

from protobuf_to_pydantic.customer_validator.v1 import check_one_of
from pydantic import BaseModel, Field, root_validator


class InvoiceItem(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem"] = Field(default_factory=list)


class OptionalMessage(BaseModel):
    _one_of_dict = {"user.OptionalMessage.a": {"fields": {"x", "y"}, "required": False}}

    x: str = Field(default="")
    y: int = Field(default=0)
    name: typing.Optional[str] = Field(default="")
    age: typing.Optional[int] = Field(default=0)
    item: typing.Optional[InvoiceItem] = Field()
    str_list: typing.List[str] = Field(default_factory=list)
    int_map: typing.Dict[str, int] = Field(default_factory=dict)
    default_template_test: float = Field(default=0.0)

    one_of_validator = root_validator(pre=True, allow_reuse=True)(check_one_of)
