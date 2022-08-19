from typing import Any

from example.python_example_proto_code.example_proto.demo import demo_pb2
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code


class TestSimpleTest:
    @staticmethod
    def _model_output(msg: Any) -> str:
        return pydantic_model_to_py_code(msg_to_pydantic_model(msg, parse_msg_desc_method="ignore"))

    def test_user_message(self) -> None:
        assert """
from enum import IntEnum

from pydantic import BaseModel
from pydantic.fields import FieldInfo


class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = FieldInfo(default="")
    age: int = FieldInfo(default=0)
    height: float = FieldInfo(default=0.0)
    sex: SexType = FieldInfo(default=0)
    is_adult: bool = FieldInfo(default=False)
    user_name: str = FieldInfo(default="")""" in self._model_output(demo_pb2.UserMessage)

    def test_map_message(self) -> None:
        assert """
import typing
from enum import IntEnum

from pydantic import BaseModel
from pydantic.fields import FieldInfo


class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = FieldInfo(default="")
    age: int = FieldInfo(default=0)
    height: float = FieldInfo(default=0.0)
    sex: SexType = FieldInfo(default=0)
    is_adult: bool = FieldInfo(default=False)
    user_name: str = FieldInfo(default="")


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = FieldInfo(default_factory=dict)
    user_flag: typing.Dict[str, bool] = FieldInfo(default_factory=dict)""" in self._model_output(demo_pb2.MapMessage)

    def test_repeated_message(self) -> None:
        assert """
import typing
from enum import IntEnum

from pydantic import BaseModel
from pydantic.fields import FieldInfo


class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = FieldInfo(default="")
    age: int = FieldInfo(default=0)
    height: float = FieldInfo(default=0.0)
    sex: SexType = FieldInfo(default=0)
    is_adult: bool = FieldInfo(default=False)
    user_name: str = FieldInfo(default="")


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = FieldInfo(default_factory=list)
    int_list: typing.List[int] = FieldInfo(default_factory=list)
    user_list: typing.List[UserMessage] = FieldInfo(default_factory=list)""" in self._model_output(
            demo_pb2.RepeatedMessage
        )

    def test_nested_message(self) -> None:
        assert """
class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = FieldInfo(default="")
    age: int = FieldInfo(default=0)
    height: float = FieldInfo(default=0.0)
    sex: SexType = FieldInfo(default=0)
    is_adult: bool = FieldInfo(default=False)
    user_name: str = FieldInfo(default="")


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = FieldInfo(default_factory=list)
    int_list: typing.List[int] = FieldInfo(default_factory=list)
    user_list: typing.List[UserMessage] = FieldInfo(default_factory=list)


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = FieldInfo(default_factory=dict)
    user_flag: typing.Dict[str, bool] = FieldInfo(default_factory=dict)


class NestedMessageUserPayMessage(BaseModel):
    bank_number: str = FieldInfo(default="")
    exp: datetime = FieldInfo(default_factory=datetime.now)
    uuid: str = FieldInfo(default="")


class NestedMessage(BaseModel):
    user_list_map: typing.Dict[str, RepeatedMessage] = FieldInfo(
        default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = FieldInfo(default_factory=dict)
    user_pay: NestedMessageUserPayMessage = FieldInfo()
    not_enable_user_pay: NestedMessageUserPayMessage = FieldInfo()
    empty: None = FieldInfo()""" in self._model_output(demo_pb2.NestedMessage)
