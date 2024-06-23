from abc import ABC, abstractmethod
from typing import Optional, Any
from urllib.parse import urlparse
from functools import reduce


class InvalidURIError(Exception):
    ...


class IDataPool(ABC):
    """A generic pool of data."""

    @abstractmethod
    def get_resource(self, uri: str) -> Any:
        ...

    def get_uri_path(self, uri: str) -> str:
        try:
            result = urlparse(uri)
            if all([result.scheme == "res", result.netloc]):
                return f"{result.netloc}{result.path}"
        except AttributeError:
            pass
        raise InvalidURIError(uri)


class DictDataPool(IDataPool):
    def __init__(self, data: dict = None):
        self.data = {} if data is None else data

    def get_resource(self, uri: str) -> Any:
        path = self.get_uri_path(uri)
        return self.deep_get(self.data, path)

    def deep_get(self, dictionary, keys, default=None):
        return reduce(
            lambda d, key: d.get(key, default)
            if isinstance(d, dict)
            else default,
            keys.split("/"),
            dictionary,
        )


if __name__ == "__main__":
    data = {"value_a": 185, "lists": {"dogs": [10, 20, 30]}}
    pool = DictDataPool(data)
    rlist = [
        "res://value_a",
        "res://lists/dogs",
        "something",
        "res://lists/dogs//failed",
    ]
    for uri in rlist:
        try:
            res = pool.get_resource(uri)
            print(res)
        except InvalidURIError:
            print("Invalid uri error:", uri)
