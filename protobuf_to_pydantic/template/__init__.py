import json
from importlib import import_module
from typing import Any, Callable, Dict, List, Optional, TypeVar

from protobuf_to_pydantic.grpc_types import RepeatedCompositeContainer, RepeatedScalarContainer

_T = TypeVar("_T")


class Template(object):
    def __init__(self, local_dict: Dict[str, Any], comment_prefix: str, **kwargs: Any) -> None:
        """
        :param local_dict: local template var
        :param comment_prefix: comment prefix, The comment prefix that needs to be resolved
        :param kwargs: Extended parameters for custom templates
        """
        self._local_dict = local_dict
        self._comment_prefix: str = comment_prefix
        self._kwargs: Dict[str, Any] = kwargs
        self._support_template_list: List[str] = [i for i in dir(self) if i.startswith("template")]

    def template_import_instance(self, module_str: str, var_str: str, json_param: str) -> Any:
        module: Any = import_module(module_str, module_str)
        for sub_var_str in var_str.split("."):
            module = getattr(module, sub_var_str)
        if json_param:
            var = module(**json.loads(json_param))  # type: ignore
        else:
            var = module
        return var

    def template_import(self, module_str: str, var_str: str) -> Any:
        module = import_module(module_str, module_str)
        for sub_var_str in var_str.split("."):
            module = getattr(module, sub_var_str)
        return module

    def template_local(self, local_var_name: str) -> Any:
        return self._local_dict[local_var_name]

    def template_builtin(self, builtin_name: str) -> Any:
        return __builtins__.get(builtin_name)  # type: ignore

    def _template_str_handler(self, template_str: str) -> Any:
        try:
            template_str_list: List[str] = template_str.split("|")
            template_rule, *template_var_list = template_str_list
            template_fn: Optional[Callable] = getattr(self, f"template_{template_rule}", None)
            if not template_fn:
                raise ValueError(f"Only support {' ,'.join(self._support_template_list)}. not {template_str}")
            return template_fn(*template_var_list)
        except Exception as e:
            raise ValueError(f"parse {template_str} error: {e}") from e

    def handle_template_var(self, container: _T) -> _T:
        if isinstance(container, (list, RepeatedCompositeContainer, RepeatedScalarContainer)):
            return [self.handle_template_var(i) for i in container]  # type: ignore[return-value]
        elif isinstance(container, dict):
            return {k: self.handle_template_var(v) for k, v in container.items()}
        elif isinstance(container, str) and container.startswith(f"{self._comment_prefix}@"):
            container = container.replace(f"{self._comment_prefix}@", "")
            return self._template_str_handler(container)
        else:
            return container
