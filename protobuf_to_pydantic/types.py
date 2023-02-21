from typing import Any, Callable, Dict, Optional, Set, Type, Union

from pydantic.fields import FieldInfo
from typing_extensions import NotRequired, TypedDict

Number = Union[int, float]


class OneOfTypedDict(TypedDict):
    required: bool
    fields: Set[str]


class FieldInfoTypedDict(TypedDict):
    extra: dict
    skip: NotRequired[bool]
    enable: NotRequired[bool]
    miss_default: NotRequired[bool]
    validator: NotRequired[Dict[str, classmethod]]
    type: NotRequired[Any]
    map_type: NotRequired[Dict[str, Type]]
    sub: NotRequired["FieldInfoTypedDict"]
    field: NotRequired[Optional[Type[FieldInfo]]]
    default: NotRequired[Optional[Any]]
    default_factory: NotRequired[Optional[Callable]]
    example: NotRequired[Optional[Any]]
    example_factory: NotRequired[Optional[Callable]]
    alias: NotRequired[Optional[str]]
    title: NotRequired[Optional[str]]
    description: NotRequired[Optional[str]]
    const: NotRequired[Optional[Any]]
    gt: NotRequired[Optional[Number]]
    ge: NotRequired[Optional[Number]]
    lt: NotRequired[Optional[Number]]
    le: NotRequired[Optional[Number]]
    min_length: NotRequired[Optional[int]]
    max_length: NotRequired[Optional[int]]
    min_items: NotRequired[Optional[int]]
    max_items: NotRequired[Optional[int]]
    unique_items: NotRequired[Optional[bool]]
    multiple_of: NotRequired[Optional[int]]
    regex: NotRequired[Optional[str]]


class DescFromOptionTypedDict(TypedDict):
    message: Dict[str, FieldInfoTypedDict]
    one_of: Dict[str, OneOfTypedDict]
    nested: Dict[str, "DescFromOptionTypedDict"]
