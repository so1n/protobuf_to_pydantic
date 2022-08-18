from datetime import timedelta
from typing import Any, Callable, Dict, Generator, Tuple, Type, Union

from pydantic import BaseConfig, BaseModel, create_model

from protobuf_to_pydantic.grpc_types import Duration, RepeatedCompositeContainer, Timestamp


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
    pydantic_config: Type["BaseConfig"] = None,
    pydantic_base: Type["BaseModel"] = None,
    pydantic_module: str = "pydantic.main",
    pydantic_validators: Dict[str, classmethod] = None,
) -> Type["BaseModel"]:
    """pydantic self.pait_response_model helper
    if use create_model('DynamicModel', **annotation_dict), mypy will tip error
    """
    return create_model(
        class_name,
        __config__=pydantic_config,
        __base__=pydantic_base,
        __module__=pydantic_module,
        __validators__=pydantic_validators,
        **annotation_dict,
    )


def replace_protobuf_type_to_python_type(value: Any) -> Any:
    if isinstance(value, Duration):
        return timedelta(microseconds=value.ToMicroseconds())
    elif isinstance(value, Timestamp):
        return value.ToMicroseconds() / 1000000
    elif isinstance(value, (list, RepeatedCompositeContainer)):
        return [replace_protobuf_type_to_python_type(i) for i in value]
    else:
        return value
