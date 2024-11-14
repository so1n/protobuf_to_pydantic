from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from protobuf_to_pydantic._pydantic_adapter import VERSION

if VERSION < "2.6.0":

    class MyBaseSchema(BaseModel):
        model_config = ConfigDict(
            alias_generator=to_camel,
            populate_by_name=True,
        )

else:
    from pydantic import AliasGenerator

    class MyBaseSchema(BaseModel):  # type: ignore[no-redef]
        model_config = ConfigDict(
            alias_generator=AliasGenerator(validation_alias=to_camel),
            populate_by_name=True,
        )


base_model_class = MyBaseSchema
