import time
from typing import Any
from uuid import uuid4

from google.protobuf import __version__

from protobuf_to_pydantic._pydantic_adapter import is_v1

if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1.example.example_proto.demo import demo_pb2
    else:
        from example.proto_pydanticv2.example.example_proto.demo import demo_pb2  # type: ignore[no-redef]
else:
    if is_v1:
        from example.proto_3_20_pydanticv1.example.example_proto.demo import demo_pb2  # type: ignore[no-redef]
    else:
        from example.proto_3_20_pydanticv2.example.example_proto.demo import demo_pb2  # type: ignore[no-redef]

from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code
from protobuf_to_pydantic.util import format_content
from tests.test_gen_code.test_helper import P2CNoHeader


def exp_time() -> float:
    return time.time()


class BaseTestTextComment:
    @staticmethod
    def _model_output(msg: Any) -> str:
        local_dict = {"exp_time": exp_time, "uuid4": uuid4}
        return pydantic_model_to_py_code(
            msg_to_pydantic_model(
                msg,
                parse_msg_desc_method=demo_pb2,
                local_dict=local_dict
            ),
            p2c_class=P2CNoHeader
        )

    def test_user_message(self) -> None:
        content = """
class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto\"\"\"

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(BaseModel):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto\"\"\"

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    class Config:
        validate_all = True

    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", ge=0.0, example=18)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", description="user name", min_length=1, max_length=10, example="so1n")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage,
        customer_string="c1", customer_int=1
    )
"""
        if not is_v1:
            content = """
class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto\"\"\"

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(BaseModel):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto\"\"\"

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    model_config = ConfigDict(validate_default=True)

    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", example=18, ge=0)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", description="user name", example="so1n", min_length=1, max_length=10)
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage,
        customer_string="c1", customer_int=1
    )
"""
        assert format_content(content) in self._model_output(demo_pb2.UserMessage)

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
        assert format_content(content) in self._model_output(demo_pb2.OtherMessage)

    def test_map_message(self) -> None:
        content = """
class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto\"\"\"

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(BaseModel):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto\"\"\"

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    class Config:
        validate_all = True

    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", ge=0.0, example=18)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", description="user name", min_length=1, max_length=10, example="so1n")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage,
        customer_string="c1", customer_int=1
    )


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict)
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict)
"""
        if not is_v1:
            content = """
class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto\"\"\"

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(BaseModel):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto\"\"\"

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    model_config = ConfigDict(validate_default=True)

    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", example=18, ge=0)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", description="user name", example="so1n", min_length=1, max_length=10)
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage,
        customer_string="c1", customer_int=1
    )


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict)
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict)
"""
        assert format_content(content) in self._model_output(demo_pb2.MapMessage)

    def test_repeated_message(self) -> None:
        content = """
class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto\"\"\"

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(BaseModel):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto\"\"\"

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    class Config:
        validate_all = True

    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", ge=0.0, example=18)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", description="user name", min_length=1, max_length=10, example="so1n")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage,
        customer_string="c1", customer_int=1
    )


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = Field(default_factory=list, min_items=3, max_items=5)
    int_list: typing.List[int] = Field(default_factory=list, min_items=1, max_items=5, unique_items=True)
    user_list: typing.List[UserMessage] = Field(default_factory=list)
"""
        if not is_v1:
            content = """
class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto\"\"\"

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(BaseModel):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto\"\"\"

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    model_config = ConfigDict(validate_default=True)

    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", example=18, ge=0)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", description="user name", example="so1n", min_length=1, max_length=10)
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage,
        customer_string="c1", customer_int=1
    )


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = Field(default_factory=list, min_length=3, max_length=5)
    int_list: typing.Set[int] = Field(default_factory=set, min_length=1, max_length=5)
    user_list: typing.List[UserMessage] = Field(default_factory=list)

"""
        assert format_content(content) in self._model_output(demo_pb2.RepeatedMessage)

    def test_nested_message(self) -> None:
        content = """
class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto\"\"\"

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(BaseModel):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto\"\"\"

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    class Config:
        validate_all = True

    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", ge=0.0, example=18)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", description="user name", min_length=1, max_length=10, example="so1n")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage,
        customer_string="c1", customer_int=1
    )


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = Field(default_factory=list, min_items=3, max_items=5)
    int_list: typing.List[int] = Field(default_factory=list, min_items=1, max_items=5, unique_items=True)
    user_list: typing.List[UserMessage] = Field(default_factory=list)


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict)
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict)


class AfterReferMessage(BaseModel):
    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", ge=0.0, example=18)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: PaymentCardNumber = Field(default="")
        exp: datetime = Field(default_factory=exp_time)
        uuid: str = Field(default_factory=uuid4)

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    class Config:
        validate_all = True

    user_list_map: typing.Dict[str, RepeatedMessage] = Field(default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = Field(default_factory=dict)
    user_pay: UserPayMessage = Field(default_factory=UserPayMessage)
    include_enum: IncludeEnum = Field(default=0)
    empty: typing.Any = Field()
    after_refer: AfterReferMessage = Field(default_factory=AfterReferMessage)
"""
        if not is_v1:
            content = """
class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto\"\"\"

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(BaseModel):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto\"\"\"

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    model_config = ConfigDict(validate_default=True)

    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", example=18, ge=0)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", description="user name", example="so1n", min_length=1, max_length=10)
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage,
        customer_string="c1", customer_int=1
    )


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = Field(default_factory=list, min_length=3, max_length=5)
    int_list: typing.Set[int] = Field(default_factory=set, min_length=1, max_length=5)
    user_list: typing.List[UserMessage] = Field(default_factory=list)


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict)
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict)


class AfterReferMessage(BaseModel):
    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", example=18, ge=0)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: PaymentCardNumber = Field(default="")
        exp: datetime = Field(default_factory=exp_time)
        uuid: str = Field(default_factory=uuid4)

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    model_config = ConfigDict(validate_default=True)

    user_list_map: typing.Dict[str, RepeatedMessage] = Field(default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = Field(default_factory=dict)
    user_pay: UserPayMessage = Field(default_factory=UserPayMessage)
    include_enum: IncludeEnum = Field(default=0)
    empty: typing.Any = Field()
    after_refer: AfterReferMessage = Field(default_factory=AfterReferMessage)
"""
        assert format_content(content) in self._model_output(demo_pb2.NestedMessage)

    def test_self_referencing(self) -> None:
        assert format_content(
            """
class InvoiceItem(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem"] = Field(default_factory=list)
            """
        ) in self._model_output(demo_pb2.InvoiceItem)

    def test_circular_references(self) -> None:
        assert format_content(
            """
class Invoice3(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem2"] = Field(default_factory=list)


class InvoiceItem2(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem2"] = Field(default_factory=list)
    invoice: Invoice3 = Field(default_factory=Invoice3)
            """
        ) in self._model_output(demo_pb2.InvoiceItem2)

    def test_message_reference(self) -> None:
        assert format_content(
            """
class AnOtherMessage(BaseModel):
    class SubMessage(BaseModel):
        text: str = Field(default="")

    field1: str = Field(default="")
    field2: SubMessage = Field(default_factory=SubMessage)


class RootMessage(BaseModel):
    field1: str = Field(default="")
    field2: AnOtherMessage = Field(default_factory=AnOtherMessage)
            """
        ) in self._model_output(demo_pb2.RootMessage)

    def test_same_bane_inline_structure(self) -> None:
        assert format_content(
            """
class TestSameName0(BaseModel):
    class Body(BaseModel):
        input_model: str = Field(default="")
        input_info: typing.Dict[str, str] = Field(default_factory=dict)

    body: Body = Field(default_factory=Body)
            """
        ) in self._model_output(demo_pb2.TestSameName0)

        assert format_content(
            """
class TestSameName1(BaseModel):
    class Body(BaseModel):
        output_model: str = Field(default="")
        output_info: typing.Dict[str, str] = Field(default_factory=dict)

    body: Body = Field(default_factory=Body)
            """
        ) in self._model_output(demo_pb2.TestSameName1)

class TestTextCommentByPyi(BaseTestTextComment):
    @staticmethod
    def _model_output(msg: Any) -> str:
        local_dict = {"exp_time": exp_time, "uuid4": uuid4}
        return pydantic_model_to_py_code(
            msg_to_pydantic_model(
                msg,
                parse_msg_desc_method=demo_pb2,
                local_dict=local_dict
            ),
            p2c_class=P2CNoHeader
        )


class TestTextCommentByProtobufFProtobufField(BaseTestTextComment):
    @staticmethod
    def _model_output(msg: Any) -> str:
        local_dict = {"exp_time": exp_time, "uuid4": uuid4}
        from pathlib import Path
        if not Path("example").exists():
            # ignore exec in github action runner
            return pydantic_model_to_py_code(
                msg_to_pydantic_model(
                    msg,
                    parse_msg_desc_method=demo_pb2,
                    local_dict=local_dict
                ),
                p2c_class=P2CNoHeader
            )
        return pydantic_model_to_py_code(
            msg_to_pydantic_model(
                msg,
                parse_msg_desc_method=".",
                local_dict=local_dict
            ),
            p2c_class=P2CNoHeader
        )
