from typing import Any

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


class TestSimpleTest:
    @staticmethod
    def _model_output(msg: Any) -> str:
        return pydantic_model_to_py_code(msg_to_pydantic_model(msg, parse_msg_desc_method="ignore"))

    def test_empty_message(self) -> None:
        assert format_content("""
class EmptyMessage(BaseModel):
    pass
""")in self._model_output(demo_pb2.EmptyMessage)  # type: ignore

    def test_user_message(self) -> None:
        assert format_content("""
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
    uid: str = Field(default="")
    age: int = Field(default=0)
    height: float = Field(default=0.0)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field()
""") in self._model_output(demo_pb2.UserMessage)

    def test_struct_message(self) -> None:
        assert format_content("""
class StructMessage(BaseModel):
    metadata: typing.Dict[str, typing.Any] = Field(default_factory=dict)
""") in self._model_output(demo_pb2.StructMessage)

    def test_map_message(self) -> None:
        assert format_content("""
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
    uid: str = Field(default="")
    age: int = Field(default=0)
    height: float = Field(default=0.0)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field()


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict)
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict)
""") in self._model_output(demo_pb2.MapMessage)

    def test_repeated_message(self) -> None:
        assert format_content("""
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
    uid: str = Field(default="")
    age: int = Field(default=0)
    height: float = Field(default=0.0)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field()


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = Field(default_factory=list)
    int_list: typing.List[int] = Field(default_factory=list)
    user_list: typing.List[UserMessage] = Field(default_factory=list)
""") in self._model_output(
            demo_pb2.RepeatedMessage
        )

    def test_nested_message(self) -> None:
        assert format_content("""
import typing
from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo


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
    uid: str = Field(default="")
    age: int = Field(default=0)
    height: float = Field(default=0.0)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field()


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = Field(default_factory=list)
    int_list: typing.List[int] = Field(default_factory=list)
    user_list: typing.List[UserMessage] = Field(default_factory=list)


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict)
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict)


class AfterReferMessage(BaseModel):
    uid: str = Field(default="")
    age: int = Field(default=0)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: str = Field(default="")
        exp: datetime = Field(default_factory=datetime.now)
        uuid: str = Field(default="")

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    user_list_map: typing.Dict[str, RepeatedMessage] = Field(default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = Field(default_factory=dict)
    user_pay: UserPayMessage = Field()
    include_enum: IncludeEnum = Field(default=0)
    not_enable_user_pay: UserPayMessage = Field()
    empty: typing.Any = Field()
    after_refer: AfterReferMessage = Field()
""") in self._model_output(demo_pb2.NestedMessage)

    def test_invoice_item(self) -> None:
        assert format_content(
            """
class InvoiceItem(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem"] = Field(default_factory=list)
            """
        ) in self._model_output(demo_pb2.InvoiceItem)

    def test_field_optional(self) -> None:
        assert format_content(
            """
class OptionalMessage(BaseModel):
    name: typing.Optional[str] = Field(default="")
    age: typing.Optional[int] = Field(default=0)
    item: typing.Optional[InvoiceItem] = Field()
            """
        ) in self._model_output(demo_pb2.OptionalMessage)
