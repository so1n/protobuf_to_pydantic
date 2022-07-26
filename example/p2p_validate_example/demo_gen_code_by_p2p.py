# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic(https://github.com/so1n/protobuf_to_pydantic)
# type: ignore

from pydantic import BaseModel, validator
from pydantic.fields import FieldInfo
from pydantic.types import confloat, conint

from example.p2p_validate_example.gen_code import CustomerField
from protobuf_to_pydantic.customer_validator import in_validator, not_in_validator


class FloatTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"not_in": [1.0, 2.0, 3.0]})
    default_test: float = FieldInfo(default=1.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0.0, alias="alias", alias_priority=2)
    desc_test: float = FieldInfo(default=0.0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3)
    example_test: float = FieldInfo(default=0.0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"example": float})
    field_test: float = CustomerField(default=0.0)
    type_test: confloat() = FieldInfo(default=0.0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class DoubleTest(BaseModel):
    const_test: float = FieldInfo(default=1.0, const=True)
    range_e_test: float = FieldInfo(default=0.0, ge=1, le=10)
    range_test: float = FieldInfo(default=0.0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0.0, extra={"in": [1.0, 2.0, 3.0]})
    not_in_test: float = FieldInfo(default=0.0, extra={"not_in": [1.0, 2.0, 3.0]})
    default_test: float = FieldInfo(default=1.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0.0, alias="alias", alias_priority=2)
    desc_test: float = FieldInfo(default=0.0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0.0, multiple_of=3)
    example_test: float = FieldInfo(default=0.0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0.0, extra={"example": float})
    field_test: float = CustomerField(default=0.0)
    type_test: confloat() = FieldInfo(default=0.0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Int32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: confloat() = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Uint32Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: conint() = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Sfixed32Test(BaseModel):
    const_test: float = FieldInfo(default=0)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: float = FieldInfo(default=0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0, multiple_of=3)
    example_test: float = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0, extra={"example": float})
    field_test: float = CustomerField(default=0)
    type_test: confloat() = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Int64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: confloat() = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Sint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: conint() = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Uint64Test(BaseModel):
    const_test: int = FieldInfo(default=1, const=True)
    range_e_test: int = FieldInfo(default=0, ge=1, le=10)
    range_test: int = FieldInfo(default=0, gt=1, lt=10)
    in_test: int = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: int = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: int = FieldInfo(default=1.0)
    default_factory_test: int = FieldInfo(default_factory=int)
    miss_default_test: int = FieldInfo()
    alias_test: int = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: int = FieldInfo(default=0, description="test desc")
    multiple_of_test: int = FieldInfo(default=0, multiple_of=3)
    example_test: int = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: int = FieldInfo(default=0, extra={"example": int})
    field_test: int = CustomerField(default=0)
    type_test: conint() = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Sfixed64Test(BaseModel):
    const_test: float = FieldInfo(default=0)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: float = FieldInfo(default=0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0, multiple_of=3)
    example_test: float = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0, extra={"example": float})
    field_test: float = CustomerField(default=0)
    type_test: confloat() = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)


class Fixed32Test(BaseModel):
    const_test: float = FieldInfo(default=1, const=True)
    range_e_test: float = FieldInfo(default=0, ge=1, le=10)
    range_test: float = FieldInfo(default=0, gt=1, lt=10)
    in_test: float = FieldInfo(default=0, extra={"in": [1, 2, 3]})
    not_in_test: float = FieldInfo(default=0, extra={"not_in": [1, 2, 3]})
    default_test: float = FieldInfo(default=1.0)
    default_factory_test: float = FieldInfo(default_factory=float)
    miss_default_test: float = FieldInfo()
    alias_test: float = FieldInfo(default=0, alias="alias", alias_priority=2)
    desc_test: float = FieldInfo(default=0, description="test desc")
    multiple_of_test: float = FieldInfo(default=0, multiple_of=3)
    example_test: float = FieldInfo(default=0, extra={"example": 1.0})
    example_factory: float = FieldInfo(default=0, extra={"example": float})
    field_test: float = CustomerField(default=0)
    type_test: confloat() = FieldInfo(default=0)

    in_validator_in_test = validator("in_test", allow_reuse=True)(in_validator)
    not_in_validator_not_in_test = validator("not_in_test", allow_reuse=True)(not_in_validator)
