from typing import Any

from pydantic import confloat, conint
from pydantic.fields import FieldInfo

from protobuf_to_pydantic.gen_model import DescTemplate


class CustomerField(FieldInfo):
    pass


def customer_any() -> Any:
    return Any()  # type: ignore


desc_template: DescTemplate = DescTemplate(
    local_dict={
        "CustomerField": CustomerField,
        "confloat": confloat,
        "conint": conint,
        "customer_any": customer_any,
    },
    comment_prefix="p2p",
)
