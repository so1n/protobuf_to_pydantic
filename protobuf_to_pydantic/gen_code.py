import inspect
import pathlib
import sys
import typing
from collections import deque
from dataclasses import is_dataclass
from datetime import datetime
from enum import IntEnum
from types import ModuleType
from typing import (  # type: ignore
    Any,
    Callable,
    Deque,
    Dict,
    ForwardRef,
    List,
    Optional,
    Set,
    Type,
    TypeVar,
    Union,
    _GenericAlias,
    _SpecialForm,
)

from google.protobuf import __version__ as protobuf_version
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo
from pydantic.version import VERSION as pydantic_version
from typing_extensions import Annotated, get_args, get_origin

from protobuf_to_pydantic import _pydantic_adapter, customer_validator, gen_model
from protobuf_to_pydantic.__version__ import __version__
from protobuf_to_pydantic.customer_con_type import get_origin_code, pydantic_con_dict
from protobuf_to_pydantic.gen_model import CodeRefModel
from protobuf_to_pydantic.grpc_types import RepeatedCompositeContainer, RepeatedScalarContainer
from protobuf_to_pydantic.util import format_content, replace_protobuf_type_to_python_type

# You can decide whether to generate the 'Field' parameter by modifying the 'field_param_set'
field_param_set = set(inspect.signature(Field).parameters.keys())
field_param_set.add("metadata")

if _pydantic_adapter.is_v1:
    from pydantic import root_validator, validator

    validator_sig = inspect.signature(validator)
    root_validator_sig = inspect.signature(root_validator)
else:
    validator_sig = inspect.Signature()
    root_validator_sig = inspect.Signature()


class BaseFormatContainer(object):
    def to_text(self) -> str:
        raise NotImplementedError


class FormatContainer(BaseFormatContainer):
    def __init__(self, text: str) -> None:
        self._text = text

    def to_text(self) -> str:
        return self._text


class BaseP2C(object):
    """
    BaseModel objects into corresponding Python code
    (only protobuf-generated pydantic.BaseModel objects are supported, not overly complex pydantic.BaseModel)
    """

    head_content: str = (
        "# This is an automatically generated file, please do not change\n"
        f"# gen by protobuf_to_pydantic[{__version__}](https://github.com/so1n/protobuf_to_pydantic)\n"
        f"# Protobuf Version: {protobuf_version} \n"
        f"# Pydantic Version: {pydantic_version} \n"
    )
    tail_content: str = ""

    def __init__(
        self,
        customer_import_set: Optional[Set[str]] = None,
        customer_deque: Optional[Deque] = None,
        module_path: str = "",
        code_indent: Optional[int] = None,
        pyproject_file_path: str = "",
    ):
        self._import_set: Set[str] = customer_import_set or set()
        self._content_deque: Deque = customer_deque or deque()
        self._create_set: Set[Type[BaseModel]] = set()
        self.code_indent: int = code_indent or 4
        self.pyproject_file_path: str = pyproject_file_path

        # init module_path
        if module_path:
            module_path_obj: pathlib.Path = pathlib.Path(module_path).absolute()
            if not module_path_obj.is_dir():
                raise TypeError(f"{module_path} must dir")
            cnt: int = 0
            while True:
                if not module_path_obj.name == "..":
                    break
                module_path_obj = module_path_obj.parent
                cnt += 1
            for _ in range(cnt):
                module_path_obj = module_path_obj.parent
            module_path = str(module_path_obj.absolute())
        self._module_path: str = module_path

    def format_content(self, content_str: str) -> str:
        return format_content(content_str, pyproject_file_path=self.pyproject_file_path)

    @property
    def content(self) -> str:
        # Regardless of the order of import, you can sort through isort (if installed)
        content_str: str = "\n".join(sorted(self._import_set))

        if self._content_deque:
            _content_set: Set[str] = set()
            content_str += "\n"
            for content in self._content_deque:
                if content in _content_set:
                    continue
                _content_set.add(content)
                content_str += f"\n{content}"
        return self.format_content(self.head_content + content_str + self.tail_content)

    def _add_import_code(self, module_name: str, class_name: str = "", extra_str: str = "") -> None:
        """
        Generate import statements through module name and class name

        - 1:
            param:
                module_name=typing
            output:
                import typing
        - 2:
            param:
                module_name=typing, class_name=Dict
            output:
                from typing import Dict
        -3:
            param:
                module_name=typing, class_name=Dict, extra_str=as MyDict
            output:
                from typing import Dict as MyDict

        """
        if module_name.startswith("google.protobuf") and not extra_str.endswith("type: ignore"):
            extra_str += "  # type: ignore"
        if module_name in (gen_model.__name__, __name__):
            return
        if class_name:
            self._import_set.add(f"from {module_name} import {class_name}{extra_str}")
        else:
            self._import_set.add(f"import {module_name}")

    def _get_typing_value_code(self, type_: Any, auto_import_type_code: bool = True) -> Optional[str]:
        """
        parse typing type to python code

        At present, only Type Var, Annotated, and Literal have independent parsing logic

        :param type_: typing type
        :param auto_import_type_code: if true, add import type module code
        :return: if type_ is typing type, return python code, else return None
        """
        if type_ is Any:
            # support py311 get_origin(Any) result is None
            return "typing.Any"
        elif isinstance(type_, ForwardRef):
            return type_.__forward_arg__
        elif isinstance(type_, TypeVar):
            # Support TypeVar
            if auto_import_type_code:
                self._add_import_code(type_.__module__, type_.__name__)
            return type_.__name__

        origin_type: Optional[_GenericAlias] = get_origin(type_)
        if origin_type is None:
            return None
        if origin_type is Annotated:
            # Support Annotated
            # TODO Analysis according to different Python versions
            args_str = self._get_value_code(list(get_args(type_)))
            if auto_import_type_code:
                self._import_set.add("import typing_extensions")
            return "typing_extensions.Annotated" + args_str
        else:
            type_name = type_._name
            arg_list = list(get_args(type_))
            # py version < 3.10
            # typing.Optional[int] output is: typing.Union[int, None]
            # py version == ^3.9  Optional[int]._name is None
            if (
                get_origin(type_) in (typing.Optional, typing.Union)
                and len(arg_list) == 2
                and arg_list[1] is type(None)
            ):
                type_name = "Optional"
                sub_type_str = f"[{self._get_value_code(arg_list[0])}]"
            else:
                sub_type_str = self._get_value_code(arg_list)
            if not type_name:
                # Support like typing_extensions.Literal[True]
                if auto_import_type_code:
                    self._import_set.add(f"import {origin_type.__module__}")
                return f"{origin_type.__module__}.{origin_type._name}{sub_type_str}"
            else:
                # Support other typing
                if auto_import_type_code:
                    self._import_set.add("import typing")
                return f"typing.{type_name}{sub_type_str}"

    # TODO remove flake8: noqa: C901
    # flake8: noqa: C901
    def _get_value_code(self, type_: Any, auto_import_type_code: bool = True, sort: bool = False) -> str:
        """
        Get the output string corresponding to the type
        :param type_: needs to be parsed type
        :param auto_import_type_code: If True, will generate by the way import code
        :param sort: If True, will sort item (Ensure that the order of code generated multiple times is consistent)
        :return:
        """
        # If module name is typing, it's prioritized
        value_code = self._get_typing_value_code(type_, auto_import_type_code=auto_import_type_code)
        if value_code:
            return value_code

        type_ = replace_protobuf_type_to_python_type(type_)

        customer_con_type_origin_code = get_origin_code(type_)
        if customer_con_type_origin_code:
            module_name, type_name, param_list = customer_con_type_origin_code
            if auto_import_type_code:
                self._add_import_code(module_name, type_name)
            return f"{type_name}({', '.join([self._get_value_code(i) for i in param_list])})"

        if isinstance(type_, dict):
            sort_list: list = [(k, v) for k, v in type_.items()]
            if sort:
                sort_list.sort()
            type_name = ", ".join(
                sorted([f"{self._get_value_code(k)}: {self._get_value_code(v)}" for k, v in sort_list])
            )
            return "{" + type_name + "}"
        elif isinstance(type_, (list, tuple, set)):
            sort_list = [self._get_value_code(i) for i in type_]
            if sort or isinstance(type_, set):
                sort_list.sort()
            type_name = ", ".join(sort_list)
            if isinstance(type_, list):
                return "[" + type_name + "]"
            elif isinstance(type_, set):
                return "{" + type_name + "}"
            else:
                if len(sort_list) == 1:
                    return "(" + type_name + ", )"
                return "(" + type_name + ")"
        elif is_dataclass(type_):
            # dataclass support
            field_param_code_list = []
            for field_key in type_.__dataclass_fields__.keys():
                field_value = getattr(type_, field_key)
                if field_value == type_.__dataclass_fields__[field_key].default:
                    continue
                field_param_code_list.append(f"{field_key}={self._get_value_code(field_value)}")
            if auto_import_type_code:
                self._parse_type_to_import_code(type_)
            return f"{type_.__class__.__name__}({', '.join(field_param_code_list)})"
        elif inspect.isfunction(type_) or "cyfunction" in str(type_):
            # pydantic confunc support
            if auto_import_type_code:
                self._parse_type_to_import_code(type_)
            return type_.__name__
        elif getattr(type_, "__module__", None) == "pydantic.functional_validators":
            # support BeforeValidator(func=xxx)
            if auto_import_type_code:
                self._parse_type_to_import_code(type_)
            return f"{type_.__class__.__name__}(func={self._get_value_code(type_.func)})"
        elif inspect.isclass(type_):
            if type_.__mro__[1] in pydantic_con_dict:
                # pydantic con class support
                return self._get_pydantic_con_type_code(type_)
            if type_ is type(None):
                return "None"
            if auto_import_type_code:
                self._parse_type_to_import_code(type_)
            return getattr(type_, "__name__")
        elif getattr(type_, "DESCRIPTOR", None):
            # protobuf message support
            message_name: str = type_.__class__.__name__
            attr_str: str = " ,".join([f"{i[0].name}={repr(i[1])}" for i in type_.ListFields()])
            if auto_import_type_code:
                self._parse_type_to_import_code(type_)
            return f"{message_name}({attr_str})"
        elif isinstance(type_, BaseFormatContainer):
            return type_.to_text()
        else:
            if auto_import_type_code:
                self._parse_type_to_import_code(type_)

            qualname: str = getattr(type_, "__qualname__", "")
            if inspect.ismethod(type_):
                type_name = qualname
                self._parse_type_to_import_code(type_name)
            elif (
                qualname
                and qualname.startswith("datetime")
                and (
                    (getattr(type_, "__objclass__", None) is datetime) or (getattr(type_, "__self__", None) is datetime)
                )
            ):
                # support datetime.datetime.xxx
                type_name = qualname
                self._parse_type_to_import_code(datetime)
            else:
                type_module = inspect.getmodule(type_)
                if type_module and type_module.__name__ == "builtins" or inspect.isfunction(type_module):
                    type_name = type_.__name__
                else:
                    type_name = repr(type_)

                # Compatible with datetime.* name
                type_name = type_name.replace("'", '"').replace("datetime.", "")
            return type_name

    def _model_config_handle(self, model: Type[BaseModel], indent: int = 0) -> str:
        model_config = _pydantic_adapter.get_model_config_dict(model)
        if not model_config:
            return ""
        if _pydantic_adapter.is_v1:
            config_str: str = ""
            for key, value in model_config.items():
                config_str += f"{' ' * (indent + self.code_indent)}{key} = {value}\n"
            # The Config class does not need to consider inheritance relationships
            # because pydantic.BaseModel only reads the values of the Config class
            # output:
            #   class Config:
            #       allow_mutation = False
            config_str = f"{' ' * indent}class Config:\n" + config_str
        else:
            # output:
            #   model_config = ConfigDict(allow_mutation=False)
            self._add_import_code("pydantic", "ConfigDict")
            config_list = []
            for k, v in model_config.items():
                config_list.append(f"{k}={self._get_value_code(v)}")
            config_str = f"{' ' * indent}model_config = ConfigDict({','.join(config_list)})\n"
        return config_str

    def _model_nested_handle(self, model: Type[BaseModel], indent: int = 0) -> str:
        code_ref = CodeRefModel.from_model(model)
        if not code_ref.nested_message_dict:
            return ""
        nested_str = ""
        for _, msg in code_ref.nested_message_dict.items():
            if issubclass(msg, IntEnum):
                nested_str += self._gen_enum_py_code(msg, indent=indent, ignore_nested_model=False)
            else:
                nested_str += self._gen_pydantic_model_py_code(msg, indent=indent, ignore_nested_model=False)
        return nested_str

    def _model_attribute_handle(self, model: Type[BaseModel], indent: int = 0) -> str:
        attribute_str: str = ""
        # support protobuf one_of
        for key in ("_one_of_dict",):
            model_attribute_dict = getattr(model, key, None)
            if not model_attribute_dict:
                continue
            attribute_str += f"{' ' * indent}{key} = {self._get_value_code(model_attribute_dict)}\n"
        return attribute_str

    def _model_field_handle(self, model: Type[BaseModel], indent: int = 0) -> str:
        field_str: str = ""
        for key, value in _pydantic_adapter.model_fields(model).items():
            if hasattr(value, "annotation") or _pydantic_adapter.is_v1:
                value_outer_type = value.annotation  # type: ignore
                value_type = value.annotation  # type: ignore
            else:
                raise RuntimeError("can not load value type")
            # Type Hint handler
            if value_outer_type.__module__ != "builtins":
                if inspect.isclass(value_type) and issubclass(value_type, IntEnum):
                    # Parse protobuf enum
                    self._import_set.add("from enum import IntEnum")
                    enum_code: str = self._gen_enum_py_code(value_type, indent=indent - self.code_indent)
                    if enum_code:
                        self._content_deque.append(enum_code)
                else:
                    # It is not necessary to consider other types since
                    # it is converted from the message object generated by protobuf
                    value_outer_type = model.__annotations__[key]
                # Extracting the exact Type Hint text
                if isinstance(value_outer_type, _GenericAlias):
                    value_type_name = self._get_typing_value_code(value_outer_type) or ""
                elif isinstance(value_outer_type, _SpecialForm):
                    value_type_name = f"typing.{value_outer_type._name}"  # type: ignore[attr-defined]
                    self._import_set.add("import typing")
                elif inspect.isclass(value_outer_type) and value_outer_type.__mro__[1] in pydantic_con_dict:
                    # Only pydantic v1 need to be considered
                    # only support like repeated[string]
                    value_type_name = self._get_pydantic_con_type_code(value_outer_type)
                else:
                    if isinstance(value_outer_type, str):
                        value_type_name = value_outer_type
                    else:
                        value_type_name = self._get_value_code(value_outer_type)
            else:
                value_type_name = getattr(value_outer_type, "__name__", "None")

            # TODO fix con_func bug:https://github.com/pydantic/pydantic/issues/156
            # ignore_flag: bool = False
            # for con_func in customer_con_type.__all__:
            #     if con_func in value_type_name:
            #         pass

            field_str += " " * indent + f"{key}: {value_type_name} = {self._field_info_handle(value)}\n"
            # if ignore_flag:
            #     field_str += "  # type: ignore"
            # field_str += "\n"
        return field_str

    def _get_pydantic_con_type_code(self, type_: Any) -> str:
        con_func: Callable = pydantic_con_dict[type_.__mro__[1]]
        self._parse_type_to_import_code(con_func)

        param_str_list: List[str] = []
        for _key in inspect.signature(con_func).parameters.keys():
            _value = getattr(type_, _key, None)
            if not _value:
                continue
            if inspect.isclass(_value) and _value.__mro__[1] in pydantic_con_dict:
                _value = self._get_pydantic_con_type_code(_value)
                # self._parse_type_to_import_code(_value)
            else:
                _value = self._get_value_code(_value)
            param_str_list.append(f"{_key}={_value}")
        return f"{con_func.__name__}({', '.join(param_str_list)})"

    def _gen_enum_py_code(self, type_: Any, indent: int = 0, ignore_nested_model: bool = True) -> str:
        # Parse protobuf enum
        if ignore_nested_model and getattr(type_, "_is_nested", False):
            return ""
        self._import_set.add("from enum import IntEnum")
        enum_class_str = " " * indent + f"class {type_.__name__}(IntEnum):\n"
        if type_.__doc__:
            enum_class_str += " " * (indent + self.code_indent) + '"""' + type_.__doc__ + '"""' + "\n"
        for enum_name, enum_value in type_.__members__.items():
            enum_class_str += " " * (indent + self.code_indent) + f"{enum_name} = {enum_value.value}\n"
        return enum_class_str

    def _gen_pydantic_model_py_code(
        self, model: Type[BaseModel], indent: int = 0, ignore_nested_model: bool = True
    ) -> str:
        if ignore_nested_model and getattr(model, "_is_nested", False):
            return ""
        if hasattr(model, "_base_model"):
            base_class: type = getattr(model, "_base_model")
        else:
            base_class = BaseModel
            for mro_model in model.__mro__[1:]:
                # pydantic v2 first mro model is "abc.BaseModel"
                if mro_model.__module__ == "abc":
                    continue
                base_class = mro_model
                break

        if base_class is BaseModel:
            self._import_set.add("from pydantic import BaseModel")
        else:
            self._add_import_code(base_class.__module__, base_class.__name__)

        class_str: str = " " * indent + f"class {model.__name__}({base_class.__name__}):\n"
        if model.__doc__:
            class_str += " " * (indent + self.code_indent) + '"""' + model.__doc__ + '"""\n'

        nested_class_str: str = self._model_nested_handle(model, indent=indent + self.code_indent)
        if nested_class_str:
            class_str += nested_class_str + "\n"

        config_class: str = self._model_config_handle(model, indent=indent + self.code_indent)
        if config_class:
            class_str += config_class + "\n"

        attribute_str: str = self._model_attribute_handle(model, indent=indent + self.code_indent)
        if attribute_str:
            class_str += attribute_str + "\n"

        field_str = self._model_field_handle(model, indent=indent + self.code_indent)
        if field_str:
            class_str += field_str + "\n"

        validator_str: str = self._model_validator_handle(model, indent=indent + self.code_indent)
        if validator_str:
            class_str += f"{validator_str}\n"
        if not any([model.__doc__, config_class, nested_class_str, attribute_str, field_str, validator_str]):
            class_str += " " * (indent + self.code_indent) + "pass\n"

        if class_str.endswith("\n\n"):
            class_str = class_str[:-1]
        return class_str

    def _gen_pydantic_model_py_code_to_content_deque(self, model: Type[BaseModel], indent: int = 0) -> None:
        if model in self._create_set:
            # ignore parsed model
            return None
        pydantic_model_code: str = self._gen_pydantic_model_py_code(model, indent=indent)
        if pydantic_model_code:
            pydantic_model_code += "\n"
            self._content_deque.append(pydantic_model_code)
        self._create_set.add(model)

    def _parse_type_to_import_code(self, type_: Any) -> None:
        """Parse the type and generate the corresponding import"""
        type_module: Optional[ModuleType] = inspect.getmodule(type_)
        if not type_module:
            # The corresponding module could not be found,
            # it may be a nested type, or the module needs to be found by some other means
            if isinstance(type_, (list, RepeatedScalarContainer, RepeatedCompositeContainer)):
                for i in type_:
                    self._parse_type_to_import_code(i)
            elif isinstance(type_, dict):
                for i in type_.values():
                    self._parse_type_to_import_code(i)
            else:
                type_module = inspect.getmodule(type_.__class__)

        if type_module is None:
            return
        elif getattr(type_module, "__name__", "builtins") == "builtins":
            # The built-in method does not use a guide package
            return
        elif inspect.ismethod(type_) and hasattr(type_, "__self__"):
            # If is bound method, should import class
            self._parse_type_to_import_code(type_.__self__)
            return
        elif isinstance(type_, _GenericAlias):
            # type hint handle
            self._import_set.add("import typing")
            for type_ in type_.__args__:
                self._parse_type_to_import_code(type_)
            return
        elif isinstance(type_, type) and inspect.isclass(type_) and issubclass(type_, BaseModel):
            # pydantic.BaseModel handle
            self._gen_pydantic_model_py_code_to_content_deque(type_)
        else:
            # other type handle
            if type_module.__name__ == "__main__":
                start_path: str = sys.path[0]
                module_file = type_module.__file__ or ""
                if self._module_path:
                    if not module_file.startswith(self._module_path):
                        type_module_file: str = start_path + "/" + module_file
                    else:
                        type_module_file = module_file
                    module_name = self._module_path.split("/")[-1] + type_module_file.replace(self._module_path, "")
                else:
                    # Find the name of the module for the variable that starts the code file
                    if not module_file.startswith(start_path):
                        # Compatible scripts are run directly in the submodule
                        module_name = f"{start_path.split('/')[-1]}.{module_file.split('/')[-1]}"
                    else:
                        module_name = start_path.split("/")[-1] + module_file.replace(start_path, "")
                module_name = module_name.replace("/", ".").replace(".py", "")

                class_name: str = self._get_value_code(type_, auto_import_type_code=False)
            else:
                module_name = type_module.__name__
                if not inspect.isclass(type_) and not inspect.isfunction(type_):
                    class_name = type_.__class__.__name__
                    if class_name == "cython_function_or_method":
                        class_name = type_.__name__
                else:
                    class_name = type_.__name__

            self._add_import_code(module_name, class_name)

    def _field_info_handle(self, field_info: FieldInfo) -> str:
        # Introduce the corresponding class for FieldInfo's properties
        if _pydantic_adapter.is_v1:
            # in v1, field_info is ModelField
            field_info = field_info.field_info  # type: ignore[attr-defined]

        field_param_dict: Dict[str, Any] = {}

        field_attr_dict = {k: v for k, v in field_info.__repr_args__()}

        if "default" not in field_attr_dict and field_info.default is None and _pydantic_adapter.VERSION < "2.7":
            # see issue: https://github.com/pydantic/pydantic/pull/8801
            field_attr_dict["default"] = None

        for k, v in field_attr_dict.items():
            if k not in field_param_set:
                continue
            v = getattr(field_info, k)
            if k == "default" and str(v) == "PydanticUndefined":
                # Ignore the default value of the pydantic field
                continue
            if k == "metadata":
                for metadata in v:
                    if not metadata:
                        continue
                    for metadata_key in getattr(metadata, "__annotations__", []):
                        if metadata_key not in field_info.metadata_lookup:
                            continue
                        metadata_value = getattr(metadata, metadata_key)
                        if metadata.__dataclass_fields__[metadata_key].default == metadata_value:
                            # If the value obtained is the same as the default value,
                            # it will not be added to the field param dict
                            continue
                        # Field's metadata will hold duplicate values, but Field only needs the first value
                        if metadata_key in field_param_dict:
                            continue
                        field_param_dict[metadata_key] = metadata_value
            elif k in ("extra", "json_schema_extra"):
                if not v:
                    # Ignore cases where the value of extra is empty
                    continue
                for extra_k, extra_v in v.items():
                    field_param_dict[extra_k] = extra_v
            else:
                field_param_dict[k] = v

        field_param_code_list: List[str] = []
        for k, v in field_param_dict.items():
            field_param_code_list.append(f"{k}={self._get_value_code(v)}")
            self._parse_type_to_import_code(v)

        # For different versions of pydantic, their fields are the same, but the position of the parameters is different
        # need to ensure that the generated code is consistent across different versions of pydantic
        # field_param_code_list.sort()
        if field_info.__class__.__name__ == "FieldInfo":
            self._add_import_code("pydantic", "Field")
            field_info_str: str = f"Field({', '.join(field_param_code_list)})"
        else:
            self._parse_type_to_import_code(field_info.__class__)
            field_info_str = f"{field_info.__class__.__name__}({', '.join(field_param_code_list)})"
        return field_info_str

    def _validator_handle(self, validator_dict: Dict[str, classmethod], indent: int) -> str:
        content = ""
        if _pydantic_adapter.is_v1:
            for validator_name, validator_class in validator_dict.items():
                if hasattr(validator_class, "__validator_config__"):
                    field_name_param, validator_instance = validator_class.__validator_config__
                    func = validator_instance.func
                    if not func.__module__.startswith(customer_validator.__name__):
                        continue

                    param_list = [
                        f"{i}={self._get_value_code(getattr(validator_instance, i))}"
                        # validator not support `skip_on_failure` param
                        for i in ["pre", "each_item", "always", "check_fields"]
                        if getattr(validator_instance, i) != validator_sig.parameters[i].default
                    ]
                    param_list.append("allow_reuse=True")
                    self._add_import_code("pydantic", "validator")
                    self._add_import_code(func.__module__, func.__name__)
                    field_param_str = ", ".join([self._get_value_code(i) for i in field_name_param])
                    content += (
                        " " * indent
                        + f"{validator_name} = validator({field_param_str}, {', '.join(param_list)})({func.__name__})\n"
                    )
                elif hasattr(validator_class, "__root_validator_config__"):
                    validator_instance = validator_class.__root_validator_config__
                    func = validator_instance.func

                    if not func.__module__.startswith(customer_validator.__name__):
                        continue
                    self._add_import_code("pydantic", "root_validator")
                    self._add_import_code(func.__module__, func.__name__)
                    param_list = [
                        f"{i}={self._get_value_code(getattr(validator_instance, i))}"
                        for i in ["pre", "skip_on_failure"]
                        if getattr(validator_instance, i) != root_validator_sig.parameters[i].default
                    ]
                    param_list.append("allow_reuse=True")
                    content += (
                        " " * indent + f"{validator_name} = root_validator({', '.join(param_list)})({func.__name__})\n"
                    )
                else:
                    raise TypeError(f"Unknown validator type: {validator_class}")
        else:
            for name, validator_class in validator_dict.items():
                validator_wrapper_func_name = self._get_value_code(
                    validator_class.wrapped.__func__  # type: ignore[attr-defined]
                )

                decorator_info_dict = {
                    k: getattr(validator_class.decorator_info, k)  # type: ignore[attr-defined]
                    for k in validator_class.decorator_info.__dataclass_fields__.keys()  # type: ignore[attr-defined]
                    if k not in ("decorator_repr",)
                    and getattr(validator_class.decorator_info, k)  # type: ignore[attr-defined]
                    is not _pydantic_adapter.PydanticUndefined
                }

                if "fields" in decorator_info_dict:
                    validator_func_name = "field_validator"
                    validator_field_param_str = ",".join([f'"{i}"' for i in decorator_info_dict["fields"]]) + ", "
                else:
                    validator_func_name = "model_validator"
                    validator_field_param_str = ""

                validator_param_str = validator_field_param_str + ",".join(
                    [f"{k}={self._get_value_code(v)}" for k, v in decorator_info_dict.items() if k != "fields"]
                )
                content += (
                    f"{' ' * indent}"
                    f"{name} = {validator_func_name}({validator_param_str})({validator_wrapper_func_name})\n"
                )
                self._add_import_code("pydantic", validator_func_name)
        return content

    def _model_validator_handle(self, model: Type[BaseModel], indent: int = 0) -> str:
        # TODO Here currently only consider the support for pgv&p2p, the follow-up to fill in
        code_ref = CodeRefModel.from_model(model)
        return self._validator_handle(code_ref.validators, indent=indent)


class P2C(BaseP2C):
    """
    BaseModel objects into corresponding Python code
    (only protobuf-generated pydantic.BaseModel objects are supported, not overly complex pydantic.BaseModel)
    """

    def __init__(
        self,
        *model: Type[BaseModel],
        customer_import_set: Optional[Set[str]] = None,
        customer_deque: Optional[Deque] = None,
        module_path: str = "",
        code_indent: Optional[int] = None,
        pyproject_file_path: str = "",
    ):
        super().__init__(
            customer_import_set=customer_import_set,
            customer_deque=customer_deque,
            module_path=module_path,
            code_indent=code_indent,
            pyproject_file_path=pyproject_file_path,
        )
        for _module in model:
            self._gen_pydantic_model_py_code_to_content_deque(_module)


def pydantic_model_to_py_code(
    *model: Type[BaseModel],
    customer_import_set: Optional[Set[str]] = None,
    customer_deque: Optional[Deque] = None,
    module_path: str = "",
    code_indent: Optional[int] = None,
    p2c_class: Type[P2C] = P2C,
    pyproject_file_path: str = "",
) -> str:
    """
    :param model:  the model(s) to generate code for
    :param customer_import_set: Customize the text that needs to be imported into the Python package
    :param customer_deque: Customize the code to be generated
    :param module_path:
    :param code_indent: Code indentation, default is 4
    :param pyproject_file_path: pyproject.toml path
    :param p2c_class:  The class that actually executes
    :return:
    """
    return p2c_class(
        *model,
        customer_import_set=customer_import_set,
        customer_deque=customer_deque,
        module_path=module_path,
        code_indent=code_indent,
        pyproject_file_path=pyproject_file_path,
    ).content


def pydantic_model_to_py_file(
    filename: str,
    *model: Type[BaseModel],
    customer_import_set: Optional[Set[str]] = None,
    customer_deque: Optional[Deque] = None,
    open_mode: str = "w",
    module_path: str = "",
    code_indent: Optional[int] = None,
    pyproject_file_path: str = "",
    p2c_class: Type[P2C] = P2C,
) -> None:
    py_code_content: str = pydantic_model_to_py_code(
        *model,
        customer_import_set=customer_import_set,
        customer_deque=customer_deque,
        module_path=module_path,
        code_indent=code_indent,
        pyproject_file_path=pyproject_file_path,
        p2c_class=p2c_class,
    )
    with open(filename, mode=open_mode) as f:
        f.write(py_code_content)
