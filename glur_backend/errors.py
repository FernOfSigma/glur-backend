from typing import Any

from .constants import METHODS


class InvalidMethodError(Exception):
    def __init__(self, method: str, *args: Any):
        super().__init__(*args)
        self.method = method

    def __str__(self) -> str:
        # Wrap every method name in single quotes.
        method_list = [f"'{method}'" for method in METHODS]
        return (
            f"Invalid HTTP method: '{self.method}': "
            f"Must be one of {', '.join(method_list)}"
        )
