from enum import IntEnum
from typing import Set, Tuple, Type

from pydantic import BaseModel


def _pydantic_model_to_py_code(model: Type[BaseModel]) -> Tuple[Set[str], Set[str], Set[str]]:
    import_set: Set[str] = {"from pydantic import BaseModel"}
    depend_set: Set[str] = set()
    class_str: str = f"class {model.__name__}(BaseModel):\n"
    for key, value in model.__fields__.items():
        if value.type_.__module__ != "builtins":
            if issubclass(value.type_, IntEnum):
                import_set.add("from enum import IntEnum")
                depend_set_str = f"class {value.type_.__name__}(IntEnum):\n"
                for enum_name, enum_value in value.type_.__members__.items():
                    depend_set_str += " " * 4 + f"{enum_name} = {enum_value.value}\n"
                depend_set.add(depend_set_str)
        import_set.add(f"from {value.field_info.__module__} import {value.field_info.__class__.__name__}\n")
        class_str = class_str + " " * 4 + f"{key}: {value.type_.__name__} = {value.field_info.__repr__()}\n"
    return import_set, depend_set, {class_str}


def pydantic_model_to_py_code(*model: Type[BaseModel]) -> str:
    import_set: Set[str] = set()
    depend_set: Set[str] = set()
    class_set: Set[str] = set()
    for _model in model:
        _import_set, _depend_set, _class_set = _pydantic_model_to_py_code(_model)
        if _import_set:
            import_set.update(_import_set)
        if _depend_set:
            depend_set.update(_depend_set)
        if _class_set:
            class_set.update(_class_set)

    content_str: str = "\n".join(sorted(import_set))
    if depend_set:
        content_str += "\n\n"
        content_str += "\n".join(sorted(depend_set))
    if class_set:
        content_str += "\n\n"
        content_str += "\n\n".join(class_set)

    return content_str
