import logging
from typing import Dict, Set, Type

from protobuf_to_pydantic.constant import protobuf_common_type_dict
from protobuf_to_pydantic.field_info_rule.protobuf_option_to_field_info.desc import gen_field_info_dict_from_field_desc
from protobuf_to_pydantic.field_info_rule.types import MessageOptionTypedDict, OneOfTypedDict
from protobuf_to_pydantic.grpc_types import Descriptor, FieldDescriptor, Message

_logger: logging.Logger = logging.getLogger(__name__)

_global_message_option_dict: Dict[str, Dict[str, MessageOptionTypedDict]] = {}


class ParseFromPbOption(object):
    protobuf_pkg: str  # Extend the package name of protobuf

    def __init__(self, message: Type[Message]):
        self.message = message
        self._message_option_dict: Dict[str, MessageOptionTypedDict] = {}
        if self.protobuf_pkg not in _global_message_option_dict:
            _global_message_option_dict[self.protobuf_pkg] = self._message_option_dict
        else:
            self._message_option_dict = _global_message_option_dict[self.protobuf_pkg]

    def parse(self) -> Dict[str, MessageOptionTypedDict]:
        descriptor: Descriptor = self.message.DESCRIPTOR
        if descriptor.name in self._message_option_dict:
            return self._message_option_dict

        self._message_option_dict[descriptor.name] = self.get_message_option_dict_from_desc(descriptor)
        return self._message_option_dict

    def get_message_option_dict_from_desc(self, descriptor: Descriptor) -> MessageOptionTypedDict:  # noqa:C901
        """Extract the information of each field through the Options of Protobuf Message"""
        if descriptor.name in self._message_option_dict:
            return self._message_option_dict[descriptor.name]
        message_option_dict: MessageOptionTypedDict = {"message": {}, "one_of": {}, "nested": {}, "metadata": {}}

        # Options for processing Messages
        for option_descriptor, option_value in descriptor.GetOptions().ListFields():
            # If parsing is disabled, Options will not continue to be parsed, and empty information will be set
            if (option_descriptor.full_name == f"{self.protobuf_pkg}.disabled" and option_value) or (
                option_descriptor.full_name == f"{self.protobuf_pkg}.ignored" and option_value
            ):
                return message_option_dict
        # Handle one_ofs of Message
        one_of_dict: Dict[str, OneOfTypedDict] = {}
        for one_of in descriptor.oneofs:
            required: bool = False
            optional_fields: Set[str] = set()
            for one_of_descriptor, one_ov_value in one_of.GetOptions().ListFields():
                if one_of_descriptor.full_name == f"{self.protobuf_pkg}.required":
                    required = True
                    # if one_of.full_name in self._msg_desc_dict:
                    #     continue
                    # Support one of is required
                elif one_of_descriptor.full_name == f"{self.protobuf_pkg}.oneof_extend":
                    # Support one of is optional
                    for one_of_extend_field_descriptor, result in one_ov_value.ListFields():
                        for one_of_optional_name in result:
                            optional_fields.add(one_of_optional_name)

            if required or optional_fields:
                one_of_dict[one_of.full_name] = {
                    "required": required,
                    "optional_fields": optional_fields,
                    # optional cannot get the value of the current one of,
                    # so it needs to be processed in subsequent processing
                    "fields": set(),
                }
        if one_of_dict:
            message_option_dict["one_of"] = one_of_dict
        # Process all fields of Message
        for field in descriptor.fields:
            type_name: str = ""
            if field.type == FieldDescriptor.TYPE_MESSAGE:
                # Convert some types of Protobuf
                message_type_name: str = field.message_type.name
                if message_type_name in ("Duration", "Any", "Timestamp", "Struct"):
                    type_name = message_type_name.lower()
                elif message_type_name.endswith("Entry"):
                    type_name = "map"
                elif message_type_name == "Empty":
                    continue
                else:
                    type_name = "message"
            if field.label == FieldDescriptor.LABEL_REPEATED and not (
                field.message_type and field.message_type.name.endswith("Entry")
            ):
                # Support Protobuf.RepeatedXXX
                type_name = "repeated"
            if not type_name:
                # Support Protobuf common type
                type_name = protobuf_common_type_dict.get(field.type, "")
                if not type_name:
                    _logger.warning(
                        f"{__name__} not support protobuf type id:{field.type} from field name{field.full_name}"
                    )
                    continue
            field_info_dict = gen_field_info_dict_from_field_desc(type_name, field.full_name, field, self.protobuf_pkg)
            if field_info_dict["skip"]:
                # If skip is True, the corresponding validation rule is not applied
                continue
            message_option_dict["message"][field.name] = field_info_dict
            if type_name == "message":
                message_option_dict["nested"][field.message_type.name] = self.get_message_option_dict_from_desc(
                    field.message_type
                )
            elif type_name == "map":
                for sub_field in field.message_type.fields:
                    if not sub_field.message_type:
                        continue
                    # keys and values
                    message_option_dict["nested"][sub_field.message_type.name] = self.get_message_option_dict_from_desc(
                        sub_field.message_type
                    )
        self._message_option_dict[descriptor.name] = message_option_dict
        return message_option_dict
