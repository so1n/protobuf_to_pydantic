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


class BaseGenCodeP2pModelValidator(BaseTestP2pModelValidator):
    core_module: Any
    replace_message_fn: Callable = staticmethod(stub_func)  # type: ignore

    @property
    def number_model_class_list(self):
        return [
            self.core_module.FloatTest, self.core_module.DoubleTest, self.core_module.Int32Test,
            self.core_module.Uint32Test, self.core_module.Sfixed32Test, self.core_module.Int64Test,
            self.core_module.Sint64Test, self.core_module.Uint64Test, self.core_module.Sfixed64Test,
            self.core_module.Fixed32Test, self.core_module.Fixed64Test
        ]

    def test_bool(self) -> None:
        self._test_bool(self.replace_message_fn(self.core_module.BoolTest, local_dict=local_dict))

    def test_string(self) -> None:
        self._test_string(self.replace_message_fn(self.core_module.StringTest, local_dict=local_dict))

    def test_bytes(self) -> None:
        self._test_bytes(self.replace_message_fn(self.core_module.BytesTest, local_dict=local_dict))

    def test_enum(self) -> None:
        self._test_enum(self.core_module.EnumTest)

    def test_map(self) -> None:
        self._test_map(self.core_module.MapTest)

    def test_repeated(self) -> None:
        self._test_repeated(self.core_module.RepeatedTest)

    def test_any(self) -> None:
        self._test_any(self.core_module.AnyTest)

    def test_duration(self) -> None:
        self._test_duration(self.core_module.DurationTest)

    def test_timestamp(self) -> None:
        self._test_timestamp(self.core_module.TimestampTest)

    def test_nested(self) -> None:
        self._test_nested(self.core_module.NestedMessage)

    def test_one_of(self) -> None:
        self._test_one_of(self.core_module.OneOfTest)

    def test_one_of_not(self) -> None:
        self._test_one_of_not(self.core_module.OneOfNotTest)

    def test_one_of_optional(self) -> None:
        self._test_one_of_optional(self.core_module.OneOfOptionalTest)

    def test_optional_message(self) -> None:
        self._test_optional_message(self.core_module.OptionalMessage)

class TestP2pModelValidator(BaseGenCodeP2pModelValidator):
    core_module = demo_gen_code_by_p2p
