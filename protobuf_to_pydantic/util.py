from datetime import timedelta
from typing import Any, Dict, Tuple, Type

from pydantic import BaseConfig, BaseModel, create_model

from protobuf_to_pydantic.grpc_types import Duration, RepeatedCompositeContainer, Timestamp


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


def replace_type(value: Any) -> Any:
    if isinstance(value, Duration):
        return timedelta(microseconds=value.ToMicroseconds())
    elif isinstance(value, Timestamp):
        return value.ToDatetime()
    elif isinstance(value, (list, RepeatedCompositeContainer)):
        return [replace_type(i) for i in value]
    else:
        return value
