from typing import Callable, Type

import pytest
from pydantic import ValidationError

from protobuf_to_pydantic import _pydantic_adapter


class BaseTestAliasDemoValidator:
    replace_message_fn: Callable = staticmethod(lambda x:x)  # type: ignore[assignment]

    def _test_alias_demo(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        if not _pydantic_adapter.is_v1:
            model_class(
                **{
                "sourceId": "123",
                "data": {
                    "locationValue": {
                        "latitude": 10.01,
                        "longitude": -10.01,
                        "altitudeMeters":10.01
                    }
                }
            })
        model_class(
            **{
                "source_id": "123",
                "data": {
                    "location_value": {
                        "latitude": 10.01,
                        "longitude": -10.01,
                        "altitudeMeters": 10.01
                    }
                }
            })
        model_class(
            **{
                "source_id": "123",
                "data": {"time_value": "2000-01-01 10:00:00"}
            })

class BaseTestAllFieldSetOptionalDemoValidator:
    replace_message_fn: Callable = staticmethod(lambda x:x)  # type: ignore[assignment]

    def _test_user_message(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class(uid=None, user_name="so1n")

    def _test_other_message(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class()

    def _test_map_message(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class()

    def _test_repeated_message(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class()

    def _test_after_refer_message(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class(uid=None)

    def _test_nested_message(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class(**{"after_refer": {"uid": None}})

    def _test_invoice_item(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class()

    def _test_empty_message(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class()

    def _test_optional_message(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class(x="1")
        model_class(y=1)

    def _test_invoice_item2(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class()

    def _test_root_message(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class()


class BaseTestDemoValidator:
    pass

class BaseTestSingleConfigValidator:
    replace_message_fn: Callable = staticmethod(lambda x:x)  # type: ignore[assignment]

    def _test_user_message(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class(**{"uid": "10086", "age": 1, "height": 1, "user_name": "aaa"})

        with pytest.raises(ValidationError):
            model_class(**{"uid": "10086", "age": -1, "height": 1, "user_name": "aaa"})

        with pytest.raises(ValidationError):
            model_class(**{"uid": "10086", "age": 1, "height": 3, "user_name": "aaa"})

        with pytest.raises(ValidationError):
            model_class(**{"uid": "10086", "age": 1, "height": 1, "user_name": ""})


class BaseTestCustomCommentHandler:
    replace_message_fn: Callable = staticmethod(lambda x:x)  # type: ignore[assignment]

    def _test_user_message(self, model_class: Type) -> None:
        model_class = self.replace_message_fn(model_class)
        model_class(**{"uid": "10086", "age": 1, "height": 1, "user_name": "aaa"})

        with pytest.raises(ValidationError):
            model_class(**{"uid": "10086", "age": -1, "height": 1, "user_name": "aaa"})

        with pytest.raises(ValidationError):
            model_class(**{"uid": "10086", "age": 1, "height": 3, "user_name": "aaa"})

        with pytest.raises(ValidationError):
            model_class(**{"uid": "10086", "age": 1, "height": 1, "user_name": ""})

        assert model_class.schema()["properties"]["height"]["description"] == "user_height"
