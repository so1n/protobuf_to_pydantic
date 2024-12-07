import difflib


def pytest_assertrepr_compare(op, left, right):  # type: ignore
    if isinstance(left, str) and isinstance(right, str) and op == "in":
        return "".join(difflib.context_diff(left, right)).split("\n")
