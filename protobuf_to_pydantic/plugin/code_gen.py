import base64
import importlib
import logging
import pathlib
import sys
import traceback
import types
from typing import Callable, Dict, Generic, Optional, Type

from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest, CodeGeneratorResponse
from mypy_protobuf.main import Descriptors, code_generation

from protobuf_to_pydantic.plugin.config import ConfigT, get_config_by_module
from protobuf_to_pydantic.util import use_worker_dir_in_ctx

# If want to parse option, need to import the corresponding file
#   see details:https://stackoverflow.com/a/59301849
from protobuf_to_pydantic.protos import p2p_validate_pb2, validate_pb2  # isort:skip


logger = logging.getLogger(__name__)


class CodeGen(Generic[ConfigT]):
    config: ConfigT

    def __init__(self, config_class: Type[ConfigT]) -> None:
        self.config_class: Type[ConfigT] = config_class

        with code_generation() as (request, response):
            self.param_dict = self.gen_param_from_request(request)
            self.gen_config()
            self.generate_pydantic_model(Descriptors(request), response)

    @staticmethod
    def gen_param_from_request(request: CodeGeneratorRequest) -> dict:
        """
        Parse the parameter information passed by the user and store it in the 'param_dict'.

        For example
            Input:
                protoc -I. --protobuf-to-pydantic_out=bar1=foo1,bar2=foo2:. example.proto
            param_dict result:
                {"bar1": "foo1", "bar2": "foo2"}
        """
        param_dict: dict = {}
        if request.parameter:
            try:
                for one_param_str in request.parameter.split(","):
                    k, v = one_param_str.split("=")
                    param_dict[k] = v
            except Exception as e:
                logger.exception(e)
                print(f"parse command-line error:{e}", file=sys.stderr)
            print(f"Parse command-line arguments:{param_dict}", file=sys.stderr)
        return param_dict

    def _get_config_by_path(self, key: str) -> None:
        """
        Get config from path.

        If not specify the directory where the configuration file is located by 'config_worker_dir_path',
        the current directory will be used by default
        """
        default_config = self.config
        path_obj: pathlib.Path = pathlib.Path(self.param_dict[key]).absolute()
        if not path_obj.exists():
            raise SystemError(f"Can not find config file at {path_obj}")
        if "config_worker_dir_path" in self.param_dict:
            worker_dir_path_obj: pathlib.Path = pathlib.Path(self.param_dict["config_worker_dir_path"]).absolute()
            if not worker_dir_path_obj.exists():
                raise SystemError(f"Can not find worker dir at {worker_dir_path_obj}")
            worker_dir_path = str(worker_dir_path_obj)
        else:
            worker_dir_path = None

        config_path: str = str(path_obj)
        msg: str = f"Load config: {config_path}"
        if worker_dir_path:
            msg += f" worker dir: {worker_dir_path}"
        print(msg, file=sys.stderr)

        try_import_module_path_list: list = [f"{path_obj.name}", f"{path_obj.parent.name}.{path_obj.name}"]

        with use_worker_dir_in_ctx(worker_dir_path):
            for sys_path in sys.path:
                if not config_path.startswith(sys_path):
                    continue
                try_import_module_path_list.append(config_path[len(sys_path) + 1 :])

            error_path_dict: dict = {}
            for module_path in try_import_module_path_list:
                module_path = module_path.replace("/", ".").replace("\\", ".").replace(".py", "")
                try:
                    self.config = get_config_by_module(importlib.import_module(module_path), self.config_class)
                    break
                except ModuleNotFoundError as e:
                    error_path_dict[module_path] = {"error": e, "traceback": traceback.format_exc()}
        if self.config == default_config:
            raise SystemError(f"Load config error. try use path and error:{error_path_dict}")

    def _get_config_by_py_code(self, key: str) -> None:
        """
        Pass the py code from the command line and convert it to config

            Except in special cases such as buf, it is not recommended to use this form to get config
        """
        try:
            plugin_config_module_name = self.param_dict.get("plugin_config_module_name", "")
            plugin_config_module: Optional[types.ModuleType] = None
            if plugin_config_module_name:
                error_str_list = [".py", "/", "\\"]
                for error_str in error_str_list:
                    if error_str in plugin_config_module_name:
                        raise SystemError(
                            f"Plugin_config_module_name error, Please check if it contains characters:{error_str_list}"
                        )
                plugin_config_module = types.ModuleType(plugin_config_module_name)
                sys.modules[plugin_config_module_name] = plugin_config_module
                module_global_dict: dict = plugin_config_module.__dict__
            else:
                module_global_dict = {}

            plugin_config_py_code_base64 = self.param_dict[key]
            equal_sign_len = len(plugin_config_py_code_base64) % 4
            if equal_sign_len:
                plugin_config_py_code_base64 += "=" * (4 - equal_sign_len)

            exec(base64.b64decode(plugin_config_py_code_base64).decode(), module_global_dict)
            if plugin_config_module:
                self.config = get_config_by_module(plugin_config_module, self.config_class)
            else:
                for key in ["local_dict", "base_model_class"]:
                    if key in self.param_dict and not plugin_config_module_name:
                        raise SystemError(f"When using config--{key}, must specify the plugin_config_module_name")
                self.config = self.config_class(**module_global_dict)
        except Exception as e:
            raise SystemError(f"Load config error:{e}. try check code")

    def gen_config(self) -> None:
        self.config = self.config_class()
        param_dict: Dict[str, Callable[[str], None]] = {
            "config_path": self._get_config_by_path,
            "plugin_config_py_code_base64": self._get_config_by_py_code,
        }
        for param_name, param_func in param_dict.items():
            if param_name in self.param_dict:
                param_func(param_name)

    def generate_pydantic_model(self, descriptors: Descriptors, response: CodeGeneratorResponse) -> None:
        for name, fd in descriptors.to_generate.items():
            config = self.config.pkg_config.get(fd.package, self.config)
            if fd.package in config.ignore_pkg_list:
                continue
            file = response.file.add()
            file.name = fd.name[:-6].replace("-", "_").replace(".", "/") + f"{config.file_name_suffix}.py"
            file.content = config.file_descriptor_proto_to_code(fd=fd, descriptors=descriptors, config=config).content
