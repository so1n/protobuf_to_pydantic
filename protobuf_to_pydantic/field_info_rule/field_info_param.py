import inspect
import warnings
from dataclasses import MISSING
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Set, Type, Union

from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo
from typing_extensions import Literal, get_args, get_origin

from protobuf_to_pydantic import _pydantic_adapter, constant
from protobuf_to_pydantic.field_info_rule.types import FieldInfoTypedDict, JsonAndDict
from protobuf_to_pydantic.util import check_dict_one_of

# You can decide whether to generate the 'Field' parameter by modifying the 'field_param_set'
field_param_set = set(inspect.signature(Field).parameters.keys())

support_con_type_module_name: List[str] = [
    "pydantic.types",
    "protobuf_to_pydantic.customer_con_type.v1",
    "protobuf_to_pydantic.customer_con_type.v2",
]


def field_info_param_dict_migration_v2_handler(field_info_param_dict: Dict[str, Any], is_warnings: bool = True) -> None:
    json_schema_extra = {}
    for k in list(field_info_param_dict.keys()):
        new_k = constant.pydantic_field_v1_migration_v2_dict.get(k, k)
        if new_k != k:
            if new_k is None:
                if is_warnings:
                    warnings.warn(
                        f"field info param `{k}` is deprecated, "
                        f"https://docs.pydantic.dev/latest/migration/#changes-to-pydanticfield"
                    )
                field_info_param_dict.pop(k)
            else:
                if is_warnings:
                    warnings.warn(
                        f"field info param `{k}` is deprecated, please use `{new_k}` instead,"
                        f" https://docs.pydantic.dev/latest/migration/#changes-to-pydanticfield"
                    )
                value = field_info_param_dict.pop(k)
                if value:
                    field_info_param_dict[new_k] = value
        else:
            if k not in field_param_set:
                json_schema_extra[k] = field_info_param_dict.pop(k)
    field_info_param_dict["json_schema_extra"] = json_schema_extra


def field_info_param_dict_handle(
    field_info_param_dict: dict,
    default: Any,
    default_factory: Optional[_pydantic_adapter.NoArgAnyCallable],
    field_type: Optional[type] = None,
    nested_call_count: int = 1,
) -> None:
    """
    Convert the field_param_dict data to Pydantic Field parameters

    :param field_info_param_dict:
    :param default: Pydantic Field default value
    :param default_factory: Pydantic Field default_factory value
    :param field_type: Pydantic Field type value
    :param nested_call_count: Each call will only process one level of type,
        if it is a nested type, a recursive call is required,
        and this parameter is used to record the number of layers of recursive calls

        e.g: List[str], List is the first layer, str is the second layer,
    :return:
    """
    # default_template support
    if (
        field_info_param_dict.get("default", MISSING).__class__ == MISSING.__class__
        and field_info_param_dict.get("default_template", MISSING).__class__ != MISSING.__class__
    ):
        field_info_param_dict["default"] = field_info_param_dict["default_template"]
    field_info_param_dict.pop("default_template", None)

    # Handle complex relationships with different defaults
    check_dict_one_of(field_info_param_dict, ["required", "default", "default_factory"])
    if field_info_param_dict.get("default_factory", None) is not None:
        field_info_param_dict.pop("default", "")
    elif field_info_param_dict.get("default", MISSING).__class__ == MISSING.__class__:
        if default_factory:
            field_info_param_dict["default_factory"] = default_factory
            field_info_param_dict.pop("default", "")
        else:
            field_info_param_dict["default"] = default
            field_info_param_dict.pop("default_factory", None)

    # const handler
    _const = field_info_param_dict.pop("const", MISSING)
    # PGV&P2P const handler
    if _const.__class__ != MISSING.__class__:
        if _pydantic_adapter.is_v1:
            field_info_param_dict["default"] = _const
            field_info_param_dict["const"] = True
        else:
            # pydantic v2 not support const, only support Literal
            field_info_param_dict["type_"] = Literal.__getitem__(_const)

    # required handler
    if field_info_param_dict.get("required", None) is True:
        _pop_default = field_info_param_dict.pop("default", "")
        _pop_default_factory = field_info_param_dict.pop("default_factory", "")
        if _pop_default or _pop_default_factory:
            warnings.warn(
                "if required is True,"
                " `default`, `default_factory`, `default_template` and `const` param values should not be set"
            )

    field_info_param_dict.pop("required", None)

    # unique handler
    if not _pydantic_adapter.is_v1 and field_info_param_dict.get("unique_items", None) is not None:
        # In pydantic v2, not support unique_items
        # only use the Set type instead of this feature
        if not field_type or get_origin(field_type) != list:
            raise RuntimeError(f"unique_items only support type List (protobuf type: repeated) not {field_type}")
        # change type: list -> set
        field_info_param_dict["type_"] = Set.__getitem__(get_args(field_type))  # type: ignore[misc]
        if field_info_param_dict["default_factory"]:
            field_info_param_dict["default_factory"] = set

    # example handler
    check_dict_one_of(field_info_param_dict, ["example", "example_factory"])
    if field_info_param_dict.get("example", MISSING).__class__ == MISSING.__class__:
        field_info_param_dict.pop("example", None)
    example_factory = field_info_param_dict.pop("example_factory", None)
    if example_factory:
        field_info_param_dict["example"] = example_factory

    # extra handler
    extra = field_info_param_dict.pop("extra", None)
    if extra:
        field_info_param_dict.update(extra)

    # type handler
    field_type = field_info_param_dict.get("type_")
    sub_field_param_dict: Optional[dict] = field_info_param_dict.pop("sub", None)
    field_type_model: Optional[ModuleType] = inspect.getmodule(field_type)
    if (
        field_type
        and not inspect.isclass(field_type)
        and field_type_model
        and field_type_model.__name__ in support_con_type_module_name
    ):
        # support https://pydantic-docs.helpmanual.io/usage/types/#constrained-types
        # Parameters needed to extract `constrained-types`
        type_param_dict: dict = {}

        if _pydantic_adapter.is_v1 or nested_call_count != 1:
            # In pydantic v2
            # If it is the first layer, all parameters need to be passed to Field, not Type
            for key in inspect.signature(field_type).parameters.keys():
                if key in field_info_param_dict:
                    type_param_dict[key] = field_info_param_dict.pop(key)
        if sub_field_param_dict and "type_" in sub_field_param_dict:
            # If a nested type is found, use the same treatment
            field_info_param_dict_handle(
                sub_field_param_dict, default, default_factory, nested_call_count=nested_call_count + 1
            )
            field_info_param_dict["type_"] = field_type(sub_field_param_dict["type_"], **type_param_dict)
        else:
            field_info_param_dict["type_"] = field_type(**type_param_dict)


class FieldInfoParamModel(BaseModel):
    field: Optional[Type[FieldInfo]] = Field(None)
    enable: bool = Field(True)
    required: bool = Field(False)
    default: Optional[Any] = Field(MISSING)
    default_factory: Optional[Callable] = Field(None)
    default_template: Any = Field(MISSING)
    example: Any = Field(MISSING)
    example_factory: Optional[Callable] = Field(None)
    alias: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    const: Any = Field(MISSING)
    gt: Union[float, int, None] = Field(None)
    ge: Union[float, int, None] = Field(None)
    lt: Union[float, int, None] = Field(None)
    le: Union[float, int, None] = Field(None)
    min_length: Optional[int] = Field(None)
    max_length: Optional[int] = Field(None)
    min_items: Optional[int] = Field(None)
    max_items: Optional[int] = Field(None)
    unique_items: Optional[bool] = Field(None)
    multiple_of: Optional[int] = Field(None)
    regex: Optional[str] = Field(None)
    extra: JsonAndDict = Field(default_factory=dict)
    json_schema_extra: JsonAndDict = Field(default_factory=dict)
    skip: bool = Field(False)
    type_: Any = Field(None, alias="type")
    validator: Optional[Dict[str, Any]] = Field(None)
    sub: Optional["FieldInfoParamModel"] = Field(None)
    map_type: Optional[dict] = Field(None)

    def to_dict(self) -> FieldInfoTypedDict:
        return self.dict()  # type: ignore
