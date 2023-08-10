import inspect
from pydantic.version import VERSION
from pydantic import BaseModel
from typing import Callable, Any, Type, Dict, Optional
from typing_extensions import Literal

is_v1: bool = VERSION.startswith("1.")


if is_v1:
    from pydantic.fields import ModelField as FieldInfo
    from pydantic.fields import Undefined as PydanticUndefined
    from pydantic.typing import NoArgAnyCallable # isort:skip
    from pydantic import root_validator, validator, BaseConfig
    from functools import partial

    # In pydantic v1, these methods are not called
    CoreSchema = None
    core_schema = None
    GetCoreSchemaHandler = None
    JsonSchemaValue = None
    GetJsonSchemaHandler = None

    PydanticUndefinedType = type(PydanticUndefined)

    def get_model_config_value(model: Type[BaseModel], key: str) -> Any:
        return getattr(model.Config, key)

    def get_model_config_dict(model: Type[BaseModel]) -> dict:
        config_dict = {}
        for key in dir(model.Config):
            if key.startswith("_"):
                continue
            value = getattr(model.Config, key)
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

    def field_validator(field_name: str, **kwargs) -> Callable:
        return validator(field_name, **kwargs)

else:
    from pydantic.fields import FieldInfo, PydanticUndefined
    from pydantic_core import CoreSchema, core_schema # isort:skip
    from pydantic import GetCoreSchemaHandler # isort:skip
    from pydantic.json_schema import JsonSchemaValue # isort:skip
    from pydantic import model_validator as _model_validator , field_validator as _field_validator
    from pydantic._internal._schema_generation_shared import GetJsonSchemaHandler # isort:skip

    from pydantic.functional_validators import  FieldValidatorModes

    NoArgAnyCallable = Callable[[], Any]
    PydanticUndefinedType = type(PydanticUndefined)

    def get_model_config_value(model: Type[BaseModel], key: str) -> Any:
        return model.model_config.get(key)

    def get_model_config_dict(model: Type[BaseModel]) -> dict:
        return model.model_config

    def model_fields(model: Type[FieldInfo]) -> Dict[str, FieldInfo]:
        return model.model_fields

    def field_validator(
        field_name: str,
        *fields: str,
        mode: FieldValidatorModes = 'after',
        check_fields: Optional[bool] = None,
        **kwargs, # ignore v1 param
    ) -> Callable:
        return _field_validator(field_name, *fields, mode=mode, check_fields=check_fields)

    def model_validator(
        *,
        mode: Literal['wrap', 'before', 'after'],
        **kwargs,  # ignore v1 param
    ) -> Callable:
        return _model_validator(mode=mode)
