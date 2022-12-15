from typing import Any

from pydantic import BaseModel, Field


class ProtobufTypeModel(BaseModel):
    type_factory: Any = Field(description="Default value factory for Python types")
    py_type_str: str = Field(description="String of Python type")
    rule_type_str: str = Field(description="Corresponding validator rule string")
