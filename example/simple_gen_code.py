from example.python_example_proto_code.example_proto.demo import demo_pb2
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file

pydantic_model_to_py_file(
    "./demo_gen_code.py",
    msg_to_pydantic_model(demo_pb2.NestedMessage),
)
pydantic_model_to_py_file(
    "./demo_gen_code_by_pyi.py",
    msg_to_pydantic_model(demo_pb2.NestedMessage, parse_msg_desc_method=demo_pb2),
)
pydantic_model_to_py_file(
    "./demo_gen_code_by_protobuf_field.py",
    msg_to_pydantic_model(
        demo_pb2.NestedMessage, parse_msg_desc_method="/home/so1n/github/protobuf_to_pydantic/example"
    ),
)
