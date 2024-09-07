import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from google.protobuf.descriptor import FieldDescriptor

from protobuf_to_pydantic import _pydantic_adapter
from protobuf_to_pydantic.constant import protobuf_common_type_dict
from protobuf_to_pydantic.customer_con_type import (
    conbytes,
    confloat,
    conint,
    conlist,
    constr,
    contimedelta,
    contimestamp,
)
from protobuf_to_pydantic.customer_validator import validate_validator_dict
from protobuf_to_pydantic.field_info_rule.protobuf_option_to_field_info.types import rule_name_pydantic_type_dict
from protobuf_to_pydantic.field_info_rule.types import FieldInfoTypedDict

logger: logging.Logger = logging.getLogger(__name__)

pgv_column_to_pydantic_dict: Dict[str, str] = {
    "min_len": "min_length",
    "min_bytes": "min_length",
    "max_len": "max_length",
    "max_bytes": "max_length",
    "pattern": "regex",
    "unique": "unique_items",
    "gte": "ge",
    "lte": "le",
    "len_bytes": "len",
    "miss_default": "required",
}

special_type_rule_name_set = {
    "lt",
    "le",
    "gt",
    "ge",
    "const",
    "in",
    "not_in",
    "lt_now",
    "gt_now",
    "within",
    "min_pairs",
    "max_pairs",
}


def get_con_type_func_from_type_name(type_name: str) -> Optional[Callable]:
    if type_name == "string":
        return constr
    elif "double" in type_name or "float" in type_name:
        return confloat
    elif "int" in type_name:
        return conint
    elif type_name == "duration":
        return contimedelta
    elif type_name == "timestamp":
        return contimestamp
    elif type_name == "bytes":
        return conbytes
    else:
        return None


class BaseProtobufOptionToFieldInfo(object):
    @property
    def rule_dict(self) -> FieldInfoTypedDict:
        raise NotImplementedError

    def sub_value_handler(self, rule_value: Any) -> Dict[str, Any]:
        raise NotImplementedError

    def sub_type_name_handler(self, rule_value: Any) -> str:
        raise NotImplementedError

    def rule_value_to_field_value_handler(self, field_type_name: str, rule_name: str, rule_value: Any) -> Any:
        raise NotImplementedError

    def value_type_conversion_handler(self, field_type_name: str, rule_name: str, rule_value: Any) -> Tuple[bool, Any]:
        return False, rule_value

    def _core_handler(
        self,
        rule_dict: Dict[str, Any],
        *,
        field_name: str,
        field_type: int,
        type_name: str,
        full_name: str,
    ) -> FieldInfoTypedDict:
        """
        Adapt some Field verification information to convert it into verification information that is compatible with
         Protobuf's special type of pydantic
        """
        field_info_type_dict: FieldInfoTypedDict = {"extra": {}, "skip": False}
        for rule_name, rule_value in rule_dict.items():
            if rule_name in type_not_support_dict.get(field_type, type_not_support_dict["Any"]):
                # Exclude unsupported fields
                if field_type in protobuf_common_type_dict:
                    rule_name = f"{protobuf_common_type_dict[field_type]}.{rule_name}"
                elif field_type == 1:
                    rule_name = f"Message.{rule_name}"

                msg: str = f"{__name__} not support `{rule_name}` rule."
                if full_name:
                    msg = msg + f"(field:{full_name})"
                logger.warning(msg)
                continue
            is_change, new_rule_value = self.value_type_conversion_handler(type_name, rule_name, rule_value)
            if is_change:
                rule_value = new_rule_value

            if rule_name in pgv_column_to_pydantic_dict:
                # Field Conversion
                rule_name = pgv_column_to_pydantic_dict[rule_name]

            if type_name in ("duration", "any", "timestamp", "map") and rule_name in special_type_rule_name_set:
                # The verification of these parameters is handed over to the validator,
                # see protobuf_to_pydantic/customer_validator for details

                # Types of priority treatment for special cases
                if "validator" not in field_info_type_dict:
                    field_info_type_dict["validator"] = {}

                _rule_name: str = f"{type_name}_{rule_name}"
                validator_name = f"{field_name}_{_rule_name}_validator"

                field_info_type_dict["extra"][_rule_name] = self.rule_value_to_field_value_handler(
                    type_name, rule_name, rule_value
                )
                field_info_type_dict["validator"][validator_name] = _pydantic_adapter.field_validator(
                    field_name, allow_reuse=True
                )(validate_validator_dict[f"{_rule_name}_validator"])
                continue
            elif rule_name in ("in", "not_in", "len", "prefix", "suffix", "contains", "not_contains"):
                # The verification of these parameters is handed over to the validator,
                # see protobuf_to_pydantic/customer_validator for details

                # Compatible with PGV attributes that are not supported by pydantic
                if "validator" not in field_info_type_dict:
                    field_info_type_dict["validator"] = {}
                validator_name = f"{field_name}_{rule_name}_validator"
                # dict key not use python keyword
                _rule_name = rule_name + "_" if rule_name in ("in",) else rule_name
                field_info_type_dict["extra"][_rule_name] = self.rule_value_to_field_value_handler(
                    type_name, rule_name, rule_value
                )
                field_info_type_dict["validator"][validator_name] = _pydantic_adapter.field_validator(
                    field_name, allow_reuse=True
                )(validate_validator_dict[f"{rule_name}_validator"])
                continue
            elif rule_name in rule_name_pydantic_type_dict:
                # Support some built-in type judgments of PGV
                field_info_type_dict["type"] = rule_name_pydantic_type_dict[rule_name]
                continue
            elif rule_name in ("keys", "values"):
                # Parse the field data of the key and value in the map
                type_name = self.sub_type_name_handler(rule_value)
                # Nested types are supported via like constr

                con_type = get_con_type_func_from_type_name(type_name)
                if not con_type:
                    # TODO nested message
                    logger.warning(f"{__name__} not support sub type `{type_name}`, please reset {full_name}")
                    continue
                if "map_type" not in field_info_type_dict:
                    field_info_type_dict["map_type"] = {}
                con_type_param_dict: dict = {}
                # Generate information corresponding to the nested type
                sub_dict = self._core_handler(
                    self.sub_value_handler(rule_value),
                    field_name=field_name,
                    field_type=field_type,
                    type_name=type_name,
                    full_name=full_name,
                )
                for _key in inspect.signature(con_type).parameters.keys():
                    param_value = sub_dict.get(_key, None)  # type: ignore
                    if param_value is not None:
                        con_type_param_dict[_key] = param_value
                    elif "extra" in sub_dict:
                        if sub_dict["extra"].get(_key, None) is not None:
                            con_type_param_dict[_key] = sub_dict["extra"][_key]

                field_info_type_dict["map_type"][rule_name] = con_type(**con_type_param_dict)
            elif rule_name == "items":
                # Process array data
                type_name = self.sub_type_name_handler(rule_value)
                # Nested types are supported via like constr
                con_type = get_con_type_func_from_type_name(type_name)
                if not con_type:
                    # TODO nested message
                    logger.warning(f"{__name__} not support sub type `{type_name}`, please reset {full_name}")
                    field_info_type_dict["type"] = List
                    continue
                sub_dict = self._core_handler(
                    self.sub_value_handler(rule_value),
                    field_name=field_name,
                    field_type=field_type,
                    type_name=type_name,
                    full_name=full_name,
                )
                if "type" not in sub_dict:
                    sub_dict["type"] = con_type

                field_info_type_dict["type"] = conlist
                field_info_type_dict["sub"] = sub_dict

            field_info_type_dict[rule_name] = rule_value  # type: ignore
        return field_info_type_dict


type_not_support_dict: Dict[Any, Set[str]] = {
    FieldDescriptor.TYPE_BYTES: {"pattern"},
    FieldDescriptor.TYPE_STRING: {"min_bytes", "max_bytes", "well_known_regex", "strict"},
    "Any": {"ignore_empty", "defined_only", "no_sparse"},
}
