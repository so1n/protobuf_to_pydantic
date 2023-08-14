from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Sequence, Type, Union

from pydantic import (
    ConstrainedBytes,
    ConstrainedFloat,
    ConstrainedInt,
    ConstrainedList,
    ConstrainedStr,
    conbytes,
    confloat,
    conint,
    conlist,
    constr,
    validate_arguments,
    validator,
)
from pydantic.types import update_not_none

from protobuf_to_pydantic import customer_validator

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator

__all__ = [
    "validator",
    "conlist",
    "conint",
    "confloat",
    "constr",
    "conbytes",
    "ConstrainedTimedelta",
    "contimedelta",
    "contimestamp",
    "ConstrainedTimestamp",
    "pydantic_con_dict",
    "set_ignore_param_value_tz",
    "get_origin_code",
]

_ignore_param_value_tz: bool = False


def set_ignore_param_value_tz(result: bool) -> None:
    global _ignore_param_value_tz
    _ignore_param_value_tz = result


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Duration[timedelta] TYPE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ConstrainedTimedelta(timedelta):
    duration_const: Optional[timedelta] = None
    duration_ge: Optional[timedelta] = None
    duration_gt: Optional[timedelta] = None
    duration_le: Optional[timedelta] = None
    duration_lt: Optional[timedelta] = None
    duration_in: Optional[Sequence[timedelta]] = None
    duration_not_in: Optional[Sequence[timedelta]] = None

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        update_not_none(
            field_schema,
            extra=dict(
                duration_const=cls.duration_const,
                duration_ge=cls.duration_ge,
                duration_gt=cls.duration_gt,
                duration_le=cls.duration_le,
                duration_lt=cls.duration_lt,
                duration_in=cls.duration_in,
                duration_not_in=cls.duration_not_in,
            ),
        )

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        if cls.duration_const:
            yield customer_validator.duration_const_validator
        if cls.duration_ge:
            yield customer_validator.duration_ge_validator
        if cls.duration_gt:
            yield customer_validator.duration_gt_validator
        if cls.duration_le:
            yield customer_validator.duration_le_validator
        if cls.duration_lt:
            yield customer_validator.duration_lt_validator
        if cls.duration_in:
            yield customer_validator.duration_in_validator
        if cls.duration_not_in:
            yield customer_validator.duration_not_in_validator


def contimedelta(
    *,
    duration_const: Optional[timedelta] = None,
    duration_ge: Optional[timedelta] = None,
    duration_gt: Optional[timedelta] = None,
    duration_le: Optional[timedelta] = None,
    duration_lt: Optional[timedelta] = None,
    duration_in: Optional[Sequence[timedelta]] = None,
    duration_not_in: Optional[Sequence[timedelta]] = None,
) -> Type[timedelta]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(
        duration_const=duration_const,
        duration_ge=duration_ge,
        duration_gt=duration_gt,
        duration_le=duration_le,
        duration_lt=duration_lt,
        duration_in=duration_in,
        duration_not_in=duration_not_in,
    )
    return type("ConstrainedTimedeltaValue", (ConstrainedTimedelta,), namespace)  # type: ignore


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Timestamp TYPE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TIMESTAMP_ANT_TYPE = Union[int, float, str, datetime]


class ConstrainedTimestamp(datetime):
    timestamp_const: Optional[TIMESTAMP_ANT_TYPE] = None
    timestamp_ge: Optional[TIMESTAMP_ANT_TYPE] = None
    timestamp_gt: Optional[TIMESTAMP_ANT_TYPE] = None
    timestamp_gt_now: Union[bool, Callable[[], TIMESTAMP_ANT_TYPE], None] = None
    timestamp_le: Optional[TIMESTAMP_ANT_TYPE] = None
    timestamp_lt: Optional[TIMESTAMP_ANT_TYPE] = None
    timestamp_lt_now: Union[bool, Callable[[], TIMESTAMP_ANT_TYPE], None] = None
    timestamp_in: Optional[Sequence[TIMESTAMP_ANT_TYPE]] = None
    timestamp_not_in: Optional[Sequence[TIMESTAMP_ANT_TYPE]] = None
    timestamp_within: Optional[timedelta] = None
    ignore_tz: bool = False

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        update_not_none(
            field_schema,
            extra=dict(
                timestamp_const=cls.timestamp_const,
                timestamp_ge=cls.timestamp_ge,
                timestamp_gt=cls.timestamp_gt,
                timestamp_gt_now=cls.timestamp_gt_now,
                timestamp_le=cls.timestamp_le,
                timestamp_lt=cls.timestamp_lt,
                timestamp_lt_now=cls.timestamp_lt_now,
                timestamp_in=cls.timestamp_in,
                timestamp_not_in=cls.timestamp_not_in,
                timestamp_within=cls.timestamp_within,
                ignore_tz=cls.ignore_tz,
            ),
        )

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate
        if cls.ignore_tz or _ignore_param_value_tz:
            yield cls.ignore_value_tz
        if cls.timestamp_const:
            yield customer_validator.timestamp_const_validator
        if cls.timestamp_ge:
            yield customer_validator.timestamp_ge_validator
        if cls.timestamp_gt:
            yield customer_validator.timestamp_gt_validator
        if cls.timestamp_gt_now:
            yield customer_validator.timestamp_gt_now_validator
        if cls.timestamp_le:
            yield customer_validator.timestamp_le_validator
        if cls.timestamp_lt:
            yield customer_validator.timestamp_lt_validator
        if cls.timestamp_lt_now:
            yield customer_validator.timestamp_lt_now_validator
        if cls.timestamp_in:
            yield customer_validator.timestamp_in_validator
        if cls.timestamp_not_in:
            yield customer_validator.timestamp_not_in_validator
        if cls.timestamp_within:
            yield customer_validator.timestamp_within_validator

    @classmethod
    @validate_arguments
    def validate(cls, v: datetime) -> datetime:
        return v

    @classmethod
    def ignore_value_tz(cls, v: datetime) -> datetime:
        return v.replace(tzinfo=None)


def contimestamp(
    *,
    timestamp_const: Optional[TIMESTAMP_ANT_TYPE] = None,
    timestamp_ge: Optional[TIMESTAMP_ANT_TYPE] = None,
    timestamp_gt: Optional[TIMESTAMP_ANT_TYPE] = None,
    timestamp_gt_now: Optional[Union[bool, Callable[[], TIMESTAMP_ANT_TYPE]]] = None,
    timestamp_le: Optional[TIMESTAMP_ANT_TYPE] = None,
    timestamp_lt: Optional[TIMESTAMP_ANT_TYPE] = None,
    timestamp_lt_now: Optional[Union[bool, Callable[[], TIMESTAMP_ANT_TYPE]]] = None,
    timestamp_in: Optional[Sequence[TIMESTAMP_ANT_TYPE]] = None,
    timestamp_not_in: Optional[Sequence[TIMESTAMP_ANT_TYPE]] = None,
    timestamp_within: Optional[timedelta] = None,
    ignore_tz: bool = False,
) -> Type:
    namespace = dict(
        timestamp_const=timestamp_const,
        timestamp_ge=timestamp_ge,
        timestamp_gt=timestamp_gt,
        timestamp_gt_now=timestamp_gt_now,
        timestamp_le=timestamp_le,
        timestamp_lt=timestamp_lt,
        timestamp_lt_now=timestamp_lt_now,
        timestamp_in=timestamp_in,
        timestamp_not_in=timestamp_not_in,
        timestamp_within=timestamp_within,
        ignore_tz=ignore_tz,
    )
    return type("ConstrainedTimestampValue", (ConstrainedTimestamp,), namespace)


pydantic_con_dict: Dict[Type, Callable] = {
    ConstrainedInt: conint,
    ConstrainedFloat: confloat,
    ConstrainedBytes: conbytes,
    ConstrainedStr: constr,
    ConstrainedList: conlist,
    ConstrainedTimedelta: contimedelta,
    ConstrainedTimestamp: contimestamp,
}


def get_origin_code(type_: Any) -> Any:
    return None
