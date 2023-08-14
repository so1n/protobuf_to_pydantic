import inspect
from typing import Any, Callable, Dict, Optional, Type

from pydantic import BaseModel
from pydantic.version import VERSION
from typing_extensions import Literal

is_v1: bool = VERSION.startswith("1.")


if is_v1:
    from functools import partial

    from pydantic import BaseConfig, root_validator, validator
    from pydantic.fields import ModelField as FieldInfo  # type: ignore[attr-defined]
    from pydantic.fields import Undefined as PydanticUndefined  # type: ignore[attr-defined]

    from pydantic.typing import NoArgAnyCallable  # isort:skip

    # In pydantic v1, these methods are not called
    CoreSchema = None
    core_schema = None
    GetCoreSchemaHandler = None
    JsonSchemaValue = None
    GetJsonSchemaHandler = None

    PydanticUndefinedType = type(PydanticUndefined)

    def get_model_config_value(model: Type[BaseModel], key: str) -> Any:
        return getattr(model.Config, key)  # type: ignore[attr-defined]

    def get_model_config_dict(model: Type[BaseModel]) -> dict:
        config_dict = {}
        for key in dir(model.Config):  # type: ignore[attr-defined]
            if key.startswith("_"):
                continue
            value = getattr(model.Config, key)  # type: ignore[attr-defined]
            if value == getattr(BaseConfig, key) or inspect.isfunction(value) or inspect.ismethod(value):
                continue
            config_dict[key] = value
        return config_dict

    def model_validator(*, mode: Literal["before", "after"], **kwargs: Any) -> Callable:
        if mode == "after":
            pre = False
        elif mode == "before":
            pre = True
        else:
            raise ValueError(f"Not support mode:`{mode}`")
        return partial(root_validator, pre=pre, **kwargs)

    def model_fields(model: Type[BaseModel]) -> Dict[str, FieldInfo]:
        return model.__fields__

    def field_validator(field_name: str, **kwargs: Any) -> Callable:
        return validator(field_name, **kwargs)

else:
    from pydantic import field_validator as _field_validator
    from pydantic import model_validator as _model_validator
    from pydantic.fields import FieldInfo, PydanticUndefined  # type: ignore
    from pydantic.functional_validators import FieldValidatorModes  # type: ignore

    from pydantic._internal._schema_generation_shared import (  # isort:skip  type: ignore
        GetJsonSchemaHandler,
    )
    from pydantic_core import CoreSchema, core_schema  # isort:skip  type: ignore
    from pydantic import GetCoreSchemaHandler  # isort:skip  type: ignore
    from pydantic.json_schema import JsonSchemaValue  # isort:skip  type: ignore

    NoArgAnyCallable = Callable[[], Any]
    PydanticUndefinedType = type(PydanticUndefined)

    def get_model_config_value(model: Type[BaseModel], key: str) -> Any:
        return model.model_config.get(key)

    def get_model_config_dict(model: Type[BaseModel]) -> dict:
        return model.model_config  # type: ignore

    def model_fields(model: Type[FieldInfo]) -> Dict[str, FieldInfo]:
        return model.model_fields  # type: ignore

    def field_validator(
        field_name: str,
        *fields: str,
        mode: FieldValidatorModes = "after",
        check_fields: Optional[bool] = None,
        **kwargs: Any,  # ignore v1 param
    ) -> Callable:
        return _field_validator(field_name, *fields, mode=mode, check_fields=check_fields)

    def model_validator(
        *,
        mode: Literal["wrap", "before", "after"],
        **kwargs: Any,  # ignore v1 param
    ) -> Callable:
        return _model_validator(mode=mode)
