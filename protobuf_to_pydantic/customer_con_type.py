from datetime import timedelta
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Type

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
    "ConTimedelta",
    "contimedelta",
    "pydantic_con_dict",
]


class ConTimedelta(timedelta):
    duration_const: Optional[timedelta] = None
    duration_ge: Optional[timedelta] = None
    duration_gt: Optional[timedelta] = None
    duration_le: Optional[timedelta] = None
    duration_lt: Optional[timedelta] = None
    duration_in: Optional[timedelta] = None
    duration_not_in: Optional[timedelta] = None

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
        yield customer_validator.duration_const_validator
        yield customer_validator.duration_ge_validator
        yield customer_validator.duration_gt_validator
        yield customer_validator.duration_le_validator
        yield customer_validator.duration_lt_validator
        yield customer_validator.duration_in_validator
        yield customer_validator.duration_not_in_validator


def contimedelta(
    *,
    duration_const: Optional[timedelta] = None,
    duration_ge: Optional[timedelta] = None,
    duration_gt: Optional[timedelta] = None,
    duration_le: Optional[timedelta] = None,
    duration_lt: Optional[timedelta] = None,
    duration_in: Optional[timedelta] = None,
    duration_not_in: Optional[timedelta] = None,
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
    return type("ConstrainedTimedeltaValue", (ConTimedelta,), namespace)  # type: ignore


pydantic_con_dict: Dict[Type, Callable] = {
    ConstrainedInt: conint,
    ConstrainedFloat: confloat,
    ConstrainedBytes: conbytes,
    ConstrainedStr: constr,
    ConstrainedList: conlist,
    ConTimedelta: contimedelta,
}
