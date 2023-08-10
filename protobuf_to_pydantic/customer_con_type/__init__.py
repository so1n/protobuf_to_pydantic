from protobuf_to_pydantic._pydantic_adapter import is_v1

if is_v1:
    from .v1 import *
else:
    from .v2 import *
