import json
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, Optional, Tuple, Type, Union

from pydantic import BaseConfig, BaseModel, create_model

if TYPE_CHECKING:
    from pydantic.main import Model
    from pydantic.typing import AnyClassMethod

from protobuf_to_pydantic.grpc_types import Duration, RepeatedCompositeContainer, RepeatedScalarContainer, Timestamp
from protobuf_to_pydantic.types import FieldInfoTypedDict


class Timedelta(timedelta):
    """Timedelta object supporting Protobuf.Duration of pydantic.field."""

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[int, float, str, timedelta]) -> timedelta:
        if isinstance(v, timedelta):
            return v
        elif isinstance(v, str):
            if v.endswith("s") and v[:-1].isdigit():
                v = v[:-1]
            v = float(v)
        return timedelta(seconds=v)


def create_pydantic_model(
    annotation_dict: Dict[str, Tuple[Type, Any]],
    class_name: str = "DynamicModel",
    pydantic_config: Optional[Type["BaseConfig"]] = None,
    pydantic_base: Union[None, Type["Model"], Tuple[Type["Model"], ...]] = None,
    pydantic_module: str = "pydantic.main",
    pydantic_validators: Optional[Dict[str, "AnyClassMethod"]] = None,
) -> Type["BaseModel"]:
    """pydantic self.pait_response_model helper
    if use create_model('DynamicModel', **annotation_dict), mypy will tip error
    """
    return create_model(  # type: ignore
        class_name,
        __config__=pydantic_config,
        __base__=pydantic_base,
        __module__=pydantic_module,
        __validators__=pydantic_validators,
        **annotation_dict,
    )


def replace_protobuf_type_to_python_type(value: Any) -> Any:
    """
    protobuf.Duration -> datetime.timedelta
    protobuf.Timestamp -> timestamp e.g 1600000000.000000
    like list -> list

    other type -> raw...
    """
    if isinstance(value, Duration):
        return timedelta(microseconds=value.ToMicroseconds())
    elif isinstance(value, Timestamp):
        return value.ToMicroseconds() / 1000000
    elif isinstance(value, (list, RepeatedCompositeContainer, RepeatedScalarContainer)):
        return [replace_protobuf_type_to_python_type(i) for i in value]
    else:
        return value


def gen_dict_from_desc_str(comment_prefix: str, desc: str) -> FieldInfoTypedDict:
    pait_dict: dict = {}
    for line in desc.split("\n"):
        line = line.strip()
        if not line.startswith(f"{comment_prefix}:"):
            continue
        line = line.replace(f"{comment_prefix}:", "")
        pait_dict.update(json.loads(line))
    return pait_dict  # type: ignore


def format_content(content_str: str) -> str:
    try:
        import isort  # type: ignore
    except ImportError:
        pass
    else:
        content_str = isort.code(content_str)

    try:
        import autoflake  # type: ignore
    except ImportError:
        pass
    else:
        content_str = autoflake.fix_code(content_str)

    try:
        import black  # type: ignore
    except ImportError:
        pass
    else:
        content_str = black.format_str(content_str, mode=black.Mode(line_length=120))
    return content_str
