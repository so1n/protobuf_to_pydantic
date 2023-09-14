import importlib
import inspect
import pathlib

from google.protobuf import __version__
from google.protobuf.any_pb2 import Any  # type: ignore
from google.protobuf.message import Message
from pydantic import confloat, conint
from pydantic.fields import FieldInfo

from protobuf_to_pydantic import _pydantic_adapter, desc_template, msg_to_pydantic_model, pydantic_model_to_py_file

target_p: str = "proto" if __version__ > "4.0.0" else "proto_3_20"
if not _pydantic_adapter.is_v1:
    target_p += "_pydanticv2"
else:
    target_p += "_pydanticv1"

module = importlib.import_module(f"example.{target_p}.example.example_proto.p2p_validate.demo_pb2")
message_class_list = []
for module_name in dir(module):
    message_class = getattr(module, module_name)
    if not inspect.isclass(message_class):
        continue
    if not issubclass(message_class, Message):
        continue
    message_class_list.append(message_class)


class CustomerField(FieldInfo):
    pass


def customer_any() -> Any:
    return Any()


now_path: pathlib.Path = pathlib.Path(__file__).absolute()


class CustomDescTemplate(desc_template.DescTemplate):
    def template_timestamp(self, length_str: str) -> int:
        timestamp: float = 1600000000
        if length_str == "10":
            return int(timestamp)
        elif length_str == "13":
            return int(timestamp * 100)
        else:
            raise KeyError(f"timestamp template not support value:{length_str}")


def gen_code() -> None:
    pydantic_model_to_py_file(
        str(now_path.parent.joinpath(target_p, "demo_gen_code_by_p2p.py")),
        *[
            msg_to_pydantic_model(
                model,
                local_dict={
                    "CustomerField": CustomerField,
                    "confloat": confloat,
                    "conint": conint,
                    "customer_any": customer_any,
                },
                desc_template=CustomDescTemplate,
            )
            for model in message_class_list
        ],
        module_path=str(now_path.parent),
    )


if __name__ == "__main__":
    print(target_p)
    gen_code()
