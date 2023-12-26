from typing import Any, Callable, Type

from google.protobuf import __version__

from protobuf_to_pydantic._pydantic_adapter import is_v1

if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1 import demo_gen_code_by_p2p
    else:
        from example.proto_pydanticv2 import demo_gen_code_by_p2p
else:
    if is_v1:
        from example.proto_3_20_pydanticv1 import demo_gen_code_by_p2p
    else:
        from example.proto_3_20_pydanticv2 import demo_gen_code_by_p2p

from tests.base.base_p2p_validate import BaseTestP2pModelValidator, local_dict


def stub_func(model_class: Type, **kwargs: Any) -> Type:
    return model_class


class TestP2pModelValidator(BaseTestP2pModelValidator):
    number_model_class_list: list = [
        demo_gen_code_by_p2p.FloatTest, demo_gen_code_by_p2p.DoubleTest, demo_gen_code_by_p2p.Int32Test,
        demo_gen_code_by_p2p.Uint32Test, demo_gen_code_by_p2p.Sfixed32Test, demo_gen_code_by_p2p.Int64Test,
        demo_gen_code_by_p2p.Sint64Test, demo_gen_code_by_p2p.Uint64Test, demo_gen_code_by_p2p.Sfixed64Test,
        demo_gen_code_by_p2p.Fixed32Test, demo_gen_code_by_p2p.Fixed64Test
    ]
    replace_message_fn: Callable = staticmethod(stub_func)  # type: ignore

    def test_bool(self) -> None:
        self._test_bool(self.replace_message_fn(demo_gen_code_by_p2p.BoolTest, local_dict=local_dict))

    def test_string(self) -> None:
        self._test_string(self.replace_message_fn(demo_gen_code_by_p2p.StringTest, local_dict=local_dict))

    def test_bytes(self) -> None:
        self._test_bytes(self.replace_message_fn(demo_gen_code_by_p2p.BytesTest, local_dict=local_dict))

    def test_enum(self) -> None:
        self._test_enum(demo_gen_code_by_p2p.EnumTest)

    def test_map(self) -> None:
        self._test_map(demo_gen_code_by_p2p.MapTest)

    def test_repeated(self) -> None:
        self._test_repeated(demo_gen_code_by_p2p.RepeatedTest)

    def test_any(self) -> None:
        self._test_any(demo_gen_code_by_p2p.AnyTest)

    def test_duration(self) -> None:
        self._test_duration(demo_gen_code_by_p2p.DurationTest)

    def test_timestamp(self) -> None:
        self._test_timestamp(demo_gen_code_by_p2p.TimestampTest)

    def test_nested(self) -> None:
        self._test_nested(demo_gen_code_by_p2p.NestedMessage)

    def test_one_of(self) -> None:
        self._test_one_of(demo_gen_code_by_p2p.OneOfTest)

    def test_one_of_not(self) -> None:
        self._test_one_of_not(demo_gen_code_by_p2p.OneOfNotTest)
    def test_one_of_optional(self) -> None:
        self._test_one_of_optional(demo_gen_code_by_p2p.OneOfOptionalTest)
