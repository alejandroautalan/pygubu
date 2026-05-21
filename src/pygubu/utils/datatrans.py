import json


class DataTransformer:
    def __init__(self, default_value=None, on_error_default=None):
        self.default_value = default_value
        self.on_error_default = on_error_default

    def transform(self, value: str, default=None):
        return value


class ListDTO(DataTransformer):
    def __init__(self, default_value=None, on_error_default=None):
        super().__init__(
            default_value,
            ["Invalid data"] if on_error_default is None else on_error_default,
        )

    def transform(self, value: str, default=None):
        val = self.default_value if default is None else default
        try:
            json_list = json.loads(value)
            if isinstance(json_list, list):
                val = json_list
            else:
                val = self.on_error_default
        except json.JSONDecodeError:
            val = self.on_error_default
        return val
