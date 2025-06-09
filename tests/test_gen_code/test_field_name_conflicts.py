"""Test for handling field names that conflict with Python built-in types."""
from typing import Type

from google.protobuf import __version__
from pydantic import BaseModel

from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code
from protobuf_to_pydantic._pydantic_adapter import is_v1
from protobuf_to_pydantic.gen_model import clear_create_model_cache
from protobuf_to_pydantic.util import format_content

# Import the generated protobuf message
if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1.example.example_proto.demo import field_name_conflict_pb2
    else:
        from example.proto_pydanticv2.example.example_proto.demo import field_name_conflict_pb2  # type: ignore[no-redef]
else:
    if is_v1:
        from example.proto_3_20_pydanticv1.example.example_proto.demo import field_name_conflict_pb2  # type: ignore[no-redef]
    else:
        from example.proto_3_20_pydanticv2.example.example_proto.demo import field_name_conflict_pb2  # type: ignore[no-redef]


class TestFieldNameConflicts:
    @staticmethod
    def _model_output(msg) -> str:
        """Generate model output for testing."""
        clear_create_model_cache()
        return pydantic_model_to_py_code(msg_to_pydantic_model(msg))

    def test_builtin_field_names_renamed(self) -> None:
        """Test that fields with names matching Python built-ins are renamed."""
        # Expected output for fields that conflict with built-in types
        if is_v1:
            expected_content = """
class ConflictingFieldNames(BaseModel):
    bytes_: bytes = Field(default=b"", alias="bytes")
    str_: str = Field(default="", alias="str")
    int_: int = Field(default=0, alias="int")
    float_: float = Field(default=0.0, alias="float")
    bool_: bool = Field(default=False, alias="bool")
    list_: typing.List[str] = Field(default_factory=list, alias="list")
    dict_: typing.Dict[str, str] = Field(default_factory=dict, alias="dict")
"""
        else:
            expected_content = """
class ConflictingFieldNames(BaseModel):
    bytes_: bytes = Field(default=b"", alias="bytes")
    str_: str = Field(default="", alias="str")
    int_: int = Field(default=0, alias="int")
    float_: float = Field(default=0.0, alias="float")
    bool_: bool = Field(default=False, alias="bool")
    list_: typing.List[str] = Field(default_factory=list, alias="list")
    dict_: typing.Dict[str, str] = Field(default_factory=dict, alias="dict")
"""

        output = self._model_output(field_name_conflict_pb2.ConflictingFieldNames)
        assert format_content(expected_content) in output

    def test_field_alias_functionality(self) -> None:
        """Test that renamed fields work correctly with aliases."""
        model: Type[BaseModel] = msg_to_pydantic_model(field_name_conflict_pb2.ConflictingFieldNames)

        # Test that we can create instance using original field names
        instance = model(
            bytes=b"test",
            str="hello",
            int=42,
            float=3.14,
            bool=True,
            list=["a", "b"],
            dict={"key": "value"}
        )

        # Verify data can be accessed
        data = instance.model_dump(by_alias=True) if hasattr(instance, 'model_dump') else instance.dict(by_alias=True)
        assert data['bytes'] == b"test"
        assert data['str'] == "hello"
        assert data['int'] == 42
        assert data['float'] == 3.14
        assert data['bool'] is True
        assert data['list'] == ["a", "b"]
        assert data['dict'] == {"key": "value"}

    def test_generated_code_validity(self) -> None:
        """Test that generated code is valid Python."""
        output = self._model_output(field_name_conflict_pb2.ConflictingFieldNames)

        # Should not have problematic patterns like "bytes: bytes"
        assert "bytes: bytes" not in output
        assert "str: str" not in output
        assert "int: int" not in output

        # Should have safe patterns with underscore
        assert "bytes_: bytes" in output
        assert "str_: str" in output
        assert "int_: int" in output

        # Generated code should compile without errors
        compile(output, '<string>', 'exec')