from inspect import getsource

from google.protobuf import __version__

from protobuf_to_pydantic._pydantic_adapter import is_v1

if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1.example.example_proto.demo import demo_p2p
    else:
        from example.proto_pydanticv2.example.example_proto.demo import demo_p2p  # type: ignore[no-redef]
else:
    if is_v1:
        from example.proto_3_20_pydanticv1.example.example_proto.demo import demo_p2p  # type: ignore[no-redef]
    else:
        from example.proto_3_20_pydanticv2.example.example_proto.demo import demo_p2p  # type: ignore[no-redef]

class TestPlugin:

    def test_empty_message(self) -> None:
        content = """
class EmptyMessage(BaseModel):
    pass
"""
        assert content.strip("\n") in getsource(demo_p2p.EmptyMessage)

    def test_user_message(self) -> None:
        if not is_v1:
            content = """
class UserMessage(BaseModel):
    \"\"\"
    user info
    \"\"\"

    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", ge=0, example=18)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: DemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", description="user name", min_length=1, max_length=10, example="so1n")
    demo_message: DemoMessage = Field(customer_string="c1", customer_int=1)
"""
        else:
            content = """
class UserMessage(BaseModel):
    \"\"\"
    user info
    \"\"\"

    uid: str = Field(example="10086", title="UID", description="user union id")
    age: int = Field(default=0, example=18, title="use age", ge=0.0)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: DemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", example="so1n", description="user name", min_length=1, max_length=10)
    demo_message: DemoMessage = Field(customer_string="c1", customer_int=1)
"""
        assert content.strip("\n") in getsource(demo_p2p.UserMessage)

    def test_other_message(self) -> None:
        if is_v1:
            content = """
class OtherMessage(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    metadata: typing.Dict[str, typing.Any] = Field(default_factory=dict)
    double_value: DoubleValue = Field(default_factory=DoubleValue)
    field_mask: typing.Optional[FieldMask] = Field(default_factory=FieldMask)
"""
        else:
            content = """
class OtherMessage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    metadata: typing.Dict[str, typing.Any] = Field(default_factory=dict)
    double_value: DoubleValue = Field(default_factory=DoubleValue)
    field_mask: typing.Optional[FieldMask] = Field(default_factory=FieldMask)
"""
        assert content.strip("\n") in getsource(demo_p2p.OtherMessage).strip("\n")

    def test_map_message(self) -> None:
        content = """
class MapMessage(BaseModel):
    \"\"\"
    test map message and bad message
    \"\"\"

    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict)
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict)
"""
        assert content.strip("\n") in getsource(demo_p2p.MapMessage).strip("\n")

    def test_repeated_message(self) -> None:
        if is_v1:
            content = """
class RepeatedMessage(BaseModel):
    \"\"\"
    test repeated msg
    \"\"\"

    str_list: typing.List[str] = Field(default_factory=list, min_items=3, max_items=5)
    int_list: typing.List[int] = Field(default_factory=list, min_items=1, max_items=5, unique_items=True)
    user_list: typing.List[UserMessage] = Field(default_factory=list)
"""
        else:
            content = """
class RepeatedMessage(BaseModel):
    \"\"\"
    test repeated msg
    \"\"\"

    str_list: typing.List[str] = Field(default_factory=list, min_length=3, max_length=5)
    int_list: typing.Set[int] = Field(default_factory=set, min_length=1, max_length=5)
    user_list: typing.List[UserMessage] = Field(default_factory=list)
"""
        assert content.strip("\n") in getsource(demo_p2p.RepeatedMessage).strip("\n")

    def test_nested_message(self) -> None:
        content = """
class NestedMessage(BaseModel):
    \"\"\"
    test nested message
    \"\"\"

    class UserPayMessage(BaseModel):
        bank_number: PaymentCardNumber = Field(default="")
        exp: datetime = Field(default_factory=exp_time)
        uuid: str = Field(default_factory=uuid4)

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    user_list_map: typing.Dict[str, RepeatedMessage] = Field(default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = Field(default_factory=dict)
    user_pay: "NestedMessage.UserPayMessage" = Field()
    include_enum: "NestedMessage.IncludeEnum" = Field(default=0)
    empty: None = Field()
    after_refer: AfterReferMessage = Field()
"""
        assert content.strip("\n") in getsource(demo_p2p.NestedMessage).strip("\n")

    def test_self_referencing(self) -> None:
        content = """
class InvoiceItem(BaseModel):
    \"\"\"
        Test self-referencing Messages
    from: https://github.com/so1n/protobuf_to_pydantic/issues/7#issuecomment-1490705932
    \"\"\"

    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem"] = Field(default_factory=list)
"""
        assert content.strip("\n") in getsource(demo_p2p.InvoiceItem).strip("\n")

    def test_field_optional(self) -> None:
        content = """
class OptionalMessage(BaseModel):
    _one_of_dict = {"OptionalMessage.a": {"fields": {"x", "yy"}, "required": True}}
    one_of_validator = model_validator(mode="before")(check_one_of)
    x: str = Field(default="")
    y: int = Field(default=0, alias="yy", title="use age", ge=0, example=18)
    name: typing.Optional[str] = Field(default="")
    age: typing.Optional[int] = Field(default=0)
    item: typing.Optional[InvoiceItem] = Field(default=None)
    str_list: typing.List[str] = Field(default_factory=list)
    int_map: typing.Dict[str, int] = Field(default_factory=dict)
    default_template_test: float = Field(default=1600000000.0)
"""
        if is_v1:
            content = """
class OptionalMessage(BaseModel):
    _one_of_dict = {"OptionalMessage.a": {"fields": {"x", "yy"}, "required": True}}
    one_of_validator = root_validator(pre=True, allow_reuse=True)(check_one_of)
    x: str = Field(default="")
    y: int = Field(default=0, example=18, alias="yy", title="use age", ge=0.0)
    name: typing.Optional[str] = Field(default="")
    age: typing.Optional[int] = Field(default=0)
    item: typing.Optional[InvoiceItem] = Field(default=None)
    str_list: typing.List[str] = Field(default_factory=list)
    int_map: typing.Dict[str, int] = Field(default_factory=dict)
    default_template_test: float = Field(default=1600000000.0)
"""
        assert content.strip("\n") in getsource(demo_p2p.OptionalMessage).strip("\n")

    def test_after_refer_message(self)->None:
        pass

    def test_circular_references(self) -> None:
        content = """
class Invoice3(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem2"] = Field(default_factory=list)"""
        assert content.strip("\n") in getsource(demo_p2p.Invoice3).strip("\n")
        content = """
class InvoiceItem2(BaseModel):
    \"\"\"
        Test Circular references
    from: https://github.com/so1n/protobuf_to_pydantic/issues/57
    \"\"\"

    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem2"] = Field(default_factory=list)
    invoice: Invoice3 = Field()"""
        assert content.strip("\n") in getsource(demo_p2p.InvoiceItem2).strip("\n")

    def test_message_reference(self) -> None:
        content = """
class AnOtherMessage(BaseModel):
    class SubMessage(BaseModel):
        text: str = Field(default="")

    field1: str = Field(default="")
    field2: SubMessage = Field()"""
        assert content.strip("\n") in getsource(demo_p2p.AnOtherMessage).strip("\n")

        content = """
class RootMessage(BaseModel):
    \"\"\"
        Test Message references
    from: https://github.com/so1n/protobuf_to_pydantic/issues/64
    \"\"\"

    field1: str = Field(default="")
    field2: AnOtherMessage = Field()"""
        assert content.strip("\n") in getsource(demo_p2p.RootMessage).strip("\n")


    def test_same_bane_inline_structure(self) -> None:
        content = """
class TestSameName0(BaseModel):
    \"\"\"
        Test inline structure of the same name
    from: https://github.com/so1n/protobuf_to_pydantic/issues/76
    \"\"\"

    class Body(BaseModel):
        input_model: str = Field(default="")
        input_info: typing.Dict[str, str] = Field(default_factory=dict)

    body: "TestSameName0.Body" = Field()"""
        assert content.strip("\n") in getsource(demo_p2p.TestSameName0).strip("\n")
        content = """
class TestSameName1(BaseModel):
    class Body(BaseModel):
        output_model: str = Field(default="")
        output_info: typing.Dict[str, str] = Field(default_factory=dict)

    body: "TestSameName1.Body" = Field()"""
        assert content.strip("\n") in getsource(demo_p2p.TestSameName1).strip("\n")
