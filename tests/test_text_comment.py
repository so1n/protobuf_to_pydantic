import time
from typing import Any
from uuid import uuid4

from example.python_example_proto_code.example_proto.demo import demo_pb2
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code


def exp_time() -> float:
    return time.time()


class BaseTestTextComment:
    @staticmethod
    def _model_output(msg: Any) -> str:
        local_dict = {"exp_time": exp_time, "uuid4": uuid4}
        return pydantic_model_to_py_code(
            msg_to_pydantic_model(
                msg,
                parse_msg_desc_method=demo_pb2,
                local_dict=local_dict
            )
        )

    def test_user_message(self) -> None:
        assert """
from enum import IntEnum

from pydantic import BaseModel
from pydantic.fields import FieldInfo


class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = FieldInfo(title="UID",
                         description="user union id",
                         extra={"example": "10086"})
    age: int = FieldInfo(default=0,
                         title="use age",
                         ge=0,
                         extra={"example": 18})
    height: float = FieldInfo(default=0.0, ge=0, le=2)
    sex: SexType = FieldInfo(default=0)
    is_adult: bool = FieldInfo(default=False)
    user_name: str = FieldInfo(default="",
                               description="user name",
                               min_length=1,
                               max_length=10,
                               extra={"example": "so1n"})""" in self._model_output(demo_pb2.UserMessage)

    def test_map_message(self) -> None:
            assert """
class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = FieldInfo(title="UID",
                         description="user union id",
                         extra={"example": "10086"})
    age: int = FieldInfo(default=0,
                         title="use age",
                         ge=0,
                         extra={"example": 18})
    height: float = FieldInfo(default=0.0, ge=0, le=2)
    sex: SexType = FieldInfo(default=0)
    is_adult: bool = FieldInfo(default=False)
    user_name: str = FieldInfo(default="",
                               description="user name",
                               min_length=1,
                               max_length=10,
                               extra={"example": "so1n"})


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
    uid: str = FieldInfo(title="UID",
                         description="user union id",
                         extra={"example": "10086"})
    age: int = FieldInfo(default=0,
                         title="use age",
                         ge=0,
                         extra={"example": 18})
    height: float = FieldInfo(default=0.0, ge=0, le=2)
    sex: SexType = FieldInfo(default=0)
    is_adult: bool = FieldInfo(default=False)
    user_name: str = FieldInfo(default="",
                               description="user name",
                               min_length=1,
                               max_length=10,
                               extra={"example": "so1n"})


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = FieldInfo(default_factory=list,
                                           min_items=3,
                                           max_items=5)
    int_list: typing.List[int] = FieldInfo(default_factory=list,
                                           min_items=1,
                                           max_items=5,
                                           unique_items=True)
    user_list: typing.List[UserMessage] = FieldInfo(default_factory=list)""" in self._model_output(
                demo_pb2.RepeatedMessage
            )

    def test_nested_message(self) -> None:
            assert """
class SexType(IntEnum):
    man = 0
    women = 1


class UserMessage(BaseModel):
    uid: str = FieldInfo(title="UID",
                         description="user union id",
                         extra={"example": "10086"})
    age: int = FieldInfo(default=0,
                         title="use age",
                         ge=0,
                         extra={"example": 18})
    height: float = FieldInfo(default=0.0, ge=0, le=2)
    sex: SexType = FieldInfo(default=0)
    is_adult: bool = FieldInfo(default=False)
    user_name: str = FieldInfo(default="",
                               description="user name",
                               min_length=1,
                               max_length=10,
                               extra={"example": "so1n"})


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = FieldInfo(default_factory=list,
                                           min_items=3,
                                           max_items=5)
    int_list: typing.List[int] = FieldInfo(default_factory=list,
                                           min_items=1,
                                           max_items=5,
                                           unique_items=True)
    user_list: typing.List[UserMessage] = FieldInfo(default_factory=list)


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = FieldInfo(default_factory=dict)
    user_flag: typing.Dict[str, bool] = FieldInfo(default_factory=dict)


class NestedMessageUserPayMessage(BaseModel):
    bank_number: PaymentCardNumber = FieldInfo(default="")
    exp: datetime = FieldInfo(default_factory=exp_time)
    uuid: str = FieldInfo(default_factory=uuid4)


class NestedMessage(BaseModel):
    user_list_map: typing.Dict[str, RepeatedMessage] = FieldInfo(
        default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = FieldInfo(default_factory=dict)
    user_pay: NestedMessageUserPayMessage = FieldInfo()
    empty: None = FieldInfo()""" in self._model_output(demo_pb2.NestedMessage)


class TestTextCommentByPyi(BaseTestTextComment):
    @staticmethod
    def _model_output(msg: Any) -> str:
        local_dict = {"exp_time": exp_time, "uuid4": uuid4}
        return pydantic_model_to_py_code(
            msg_to_pydantic_model(
                msg,
                parse_msg_desc_method=demo_pb2,
                local_dict=local_dict
            )
        )


class TestTextCommentByProtobufFProtobufField(BaseTestTextComment):
    @staticmethod
    def _model_output(msg: Any) -> str:
        local_dict = {"exp_time": exp_time, "uuid4": uuid4}
        from pathlib import Path
        if not Path("example").exists():
            # ignore exec in github action runner
            return pydantic_model_to_py_code(
                msg_to_pydantic_model(
                    msg,
                    parse_msg_desc_method=demo_pb2,
                    local_dict=local_dict
                )
            )
        return pydantic_model_to_py_code(
            msg_to_pydantic_model(
                msg,
                parse_msg_desc_method="example",
                local_dict=local_dict
            )
        )
