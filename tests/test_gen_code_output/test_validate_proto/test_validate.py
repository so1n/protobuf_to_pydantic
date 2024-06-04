import sys
import time
from typing import Any

from google.protobuf import __version__

from protobuf_to_pydantic._pydantic_adapter import is_v1

if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1.example.example_proto.validate import demo_pb2
    else:
        from example.proto_pydanticv2.example.example_proto.validate import demo_pb2  # type: ignore[no-redef]
else:
    if is_v1:
        from example.proto_3_20_pydanticv1.example.example_proto.validate import demo_pb2  # type: ignore[no-redef]
    else:
        from example.proto_3_20_pydanticv2.example.example_proto.validate import demo_pb2  # type: ignore[no-redef]

from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code
from protobuf_to_pydantic.util import format_content


def exp_time() -> float:
    return time.time()


class TestValidate:
    @staticmethod
    def _model_output(msg: Any) -> str:
        return pydantic_model_to_py_code(msg_to_pydantic_model(msg, parse_msg_desc_method="PGV"))

    @staticmethod
    def assert_contains(content: str, other_content: str) -> None:
        content = format_content(content)
        if sys.version_info >= (3, 10):
            content = content.replace("typing_extensions.Literal", "typing.Literal")
        assert content in other_content

    def test_string(self) -> None:
        content = """
class StringTest(BaseModel):
    const_test: str = Field(default="aaa", const=True)
    len_test: str = Field(default="", len=3)
    s_range_len_test: str = Field(default="", min_length=1, max_length=3)
    b_range_len_test: str = Field(default="")
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
    ignore_test: str = Field(default="")

    len_test_len_validator = validator("len_test", allow_reuse=True)(len_validator)
    prefix_test_prefix_validator = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_test_suffix_validator = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_test_contains_validator = validator("contains_test", allow_reuse=True)(contains_validator)
    not_contains_test_not_contains_validator = validator("not_contains_test", allow_reuse=True)(not_contains_validator)
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class StringTest(BaseModel):
    const_test: typing_extensions.Literal["aaa"] = Field(default="")
    len_test: str = Field(default="", len=3)
    s_range_len_test: str = Field(default="", min_length=1, max_length=3)
    b_range_len_test: str = Field(default="")
    pattern_test: str = Field(default="")
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
    uri_test: Url = Field(default="")
    uri_ref_test: UriRefStr = Field(default="")
    address_test: IPvAnyAddress = Field(default="")
    uuid_test: UUID = Field(default="")
    ignore_test: str = Field(default="")

    len_test_len_validator = field_validator("len_test", mode="after", check_fields=None)(len_validator)
    prefix_test_prefix_validator = field_validator("prefix_test", mode="after", check_fields=None)(prefix_validator)
    suffix_test_suffix_validator = field_validator("suffix_test", mode="after", check_fields=None)(suffix_validator)
    contains_test_contains_validator = field_validator("contains_test", mode="after", check_fields=None)(
        contains_validator
    )
    not_contains_test_not_contains_validator = field_validator("not_contains_test", mode="after", check_fields=None)(
        not_contains_validator
    )
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.StringTest))

    def test_any(self) -> None:
        content = """
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
        any_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )

    not_in_test_any_not_in_validator = validator("not_in_test", allow_reuse=True)(any_not_in_validator)
    in_test_any_in_validator = validator("in_test", allow_reuse=True)(any_in_validator)
"""
        if not is_v1:
            content = """
class AnyTest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    required_test: Any = Field()
    not_in_test: Any = Field(
        default_factory=Any,
        any_not_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )
    in_test: Any = Field(
        default_factory=Any,
        any_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )

    not_in_test_any_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(
        any_not_in_validator
    )
    in_test_any_in_validator = field_validator("in_test", mode="after", check_fields=None)(any_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.AnyTest))

    def test_bool(self) -> None:
        content = """
class BoolTest(BaseModel):
    bool_1_test: bool = Field(default=True, const=True)
    bool_2_test: bool = Field(default=False, const=True)
"""
        if not is_v1:
            content = """
class BoolTest(BaseModel):
    bool_1_test: typing_extensions.Literal[True] = Field(default=False)
    bool_2_test: typing_extensions.Literal[False] = Field(default=False)
"""
        self.assert_contains(content, self._model_output(demo_pb2.BoolTest))

    def test_bytes(self) -> None:
        content = """
class BytesTest(BaseModel):
    const_test: bytes = Field(default=b"demo", const=True)
    len_test: bytes = Field(default=b"", len=4)
    range_len_test: bytes = Field(default=b"", min_length=1, max_length=4)
    pattern_test: bytes = Field(default=b"")
    prefix_test: bytes = Field(default=b"", prefix=b"prefix")
    suffix_test: bytes = Field(default=b"", suffix=b"suffix")
    contains_test: bytes = Field(default=b"", contains=b"contains")
    in_test: bytes = Field(default=b"", in_=[b"a", b"b", b"c"])
    not_in_test: bytes = Field(default=b"", not_in=[b"a", b"b", b"c"])

    len_test_len_validator = validator("len_test", allow_reuse=True)(len_validator)
    prefix_test_prefix_validator = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_test_suffix_validator = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_test_contains_validator = validator("contains_test", allow_reuse=True)(contains_validator)
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class BytesTest(BaseModel):
    const_test: typing_extensions.Literal[b"demo"] = Field(default=b"")
    len_test: bytes = Field(default=b"", len=4)
    range_len_test: bytes = Field(default=b"", min_length=1, max_length=4)
    pattern_test: bytes = Field(default=b"")
    prefix_test: bytes = Field(default=b"", prefix=b"prefix")
    suffix_test: bytes = Field(default=b"", suffix=b"suffix")
    contains_test: bytes = Field(default=b"", contains=b"contains")
    in_test: bytes = Field(default=b"", in_=[b"a", b"b", b"c"])
    not_in_test: bytes = Field(default=b"", not_in=[b"a", b"b", b"c"])

    len_test_len_validator = field_validator("len_test", mode="after", check_fields=None)(len_validator)
    prefix_test_prefix_validator = field_validator("prefix_test", mode="after", check_fields=None)(prefix_validator)
    suffix_test_suffix_validator = field_validator("suffix_test", mode="after", check_fields=None)(suffix_validator)
    contains_test_contains_validator = field_validator("contains_test", mode="after", check_fields=None)(
        contains_validator
    )
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.BytesTest))

    def test_double(self) -> None:
        content = """
class DoubleTest(BaseModel):
    const_test: float = Field(default=1.0, const=True)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    ignore_test: float = Field(default=0.0)

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class DoubleTest(BaseModel):
    const_test: typing_extensions.Literal[1.0] = Field(default=0.0)
    range_e_test: float = Field(default=0.0, ge=1.0, le=10.0)
    range_test: float = Field(default=0.0, gt=1.0, lt=10.0)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    ignore_test: float = Field(default=0.0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.DoubleTest))

    def test_duration(self) -> None:
        content = """
class DurationTest(BaseModel):
    required_test: Timedelta = Field()
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

    const_test_duration_const_validator = validator("const_test", allow_reuse=True)(duration_const_validator)
    range_test_duration_lt_validator = validator("range_test", allow_reuse=True)(duration_lt_validator)
    range_test_duration_gt_validator = validator("range_test", allow_reuse=True)(duration_gt_validator)
    range_e_test_duration_le_validator = validator("range_e_test", allow_reuse=True)(duration_le_validator)
    range_e_test_duration_ge_validator = validator("range_e_test", allow_reuse=True)(duration_ge_validator)
    in_test_duration_in_validator = validator("in_test", allow_reuse=True)(duration_in_validator)
    not_in_test_duration_not_in_validator = validator("not_in_test", allow_reuse=True)(duration_not_in_validator)
"""
        if not is_v1:
            content = """
class DurationTest(BaseModel):
    required_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field()
    const_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta, duration_const=timedelta(seconds=1, microseconds=500000)
    )
    range_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta,
        duration_lt=timedelta(seconds=10, microseconds=500000),
        duration_gt=timedelta(seconds=5, microseconds=500000),
    )
    range_e_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta,
        duration_le=timedelta(seconds=10, microseconds=500000),
        duration_ge=timedelta(seconds=5, microseconds=500000),
    )
    in_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta,
        duration_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    not_in_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta,
        duration_not_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )

    const_test_duration_const_validator = field_validator("const_test", mode="after", check_fields=None)(
        duration_const_validator
    )
    range_test_duration_lt_validator = field_validator("range_test", mode="after", check_fields=None)(
        duration_lt_validator
    )
    range_test_duration_gt_validator = field_validator("range_test", mode="after", check_fields=None)(
        duration_gt_validator
    )
    range_e_test_duration_le_validator = field_validator("range_e_test", mode="after", check_fields=None)(
        duration_le_validator
    )
    range_e_test_duration_ge_validator = field_validator("range_e_test", mode="after", check_fields=None)(
        duration_ge_validator
    )
    in_test_duration_in_validator = field_validator("in_test", mode="after", check_fields=None)(duration_in_validator)
    not_in_test_duration_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(
        duration_not_in_validator
    )
"""
        self.assert_contains(content, self._model_output(demo_pb2.DurationTest))

    def test_enum(self) -> None:
        content = """
class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class EnumTest(BaseModel):
    const_test: State = Field(default=2, const=True)
    defined_only_test: State = Field(default=0)
    in_test: State = Field(default=0, in_=[0, 2])
    not_in_test: State = Field(default=0, not_in=[0, 2])

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class EnumTest(BaseModel):
    const_test: typing_extensions.Literal[2] = Field(default=0)
    defined_only_test: State = Field(default=0)
    in_test: State = Field(default=0, in_=[0, 2])
    not_in_test: State = Field(default=0, not_in=[0, 2])

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.EnumTest))
    def test_fixed32(self) -> None:
        content = """
class Fixed32Test(BaseModel):
    const_test: float = Field(default=1, const=True)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0)

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class Fixed32Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.Fixed32Test))

    def test_fixed64(self) -> None:
        content = """
class Fixed64Test(BaseModel):
    const_test: float = Field(default=1, const=True)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0)

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class Fixed64Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.Fixed64Test))

    def test_float(self) -> None:
        content = """
class FloatTest(BaseModel):
    const_test: float = Field(default=1.0, const=True)
    range_e_test: float = Field(default=0.0, ge=1, le=10)
    range_test: float = Field(default=0.0, gt=1, lt=10)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    ignore_test: float = Field(default=0.0)

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class FloatTest(BaseModel):
    const_test: typing_extensions.Literal[1.0] = Field(default=0.0)
    range_e_test: float = Field(default=0.0, ge=1.0, le=10.0)
    range_test: float = Field(default=0.0, gt=1.0, lt=10.0)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    ignore_test: float = Field(default=0.0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.FloatTest))

    def test_int32(self) -> None:
        content = """
class Int32Test(BaseModel):
    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class Int32Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.Int32Test))

    def test_int64(self) -> None:
        content = """
class Int64Test(BaseModel):
    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class Int64Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.Int64Test))

    def test_map(self) -> None:
        content = """
class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = Field(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    no_parse_test: typing.Dict[str, int] = Field(default_factory=dict)
    keys_test: typing.Dict[constr(min_length=1, max_length=5), int] = Field(default_factory=dict)
    values_test: typing.Dict[str, conint(ge=5, le=5)] = Field(default_factory=dict)
    keys_values_test: typing.Dict[constr(min_length=1, max_length=5), contimestamp(timestamp_gt_now=True)] = Field(
        default_factory=dict
    )
    ignore_test: typing.Dict[str, int] = Field(default_factory=dict)

    pair_test_map_min_pairs_validator = validator("pair_test", allow_reuse=True)(map_min_pairs_validator)
    pair_test_map_max_pairs_validator = validator("pair_test", allow_reuse=True)(map_max_pairs_validator)
"""
        if not is_v1:
            content = """
class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = Field(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    no_parse_test: typing.Dict[str, int] = Field(default_factory=dict)
    keys_test: typing.Dict[typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)], int] = Field(
        default_factory=dict
    )
    values_test: typing.Dict[str, typing_extensions.Annotated[int, Ge(ge=5), Le(le=5)]] = Field(default_factory=dict)
    keys_values_test: typing.Dict[
        typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)],
        typing_extensions.Annotated[DatetimeType, gt_now(True)],
    ] = Field(default_factory=dict)
    ignore_test: typing.Dict[str, int] = Field(default_factory=dict)

    pair_test_map_min_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_min_pairs_validator
    )
    pair_test_map_max_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_max_pairs_validator
    )
"""
        self.assert_contains(content, self._model_output(demo_pb2.MapTest))

    def test_message_disable(self) -> None:
        assert format_content("""
class MessageDisabledTest(BaseModel):
    const_test: int = Field(default=0)
    range_e_test: int = Field(default=0)
    range_test: int = Field(default=0)""") in self._model_output(demo_pb2.MessageDisabledTest)

    def test_message_ignored(self) -> None:
        assert format_content("""
class MessageIgnoredTest(BaseModel):
    const_test: int = Field(default=0)
    range_e_test: int = Field(default=0)
    range_test: int = Field(default=0)""") in self._model_output(demo_pb2.MessageIgnoredTest)

    def test_message(self) -> None:
        assert format_content("""
class MessageTest(BaseModel):
    skip_test: str = Field(default="")
    required_test: str = Field()""") in self._model_output(demo_pb2.MessageTest)

    def test_nested(self) -> None:
        content = """
class StringTest(BaseModel):
    const_test: str = Field(default="aaa", const=True)
    len_test: str = Field(default="", len=3)
    s_range_len_test: str = Field(default="", min_length=1, max_length=3)
    b_range_len_test: str = Field(default="")
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
    ignore_test: str = Field(default="")

    len_test_len_validator = validator("len_test", allow_reuse=True)(len_validator)
    prefix_test_prefix_validator = validator("prefix_test", allow_reuse=True)(prefix_validator)
    suffix_test_suffix_validator = validator("suffix_test", allow_reuse=True)(suffix_validator)
    contains_test_contains_validator = validator("contains_test", allow_reuse=True)(contains_validator)
    not_contains_test_not_contains_validator = validator("not_contains_test", allow_reuse=True)(not_contains_validator)
    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = Field(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    no_parse_test: typing.Dict[str, int] = Field(default_factory=dict)
    keys_test: typing.Dict[constr(min_length=1, max_length=5), int] = Field(default_factory=dict)
    values_test: typing.Dict[str, conint(ge=5, le=5)] = Field(default_factory=dict)
    keys_values_test: typing.Dict[constr(min_length=1, max_length=5), contimestamp(timestamp_gt_now=True)] = Field(
        default_factory=dict
    )
    ignore_test: typing.Dict[str, int] = Field(default_factory=dict)

    pair_test_map_min_pairs_validator = validator("pair_test", allow_reuse=True)(map_min_pairs_validator)
    pair_test_map_max_pairs_validator = validator("pair_test", allow_reuse=True)(map_max_pairs_validator)


class AfterReferMessage(BaseModel):
    uid: str = Field(default="", min_length=1)
    age: int = Field(default=0, ge=0, lt=500)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: str = Field(default="", min_length=13, max_length=19)
        exp: datetime = Field(default_factory=datetime.now, timestamp_gt_now=True)
        uuid: UUID = Field(default="")

        exp_timestamp_gt_now_validator = validator("exp", allow_reuse=True)(timestamp_gt_now_validator)

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
"""
        if not is_v1:
            content = """
class StringTest(BaseModel):
    const_test: typing_extensions.Literal["aaa"] = Field(default="")
    len_test: str = Field(default="", len=3)
    s_range_len_test: str = Field(default="", min_length=1, max_length=3)
    b_range_len_test: str = Field(default="")
    pattern_test: str = Field(default="")
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
    uri_test: Url = Field(default="")
    uri_ref_test: UriRefStr = Field(default="")
    address_test: IPvAnyAddress = Field(default="")
    uuid_test: UUID = Field(default="")
    ignore_test: str = Field(default="")

    len_test_len_validator = field_validator("len_test", mode="after", check_fields=None)(len_validator)
    prefix_test_prefix_validator = field_validator("prefix_test", mode="after", check_fields=None)(prefix_validator)
    suffix_test_suffix_validator = field_validator("suffix_test", mode="after", check_fields=None)(suffix_validator)
    contains_test_contains_validator = field_validator("contains_test", mode="after", check_fields=None)(
        contains_validator
    )
    not_contains_test_not_contains_validator = field_validator("not_contains_test", mode="after", check_fields=None)(
        not_contains_validator
    )
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = Field(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    no_parse_test: typing.Dict[str, int] = Field(default_factory=dict)
    keys_test: typing.Dict[typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)], int] = Field(
        default_factory=dict
    )
    values_test: typing.Dict[str, typing_extensions.Annotated[int, Ge(ge=5), Le(le=5)]] = Field(default_factory=dict)
    keys_values_test: typing.Dict[
        typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)],
        typing_extensions.Annotated[DatetimeType, gt_now(True)],
    ] = Field(default_factory=dict)
    ignore_test: typing.Dict[str, int] = Field(default_factory=dict)

    pair_test_map_min_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_min_pairs_validator
    )
    pair_test_map_max_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_max_pairs_validator
    )


class AfterReferMessage(BaseModel):
    uid: str = Field(default="", min_length=1)
    age: int = Field(default=0, ge=0, lt=500)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: str = Field(default="", min_length=13, max_length=19)
        exp: datetime = Field(default_factory=datetime.now, timestamp_gt_now=True)
        uuid: UUID = Field(default="")

        exp_timestamp_gt_now_validator = field_validator("exp", mode="after", check_fields=None)(
            timestamp_gt_now_validator
        )

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
"""
        self.assert_contains(content, self._model_output(demo_pb2.NestedMessage))



    def test_one_of_not(self) -> None:
        content = """
class OneOfNotTest(BaseModel):
    _one_of_dict = {"validate_test.OneOfNotTest.id": {"fields": {"x", "y"}, "required": False}}

    header: str = Field(default="")
    x: str = Field(default="")
    y: int = Field(default=0)

    one_of_validator = root_validator(pre=True, allow_reuse=True)(check_one_of)
"""
        if not is_v1:
            content = """
class OneOfNotTest(BaseModel):
    _one_of_dict = {"validate_test.OneOfNotTest.id": {"fields": {"x", "y"}, "required": False}}

    header: str = Field(default="")
    x: str = Field(default="")
    y: int = Field(default=0)

    one_of_validator = model_validator(mode="before")(check_one_of)
"""
        self.assert_contains(content, self._model_output(demo_pb2.OneOfNotTest))

    def test_one_of(self) -> None:
        content = """
class OneOfTest(BaseModel):
    _one_of_dict = {"validate_test.OneOfTest.id": {"fields": {"x", "y"}, "required": True}}

    header: str = Field(default="")
    x: str = Field(default="")
    y: int = Field(default=0)

    one_of_validator = root_validator(pre=True, allow_reuse=True)(check_one_of)
"""
        if not is_v1:
            content = """
class OneOfTest(BaseModel):
    _one_of_dict = {"validate_test.OneOfTest.id": {"fields": {"x", "y"}, "required": True}}

    header: str = Field(default="")
    x: str = Field(default="")
    y: int = Field(default=0)

    one_of_validator = model_validator(mode="before")(check_one_of)
"""
        self.assert_contains(content, self._model_output(demo_pb2.OneOfTest))

    def test_repeated(self) -> None:
        content = """
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
        item_type=contimedelta(duration_gt=timedelta(seconds=10), duration_lt=timedelta(seconds=20)),
        min_items=1,
        max_items=5,
    ) = Field(default_factory=list)
    items_bytes_test: conlist(item_type=conbytes(min_length=1, max_length=5), min_items=1, max_items=5) = Field(
        default_factory=list
    )
    ignore_test: typing.List[str] = Field(default_factory=list)
"""
        if not is_v1:
            content = """
class RepeatedTest(BaseModel):
    range_test: typing.List[str] = Field(default_factory=list, min_length=1, max_length=5)
    unique_test: typing.Set[str] = Field(default_factory=set)
    items_string_test: typing.List[
        typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)]
    ] = Field(default_factory=list, min_length=1, max_length=5)
    items_double_test: typing.List[typing_extensions.Annotated[float, Gt(gt=1.0), Lt(lt=5.0)]] = Field(
        default_factory=list, min_length=1, max_length=5
    )
    items_int32_test: typing.List[typing_extensions.Annotated[int, Gt(gt=1), Lt(lt=5)]] = Field(
        default_factory=list, min_length=1, max_length=5
    )
    items_timestamp_test: typing.List[
        typing_extensions.Annotated[DatetimeType, t_gt(1600000000.0), t_lt(1600000010.0)]
    ] = Field(default_factory=list, min_length=1, max_length=5)
    items_duration_test: typing.List[
        typing_extensions.Annotated[TimedeltaType, Gt(gt=timedelta(seconds=10)), Lt(lt=timedelta(seconds=20))]
    ] = Field(default_factory=list, min_length=1, max_length=5)
    items_bytes_test: typing.List[
        typing_extensions.Annotated[bytes, MinLen(min_length=1), MaxLen(max_length=5)]
    ] = Field(default_factory=list, min_length=1, max_length=5)
    ignore_test: typing.List[str] = Field(default_factory=list)
"""
        self.assert_contains(content, self._model_output(demo_pb2.RepeatedTest))

    def test_sfixed32(self) -> None:
        content = """
class Sfixed32Test(BaseModel):
    const_test: float = Field(default=1, const=True)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0)

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class Sfixed32Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.Sfixed32Test))

    def test_sfixed64(self) -> None:
        content = """
class Sfixed64Test(BaseModel):
    const_test: float = Field(default=1, const=True)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0)

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class Sfixed64Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    ignore_test: float = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.Sfixed64Test))

    def test_sint64(self) -> None:
        content = """
class Sint64Test(BaseModel):
    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class Sint64Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.Sint64Test))

    def test_timestamp(self) -> None:
        content = """
class TimestampTest(BaseModel):
    required_test: datetime = Field()
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

    const_test_timestamp_const_validator = validator("const_test", allow_reuse=True)(timestamp_const_validator)
    range_test_timestamp_lt_validator = validator("range_test", allow_reuse=True)(timestamp_lt_validator)
    range_test_timestamp_gt_validator = validator("range_test", allow_reuse=True)(timestamp_gt_validator)
    range_e_test_timestamp_le_validator = validator("range_e_test", allow_reuse=True)(timestamp_le_validator)
    range_e_test_timestamp_ge_validator = validator("range_e_test", allow_reuse=True)(timestamp_ge_validator)
    lt_now_test_timestamp_lt_now_validator = validator("lt_now_test", allow_reuse=True)(timestamp_lt_now_validator)
    gt_now_test_timestamp_gt_now_validator = validator("gt_now_test", allow_reuse=True)(timestamp_gt_now_validator)
    within_test_timestamp_within_validator = validator("within_test", allow_reuse=True)(timestamp_within_validator)
    within_and_gt_now_test_timestamp_gt_now_validator = validator("within_and_gt_now_test", allow_reuse=True)(
        timestamp_gt_now_validator
    )
    within_and_gt_now_test_timestamp_within_validator = validator("within_and_gt_now_test", allow_reuse=True)(
        timestamp_within_validator
    )
"""
        if not is_v1:
            content = """
class TimestampTest(BaseModel):
    required_test: datetime = Field()
    const_test: datetime = Field(default_factory=datetime.now, timestamp_const=1600000000.0)
    range_test: datetime = Field(default_factory=datetime.now, timestamp_lt=1600000010.0, timestamp_gt=1600000000.0)
    range_e_test: datetime = Field(default_factory=datetime.now, timestamp_le=1600000010.0, timestamp_ge=1600000000.0)
    lt_now_test: datetime = Field(default_factory=datetime.now, timestamp_lt_now=True)
    gt_now_test: datetime = Field(default_factory=datetime.now, timestamp_gt_now=True)
    within_test: datetime = Field(default_factory=datetime.now, timestamp_within=timedelta(seconds=1))
    within_and_gt_now_test: datetime = Field(
        default_factory=datetime.now, timestamp_gt_now=True, timestamp_within=timedelta(seconds=3600)
    )

    const_test_timestamp_const_validator = field_validator("const_test", mode="after", check_fields=None)(
        timestamp_const_validator
    )
    range_test_timestamp_lt_validator = field_validator("range_test", mode="after", check_fields=None)(
        timestamp_lt_validator
    )
    range_test_timestamp_gt_validator = field_validator("range_test", mode="after", check_fields=None)(
        timestamp_gt_validator
    )
    range_e_test_timestamp_le_validator = field_validator("range_e_test", mode="after", check_fields=None)(
        timestamp_le_validator
    )
    range_e_test_timestamp_ge_validator = field_validator("range_e_test", mode="after", check_fields=None)(
        timestamp_ge_validator
    )
    lt_now_test_timestamp_lt_now_validator = field_validator("lt_now_test", mode="after", check_fields=None)(
        timestamp_lt_now_validator
    )
    gt_now_test_timestamp_gt_now_validator = field_validator("gt_now_test", mode="after", check_fields=None)(
        timestamp_gt_now_validator
    )
    within_test_timestamp_within_validator = field_validator("within_test", mode="after", check_fields=None)(
        timestamp_within_validator
    )
    within_and_gt_now_test_timestamp_gt_now_validator = field_validator(
        "within_and_gt_now_test", mode="after", check_fields=None
    )(timestamp_gt_now_validator)
    within_and_gt_now_test_timestamp_within_validator = field_validator(
        "within_and_gt_now_test", mode="after", check_fields=None
    )(timestamp_within_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.TimestampTest))
    def test_unit32(self) -> None:
        content = """
class Uint32Test(BaseModel):
    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class Uint32Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.Uint32Test))

    def test_unit64(self) -> None:
        content = """
class Uint64Test(BaseModel):
    const_test: int = Field(default=1, const=True)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = validator("in_test", allow_reuse=True)(in_validator)
    not_in_test_not_in_validator = validator("not_in_test", allow_reuse=True)(not_in_validator)
"""
        if not is_v1:
            content = """
class Uint64Test(BaseModel):
    const_test: typing_extensions.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    ignore_test: int = Field(default=0)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
"""
        self.assert_contains(content, self._model_output(demo_pb2.Uint64Test))
