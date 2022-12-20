from collections import deque
from typing import Any, Deque, List, Optional, Set, Type

from protobuf_to_pydantic.gen_model import DescTemplate


class Config(object):
    # At present, it is only a simple implementation,
    # and the convenience of adding configuration needs to be considered in the future
    __slots__ = (
        "local_dict",
        "desc_template",
        "comment_prefix",
        "customer_import_set",
        "customer_deque",
        "module_path",
        "code_indent",
        "ignore_pkg_list",
    )

    def __init__(
        self,
        local_dict: Optional[dict] = None,
        comment_prefix: str = "p2p",
        customer_import_set: Optional[Set[str]] = None,
        customer_deque: Optional[Deque] = None,
        module_path: str = "",
        code_indent: Optional[int] = None,
        desc_template: Optional[Type[DescTemplate]] = None,
        ignore_pkg_list: Optional[List[str]] = None,
    ):
        self.local_dict: dict = local_dict or {}
        self.desc_template: DescTemplate = (desc_template or DescTemplate)(self.local_dict, comment_prefix)
        self.comment_prefix: str = comment_prefix
        self.customer_import_set: Set[str] = customer_import_set or set()
        self.customer_deque: Deque = customer_deque or deque()
        self.module_path: str = module_path
        self.code_indent: int = code_indent or 4
        self.ignore_pkg_list: List[str] = ignore_pkg_list or []


def get_config_by_module(module: Any) -> Config:
    param_dict: dict = {}
    for key in Config.__slots__:
        if not hasattr(module, key):
            continue
        param_dict[key] = getattr(module, key)
    return Config(**param_dict)
