from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any, Callable
from uuid import uuid4

import pytest
from google.protobuf.any_pb2 import Any as AnyMessage  # type: ignore
from pydantic import ValidationError

from example.example_proto_python_code.example_proto.validate import demo_pb2
from protobuf_to_pydantic import msg_to_pydantic_model


class BaseTestPgvModelValidator:
    number_model_class_list: list = []
    replace_message_fn: Callable = staticmethod(lambda model_class, **kwargs: model_class)  # type: ignore

    def _check_message_validate(self, message_class: Any, normal_dict: dict, error_map_dict: dict) -> None:
        self.replace_message_fn(message_class, parse_msg_desc_method="PGV")(**normal_dict)
        for key, value in error_map_dict.items():
            error_normal_dict: dict = deepcopy(normal_dict)
            error_normal_dict[key] = value
            with pytest.raises(ValidationError):
                self.replace_message_fn(message_class, parse_msg_desc_method="PGV")(**error_normal_dict)

    def test_number_model_in_validator(self) -> None:
        for model_class in self.number_model_class_list:
            for i in [1, 2, 3]:
                self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(in_test=i)
            for i in [0, 4]:
                with pytest.raises(ValidationError):
                    self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(in_test=i)

    def test_number_model_not_in_validator(self) -> None:
        for model_class in self.number_model_class_list:
            for i in [1, 2, 3]:
                with pytest.raises(ValidationError):
                    self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(not_in_test=i)
            for i in [0, 4]:
                self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(not_in_test=i)

    def _test_bool(self, model_class: Any) -> None:
        self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(bool_1_test=True, bool_2_test=False)
        with pytest.raises(ValidationError):
            self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(bool_1_test=False, bool_2_test=False)
            self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(bool_1_test=True, bool_2_test=True)

    def _test_string(self, model_class: Any) -> None:
        normal_dict: dict = {
            "const_test": "aaa",
            "len_test": "aaa",
            "s_range_len_test": "aa",
            "pattern_test": "testaa",
            "prefix_test": "prefix_testaa",
            "suffix_test": "aa_suffix",
            "contains_test": "aaa_contains_test",
            "not_contains_test": "aaa",
            "in_test": "a",
            "not_in_test": "d",
            "email_test": "example@example.com",
            "hostname_test": "127.0.0.1",
            "ip_test": "127.0.0.1",
            "ipv4_test": "127.0.0.1",
            "ipv6_test": "::1",
            "uri_test": "http://127.0.0.1",
            "uri_ref_test": "http://127.0.0.1/paths",
            "address_test": "127.0.0.1",
            "uuid_test": str(uuid4())
        }

        self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(**normal_dict)
        for column in [
            "len_test", "s_range_len_test", "pattern_test", "prefix_test", "suffix_test", "contains_test",
            "not_contains_test", "in_test", "not_in_test", "email_test", "hostname_test", "ip_test", "ipv4_test",
            "ipv6_test", "uri_test", "uri_ref_test", "address_test", "uuid_test"
        ]:
            error_normal_dict: dict = deepcopy(normal_dict)
            error_normal_dict[column] = "aaaa"
            error_normal_dict["not_contains_test"] = "not_contains"
            with pytest.raises(ValidationError):
                self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(**error_normal_dict)

    def _test_bytes(self, model_class: Any) -> None:
        normal_dict: dict = {
            "const_test": b"demo",
            "len_test": b"aaaa",
            "range_len_test": b"aa",
            "pattern_test": b"testaa",
            "prefix_test": b"prefix_testaa",
            "suffix_test": b"aa_suffix",
            "contains_test": b"aaa_contains_test",
            "in_test": b"a",
            "not_in_test": b"d",
        }

        self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(**normal_dict)
        for column in [
            "len_test", "range_len_test", "prefix_test", "suffix_test", "contains_test",
            "in_test", "not_in_test"
        ]:
            error_normal_dict: dict = deepcopy(normal_dict)
            error_normal_dict[column] = b"aaaaa"
            error_normal_dict["not_in_test"] = b"a"
            with pytest.raises(ValidationError):
                self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(**error_normal_dict)

    def _test_enum(self, model_class: Any) -> None:
        normal_dict: dict = {
            "const_test": 2,
            "in_test": 0,
            "not_in_test": 1,
        }
        error_map_dict: dict = {
            "const_test": 4,
            "in_test": 4,
            "not_in_test": 2,
        }
        self._check_message_validate(model_class, normal_dict, error_map_dict)

    def _test_map(self, model_class: Any) -> None:
        normal_dict: dict = {
            "pair_test": {"a": 1},
            "no_parse_test": {"a": 1},
            "keys_test": {"a": 1},
            "values_test": {"a": 5},
            "keys_values_test": {"a": datetime.now() + timedelta(days=1)},
            "ignore_test": {"a": 1}
        }
        error_map_dict: dict = {
            "pair_test": {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6},
            "keys_test": {"aaaaaa": 1},
            "values_test": {"a": 1},
            "keys_values_test": {"a": datetime.now() - timedelta(days=1)},
        }
        self._check_message_validate(model_class, normal_dict, error_map_dict)

    def _test_repeated(self, model_class: Any) -> None:
        normal_dict: dict = {
            "range_test": ["a"],
            "unique_test": ["a", "b", "c"],
            "items_string_test": ["abc", "def"],
            "items_double_test": [1.2, 3.4],
            "items_int32_test": [2, 3],
            "items_timestamp_test": [datetime.fromtimestamp(1600000001)],
            "items_duration_test": [timedelta(seconds=15)],
            "items_bytes_test": [b"a", b"b"],
            "ignore_test": ["a", "b"]
        }
        error_map_dict: dict = {
            "range_test": ["a", "b", "c", "d", "e", "f"],
            "unique_test": ["a", "b", "c", "c"],
            "items_string_test": ["abc", "def", "abcdef"],
            "items_double_test": [1.2, 3.4, "5.6"],
            "items_int32_test": [2, 3, 6],
            "items_timestamp_test": [datetime.fromtimestamp(1600000100)],
            "items_duration_test": [timedelta(seconds=25)],
            "items_bytes_test": [b"a", b"b", b"c", b"d", b"e", b"f"],
        }
        self._check_message_validate(model_class, normal_dict, error_map_dict)

    def _test_any(self, model_class: Any) -> None:
        normal_dict: dict = {
            "required_test": AnyMessage(),
            "not_in_test": AnyMessage(),
            "in_test": AnyMessage(type_url="type.googleapis.com/google.protobuf.Timestamp",),
        }
        error_map_dict: dict = {
            "in_test": AnyMessage(),
            "not_in_test": AnyMessage(type_url="type.googleapis.com/google.protobuf.Timestamp"),
        }
        self._check_message_validate(model_class, normal_dict, error_map_dict)

    def _test_duration(self, model_class: Any) -> None:
        normal_dict: dict = {
            "required_test": timedelta(seconds=3600).total_seconds(),
            "const_test": timedelta(seconds=1, microseconds=500000),
            "range_test": timedelta(seconds=6),
            "range_e_test": timedelta(seconds=10, microseconds=500000),
            "in_test": timedelta(seconds=1, microseconds=500000),
            "not_in_test": timedelta(seconds=2, microseconds=500000),
        }
        error_map_dict: dict = {
            "const_test": timedelta(seconds=2, microseconds=500000),
            "range_test": timedelta(seconds=4),
            "range_e_test": timedelta(seconds=10, microseconds=500001),
            "in_test": timedelta(microseconds=500000),
            "not_in_test": timedelta(seconds=1, microseconds=500000),
        }
        self._check_message_validate(model_class, normal_dict, error_map_dict)

    def _test_timestamp(self, model_class: Any) -> None:
        normal_dict: dict = {
            "required_test": datetime.now(),
            "const_test": datetime.fromtimestamp(1600000000),
            "range_test": datetime.fromtimestamp(1600000009),
            "range_e_test": datetime.fromtimestamp(1600000010),
            "lt_now_test": datetime.now() - timedelta(days=1),
            "gt_now_test": datetime.now() + timedelta(days=1),
            "within_test": datetime.now(),
            "within_and_gt_now_test": datetime.now() + timedelta(seconds=3590),
        }
        error_map_dict: dict = {
            "const_test": datetime.fromtimestamp(1600000001),
            "range_test": datetime.fromtimestamp(1600000010),
            "range_e_test": datetime.fromtimestamp(1600000011),
            "lt_now_test": datetime.now() + timedelta(days=1),
            "gt_now_test": datetime.now() - timedelta(days=1),
            "within_test": datetime.now() + timedelta(days=1),
            "within_and_gt_now_test": datetime.now() + timedelta(seconds=3660),
        }
        self._check_message_validate(model_class, normal_dict, error_map_dict)

    def _test_nested(self, model_class: Any) -> None:
        normal_dict: dict = {
            "string_in_map_test": {
                "a": {
                    "const_test": "aaa",
                    "len_test": "aaa",
                    "s_range_len_test": "aa",
                    "pattern_test": "testaa",
                    "prefix_test": "prefix_testaa",
                    "suffix_test": "aa_suffix",
                    "contains_test": "aaa_contains_test",
                    "not_contains_test": "aaa",
                    "in_test": "a",
                    "not_in_test": "d",
                    "email_test": "example@example.com",
                    "hostname_test": "127.0.0.1",
                    "ip_test": "127.0.0.1",
                    "ipv4_test": "127.0.0.1",
                    "ipv6_test": "::1",
                    "uri_test": "http://127.0.0.1",
                    "uri_ref_test": "http://127.0.0.1/paths",
                    "address_test": "127.0.0.1",
                    "uuid_test": str(uuid4())
                }
            },
            "map_in_map_test": {
                "a": {
                    "pair_test": {"a": 1},
                    "no_parse_test": {"a": 1},
                    "keys_test": {"a": 1},
                    "values_test": {"a": 5},
                    "keys_values_test": {"a": datetime.now() + timedelta(days=1)},
                    "ignore_test": {"a": 1}
                }
            },
            "user_pay": {
                "bank_number": "abcabcabcabcabc",
                "exp": datetime.now() + timedelta(days=1),
                "uuid": str(uuid4())
            },
            "not_enable_user_pay": {
                "bank_number": "abc",
                "exp": datetime.now() - timedelta(days=1),
                "uuid": "abc"
            },
            "empty": None
        }
        self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(**normal_dict)

    def _test_one_of(self, model_class: Any) -> None:
        # test init
        self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(x="1")
        self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(y=2)
        with pytest.raises(ValidationError):
            self.replace_message_fn(model_class, parse_msg_desc_method="PGV")(x="1", y=2)

        # test pgv
        with pytest.raises(ValidationError):
            self.replace_message_fn(model_class, parse_msg_desc_method="PGV")()

    def _test_one_of_not(self, model_class: Any) -> None:
        self.replace_message_fn(model_class, parse_msg_desc_method="PGV")()

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
