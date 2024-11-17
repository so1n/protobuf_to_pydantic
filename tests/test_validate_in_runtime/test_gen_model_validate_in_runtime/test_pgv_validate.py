from typing import Callable

from google.protobuf import __version__
from google.protobuf.any_pb2 import Any as AnyMessage  # type: ignore

from protobuf_to_pydantic._pydantic_adapter import is_v1

if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1.example.example_proto.validate import demo_pb2
    else:
        from example.proto_pydanticv2.example.example_proto.validate import demo_pb2
else:
    if is_v1:
        from example.proto_3_20_pydanticv1.example.example_proto.validate import demo_pb2
    else:
        from example.proto_3_20_pydanticv2.example.example_proto.validate import demo_pb2

from protobuf_to_pydantic import msg_to_pydantic_model
from tests.base.test_pgv_validate import BaseTestPgvModelValidator


class TestPgvModelValidator(BaseTestPgvModelValidator):
    number_model_class_list: list = [
        demo_pb2.FloatTest, demo_pb2.DoubleTest, demo_pb2.Int32Test, demo_pb2.Uint32Test, demo_pb2.Sfixed32Test,
        demo_pb2.Int64Test, demo_pb2.Sint64Test, demo_pb2.Uint64Test, demo_pb2.Sfixed64Test, demo_pb2.Fixed32Test,
        demo_pb2.Fixed64Test
    ]
    replace_message_fn: Callable = staticmethod(msg_to_pydantic_model)  # type: ignore

    def test_bool(self) -> None:
        self._test_bool(demo_pb2.BoolTest)

    def test_string(self) -> None:
        self._test_string(demo_pb2.StringTest)

    def test_bytes(self) -> None:
        self._test_bytes(demo_pb2.BytesTest)

    def test_enum(self) -> None:
        self._test_enum(demo_pb2.EnumTest)

    def test_repeated(self) -> None:
        self._test_repeated(demo_pb2.RepeatedTest)

    def test_map(self) -> None:
        self._test_map(demo_pb2.MapTest)

    def test_any(self) -> None:
        self._test_any(demo_pb2.AnyTest)

    def test_duration(self) -> None:
        self._test_duration(demo_pb2.DurationTest)

    def test_timestamp(self) -> None:
        self._test_timestamp(demo_pb2.TimestampTest)

    def test_nested(self) -> None:
        self._test_nested(demo_pb2.NestedMessage)

    def test_one_of(self) -> None:
        self._test_one_of(demo_pb2.OneOfTest)

    def test_one_of_not(self) -> None:
        self._test_one_of_not(demo_pb2.OneOfNotTest)
