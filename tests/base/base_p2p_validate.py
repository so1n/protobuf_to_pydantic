from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any, Callable, Type
from uuid import uuid1, uuid4

import pytest
from pydantic import ValidationError

from example.gen_p2p_code import CustomCommentTemplate, CustomerField, confloat, conint, customer_any
from protobuf_to_pydantic._pydantic_adapter import is_v1
from protobuf_to_pydantic.grpc_types import AnyMessage

local_dict: dict = {
    "CustomerField": CustomerField,
    "confloat": confloat,
    "conint": conint,
    "customer_any": customer_any,
}


class BaseTestP2pModelValidator:
    number_model_class_list: list = []
    replace_message_fn: Callable = staticmethod(lambda model_class, **kwargs: model_class)  # type: ignore

    def _check_message_validate(self, message_class: Any, normal_dict: dict, error_map_dict: dict) -> None:
        self.replace_message_fn(message_class, local_dict=local_dict)(**normal_dict)
        for key, value in error_map_dict.items():
            error_normal_dict: dict = deepcopy(normal_dict)
            error_normal_dict[key] = value
            with pytest.raises(ValidationError):
                self.replace_message_fn(message_class, local_dict=local_dict)(**error_normal_dict)

    def test_number_model_in_validator(self) -> None:

        for model_class in self.number_model_class_list:
            for i in [1, 2, 3]:
                self.replace_message_fn(model_class, local_dict=local_dict, template=CustomCommentTemplate)(in_test=i, miss_default_test=1.0, required_test=1.0)
            for i in [0, 4]:
                with pytest.raises(ValidationError):
                    self.replace_message_fn(model_class, local_dict=local_dict, template=CustomCommentTemplate)(in_test=i, miss_default_test=1.0, required_test=1.0)

    def test_number_model_not_in_validator(self) -> None:
        for model_class in self.number_model_class_list:
            for i in [1, 2, 3]:
                with pytest.raises(ValidationError):
                    self.replace_message_fn(model_class, local_dict=local_dict, template=CustomCommentTemplate)(not_in_test=i, miss_default_test=1.0, required_test=1.0)
            for i in [0, 4]:
                self.replace_message_fn(model_class, local_dict=local_dict, template=CustomCommentTemplate)(not_in_test=i, miss_default_test=1.0, required_test=1.0)

    def test_number_model_miss_default_validator(self) -> None:
        for model_class in self.number_model_class_list:
            with pytest.raises(ValidationError):
                self.replace_message_fn(model_class, local_dict=local_dict, template=CustomCommentTemplate)()

    def test_number_model_miss_multiple_of_validator(self) -> None:
        for model_class in self.number_model_class_list:
            self.replace_message_fn(model_class, local_dict=local_dict, template=CustomCommentTemplate)(miss_default_test=1.0, multiple_of_test=6.0, required_test=1.0)
            with pytest.raises(ValidationError):
                self.replace_message_fn(model_class, local_dict=local_dict, template=CustomCommentTemplate)(miss_default_test=1.0, multiple_of_test=7.0, required_test=1.0)

    def _test_bool(self, model_class: Type) -> None:
        model_class(bool_1_test=True, bool_2_test=False, miss_default_test=True, required_test=True)
        with pytest.raises(ValidationError):
            model_class(bool_1_test=False, bool_2_test=False, miss_default_test=True, required_test=True)
            model_class(bool_1_test=True, bool_2_test=True, miss_default_test=True, required_test=True)

    def _test_string(self, model_class: Type) -> None:
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
            "uuid_test": str(uuid4()),
            "pydantic_type_test": str(uuid1()),
            "miss_default_test": "aa",
            "required_test": "aa",
        }
        model_class(**normal_dict)
        for column in [
            "len_test", "s_range_len_test", "pattern_test", "prefix_test", "suffix_test", "contains_test",
            "not_contains_test", "in_test", "not_in_test", "email_test", "hostname_test", "ip_test", "ipv4_test",
            "ipv6_test", "uri_test", "uri_ref_test", "address_test", "uuid_test", "pydantic_type_test"
        ]:
            error_normal_dict: dict = deepcopy(normal_dict)
            error_normal_dict[column] = "aaaa"
            error_normal_dict["not_contains_test"] = "not_contains"
            with pytest.raises(ValidationError):
                model_class(**error_normal_dict)

    def _test_bytes(self, model_class: Type) -> None:
        normal_dict: dict = {
            "const_test": b"demo",
            "range_len_test": b"aa",
            "pattern_test": b"testaa",
            "prefix_test": b"prefix_testaa",
            "suffix_test": b"aa_suffix",
            "contains_test": b"aaa_contains_test",
            "in_test": b"a",
            "not_in_test": b"d",
            "miss_default_test": b"d",
            "required_test": b"d",
        }

        model_class(**normal_dict)
        for column in [
            "range_len_test", "prefix_test", "suffix_test", "contains_test",
            "in_test", "not_in_test"
        ]:
            error_normal_dict: dict = deepcopy(normal_dict)
            error_normal_dict[column] = b"aaaaa"
            error_normal_dict["not_in_test"] = b"a"
            with pytest.raises(ValidationError):
                model_class(**error_normal_dict)

    def _test_enum(self, model_class: Type) -> None:
        normal_dict: dict = {
            "const_test": 2,
            "in_test": 0,
            "not_in_test": 1,
            "miss_default_test": 1,
            "required_test": 1,
        }
        error_map_dict: dict = {
            "const_test": 4,
            "in_test": 4,
            "not_in_test": 2,
        }
        self._check_message_validate(model_class, normal_dict, error_map_dict)

    def _test_map(self, model_class: Type) -> None:
        normal_dict: dict = {
            "pair_test": {"a": 1},
            "no_parse_test": {"a": 1},
            "keys_test": {"a": 1},
            "values_test": {"a": 5},
            "keys_values_test": {"a": datetime.now() + timedelta(days=1)},
            "miss_default_test": {"a": 1},
            "required_test": {"a": 1},
        }
        error_map_dict: dict = {
            "pair_test": {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6},
            "keys_test": {"aaaaaa": 1},
            "values_test": {"a": 1},
            "keys_values_test": {"a": datetime.now() - timedelta(days=1)},
        }
        self._check_message_validate(model_class, normal_dict, error_map_dict)

    def _test_repeated(self, model_class: Type) -> None:
        normal_dict: dict = {
            "range_test": ["a"],
            "unique_test": ["a", "b", "c"],
            "items_string_test": ["abc", "def"],
            "items_double_test": [1.2, 3.4],
            "items_int32_test": [2, 3],
            # In pydantic v2 support datetime gt, ge, lt and le validate
            # But when their parameter timestamp, the generated datetime is with the time zone
            # So Gt(16000000000) can only be compared with 1600000000,
            # GT(datetime.fromtimestamp(1600000000)) can only be compared with datetime.fromtimestamp(16000000000).
            "items_timestamp_test": [datetime.fromtimestamp(1600000001) if is_v1 else 1600000001],
            "items_duration_test": [timedelta(seconds=10)],
            "items_bytes_test": [b"a", b"b"],
            "miss_default_test": ["a", "b"],
            "required_test": ["a", "b"],
        }
        error_map_dict: dict = {
            "range_test": ["a", "b", "c", "d", "e", "f"],
            "items_string_test": ["abc", "def", "abcdef"],
            "items_double_test": [1.2, 3.4, "5.6"],
            "items_int32_test": [2, 3, 6],
            "items_timestamp_test": [datetime.fromtimestamp(1600000100)],
            "items_duration_test": [timedelta(seconds=25)],
            "items_bytes_test": [b"a", b"b", b"c", b"d", b"e", b"f"],
        }
        if is_v1:
            # In pydantic v2, unique_test will not raise error when the repeated field is not unique
            error_map_dict["unique_test"] = ["a", "b", "c", "c"]

        self._check_message_validate(model_class, normal_dict, error_map_dict)

    def _test_any(self, model_class: Type) -> None:
        normal_dict: dict = {
            "required_test": AnyMessage(),
            "not_in_test": AnyMessage(),
            "in_test": AnyMessage(type_url="type.googleapis.com/google.protobuf.Timestamp",),
            "miss_default_test": AnyMessage(type_url="type.googleapis.com/google.protobuf.Timestamp", ),
        }
        error_map_dict: dict = {
            "in_test": AnyMessage(),
            "not_in_test": AnyMessage(type_url="type.googleapis.com/google.protobuf.Timestamp"),
        }
        self._check_message_validate(model_class, normal_dict, error_map_dict)

    def _test_duration(self, model_class: Type) -> None:
        normal_dict: dict = {
            "required_test": timedelta(seconds=3600).total_seconds(),
            "const_test": timedelta(seconds=1, microseconds=500000),
            "range_test": timedelta(seconds=6),
            "range_e_test": timedelta(seconds=10, microseconds=500000),
            "in_test": timedelta(seconds=1, microseconds=500000),
            "not_in_test": timedelta(seconds=2, microseconds=500000),
            "miss_default_test": timedelta(seconds=2, microseconds=500000),
        }
        error_map_dict: dict = {
            "const_test": timedelta(seconds=2, microseconds=500000),
            "range_test": timedelta(seconds=4),
            "range_e_test": timedelta(seconds=10, microseconds=500001),
            "in_test": timedelta(microseconds=500000),
            "not_in_test": timedelta(seconds=1, microseconds=500000),
        }
        self._check_message_validate(model_class, normal_dict, error_map_dict)

    def _test_timestamp(self, model_class: Type) -> None:
        normal_dict: dict = {
            "required_test": datetime.now(),
            "const_test": datetime.fromtimestamp(1600000000),
            "range_test": datetime.fromtimestamp(1600000009),
            "range_e_test": datetime.fromtimestamp(1600000010),
            "lt_now_test": datetime.now() - timedelta(days=1),
            "gt_now_test": datetime.now() + timedelta(days=1),
            "within_test": datetime.now(),
            "within_and_gt_now_test": datetime.now() + timedelta(seconds=3590),
            "miss_default_test": datetime.now(),
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
                    "uuid_test": str(uuid4()),
                    "pydantic_type_test": str(uuid1()),
                    "miss_default_test": "aa",
                    "required_test": "aa",
                }
            },
            "map_in_map_test": {
                "a": {
                    "pair_test": {"a": 1},
                    "no_parse_test": {"a": 1},
                    "keys_test": {"a": 1},
                    "values_test": {"a": 5},
                    "keys_values_test": {"a": datetime.now() + timedelta(days=1)},
                    "miss_default_test": {"a": 1},
                    "required_test": {"a": 1},
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
            "empty": None,
            "after_refer": {
                "uid": "10086",
                "age": 18
            }
        }
        if is_v1:
            self.replace_message_fn(model_class, local_dict=local_dict).update_forward_refs(**normal_dict)
        else:
            model_class = self.replace_message_fn(model_class, local_dict=local_dict)
            model_class.model_rebuild()
            model_class(**normal_dict)

    def _test_one_of(self, model_class: Any) -> None:
        # test init
        self.replace_message_fn(model_class, local_dict=local_dict)(x="1")
        self.replace_message_fn(model_class, local_dict=local_dict)(y=2)
        with pytest.raises(ValidationError):
            self.replace_message_fn(model_class, local_dict=local_dict)(x="1", y=2)

        # test pgv
        with pytest.raises(ValidationError):
            self.replace_message_fn(model_class, local_dict=local_dict)()

    def _test_one_of_not(self, model_class: Any) -> None:
        self.replace_message_fn(model_class, local_dict=local_dict)()

    def _test_one_of_optional(self, model_class: Any) -> None:
        # check one of optional
        self.replace_message_fn(model_class, local_dict=local_dict)(x=None)
        self.replace_message_fn(model_class, local_dict=local_dict)(y=None)

        with pytest.raises(ValidationError):
            self.replace_message_fn(model_class, local_dict=local_dict)(z=None)

        # check other column optional
        self.replace_message_fn(model_class, local_dict=local_dict)(x=None, name=None, age=None)

    def _test_optional_message(self, model_class: Any) -> None:
        with pytest.raises(ValidationError):
            self.replace_message_fn(model_class, local_dict=local_dict)()

        with pytest.raises(ValidationError):
            self.replace_message_fn(model_class, local_dict=local_dict)(my_message1=None)

        if not is_v1:
            with pytest.raises(ValidationError):
                self.replace_message_fn(model_class, local_dict=local_dict)(
                    my_message3={"const_test": 1, "range_e_test": 2, "range_test": 2}
                )

        self.replace_message_fn(model_class, local_dict=local_dict)(
            my_message1=None, my_message3={"const_test": 1, "range_e_test": 2, "range_test": 2}
        )
