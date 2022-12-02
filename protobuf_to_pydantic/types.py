from typing import Set

from typing_extensions import TypedDict


class OneOfTypedDict(TypedDict):
    required: bool
    fields: Set[str]
