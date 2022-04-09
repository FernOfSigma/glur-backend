from .constants import METHODS


class InvalidMethodError(Exception):
    def __init__(self, method, *args):
        super().__init__(*args)
        self.method = method

    def __str__(self):
        # Wrap every method name in single quotes.
        method_list = [f"'{method}'" for method in METHODS]
        return (
            f"Invalid HTTP method: '{self.method}': "
            f"Must be one of {', '.join(method_list)}"
        )
