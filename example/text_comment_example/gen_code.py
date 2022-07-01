import time

from example.python_example_proto_code.example_proto.demo import demo_pb2
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file


def exp_time() -> float:
    return time.time()


if __name__ == "__main__":
    pydantic_model_to_py_file(
        "./use_module_path/demo_gen_code_by_pyi.py",
        msg_to_pydantic_model(demo_pb2.NestedMessage, parse_msg_desc_method=demo_pb2, local_dict=locals()),
        module_path="../",
    )
    pydantic_model_to_py_file(
        "./use_module_path/demo_gen_code_by_protobuf_field.py",
        msg_to_pydantic_model(
            demo_pb2.NestedMessage,
            parse_msg_desc_method="/home/so1n/github/protobuf_to_pydantic/example",
            local_dict=locals(),
        ),
        module_path="../",
    )
    pydantic_model_to_py_file(
        "./not_use_module_path/demo_gen_code_by_pyi.py",
        msg_to_pydantic_model(demo_pb2.NestedMessage, parse_msg_desc_method=demo_pb2, local_dict=locals()),
    )
    pydantic_model_to_py_file(
        "./not_use_module_path/demo_gen_code_by_protobuf_field.py",
        msg_to_pydantic_model(
            demo_pb2.NestedMessage,
            parse_msg_desc_method="/home/so1n/github/protobuf_to_pydantic/example",
            local_dict=locals(),
        ),
    )
