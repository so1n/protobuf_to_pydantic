import time
from typing import Any

from google.protobuf import __version__

if __version__ > "4.0.0":
    from example.proto.example.example_proto.p2p_validate import demo_pb2
else:
    from example.proto_3_20.example.example_proto.p2p_validate import demo_pb2  # type: ignore[no-redef]

from example.gen_p2p_code import CustomerField, confloat, conint, customer_any
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code
from protobuf_to_pydantic.util import format_content


def exp_time() -> float:
    return time.time()


class TestP2pValidate:
    @staticmethod
    def _model_output(msg: Any) -> str:
        local_dict: dict = {
            "CustomerField": CustomerField,
            "confloat": confloat,
            "conint": conint,
            "customer_any": customer_any,
        }
        return pydantic_model_to_py_code(msg_to_pydantic_model(msg, local_dict=local_dict))

    def test_any(self) -> None:
        assert format_content("""
class AnyTest(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    required_test: Any = Field()
    not_in_test: Any = Field(
        default_factory=Any,
        any_not_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )
    in_test: Any = Field(
        default_factory=Any,
        any_in=[
            "type.googleapis.com/google.protobuf.Timestamp",
            Any(type_url="type.googleapis.com/google.protobuf.Duration"),
        ],
    )
    default_test: Any = Field(default=Any(type_url="type.googleapis.com/google.protobuf.Duration"))
    default_factory_test: Any = Field(default_factory=customer_any)
    miss_default_test: Any = Field()
    alias_test: Any = Field(default_factory=Any, alias="alias", alias_priority=2)
    desc_test: Any = Field(default_factory=Any, description="test desc")
    example_test: Any = Field(default_factory=Any, example="type.googleapis.com/google.protobuf.Duration")
    example_factory_test: Any = Field(default_factory=Any, example=customer_any)
    field_test: Any = CustomerField(default_factory=Any)
    title_test: Any = Field(default_factory=Any, title="title_test")
    extra_test: Any = Field(default_factory=Any, customer_string="c1", customer_int=1)

    any_not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(any_not_in_validator)
    any_in_validator_in_test = validator("in_test", allow_reuse=True)(any_in_validator)
""") in self._model_output(demo_pb2.AnyTest)

    def test_bool(self) -> None:
        assert format_content("""
class BoolTest(BaseModel):
    bool_1_test: bool = Field(default=True, const=True)
    bool_2_test: bool = Field(default=False, const=True)
    default_test: bool = Field(default=True)
    miss_default_test: bool = Field()
    alias_test: bool = Field(default=False, alias="alias", alias_priority=2)
    desc_test: bool = Field(default=False, description="test desc")
    example_test: bool = Field(default=False, example=True)
    field_test: bool = CustomerField(default=False)
    title_test: bool = Field(default=False, title="title_test")
    extra_test: bool = Field(default=False, customer_string="c1", customer_int=1)
""") in self._model_output(demo_pb2.BoolTest)

    def test_bytes(self) -> None:
        assert format_content("""
class BytesTest(BaseModel):
    const_test: bytes = Field(default=b"demo", const=True)
    range_len_test: bytes = Field(default=b"", min_length=1, max_length=4)
    prefix_test: bytes = Field(default=b"", prefix=b"prefix")
    suffix_test: bytes = Field(default=b"", suffix=b"suffix")
    contains_test: bytes = Field(default=b"", contains=b"contains")
    in_test: bytes = Field(default=b"", in_=[b"a", b"b", b"c"])
    not_in_test: bytes = Field(default=b"", not_in=[b"a", b"b", b"c"])
    default_test: bytes = Field(default=b"default")
    default_factory_test: bytes = Field(default_factory=bytes)
    miss_default_test: bytes = Field()
    alias_test: bytes = Field(default=b"", alias="alias", alias_priority=2)
    desc_test: bytes = Field(default=b"", description="test desc")
    example_test: bytes = Field(default=b"", example=b"example")
    example_factory_test: bytes = Field(default=b"", example=bytes)
    field_test: bytes = CustomerField(default=b"")
    title_test: bytes = Field(default=b"", title="title_test")
    type_test: constr() = Field(default=b"")
    extra_test: bytes = Field(default=b"", customer_string="c1", customer_int=1)

    prefix_validator_prefix_test = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_validator_suffix_test = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_validator_contains_test = validator("contains_test", allow_reuse=True)(contains_validator)
    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.BytesTest)

    def test_double(self) -> None:
        assert format_content("""
class DoubleTest(BaseModel):
    const_test: float = Field(default=1.0, const=True)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    default_test: float = Field(default=1.0)
    default_factory_test: float = Field(default_factory=float)
    miss_default_test: float = Field()
    alias_test: float = Field(default=0.0, alias="alias", alias_priority=2)
    desc_test: float = Field(default=0.0, description="test desc")
    multiple_of_test: float = Field(default=0.0, multiple_of=3)
    example_test: float = Field(default=0.0, example=1.0)
    example_factory: float = Field(default=0.0, example=float)
    field_test: float = CustomerField(default=0.0)
    type_test: confloat() = Field(default=0.0)
    title_test: float = Field(default=0.0, title="title_test")
    extra_test: float = Field(default=0.0, customer_string="c1", customer_int=1)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.DoubleTest)

    def test_duration(self) -> None:
        assert format_content("""
class DurationTest(BaseModel):
    const_test: Timedelta = Field(
        default_factory=Timedelta, duration_const=timedelta(seconds=1, microseconds=500000)
    )
    range_test: Timedelta = Field(
        default_factory=Timedelta,
        duration_lt=timedelta(seconds=10, microseconds=500000),
        duration_gt=timedelta(seconds=5, microseconds=500000),
    )
    range_e_test: Timedelta = Field(
        default_factory=Timedelta,
        duration_le=timedelta(seconds=10, microseconds=500000),
        duration_ge=timedelta(seconds=5, microseconds=500000),
    )
    in_test: Timedelta = Field(
        default_factory=Timedelta,
        duration_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    not_in_test: Timedelta = Field(
        default_factory=Timedelta,
        duration_not_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    default_test: Timedelta = Field(default=timedelta(seconds=1, microseconds=500000))
    default_factory_test: Timedelta = Field(default_factory=timedelta)
    miss_default_test: Timedelta = Field()
    alias_test: Timedelta = Field(default_factory=Timedelta, alias="alias", alias_priority=2)
    desc_test: Timedelta = Field(default_factory=Timedelta, description="test desc")
    example_test: Timedelta = Field(default_factory=Timedelta, example=timedelta(seconds=1, microseconds=500000))
    example_factory_test: Timedelta = Field(default_factory=Timedelta, example=timedelta)
    field_test: Timedelta = CustomerField(default_factory=Timedelta)
    title_test: Timedelta = Field(default_factory=Timedelta, title="title_test")
    type_test: timedelta = Field(default_factory=Timedelta)
    extra_test: Timedelta  = Field(default_factory=Timedelta, customer_string="c1", customer_int=1)

    duration_const_validator_const_test = validator("const_test", allow_reuse=True)(duration_const_validator)
    duration_lt_validator_range_test = validator("range_test", allow_reuse=True)(duration_lt_validator)
    duration_gt_validator_range_test = validator("range_test", allow_reuse=True)(duration_gt_validator)
    duration_le_validator_range_e_test = validator("range_e_test", allow_reuse=True)(duration_le_validator)
    duration_ge_validator_range_e_test = validator("range_e_test", allow_reuse=True)(duration_ge_validator)
    duration_in_validator_in_test = validator("in_test", allow_reuse=True)(duration_in_validator)
    duration_not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(duration_not_in_validator)
""") in self._model_output(demo_pb2.DurationTest)

    def test_enum(self) -> None:
        assert format_content("""
class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class EnumTest(BaseModel):
    const_test: State = Field(default=2, const=True)
    in_test: State = Field(default=0, in_=[0, 2])
    not_in_test: State = Field(default=0, not_in=[0, 2])
    default_test: State = Field(default=1)
    miss_default_test: State = Field()
    alias_test: State = Field(default=0, alias="alias", alias_priority=2)
    desc_test: State = Field(default=0, description="test desc")
    example_test: State = Field(default=0, example=2)
    field_test: State = CustomerField(default=0)
    title_test: State = Field(default=0, title="title_test")
    extra_test: State  = Field(default=0, customer_string="c1", customer_int=1)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.EnumTest)

    def test_fixed32(self) -> None:
        assert format_content("""
class Fixed32Test(BaseModel):
    const_test: float = Field(default=1, const=True)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    default_test: float = Field(default=1.0)
    default_factory_test: float = Field(default_factory=float)
    miss_default_test: float = Field()
    alias_test: float = Field(default=0, alias="alias", alias_priority=2)
    desc_test: float = Field(default=0, description="test desc")
    multiple_of_test: float = Field(default=0, multiple_of=3)
    example_test: float = Field(default=0, example=1.0)
    example_factory: float = Field(default=0, example=float)
    field_test: float = CustomerField(default=0)
    type_test: confloat() = Field(default=0)
    title_test: float = Field(default=0, title="title_test")
    extra_test: float = Field(default=0, customer_string="c1", customer_int=1)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.Fixed32Test)

    def test_fixed64(self) -> None:
        assert format_content("""
class Fixed64Test(BaseModel):
    const_test: float = Field(default=0)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    default_test: float = Field(default=1.0)
    default_factory_test: float = Field(default_factory=float)
    miss_default_test: float = Field()
    alias_test: float = Field(default=0, alias="alias", alias_priority=2)
    desc_test: float = Field(default=0, description="test desc")
    multiple_of_test: float = Field(default=0, multiple_of=3)
    example_test: float = Field(default=0, example=1.0)
    example_factory: float = Field(default=0, example=float)
    field_test: float = CustomerField(default=0)
    type_test: confloat() = Field(default=0)
    title_test: float = Field(default=0, title="title_test")
    extra_test: float = Field(default=0, customer_string="c1", customer_int=1)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.Fixed64Test)

    def test_float(self) -> None:
        assert format_content("""
class FloatTest(BaseModel):
    const_test: float = Field(default=1.0, const=True)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    default_test: float = Field(default=1.0)
    default_factory_test: float = Field(default_factory=float)
    miss_default_test: float = Field()
    alias_test: float = Field(default=0.0, alias="alias", alias_priority=2)
    desc_test: float = Field(default=0.0, description="test desc")
    multiple_of_test: float = Field(default=0.0, multiple_of=3)
    example_test: float = Field(default=0.0, example=1.0)
    example_factory: float = Field(default=0.0, example=float)
    field_test: float = CustomerField(default=0.0)
    type_test: confloat() = Field(default=0.0)
    title_test: float = Field(default=0.0, title="title_test")
    extra_test: float = Field(default=0.0, customer_string="c1", customer_int=1)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.FloatTest)

    def test_int32(self) -> None:
        assert format_content("""
class Int32Test(BaseModel):
    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_factory_test: int = Field(default_factory=int)
    miss_default_test: int = Field()
    alias_test: int = Field(default=0, alias="alias", alias_priority=2)
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: confloat() = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.Int32Test)

    def test_int64(self) -> None:
        assert format_content("""
class Int64Test(BaseModel):
    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_factory_test: int = Field(default_factory=int)
    miss_default_test: int = Field()
    alias_test: int = Field(default=0, alias="alias", alias_priority=2)
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: confloat() = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.Int64Test)

    def test_map(self) -> None:
        assert format_content("""
class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = Field(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    keys_test: typing.Dict[constr(min_length=1, max_length=5), int] = Field(default_factory=dict)
    values_test: typing.Dict[str, conint(ge=5, le=5)] = Field(default_factory=dict)
    keys_values_test: typing.Dict[constr(min_length=1, max_length=5), contimestamp(timestamp_gt_now=True)] = Field(
        default_factory=dict
    )
    default_factory_test: typing.Dict[str, int] = Field(default_factory=dict)
    miss_default_test: typing.Dict[str, int] = Field()
    alias_test: typing.Dict[str, int] = Field(default_factory=dict, alias="alias", alias_priority=2)
    desc_test: typing.Dict[str, int] = Field(default_factory=dict, description="test desc")
    example_factory_test: typing.Dict[str, int] = Field(default_factory=dict, example=dict)
    field_test: typing.Dict[str, int] = CustomerField(default_factory=dict)
    title_test: typing.Dict[str, int] = Field(default_factory=dict, title="title_test")
    type_test: dict = Field(default_factory=dict)
    extra_test: typing.Dict[str, int] = Field(default_factory=dict, customer_string="c1", customer_int=1)

    map_min_pairs_validator_pair_test = validator("pair_test", allow_reuse=True)(map_min_pairs_validator)
    map_max_pairs_validator_pair_test = validator("pair_test", allow_reuse=True)(map_max_pairs_validator)
""") in self._model_output(demo_pb2.MapTest)

    def test_message_ignored(self) -> None:
        assert format_content("""
class MessageIgnoredTest(BaseModel):
    const_test: int = Field(default=0)
    range_e_test: int = Field(default=0)
    range_test: int = Field(default=0)
""") in self._model_output(demo_pb2.MessageIgnoredTest)

    def test_message(self) -> None:
        assert format_content("""
class MessageTest(BaseModel):
    skip_test: str = Field(default="")
    required_test: str = Field()
    extra_test: str = Field(default="")
""") in self._model_output(demo_pb2.MessageTest)

    def test_nested(self) -> None:
        assert format_content("""
class StringTest(BaseModel):
    const_test: str = Field(default="aaa", const=True)
    len_test: str = Field(default="", len=3)
    s_range_len_test: str = Field(default="", min_length=1, max_length=3)
    pattern_test: str = Field(default="", regex="^test")
    prefix_test: str = Field(default="", prefix="prefix")
    suffix_test: str = Field(default="", suffix="suffix")
    contains_test: str = Field(default="", contains="contains")
    not_contains_test: str = Field(default="", not_contains="not_contains")
    in_test: str = Field(default="", in_=["a", "b", "c"])
    not_in_test: str = Field(default="", not_in=["a", "b", "c"])
    email_test: EmailStr = Field(default="")
    hostname_test: HostNameStr = Field(default="")
    ip_test: IPvAnyAddress = Field(default="")
    ipv4_test: IPv4Address = Field(default="")
    ipv6_test: IPv6Address = Field(default="")
    uri_test: AnyUrl = Field(default="")
    uri_ref_test: UriRefStr = Field(default="")
    address_test: IPvAnyAddress = Field(default="")
    uuid_test: UUID = Field(default="")
    pydantic_type_test: str = Field(default="")
    default_test: str = Field(default="default")
    default_factory_test: str = Field(default_factory=uuid4)
    miss_default_test: str = Field()
    alias_test: str = Field(default="", alias="alias", alias_priority=2)
    desc_test: str = Field(default="", description="test desc")
    example_test: str = Field(default="", example="example")
    example_factory_test: str = Field(default="", example=uuid4)
    field_test: str = CustomerField(default="")
    title_test: str = Field(default="", title="title_test")
    type_test: constr() = Field(default="")
    extra_test: str = Field(default="", customer_string="c1", customer_int=1)

    len_validator_len_test = validator("len_test", allow_reuse=True)(len_validator)
    prefix_validator_prefix_test = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_validator_suffix_test = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_validator_contains_test = validator("contains_test", allow_reuse=True)(contains_validator)
    not_contains_validator_not_contains_test = validator("not_contains_test", allow_reuse=True)(not_contains_validator)
    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = Field(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    keys_test: typing.Dict[constr(min_length=1, max_length=5), int] = Field(default_factory=dict)
    values_test: typing.Dict[str, conint(ge=5, le=5)] = Field(default_factory=dict)
    keys_values_test: typing.Dict[constr(min_length=1, max_length=5), contimestamp(timestamp_gt_now=True)] = Field(
        default_factory=dict
    )
    default_factory_test: typing.Dict[str, int] = Field(default_factory=dict)
    miss_default_test: typing.Dict[str, int] = Field()
    alias_test: typing.Dict[str, int] = Field(default_factory=dict, alias="alias", alias_priority=2)
    desc_test: typing.Dict[str, int] = Field(default_factory=dict, description="test desc")
    example_factory_test: typing.Dict[str, int] = Field(default_factory=dict, example=dict)
    field_test: typing.Dict[str, int] = CustomerField(default_factory=dict)
    title_test: typing.Dict[str, int] = Field(default_factory=dict, title="title_test")
    type_test: dict = Field(default_factory=dict)
    extra_test: typing.Dict[str, int] = Field(default_factory=dict, customer_string="c1", customer_int=1)

    map_min_pairs_validator_pair_test = validator("pair_test", allow_reuse=True)(map_min_pairs_validator)
    map_max_pairs_validator_pair_test = validator("pair_test", allow_reuse=True)(map_max_pairs_validator)


class AfterReferMessage(BaseModel):
    uid: str = Field(title="UID", description="user union id",
example="10086")
    age: int = Field(default=0, title="use age", ge=0, example=18.0)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: str = Field(default="", min_length=13, max_length=19)
        exp: datetime = Field(default_factory=datetime.now, timestamp_gt_now=True)
        uuid: UUID = Field(default="")

        timestamp_gt_now_validator_exp = validator("exp", allow_reuse=True)(timestamp_gt_now_validator)

    class NotEnableUserPayMessage(BaseModel):
        bank_number: str = Field(default="")
        exp: datetime = Field(default_factory=datetime.now)
        uuid: str = Field(default="")

    string_in_map_test: typing.Dict[str, StringTest] = Field(default_factory=dict)
    map_in_map_test: typing.Dict[str, MapTest] = Field(default_factory=dict)
    user_pay: UserPayMessage = Field()
    not_enable_user_pay: NotEnableUserPayMessage = Field()
    empty: typing.Any = Field()
    after_refer: AfterReferMessage = Field()
""") in self._model_output(demo_pb2.NestedMessage)

    def test_one_of_not(self) -> None:
        assert format_content("""
class OneOfNotTest(BaseModel):
    _one_of_dict = {"p2p_validate_test.OneOfNotTest.id": {"fields": {"x", "y"}, "required": False}}

    header: str = Field(default="")
    x: str = Field(default="")
    y: int = Field(default=0)

    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)
""") in self._model_output(demo_pb2.OneOfNotTest)

    def test_one_of(self) -> None:
        assert format_content("""
class OneOfTest(BaseModel):
    _one_of_dict = {"p2p_validate_test.OneOfTest.id": {"fields": {"x", "y"}, "required": True}}

    header: str = Field(default="")
    x: str = Field(default="")
    y: int = Field(default=0)

    _check_one_of = root_validator(pre=True, allow_reuse=True)(check_one_of)
""") in self._model_output(demo_pb2.OneOfTest)

    def test_repeated(self) -> None:
        assert format_content("""
class RepeatedTest(BaseModel):
    range_test: typing.List[str] = Field(default_factory=list, min_items=1, max_items=5)
    unique_test: typing.List[str] = Field(default_factory=list, unique_items=True)
    items_string_test: conlist(item_type=constr(min_length=1, max_length=5), min_items=1, max_items=5) = Field(
        default_factory=list
    )
    items_double_test: conlist(item_type=confloat(gt=1, lt=5), min_items=1, max_items=5) = Field(
        default_factory=list
    )
    items_int32_test: conlist(item_type=conint(gt=1, lt=5), min_items=1, max_items=5) = Field(default_factory=list)
    items_timestamp_test: conlist(
        item_type=contimestamp(timestamp_gt=1600000000.0, timestamp_lt=1600000010.0), min_items=1, max_items=5
    ) = Field(default_factory=list)
    items_duration_test: conlist(
        item_type=contimedelta(duration_ge=timedelta(seconds=10), duration_le=timedelta(seconds=10)),
        min_items=1,
        max_items=5,
    ) = Field(default_factory=list)
    items_bytes_test: conlist(item_type=conbytes(min_length=1, max_length=5), min_items=1, max_items=5) = Field(
        default_factory=list
    )
    default_factory_test: typing.List[str] = Field(default_factory=list)
    miss_default_test: typing.List[str] = Field()
    alias_test: typing.List[str] = Field(default_factory=list, alias="alias", alias_priority=2)
    desc_test: typing.List[str] = Field(default_factory=list, description="test desc")
    example_factory_test: typing.List[str] = Field(default_factory=list, example=list)
    field_test: typing.List[str] = CustomerField(default_factory=list)
    title_test: typing.List[str] = Field(default_factory=list, title="title_test")
    type_test: list = Field(default_factory=list)
    extra_test: typing.List[str] = Field(default_factory=list, customer_string="c1", customer_int=1)
""") in self._model_output(demo_pb2.RepeatedTest)

    def test_sfixed32(self) -> None:
        assert format_content("""
class Sfixed32Test(BaseModel):
    const_test: float = Field(default=0)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    default_test: float = Field(default=1.0)
    default_factory_test: float = Field(default_factory=float)
    miss_default_test: float = Field()
    alias_test: float = Field(default=0, alias="alias", alias_priority=2)
    desc_test: float = Field(default=0, description="test desc")
    multiple_of_test: float = Field(default=0, multiple_of=3)
    example_test: float = Field(default=0, example=1.0)
    example_factory: float = Field(default=0, example=float)
    field_test: float = CustomerField(default=0)
    type_test: confloat() = Field(default=0)
    title_test: float = Field(default=0, title="title_test")
    extra_test: float = Field(default=0, customer_string="c1", customer_int=1)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.Sfixed32Test)

    def test_sfixed64(self) -> None:
        assert format_content("""
class Sfixed64Test(BaseModel):
    const_test: float = Field(default=0)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    default_test: float = Field(default=1.0)
    default_factory_test: float = Field(default_factory=float)
    miss_default_test: float = Field()
    alias_test: float = Field(default=0, alias="alias", alias_priority=2)
    desc_test: float = Field(default=0, description="test desc")
    multiple_of_test: float = Field(default=0, multiple_of=3)
    example_test: float = Field(default=0, example=1.0)
    example_factory: float = Field(default=0, example=float)
    field_test: float = CustomerField(default=0)
    type_test: confloat() = Field(default=0)
    title_test: float = Field(default=0, title="title_test")
    extra_test: float = Field(default=0, customer_string="c1", customer_int=1)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.Sfixed64Test)

    def test_sint64(self) -> None:
        assert format_content("""
class Sint64Test(BaseModel):
    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_factory_test: int = Field(default_factory=int)
    miss_default_test: int = Field()
    alias_test: int = Field(default=0, alias="alias", alias_priority=2)
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: conint() = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.Sint64Test)

    def test_string(self) -> None:
        assert format_content("""
class StringTest(BaseModel):
    const_test: str = Field(default="aaa", const=True)
    len_test: str = Field(default="", len=3)
    s_range_len_test: str = Field(default="", min_length=1, max_length=3)
    pattern_test: str = Field(default="", regex="^test")
    prefix_test: str = Field(default="", prefix="prefix")
    suffix_test: str = Field(default="", suffix="suffix")
    contains_test: str = Field(default="", contains="contains")
    not_contains_test: str = Field(default="", not_contains="not_contains")
    in_test: str = Field(default="", in_=["a", "b", "c"])
    not_in_test: str = Field(default="", not_in=["a", "b", "c"])
    email_test: EmailStr = Field(default="")
    hostname_test: HostNameStr = Field(default="")
    ip_test: IPvAnyAddress = Field(default="")
    ipv4_test: IPv4Address = Field(default="")
    ipv6_test: IPv6Address = Field(default="")
    uri_test: AnyUrl = Field(default="")
    uri_ref_test: UriRefStr = Field(default="")
    address_test: IPvAnyAddress = Field(default="")
    uuid_test: UUID = Field(default="")
    pydantic_type_test: str = Field(default="")
    default_test: str = Field(default="default")
    default_factory_test: str = Field(default_factory=uuid4)
    miss_default_test: str = Field()
    alias_test: str = Field(default="", alias="alias", alias_priority=2)
    desc_test: str = Field(default="", description="test desc")
    example_test: str = Field(default="", example="example")
    example_factory_test: str = Field(default="", example=uuid4)
    field_test: str = CustomerField(default="")
    title_test: str = Field(default="", title="title_test")
    type_test: constr() = Field(default="")
    extra_test: str = Field(default="", customer_string="c1", customer_int=1)

    len_validator_len_test = validator("len_test", allow_reuse=True)(len_validator)
    prefix_validator_prefix_test = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_validator_suffix_test = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_validator_contains_test = validator("contains_test", allow_reuse=True)(contains_validator)
    not_contains_validator_not_contains_test = validator("not_contains_test", allow_reuse=True)(not_contains_validator)
    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.StringTest)

    def test_timestamp(self) -> None:
        assert format_content("""
class TimestampTest(BaseModel):
    const_test: datetime = Field(default_factory=datetime.now, timestamp_const=1600000000.0)
    range_test: datetime = Field(default_factory=datetime.now, timestamp_lt=1600000010.0, timestamp_gt=1600000000.0)
    range_e_test: datetime = Field(
        default_factory=datetime.now, timestamp_le=1600000010.0, timestamp_ge=1600000000.0
    )
    lt_now_test: datetime = Field(default_factory=datetime.now, timestamp_lt_now=True)
    gt_now_test: datetime = Field(default_factory=datetime.now, timestamp_gt_now=True)
    within_test: datetime = Field(default_factory=datetime.now, timestamp_within=timedelta(seconds=1))
    within_and_gt_now_test: datetime = Field(
        default_factory=datetime.now, timestamp_gt_now=True, timestamp_within=timedelta(seconds=3600)
    )
    default_test: datetime = Field(default=1.5)
    default_factory_test: datetime = Field(default_factory=datetime.now)
    miss_default_test: datetime = Field()
    alias_test: datetime = Field(default_factory=datetime.now, alias="alias", alias_priority=2)
    desc_test: datetime = Field(default_factory=datetime.now, description="test desc")
    example_test: datetime = Field(default_factory=datetime.now, example=1.5)
    example_factory_test: datetime = Field(default_factory=datetime.now, example=datetime.now)
    field_test: datetime = CustomerField(default_factory=datetime.now)
    title_test: datetime = Field(default_factory=datetime.now, title="title_test")
    type_test: datetime = Field(default_factory=datetime.now)
    extra_test: datetime  = Field(default_factory=datetime.now, customer_string="c1", customer_int=1)

    timestamp_const_validator_const_test = validator("const_test", allow_reuse=True)(timestamp_const_validator)
    timestamp_lt_validator_range_test = validator("range_test", allow_reuse=True)(timestamp_lt_validator)
    timestamp_gt_validator_range_test = validator("range_test", allow_reuse=True)(timestamp_gt_validator)
    timestamp_le_validator_range_e_test = validator("range_e_test", allow_reuse=True)(timestamp_le_validator)
    timestamp_ge_validator_range_e_test = validator("range_e_test", allow_reuse=True)(timestamp_ge_validator)
    timestamp_lt_now_validator_lt_now_test = validator("lt_now_test", allow_reuse=True)(timestamp_lt_now_validator)
    timestamp_gt_now_validator_gt_now_test = validator("gt_now_test", allow_reuse=True)(timestamp_gt_now_validator)
    timestamp_within_validator_within_test = validator("within_test", allow_reuse=True)(timestamp_within_validator)
    timestamp_gt_now_validator_within_and_gt_now_test = validator("within_and_gt_now_test", allow_reuse=True)(
        timestamp_gt_now_validator
    )
    timestamp_within_validator_within_and_gt_now_test = validator("within_and_gt_now_test", allow_reuse=True)(
        timestamp_within_validator
    )
""") in self._model_output(demo_pb2.TimestampTest)

    def test_unit32(self) -> None:
        assert format_content("""
class Uint32Test(BaseModel):
    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_factory_test: int = Field(default_factory=int)
    miss_default_test: int = Field()
    alias_test: int = Field(default=0, alias="alias", alias_priority=2)
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: conint() = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.Uint32Test)

    def test_unit64(self) -> None:
        assert format_content("""
class Uint64Test(BaseModel):
    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_factory_test: int = Field(default_factory=int)
    miss_default_test: int = Field()
    alias_test: int = Field(default=0, alias="alias", alias_priority=2)
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: conint() = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
""") in self._model_output(demo_pb2.Uint64Test)
