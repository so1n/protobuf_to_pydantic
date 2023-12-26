from typing import Callable

from google.protobuf import __version__

from protobuf_to_pydantic._pydantic_adapter import is_v1

if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1.example.example_proto.p2p_validate import demo_pb2 as p2p_demo_pb2
    else:
        from example.proto_pydanticv2.example.example_proto.p2p_validate import demo_pb2 as p2p_demo_pb2
else:
    if is_v1:
        from example.proto_3_20_pydanticv1.example.example_proto.p2p_validate import demo_pb2 as p2p_demo_pb2
    else:
        from example.proto_3_20_pydanticv2.example.example_proto.p2p_validate import demo_pb2 as p2p_demo_pb2

from protobuf_to_pydantic import msg_to_pydantic_model
from tests.base.base_p2p_validate import BaseTestP2pModelValidator, local_dict


class TestP2pModelValidator(BaseTestP2pModelValidator):
    number_model_class_list: list = [
        p2p_demo_pb2.FloatTest, p2p_demo_pb2.DoubleTest, p2p_demo_pb2.Int32Test, p2p_demo_pb2.Uint32Test,
        p2p_demo_pb2.Sfixed32Test, p2p_demo_pb2.Int64Test, p2p_demo_pb2.Sint64Test, p2p_demo_pb2.Uint64Test,
        p2p_demo_pb2.Sfixed64Test, p2p_demo_pb2.Fixed32Test, p2p_demo_pb2.Fixed64Test
    ]
    replace_message_fn: Callable = staticmethod(msg_to_pydantic_model)  # type: ignore

    def test_bool(self) -> None:
        self._test_bool(self.replace_message_fn(p2p_demo_pb2.BoolTest, local_dict=local_dict))

    def test_string(self) -> None:
        self._test_string(self.replace_message_fn(p2p_demo_pb2.StringTest, local_dict=local_dict))

    def test_bytes(self) -> None:
        self._test_bytes(self.replace_message_fn(p2p_demo_pb2.BytesTest, local_dict=local_dict))

    def test_enum(self) -> None:
        self._test_enum(p2p_demo_pb2.EnumTest)

    def test_map(self) -> None:
        self._test_map(p2p_demo_pb2.MapTest)

    def test_repeated(self) -> None:
        self._test_repeated(p2p_demo_pb2.RepeatedTest)

    def test_any(self) -> None:
        self._test_any(p2p_demo_pb2.AnyTest)

    def test_duration(self) -> None:
        self._test_duration(p2p_demo_pb2.DurationTest)

    def test_timestamp(self) -> None:
        self._test_timestamp(p2p_demo_pb2.TimestampTest)

    def test_nested(self) -> None:
        self._test_nested(p2p_demo_pb2.NestedMessage)

    def test_one_of(self) -> None:
        self._test_one_of(p2p_demo_pb2.OneOfTest)

    def test_one_of_not(self) -> None:
        self._test_one_of_not(p2p_demo_pb2.OneOfNotTest)

    def test_one_of_optional(self) -> None:
        self._test_one_of_optional(p2p_demo_pb2.OneOfOptionalTest)
