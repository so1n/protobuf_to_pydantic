from protobuf_to_pydantic._pydantic_adapter import is_v1

if is_v1:
    from .v1 import *  # noqa
else:
    from .v2 import *  # noqa

from .rule import set_now_default_factory
