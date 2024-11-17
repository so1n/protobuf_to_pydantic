from ipaddress import IPv4Address, IPv6Address
from typing import TYPE_CHECKING, Any, Dict, Type
from urllib import parse as urlparse
from uuid import UUID

from pydantic import AnyUrl, EmailStr, IPvAnyAddress

from protobuf_to_pydantic import _pydantic_adapter

if TYPE_CHECKING:
    from pydantic.networks import CallableGenerator


def _validate_host_name(host: str) -> bool:
    if not host:
        return False
    if len(host) > 253:
        return False

    if host[-1] == ".":
        host = host[:-1]

    for part in host.split("."):
        if len(part) == 0 or len(part) > 63:
            return False

        # Host names cannot begin or end with hyphens
        if part[0] == "-" or part[-1] == "-":
            return False
        for r in part:
            if (r < "A" or r > "Z") and (r < "a" or r > "z") and (r < "0" or r > "9") and r != "-":
                return False
    return True


class HostNameStr(str):
    @classmethod
    def validate(cls, value: str) -> str:
        if not _validate_host_name(value):
            raise ValueError("not a valid email")
        return value

    ###############
    # Pydantic V1 #
    ###############
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type="string", format="host")

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    ###############
    # Pydantic V2 #
    ###############
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: _pydantic_adapter.CoreSchema, handler: _pydantic_adapter.GetJsonSchemaHandler  # type: ignore
    ) -> _pydantic_adapter.JsonSchemaValue:  # type: ignore
        field_schema: dict = {}
        cls.__modify_schema__(field_schema)
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(  # type: ignore[no-untyped-def]
        cls,
        source: Type[Any],
        *args,
        **kwargs,  # fix https://github.com/pydantic/pydantic/issues/6506
    ) -> _pydantic_adapter.CoreSchema:  # type: ignore[name-defined,valid-type]
        def _validate(
            __input_value: Any, _: _pydantic_adapter.core_schema.ValidationInfo  # type: ignore[name-defined]
        ) -> str:
            return cls.validate(__input_value)

        # Why another change? The API of pydantic v2 is so fucked
        return _pydantic_adapter.core_schema.general_plain_validator_function(  # type: ignore[attr-defined]
            _validate, serialization=_pydantic_adapter.core_schema.to_string_ser_schema()  # type: ignore[attr-defined]
        )


class UriRefStr(str):
    @classmethod
    def validate(cls, value: str) -> str:
        url = urlparse.urlparse(value)
        if not all([url.scheme, url.path]) and url.fragment:
            raise ValueError("not a valid uri ref")
        return value

    ###############
    # Pydantic V1 #
    ###############
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type="string", format="uri_ref")

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    ###############
    # Pydantic V2 #
    ###############
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: _pydantic_adapter.CoreSchema, handler: _pydantic_adapter.GetJsonSchemaHandler  # type: ignore
    ) -> _pydantic_adapter.JsonSchemaValue:  # type: ignore[valid-type]
        field_schema: dict = {}
        cls.__modify_schema__(field_schema)
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(  # type: ignore[no-untyped-def]
        cls,
        source: Type[Any],
        *args,
        **kwargs,  # fix https://github.com/pydantic/pydantic/issues/6506
    ) -> _pydantic_adapter.CoreSchema:  # type: ignore[name-defined,valid-type]
        def _validate(
            __input_value: Any, _: _pydantic_adapter.core_schema.ValidationInfo  # type: ignore[name-defined]
        ) -> str:
            return cls.validate(__input_value)

        return _pydantic_adapter.core_schema.general_plain_validator_function(  # type: ignore[attr-defined]
            _validate, serialization=_pydantic_adapter.core_schema.to_string_ser_schema()  # type: ignore[attr-defined]
        )


rule_name_pydantic_type_dict: Dict[str, Any] = {
    "email": EmailStr,
    "hostname": HostNameStr,
    "ip": IPvAnyAddress,
    "ipv4": IPv4Address,
    "ipv6": IPv6Address,
    "uri": AnyUrl,
    "uri_ref": UriRefStr,
    "address": IPvAnyAddress,
    "uuid": UUID,
}
