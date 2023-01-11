import json


class ListDTO:
    def transform(self, value: str):
        val = None
        try:
            val = json.loads(value)
        except json.JSONDecodeError:
            val = ["invalid data"]
        return val
