import time

from example.python_example_proto_code.example_proto.demo import demo_pb2
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file


def exp_time() -> float:
    return time.time()


if __name__ == "__main__":
    pydantic_model_to_py_file(
        "./demo_gen_code.py",
        msg_to_pydantic_model(demo_pb2.NestedMessage),
        enable_yapf=False,
    )
