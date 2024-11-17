from functools import partial
from typing import Callable

import pytest
from google.protobuf import __version__
from pydantic import ValidationError

from example.populate_by_name_plugin_config import MyBaseSchema
from protobuf_to_pydantic import msg_to_pydantic_model
from protobuf_to_pydantic._pydantic_adapter import is_v1
from tests.base.base_demo_validate import (
    BaseTestAliasDemoValidator,
    BaseTestAllFieldSetOptionalDemoValidator,
    BaseTestDemoValidator,
    BaseTestSingleConfigValidator,
)
from tests.base.base_p2p_validate import local_dict

if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1.example.example_proto.demo import (
            alias_demo_pb2,
            all_feidl_set_optional_demo_pb2,
            demo_pb2,
            single_config_pb2,
        )
    else:
        from example.proto_pydanticv2.example.example_proto.demo import (  # type: ignore[no-redef]
            alias_demo_pb2,
            all_feidl_set_optional_demo_pb2,
            demo_pb2,
            single_config_pb2,
        )
else:
    if is_v1:
        from example.proto_3_20_pydanticv1.example.example_proto.demo import (  # type: ignore[no-redef]
            alias_demo_pb2,
            all_feidl_set_optional_demo_pb2,
            demo_pb2,
            single_config_pb2,
        )
    else:
        from example.proto_3_20_pydanticv2.example.example_proto.demo import (  # type: ignore[no-redef]
            alias_demo_pb2,
            all_feidl_set_optional_demo_pb2,
            demo_pb2,
            single_config_pb2,
        )

class TestAliasDemoValidator(BaseTestAliasDemoValidator):
    replace_message_fn: Callable = staticmethod(  # type: ignore
        partial(
            msg_to_pydantic_model,
            local_dict=local_dict,
            parse_msg_desc_method=alias_demo_pb2,
            pydantic_base=MyBaseSchema
        ))

    def test_alias_demo(self) -> None:
        super()._test_alias_demo(alias_demo_pb2.Report)

class TestAllFieldSetOptionalDemoValidator(BaseTestAllFieldSetOptionalDemoValidator):
    replace_message_fn: Callable = staticmethod(  # type: ignore
        partial(
            msg_to_pydantic_model,
            local_dict=local_dict,
            all_field_set_optional=True
        ))

    def test_user_message(self) -> None:
        super()._test_user_message(all_feidl_set_optional_demo_pb2.UserMessage)

    def test_other_message(self) -> None:
        super()._test_other_message(all_feidl_set_optional_demo_pb2.OtherMessage)

    def test_map_message(self) -> None:
        super()._test_map_message(all_feidl_set_optional_demo_pb2.MapMessage)

    def test_repeated_message(self) -> None:
        super()._test_repeated_message(all_feidl_set_optional_demo_pb2.RepeatedMessage)

    def test_after_refer_message(self) -> None:
        super()._test_after_refer_message(all_feidl_set_optional_demo_pb2.AfterReferMessage)

    def test_nested_message(self) -> None:
        super()._test_nested_message(all_feidl_set_optional_demo_pb2.NestedMessage)

    def test_invoice_item(self) -> None:
        super()._test_invoice_item(all_feidl_set_optional_demo_pb2.InvoiceItem)

    def test_empty_message(self) -> None:
        super()._test_empty_message(all_feidl_set_optional_demo_pb2.EmptyMessage)

    def test_optional_message(self) -> None:
        super()._test_optional_message(all_feidl_set_optional_demo_pb2.OptionalMessage)

    def test_invoice_item2(self) -> None:
        super(all_feidl_set_optional_demo_pb2.InvoiceItem2)

    def test_root_message(self) -> None:
        super(all_feidl_set_optional_demo_pb2.RootMessage)


class TestDemoValidator:
    pass

class TestSingleConfigValidator(BaseTestSingleConfigValidator):
    replace_message_fn: Callable = staticmethod(  # type: ignore
        partial(
            msg_to_pydantic_model,
            comment_prefix="aha",
            parse_msg_desc_method=single_config_pb2
        ))

    def test_user_message(self) -> None:
        super()._test_user_message(single_config_pb2.UserMessage)
