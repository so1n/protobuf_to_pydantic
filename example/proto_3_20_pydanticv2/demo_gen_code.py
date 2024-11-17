# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.0](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 3.20.3
# Pydantic Version: 2.5.3
import typing

from protobuf_to_pydantic.customer_validator.v2 import check_one_of
from pydantic import BaseModel, Field, model_validator


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

    one_of_validator = model_validator(mode="before")(check_one_of)
