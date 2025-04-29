import pytest
from google.protobuf import __version__
from pydantic import ValidationError

from protobuf_to_pydantic._pydantic_adapter import is_v1
from tests.base.base_demo_validate import (
    BaseTestAliasDemoValidator,
    BaseTestAllFieldSetOptionalDemoValidator,
    BaseTestCustomCommentHandler,
    BaseTestDemoValidator,
    BaseTestSingleConfigValidator,
)

if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1.example.example_proto.demo import (  # type: ignore[no-redef]
            alias_demo_p2p,
            all_feidl_set_optional_demo_p2p,
            custom_comment_handler_p2p,
            demo_p2p,
            single_config_p2p,
        )
    else:
        from example.proto_pydanticv2.example.example_proto.demo import (  # type: ignore[no-redef]
            alias_demo_p2p,
            all_feidl_set_optional_demo_p2p,
            custom_comment_handler_p2p,
            demo_p2p,
            single_config_p2p,
        )
else:
    if is_v1:
        from example.proto_3_20_pydanticv1.example.example_proto.demo import (  # type: ignore[no-redef]
            alias_demo_p2p,
            all_feidl_set_optional_demo_p2p,
            custom_comment_handler_p2p,
            demo_p2p,
            single_config_p2p,
        )
    else:
        from example.proto_3_20_pydanticv2.example.example_proto.demo import (  # type: ignore[no-redef]
            alias_demo_p2p,
            all_feidl_set_optional_demo_p2p,
            custom_comment_handler_p2p,
            demo_p2p,
            single_config_p2p,
        )

class TestAliasDemoValidator(BaseTestAliasDemoValidator):
    def test_alias_demo(self) -> None:
        super()._test_alias_demo(alias_demo_p2p.Report)

class TestAllFieldSetOptionalDemoValidator(BaseTestAllFieldSetOptionalDemoValidator):
    def test_user_message(self) -> None:
        super()._test_user_message(all_feidl_set_optional_demo_p2p.UserMessage)

    def test_other_message(self) -> None:
        super()._test_other_message(all_feidl_set_optional_demo_p2p.OtherMessage)

    def test_map_message(self) -> None:
        super()._test_map_message(all_feidl_set_optional_demo_p2p.MapMessage)

    def test_repeated_message(self) -> None:
        super()._test_repeated_message(all_feidl_set_optional_demo_p2p.RepeatedMessage)

    def test_after_refer_message(self) -> None:
        super()._test_after_refer_message(all_feidl_set_optional_demo_p2p.AfterReferMessage)

    def test_nested_message(self) -> None:
        super()._test_nested_message(all_feidl_set_optional_demo_p2p.NestedMessage)

    def test_invoice_item(self) -> None:
        super()._test_invoice_item(all_feidl_set_optional_demo_p2p.InvoiceItem)

    def test_empty_message(self) -> None:
        super()._test_empty_message(all_feidl_set_optional_demo_p2p.EmptyMessage)

    def test_optional_message(self) -> None:
        super()._test_optional_message(all_feidl_set_optional_demo_p2p.OptionalMessage)

    def test_invoice_item2(self) -> None:
        super(all_feidl_set_optional_demo_p2p.InvoiceItem2)

    def test_root_message(self) -> None:
        super(all_feidl_set_optional_demo_p2p.RootMessage)


class TestDemoValidator:
    pass

class TestSingleConfigValidator(BaseTestSingleConfigValidator):

    def test_user_message(self) -> None:
        super()._test_user_message(single_config_p2p.UserMessage)


class TestTestCustomCommentHandler(BaseTestCustomCommentHandler):
    def test_user_message(self) -> None:
        super()._test_user_message(custom_comment_handler_p2p.UserMessage)
