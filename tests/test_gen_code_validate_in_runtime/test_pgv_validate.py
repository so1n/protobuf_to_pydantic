from typing import Any, Callable, Type

from google.protobuf.any_pb2 import Any as AnyMessage  # type: ignore

from example.validate_example import demo_gen_code_by_pgv
from tests.base.test_pgv_validate import BaseTestPgvModelValidator


def stub_func(model_class: Type, **kwargs: Any) -> Type:
    return model_class


class TestPgvModelValidator(BaseTestPgvModelValidator):
    number_model_class_list: list = [
        demo_gen_code_by_pgv.FloatTest, demo_gen_code_by_pgv.DoubleTest, demo_gen_code_by_pgv.Int32Test,
        demo_gen_code_by_pgv.Uint32Test, demo_gen_code_by_pgv.Sfixed32Test, demo_gen_code_by_pgv.Int64Test,
        demo_gen_code_by_pgv.Sint64Test, demo_gen_code_by_pgv.Uint64Test, demo_gen_code_by_pgv.Sfixed64Test,
        demo_gen_code_by_pgv.Fixed32Test, demo_gen_code_by_pgv.Fixed64Test
    ]
    replace_message_fn: Callable = staticmethod(stub_func)  # type: ignore

    def test_bool(self) -> None:
        self._test_bool(demo_gen_code_by_pgv.BoolTest)

    def test_string(self) -> None:
        self._test_string(demo_gen_code_by_pgv.StringTest)

    def test_bytes(self) -> None:
        self._test_bytes(demo_gen_code_by_pgv.BytesTest)

    def test_enum(self) -> None:
        self._test_enum(demo_gen_code_by_pgv.EnumTest)

    def test_repeated(self) -> None:
        self._test_repeated(demo_gen_code_by_pgv.RepeatedTest)

    def test_map(self) -> None:
        self._test_map(demo_gen_code_by_pgv.MapTest)

    def test_any(self) -> None:
        self._test_any(demo_gen_code_by_pgv.AnyTest)

    def test_duration(self) -> None:
        self._test_duration(demo_gen_code_by_pgv.DurationTest)

    def test_timestamp(self) -> None:
        self._test_timestamp(demo_gen_code_by_pgv.TimestampTest)

    def test_nested(self) -> None:
        self._test_nested(demo_gen_code_by_pgv.NestedMessage)

    def test_one_of(self) -> None:
        self._test_one_of(demo_gen_code_by_pgv.OneOfTest)

    def test_one_of_not(self) -> None:
        self._test_one_of_not(demo_gen_code_by_pgv.OneOfNotTest)
