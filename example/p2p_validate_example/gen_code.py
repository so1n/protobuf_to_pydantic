from google.protobuf.any_pb2 import Any  # type: ignore
from pydantic import confloat, conint
from pydantic.fields import FieldInfo

from example.python_example_proto_code.example_proto.p2p_validate.demo_pb2 import (
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
    MessageIgnoredTest,
    MessageTest,
    NestedMessage,
    OneOfNotTest,
    OneOfTest,
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


class CustomerField(FieldInfo):
    pass


def customer_any() -> Any:
    return Any()


def gen_code() -> None:
    pydantic_model_to_py_file(
        "./demo_gen_code_by_p2p.py",
        *[
            msg_to_pydantic_model(
                model,
                local_dict={
                    "CustomerField": CustomerField,
                    "confloat": confloat,
                    "conint": conint,
                    "customer_any": customer_any,
                },
            )
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
                MessageIgnoredTest,
                NestedMessage,
                OneOfTest,
                OneOfNotTest,
            )
        ],
        module_path="../",
        enable_yapf=False,
    )


if __name__ == "__main__":
    gen_code()
