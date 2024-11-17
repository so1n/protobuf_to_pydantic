import inspect
import json
import logging
import os
import re
import sys
from contextlib import contextmanager
from dataclasses import MISSING
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Type, Union

from pydantic import BaseConfig, BaseModel, create_model

from protobuf_to_pydantic import _pydantic_adapter

if TYPE_CHECKING:
    from pydantic.main import Model
    from pydantic.typing import AnyClassMethod

from protobuf_to_pydantic.grpc_types import Duration, ProtobufRepeatedType, Timestamp


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


def camel_to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


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
    like list type -> list
    other type -> raw...
    """
    if isinstance(value, Duration):
        return timedelta(microseconds=value.ToMicroseconds())
    elif isinstance(value, Timestamp):
        return value.ToMicroseconds() / 1000000
    elif isinstance(value, (list, *ProtobufRepeatedType)):
        return [replace_protobuf_type_to_python_type(i) for i in value]
    else:
        return value


def get_dict_from_comment(comment_prefix: str, comment: str) -> dict:
    _dict: dict = {}
    try:
        for line in comment.split("\n"):
            if line.startswith("#"):
                line = line[1:]
            line = line.strip()
            if not line.startswith(f"{comment_prefix}:"):
                continue
            line = line.replace(f"{comment_prefix}:", "")
            for key, value in json.loads(line.replace("\\\\", "\\")).items():
                if not _dict.get(key):
                    _dict[key] = value
                else:
                    if not isinstance(value, type(_dict[key])):
                        raise TypeError(f"Two different types of values were detected for Key:{key}")
                    elif isinstance(value, list):
                        _dict[key].extend(value)
                    elif isinstance(value, dict):
                        _dict[key].update(value)
                    else:
                        raise TypeError(f"A key:{key} that does not support merging has been detected")
        if "miss_default" in _dict:
            _dict["required"] = _dict.pop("miss_default")
    except Exception as e:
        logging.warning(f"Can not gen dict by desc:{comment}, error: {e}")
    return _dict  # type: ignore


def get_pyproject_content(pyproject_file_path: str) -> str:
    if not pyproject_file_path:
        for path in sys.path:
            pyproject_file_path = os.path.join(path, "pyproject.toml")
            if os.path.exists(pyproject_file_path):
                break
            pyproject_file_path = ""

    if pyproject_file_path:
        with open(pyproject_file_path, "r") as f:
            return "".join(f.readlines())
    return ""


# flake8: noqa: C901
def format_content(content_str: str, pyproject_file_path: str = "") -> str:
    pyproject_dict: dict = {}
    try:
        import toml  # type: ignore
    except ImportError:
        logging.warning(
            "The toml module is not installed and the configuration information cannot be obtained through"
            " pyproject.toml"
        )
    else:
        pyproject_content = get_pyproject_content(pyproject_file_path)
        if pyproject_content:
            pyproject_dict = toml.loads(pyproject_content)
    try:
        p2p_format_dict: dict = pyproject_dict["tool"]["protobuf-to-pydantic"]["format"]
    except KeyError:
        p2p_format_dict = {}

    try:
        import isort  # type: ignore
    except ImportError:
        pass
    else:
        if p2p_format_dict.get("isort", True):
            if pyproject_file_path:
                content_str = isort.code(content_str, config=isort.Config(settings_file=pyproject_file_path))
            else:
                content_str = isort.code(content_str)

    try:
        import autoflake  # type: ignore
    except ImportError:
        pass
    else:
        autoflake_dict: dict = {}
        try:
            for k, v in pyproject_dict["tool"]["autoflake"].items():
                k = k.replace("-", "_")
                if k not in inspect.signature(autoflake.fix_code).parameters.keys():
                    continue
                autoflake_dict[k] = v

        except KeyError:
            pass
        if p2p_format_dict.get("autoflake", True):
            if autoflake_dict:
                content_str = autoflake.fix_code(content_str, **autoflake_dict)
            else:
                content_str = autoflake.fix_code(content_str)

    try:
        import black  # type: ignore
    except ImportError:
        pass
    else:
        black_config_dict: dict = {}
        try:
            black_config_dict = {k.replace("-", "_"): v for k, v in pyproject_dict["tool"]["black"].items()}
            # target_version param replace
            target_versions = {
                getattr(black.TargetVersion, i.upper()) for i in black_config_dict.pop("target_version", [])
            }
            if target_versions:
                black_config_dict["target_versions"] = target_versions

            black_config_dict = {k: v for k, v in black_config_dict.items() if k in black.Mode.__annotations__}
        except KeyError:
            pass
        if p2p_format_dict.get("black", True):
            if black_config_dict:
                content_str = black.format_str(content_str, mode=black.Mode(**black_config_dict))
            else:
                content_str = black.format_str(content_str, mode=black.Mode())
    return content_str


def check_dict_one_of(desc_dict: dict, key_list: List[str]) -> bool:
    """Check if the key also appears in the dict"""
    if (
        len(
            [
                desc_dict.get(key, None)
                for key in key_list
                if desc_dict.get(key, None) and desc_dict[key].__class__ != MISSING.__class__
            ]
        )
        > 1
    ):
        raise RuntimeError(f"Field:{key_list} cannot have both values: {desc_dict}")
    return True


@contextmanager
def use_worker_dir_in_ctx(worker_dir: Optional[str] = None) -> Generator:
    if worker_dir:
        parent_path_exist = worker_dir in sys.path
        if not parent_path_exist:
            sys.path.append(worker_dir)
            try:
                yield
            finally:
                sys.path.remove(worker_dir)
        else:
            yield
    else:
        yield


def pydantic_allow_validation_field_handler(
    field_name: str, field_alias_name: Optional[str], allow_field_set: Set[str], model_config_dict: dict
) -> None:
    """
    fix issue: #74 https://github.com/so1n/protobuf_to_pydantic/issues/74

    :param field_name: pydantic field name
    :param field_alias_name: pydantic field alias name
    :param allow_field_set: pydantic allow validation set
    :param model_config_dict: pydantic model config dict
    """
    if field_alias_name:
        allow_field_set.add(field_alias_name)
        if model_config_dict.get("populate_by_name") is not True:
            allow_field_set.remove(field_name)
    if _pydantic_adapter.VERSION < "2.6.0":
        alias_generator: Optional[Callable[[str], str]] = model_config_dict.get("alias_generator")
        alias_generator_func: Optional[Callable] = alias_generator
        if alias_generator:
            allow_field_set.add(alias_generator(field_name))
    else:
        from pydantic import AliasGenerator

        alias_generator_gte_26: Any = model_config_dict.get("alias_generator")
        if isinstance(alias_generator_gte_26, AliasGenerator):  # type: ignore
            alias_generator_func = alias_generator_gte_26.validation_alias
        else:
            alias_generator_func = alias_generator_gte_26
    if alias_generator_func:
        allow_field_set.add(alias_generator_func(field_name))
