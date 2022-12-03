import time
from uuid import uuid4

from example.example_proto_python_code.example_proto.demo import demo_pb2
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file


def exp_time() -> float:
    return time.time()


def gen_code() -> None:
    local_dict = {"exp_time": exp_time, "uuid4": uuid4}
    pydantic_model_to_py_file(
        "./use_module_path/demo_gen_code_by_pyi.py",
        *[
            msg_to_pydantic_model(model, parse_msg_desc_method=demo_pb2, local_dict=local_dict)
            for model in (
                demo_pb2.UserMessage,
                demo_pb2.MapMessage,
                demo_pb2.RepeatedMessage,
                demo_pb2.NestedMessage,
            )
        ],
        module_path="../",
    )
    pydantic_model_to_py_file(
        "./use_module_path/demo_gen_code_by_protobuf_field.py",
        *[
            msg_to_pydantic_model(
                model,
                parse_msg_desc_method="/home/so1n/github/protobuf_to_pydantic/example",
                local_dict=local_dict,
            )
            for model in (
                demo_pb2.UserMessage,
                demo_pb2.MapMessage,
                demo_pb2.RepeatedMessage,
                demo_pb2.NestedMessage,
            )
        ],
        module_path="../",
    )
    pydantic_model_to_py_file(
        "./not_use_module_path/demo_gen_code_by_pyi.py",
        *[
            msg_to_pydantic_model(model, parse_msg_desc_method=demo_pb2, local_dict=local_dict)
            for model in (
                demo_pb2.UserMessage,
                demo_pb2.MapMessage,
                demo_pb2.RepeatedMessage,
                demo_pb2.NestedMessage,
            )
        ],
    )
    pydantic_model_to_py_file(
        "./not_use_module_path/demo_gen_code_by_protobuf_field.py",
        *[
            msg_to_pydantic_model(
                model,
                parse_msg_desc_method="/home/so1n/github/protobuf_to_pydantic/example",
                local_dict=local_dict,
            )
            for model in (
                demo_pb2.UserMessage,
                demo_pb2.MapMessage,
                demo_pb2.RepeatedMessage,
                demo_pb2.NestedMessage,
            )
        ],
    )


if __name__ == "__main__":
    gen_code()
