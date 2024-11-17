from pydantic import BaseModel, ConfigDict

from protobuf_to_pydantic._pydantic_adapter import VERSION

try:
    from pydantic.alias_generators import to_camel
except ImportError:

    def to_camel(string: str) -> str:  # type: ignore[misc]
        return "".join(word.capitalize() for word in string.split("_"))


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
