from typing import Any, Callable, Type

from google.protobuf import __version__
from pydantic import BaseModel

from protobuf_to_pydantic._pydantic_adapter import is_v1

if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1.example.example_proto.validate import demo_p2p
    else:
        from example.proto_pydanticv2.example.example_proto.validate import demo_p2p
else:
    if is_v1:
        from example.proto_3_20_pydanticv1.example.example_proto.validate import demo_p2p
    else:
        from example.proto_3_20_pydanticv2.example.example_proto.validate import demo_p2p

from tests.test_validate_in_runtime.test_gen_model_validate_in_runtime.test_pgv_validate import (
    BaseTestPgvModelValidator,
)


def stub_func(model_class: Type[BaseModel], **kwargs: Any) -> Type[BaseModel]:
    return model_class


class TestP2pModelValidator(BaseTestPgvModelValidator):
    number_model_class_list: list = [
        demo_p2p.FloatTest, demo_p2p.DoubleTest, demo_p2p.Int32Test, demo_p2p.Uint32Test,
        demo_p2p.Sfixed32Test, demo_p2p.Int64Test, demo_p2p.Sint64Test, demo_p2p.Uint64Test,
        demo_p2p.Sfixed64Test, demo_p2p.Fixed32Test, demo_p2p.Fixed64Test
    ]
    replace_message_fn: Callable = staticmethod(stub_func)  # type: ignore

    def test_bool(self) -> None:
        self._test_bool(demo_p2p.BoolTest)

    def test_string(self) -> None:
        self._test_string(demo_p2p.StringTest)

    def test_bytes(self) -> None:
        self._test_bytes(demo_p2p.BytesTest)

    def test_enum(self) -> None:
        self._test_enum(demo_p2p.EnumTest)

    def test_repeated(self) -> None:
        self._test_repeated(demo_p2p.RepeatedTest)

    def test_map(self) -> None:
        self._test_map(demo_p2p.MapTest)

    def test_any(self) -> None:
        self._test_any(demo_p2p.AnyTest)

    def test_duration(self) -> None:
        self._test_duration(demo_p2p.DurationTest)

    def test_timestamp(self) -> None:
        self._test_timestamp(demo_p2p.TimestampTest)

    def test_nested(self) -> None:
        self._test_nested(demo_p2p.NestedMessage)

    def test_one_of(self) -> None:
        self._test_one_of(demo_p2p.OneOfTest)

    def test_one_of_not(self) -> None:
        self._test_one_of_not(demo_p2p.OneOfNotTest)
