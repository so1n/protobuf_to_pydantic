from example.python_example_proto_code.example_proto.validate.demo_pb2 import (
    AnyTest,
    BoolTest,
    BytesTest,
    DoubleTest,
    DurationTest,
    EnumTest,
    Fixed32Test,
    FloatTest,
    Int32Test,
    Int64Test,
    MapTest,
    MessageDisabledTest,
    MessageIgnoredTest,
    MessageTest,
    NestedMessage,
    RepeatedTest,
    Sfixed32Test,
    Sfixed64Test,
    Sint64Test,
    StringTest,
    TimestampTest,
    Uint32Test,
    Uint64Test,
)
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file


def gen_code() -> None:
    pydantic_model_to_py_file(
        "./demo_gen_code_by_pgv.py",
        *[
            msg_to_pydantic_model(model, parse_msg_desc_method="PGV")
            for model in (
                FloatTest,
                DoubleTest,
                Int32Test,
                Uint32Test,
                Sfixed32Test,
                Int64Test,
                Sint64Test,
                Uint64Test,
                Sfixed64Test,
                Fixed32Test,
                BoolTest,
                StringTest,
                BytesTest,
                EnumTest,
                MapTest,
                MessageTest,
                RepeatedTest,
                AnyTest,
                DurationTest,
                TimestampTest,
                MessageDisabledTest,
                MessageIgnoredTest,
                NestedMessage,
            )
        ],
        module_path="../",
        enable_yapf=False,
    )


if __name__ == "__main__":
    gen_code()
