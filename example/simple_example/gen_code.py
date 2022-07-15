from example.python_example_proto_code.example_proto.demo import demo_pb2
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file


def gen_code() -> None:
    pydantic_model_to_py_file(
        "./demo_gen_code.py",
        *[
            msg_to_pydantic_model(model)
            for model in (
                demo_pb2.UserMessage,
                demo_pb2.MapMessage,
                demo_pb2.RepeatedMessage,
                demo_pb2.NestedMessage,
            )
        ],
        enable_yapf=False,
    )


if __name__ == "__main__":
    gen_code()
