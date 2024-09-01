import json
from typing import Any, Callable, Dict, Generator, Optional, Set, Type, Union

from pydantic.fields import FieldInfo
from typing_extensions import NotRequired, TypedDict

from protobuf_to_pydantic._pydantic_adapter import is_v1

Number = Union[int, float]


class UseOneOfTypedDict(TypedDict):
    required: bool
    fields: Set[str]


class OneOfTypedDict(TypedDict):
    required: bool
    fields: Set[str]
    optional_fields: Optional[Set[str]]


class FieldInfoTypedDict(TypedDict):
    extra: dict
    json_schema_extra: NotRequired[dict]
    skip: NotRequired[bool]
    enable: NotRequired[bool]
    required: NotRequired[bool]
    validator: NotRequired[Dict[str, classmethod]]
    type: NotRequired[Any]
    map_type: NotRequired[Dict[str, Type]]
    sub: NotRequired["FieldInfoTypedDict"]
    field: NotRequired[Optional[Type[FieldInfo]]]
    default: NotRequired[Optional[Any]]
    default_factory: NotRequired[Optional[Callable]]
    default_template: NotRequired[Optional[Callable]]
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
    type_: NotRequired[Any]


class MessageOptionTypedDict(TypedDict):
    message: Dict[str, FieldInfoTypedDict]
    one_of: Dict[str, OneOfTypedDict]
    nested: Dict[str, "MessageOptionTypedDict"]
    metadata: Dict[str, Any]


def json_to_dict(v: Union[str, dict]) -> dict:
    if isinstance(v, str):
        try:
            v = json.loads(v)
        except json.JSONDecodeError:
            raise ValueError("JSON string is not valid JSON")
    elif not isinstance(v, dict):
        raise ValueError("JSON string is not a dict")
    return v  # type: ignore[return-value]


if is_v1:

    class JsonAndDict(dict):
        # v1 support
        @classmethod
        def __get_validators__(cls) -> Generator[Callable, None, None]:
            yield cls.validate

        @classmethod
        def validate(cls, v: Union[str, dict]) -> dict:
            return json_to_dict(v)

else:
    from pydantic import BeforeValidator
    from typing_extensions import Annotated

    JsonAndDict = Annotated[dict, BeforeValidator(json_to_dict)]  # type: ignore[misc, assignment]
