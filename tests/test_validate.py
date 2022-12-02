import time
from typing import Any

from example.example_proto_python_code.example_proto.validate.demo_pb2 import (
    AnyTest,
    BoolTest,
    BytesTest,
    DoubleTest,
    DurationTest,
    EnumTest,
    Fixed32Test,
    Fixed64Test,
    FloatTest,
    Int32Test,
    Int64Test,
    MapTest,
    MessageDisabledTest,
    MessageIgnoredTest,
    MessageTest,
    NestedMessage,
    OneOfNotTest,
    OneOfTest,
    RepeatedTest,
    Sfixed32Test,
    Sfixed64Test,
    Sint64Test,
    StringTest,
    TimestampTest,
    Uint32Test,
    Uint64Test,
)
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code


def exp_time() -> float:
    return time.time()


class TestValidate:
    @staticmethod
    def _model_output(msg: Any) -> str:
        return pydantic_model_to_py_code(msg_to_pydantic_model(msg, parse_msg_desc_method="PGV"))

    def test_string(self) -> None:
        assert """
class StringTest(BaseModel):
    const_test: str = FieldInfo(default="aaa", const=True)
    len_test: str = FieldInfo(default="", extra={"len": 3})
    s_range_len_test: str = FieldInfo(default="", min_length=1, max_length=3)
    b_range_len_test: str = FieldInfo(default="")
    pattern_test: str = FieldInfo(default="", regex="^test")
    prefix_test: str = FieldInfo(default="", extra={"prefix": "prefix"})
    suffix_test: str = FieldInfo(default="", extra={"suffix": "suffix"})
    contains_test: str = FieldInfo(default="", extra={"contains": "contains"})
    not_contains_test: str = FieldInfo(default="",
                                       extra={"not_contains": "not_contains"})
    in_test: str = FieldInfo(default="", extra={"in": ["a", "b", "c"]})
    not_in_test: str = FieldInfo(default="", extra={"not_in": ["a", "b", "c"]})
    email_test: EmailStr = FieldInfo(default="")
    hostname_test: HostNameStr = FieldInfo(default="")
    ip_test: IPvAnyAddress = FieldInfo(default="")
    ipv4_test: IPv4Address = FieldInfo(default="")
    ipv6_test: IPv6Address = FieldInfo(default="")
    uri_test: AnyUrl = FieldInfo(default="")
    uri_ref_test: UriRefStr = FieldInfo(default="")
    address_test: IPvAnyAddress = FieldInfo(default="")
    uuid_test: UUID = FieldInfo(default="")
    ignore_test: str = FieldInfo(default="")

    len_validator_len_test = validator('len_test',
                                       allow_reuse=True)(len_validator)
    prefix_validator_prefix_test = validator(
        'prefix_test', allow_reuse=True)(prefix_validator)
    suffix_validator_suffix_test = validator(
        'suffix_test', allow_reuse=True)(suffix_validator)
    contains_validator_contains_test = validator(
        'contains_test', allow_reuse=True)(contains_validator)
    not_contains_validator_not_contains_test = validator(
        'not_contains_test', allow_reuse=True)(not_contains_validator)
    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(StringTest)

    def test_any(self) -> None:
        assert """
class AnyTest(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    required_test: Any = FieldInfo()
    not_in_test: Any = FieldInfo(
        default_factory=Any,
        extra={
            "any_not_in": [
                "type.googleapis.com/google.protobuf.Duration",
                "type.googleapis.com/google.protobuf.Timestamp"
            ]
        })
    in_test: Any = FieldInfo(
        default_factory=Any,
        extra={
            "any_in": [
                "type.googleapis.com/google.protobuf.Duration",
                "type.googleapis.com/google.protobuf.Timestamp"
            ]
        })

    any_not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(any_not_in_validator)
    any_in_validator_in_test = validator('in_test',
                                         allow_reuse=True)(any_in_validator)""" in self._model_output(AnyTest)

    def test_bool(self) -> None:
        assert """
class BoolTest(BaseModel):
    bool_1_test: bool = FieldInfo(default=True, const=True)
    bool_2_test: bool = FieldInfo(default=False, const=True)""" in self._model_output(BoolTest)

    def test_bytes(self) -> None:
        assert """
class BytesTest(BaseModel):
    const_test: bytes = FieldInfo(default=b"demo", const=True)
    len_test: bytes = FieldInfo(default=b"", extra={"len": 4})
    range_len_test: bytes = FieldInfo(default=b"", min_length=1, max_length=4)
    pattern_test: bytes = FieldInfo(default=b"")
    prefix_test: bytes = FieldInfo(default=b"", extra={"prefix": b"prefix"})
    suffix_test: bytes = FieldInfo(default=b"", extra={"suffix": b"suffix"})
    contains_test: bytes = FieldInfo(default=b"",
                                     extra={"contains": b"contains"})
    in_test: bytes = FieldInfo(default=b"", extra={"in": [b"a", b"b", b"c"]})
    not_in_test: bytes = FieldInfo(default=b"",
                                   extra={"not_in": [b"a", b"b", b"c"]})

    len_validator_len_test = validator('len_test',
                                       allow_reuse=True)(len_validator)
    prefix_validator_prefix_test = validator(
        'prefix_test', allow_reuse=True)(prefix_validator)
    suffix_validator_suffix_test = validator(
        'suffix_test', allow_reuse=True)(suffix_validator)
    contains_validator_contains_test = validator(
        'contains_test', allow_reuse=True)(contains_validator)
    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(BytesTest)

    def test_double(self) -> None:
        assert """
class DoubleTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0,
                                   extra={"not_in": [1.0, 2.0, 3.0]})
    ignore_test: float = FieldInfo(default=0.0)

    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(DoubleTest)

    def test_duration(self) -> None:
        assert """
class DurationTest(BaseModel):
    required_test: Timedelta = FieldInfo()
    const_test: Timedelta = FieldInfo(
        default_factory=Timedelta,
        extra={"duration_const": timedelta(seconds=1, microseconds=500000)})
    range_test: Timedelta = FieldInfo(default_factory=Timedelta,
                                      extra={
                                          "duration_gt":
                                          timedelta(seconds=5,
                                                    microseconds=500000),
                                          "duration_lt":
                                          timedelta(seconds=10,
                                                    microseconds=500000)
                                      })
    range_e_test: Timedelta = FieldInfo(default_factory=Timedelta,
                                        extra={
                                            "duration_ge":
                                            timedelta(seconds=5,
                                                      microseconds=500000),
                                            "duration_le":
                                            timedelta(seconds=10,
                                                      microseconds=500000)
                                        })
    in_test: Timedelta = FieldInfo(default_factory=Timedelta,
                                   extra={
                                       "duration_in": [
                                           timedelta(seconds=1,
                                                     microseconds=500000),
                                           timedelta(seconds=3,
                                                     microseconds=500000)
                                       ]
                                   })
    not_in_test: Timedelta = FieldInfo(default_factory=Timedelta,
                                       extra={
                                           "duration_not_in": [
                                               timedelta(seconds=1,
                                                         microseconds=500000),
                                               timedelta(seconds=3,
                                                         microseconds=500000)
                                           ]
                                       })

    duration_const_validator_const_test = validator(
        'const_test', allow_reuse=True)(duration_const_validator)
    duration_lt_validator_range_test = validator(
        'range_test', allow_reuse=True)(duration_lt_validator)
    duration_gt_validator_range_test = validator(
        'range_test', allow_reuse=True)(duration_gt_validator)
    duration_le_validator_range_e_test = validator(
        'range_e_test', allow_reuse=True)(duration_le_validator)
    duration_ge_validator_range_e_test = validator(
        'range_e_test', allow_reuse=True)(duration_ge_validator)
    duration_in_validator_in_test = validator(
        'in_test', allow_reuse=True)(duration_in_validator)
    duration_not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(duration_not_in_validator)""" in self._model_output(DurationTest)

    def test_enum(self) -> None:
        assert """
class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class EnumTest(BaseModel):
    const_test: State = FieldInfo(default=2, const=True)
    defined_only_test: State = FieldInfo(default=0)
    in_test: State = FieldInfo(default=0, extra={"in": [0, 2]})
    not_in_test: State = FieldInfo(default=0, extra={"not_in": [0, 2]})

    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(EnumTest)

    def test_fixed32(self) -> None:
        assert """
class Fixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0)

    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(Fixed32Test)

    def test_fixed64(self) -> None:
        assert """
class Fixed64Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0)

    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(Fixed64Test)

    def test_float(self) -> None:
        assert """
class FloatTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0,
                                   extra={"not_in": [1.0, 2.0, 3.0]})
    ignore_test: float = FieldInfo(default=0.0)

    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(FloatTest)

    def test_int32(self) -> None:
        assert """
class Int32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(Int32Test)

    def test_int64(self) -> None:
        assert """
class Int64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(Int64Test)

    def test_map(self) -> None:
        assert """
class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = FieldInfo(default_factory=dict,
                                                 extra={
                                                     "map_max_pairs": 5,
                                                     "map_min_pairs": 1
                                                 })
    no_parse_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    keys_test: typing.Dict[constr(min_length=1, max_length=5),
                           int] = FieldInfo(default_factory=dict)
    values_test: typing.Dict[str, conint(ge=5, le=5)] = FieldInfo(
        default_factory=dict)
    keys_values_test: typing.Dict[constr(min_length=1, max_length=5),
                                  contimestamp(
                                      timestamp_gt_now=True)] = FieldInfo(
                                          default_factory=dict)
    ignore_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)

    map_min_pairs_validator_pair_test = validator(
        'pair_test', allow_reuse=True)(map_min_pairs_validator)
    map_max_pairs_validator_pair_test = validator(
        'pair_test', allow_reuse=True)(map_max_pairs_validator)""" in self._model_output(MapTest)

    def test_message_disable(self) -> None:
        assert """
class MessageDisabledTest(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)""" in self._model_output(MessageDisabledTest)

    def test_message_ignored(self) -> None:
        assert """
class MessageIgnoredTest(BaseModel):
    const_test: int = FieldInfo(default=0)
    range_e_test: int = FieldInfo(default=0)
    range_test: int = FieldInfo(default=0)""" in self._model_output(MessageIgnoredTest)

    def test_message(self) -> None:
        assert """
class MessageTest(BaseModel):
    skip_test: str = FieldInfo(default="")
    required_test: str = FieldInfo()""" in self._model_output(MessageTest)

    def test_nested(self) -> None:
        assert """
class StringTest(BaseModel):
    const_test: str = FieldInfo(default="aaa", const=True)
    len_test: str = FieldInfo(default="", extra={"len": 3})
    s_range_len_test: str = FieldInfo(default="", min_length=1, max_length=3)
    b_range_len_test: str = FieldInfo(default="")
    pattern_test: str = FieldInfo(default="", regex="^test")
    prefix_test: str = FieldInfo(default="", extra={"prefix": "prefix"})
    suffix_test: str = FieldInfo(default="", extra={"suffix": "suffix"})
    contains_test: str = FieldInfo(default="", extra={"contains": "contains"})
    not_contains_test: str = FieldInfo(default="",
                                       extra={"not_contains": "not_contains"})
    in_test: str = FieldInfo(default="", extra={"in": ["a", "b", "c"]})
    not_in_test: str = FieldInfo(default="", extra={"not_in": ["a", "b", "c"]})
    email_test: EmailStr = FieldInfo(default="")
    hostname_test: HostNameStr = FieldInfo(default="")
    ip_test: IPvAnyAddress = FieldInfo(default="")
    ipv4_test: IPv4Address = FieldInfo(default="")
    ipv6_test: IPv6Address = FieldInfo(default="")
    uri_test: AnyUrl = FieldInfo(default="")
    uri_ref_test: UriRefStr = FieldInfo(default="")
    address_test: IPvAnyAddress = FieldInfo(default="")
    uuid_test: UUID = FieldInfo(default="")
    ignore_test: str = FieldInfo(default="")

    len_validator_len_test = validator('len_test',
                                       allow_reuse=True)(len_validator)
    prefix_validator_prefix_test = validator(
        'prefix_test', allow_reuse=True)(prefix_validator)
    suffix_validator_suffix_test = validator(
        'suffix_test', allow_reuse=True)(suffix_validator)
    contains_validator_contains_test = validator(
        'contains_test', allow_reuse=True)(contains_validator)
    not_contains_validator_not_contains_test = validator(
        'not_contains_test', allow_reuse=True)(not_contains_validator)
    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = FieldInfo(default_factory=dict,
                                                 extra={
                                                     "map_max_pairs": 5,
                                                     "map_min_pairs": 1
                                                 })
    no_parse_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)
    keys_test: typing.Dict[constr(min_length=1, max_length=5),
                           int] = FieldInfo(default_factory=dict)
    values_test: typing.Dict[str, conint(ge=5, le=5)] = FieldInfo(
        default_factory=dict)
    keys_values_test: typing.Dict[constr(min_length=1, max_length=5),
                                  contimestamp(
                                      timestamp_gt_now=True)] = FieldInfo(
                                          default_factory=dict)
    ignore_test: typing.Dict[str, int] = FieldInfo(default_factory=dict)

    map_min_pairs_validator_pair_test = validator(
        'pair_test', allow_reuse=True)(map_min_pairs_validator)
    map_max_pairs_validator_pair_test = validator(
        'pair_test', allow_reuse=True)(map_max_pairs_validator)


class NestedMessageUserPayMessage(BaseModel):
    bank_number: str = FieldInfo(default="", min_length=13, max_length=19)
    exp: datetime = FieldInfo(default_factory=datetime.now,
                              extra={"timestamp_gt_now": True})
    uuid: UUID = FieldInfo(default="")

    timestamp_gt_now_validator_exp = validator(
        'exp', allow_reuse=True)(timestamp_gt_now_validator)


class NestedMessageNotEnableUserPayMessage(BaseModel):
    bank_number: str = FieldInfo(default="")
    exp: datetime = FieldInfo(default_factory=datetime.now)
    uuid: str = FieldInfo(default="")


class NestedMessage(BaseModel):
    string_in_map_test: typing.Dict[str, StringTest] = FieldInfo(
        default_factory=dict)
    map_in_map_test: typing.Dict[str,
                                 MapTest] = FieldInfo(default_factory=dict)
    user_pay: NestedMessageUserPayMessage = FieldInfo()
    not_enable_user_pay: NestedMessageNotEnableUserPayMessage = FieldInfo()
    empty: None = FieldInfo()""" in self._model_output(NestedMessage)

    def test_one_of_not(self) -> None:
        assert """
class OneOfNotTest(BaseModel):
    _one_of_dict = {
        "validate_test.OneOfNotTest.id": {
            "fields": {"x", "y"},
            "required": False
        }
    }

    header: str = FieldInfo(default="")
    x: str = FieldInfo(default="")
    y: int = FieldInfo(default=0)

    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)""" in self._model_output(OneOfNotTest)

    def test_one_of(self) -> None:
        assert """
class OneOfTest(BaseModel):
    _one_of_dict = {
        "validate_test.OneOfTest.id": {
            "fields": {"x", "y"},
            "required": True
        }
    }

    header: str = FieldInfo(default="")
    x: str = FieldInfo(default="")
    y: int = FieldInfo(default=0)

    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)""" in self._model_output(OneOfTest)

    def test_repeated(self) -> None:
        assert """
class RepeatedTest(BaseModel):
    range_test: typing.List[str] = FieldInfo(default_factory=list,
                                             min_items=1,
                                             max_items=5)
    unique_test: typing.List[str] = FieldInfo(default_factory=list,
                                              unique_items=True)
    items_string_test: conlist(item_type=constr(min_length=1, max_length=5),
                               min_items=1,
                               max_items=5) = FieldInfo(default_factory=list)
    items_double_test: conlist(item_type=confloat(gt=1, lt=5),
                               min_items=1,
                               max_items=5) = FieldInfo(default_factory=list)
    items_int32_test: conlist(item_type=conint(gt=1, lt=5),
                              min_items=1,
                              max_items=5) = FieldInfo(default_factory=list)
    items_timestamp_test: conlist(
        item_type=contimestamp(timestamp_gt=1600000000.0,
                               timestamp_lt=1600000010.0),
        min_items=1,
        max_items=5) = FieldInfo(default_factory=list)
    items_duration_test: conlist(item_type=contimedelta(
        duration_gt=timedelta(seconds=10), duration_lt=timedelta(seconds=20)),
                                 min_items=1,
                                 max_items=5) = FieldInfo(default_factory=list)
    items_bytes_test: conlist(item_type=conbytes(min_length=1, max_length=5),
                              min_items=1,
                              max_items=5) = FieldInfo(default_factory=list)
    ignore_test: typing.List[str] = FieldInfo(default_factory=list)""" in self._model_output(RepeatedTest)

    def test_sfixed32(self) -> None:
        assert """
class Sfixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0)

    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(Sfixed32Test)

    def test_sfixed64(self) -> None:
        assert """
class Sfixed64Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    ignore_test: float = FieldInfo(default=0)

    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(Sfixed64Test)

    def test_sint64(self) -> None:
        assert """
class Sint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(Sint64Test)

    def test_timestamp(self) -> None:
        assert """
class TimestampTest(BaseModel):
    required_test: datetime = FieldInfo()
    const_test: datetime = FieldInfo(default_factory=datetime.now,
                                     extra={"timestamp_const": 1600000000.0})
    range_test: datetime = FieldInfo(default_factory=datetime.now,
                                     extra={
                                         "timestamp_gt": 1600000000.0,
                                         "timestamp_lt": 1600000010.0
                                     })
    range_e_test: datetime = FieldInfo(default_factory=datetime.now,
                                       extra={
                                           "timestamp_ge": 1600000000.0,
                                           "timestamp_le": 1600000010.0
                                       })
    lt_now_test: datetime = FieldInfo(default_factory=datetime.now,
                                      extra={"timestamp_lt_now": True})
    gt_now_test: datetime = FieldInfo(default_factory=datetime.now,
                                      extra={"timestamp_gt_now": True})
    within_test: datetime = FieldInfo(
        default_factory=datetime.now,
        extra={"timestamp_within": timedelta(seconds=1)})
    within_and_gt_now_test: datetime = FieldInfo(default_factory=datetime.now,
                                                 extra={
                                                     "timestamp_gt_now":
                                                     True,
                                                     "timestamp_within":
                                                     timedelta(seconds=3600)
                                                 })

    timestamp_const_validator_const_test = validator(
        'const_test', allow_reuse=True)(timestamp_const_validator)
    timestamp_lt_validator_range_test = validator(
        'range_test', allow_reuse=True)(timestamp_lt_validator)
    timestamp_gt_validator_range_test = validator(
        'range_test', allow_reuse=True)(timestamp_gt_validator)
    timestamp_le_validator_range_e_test = validator(
        'range_e_test', allow_reuse=True)(timestamp_le_validator)
    timestamp_ge_validator_range_e_test = validator(
        'range_e_test', allow_reuse=True)(timestamp_ge_validator)
    timestamp_lt_now_validator_lt_now_test = validator(
        'lt_now_test', allow_reuse=True)(timestamp_lt_now_validator)
    timestamp_gt_now_validator_gt_now_test = validator(
        'gt_now_test', allow_reuse=True)(timestamp_gt_now_validator)
    timestamp_within_validator_within_test = validator(
        'within_test', allow_reuse=True)(timestamp_within_validator)
    timestamp_gt_now_validator_within_and_gt_now_test = validator(
        'within_and_gt_now_test', allow_reuse=True)(timestamp_gt_now_validator)
    timestamp_within_validator_within_and_gt_now_test = validator(
        'within_and_gt_now_test', allow_reuse=True)(timestamp_within_validator)""" in self._model_output(TimestampTest)

    def test_unit32(self) -> None:
        assert """
class Uint32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(Uint32Test)

    def test_unit64(self) -> None:
        assert """
class Uint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    ignore_test: int = FieldInfo(default=0)

    in_validator_in_test = validator('in_test', allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator(
        'not_in_test', allow_reuse=True)(not_in_validator)""" in self._model_output(Uint64Test)
