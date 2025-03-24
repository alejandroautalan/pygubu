from abc import ABC, abstractmethod
from typing import Optional, Any, List
from urllib.parse import urlparse
from functools import reduce
from enum import Enum, auto


class ResourceError(Exception):
    ...


class ResourceValue(Enum):
    UNDEFINED = auto()


class ResouceDefinition:
    def __init__(self, uid: str, meta: dict = None):
        self.uid = uid
        self.meta = {} if meta is None else meta

    def __repr__(self):
        return f"{type(self).__name__}({self.uid}, {self.meta})"


class IDataPool(ABC):
    """A generic pool of data."""

    @abstractmethod
    def get_resource(
        self, uri: str, *, default_value=ResourceValue.UNDEFINED, **kw
    ) -> Any:
        """Get resource value from pool.

        If value for uri is not defined, must return ResourceValue.UNDEFINED
        If uri is invalid, must return ResourceError
        For any other error must return ResourceError
        """
        ...

    def get_uri_path(self, uri: str) -> str:
        try:
            result = urlparse(uri)
            if all([result.scheme == "res", result.netloc]):
                return f"{result.netloc}{result.path}"
        except AttributeError:
            pass
        raise ResourceError(f"Invalid URI: {uri}")


class DictDataPool(IDataPool):
    def __init__(self, data: dict = None):
        self.data = {} if data is None else data

    def get_resource(
        self, uri: str, *, default_value=ResourceValue.UNDEFINED, **kw
    ) -> Any:
        path = self.get_uri_path(uri)
        return self.deep_get(self.data, path, default_value)

    def deep_get(self, dictionary, keys, default):
        return reduce(
            lambda d, key: d.get(key, default)
            if isinstance(d, dict)
            else default,
            keys.split("/"),
            dictionary,
        )


class ChainedResoucePool(IDataPool):
    def __init__(self, chain: List[IDataPool]):
        self.chain = chain

    def get_resource(
        self, uri: str, *, default_value=ResourceValue.UNDEFINED, **kw
    ) -> Any:
        value = ResourceValue.UNDEFINED
        for rpool in self.chain:
            value = rpool.get_resource(uri, **kw)
            is_undefined = (
                isinstance(value, ResourceValue)
                and value == ResourceValue.UNDEFINED
            )
            if not is_undefined:
                break
        is_undefined = (
            isinstance(value, ResourceValue)
            and value == ResourceValue.UNDEFINED
        )
        if is_undefined:
            value = default_value
        return value


class PygubuResourcePool(IDataPool):
    ...


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
        except ResourceError:
            print("Invalid uri error:", uri)

    print("Chained test:")
    data1 = dict(dog_age=5)
    data2 = dict(dog_age=10, dog_name="generic dog")
    pool_a = DictDataPool(data1)
    pool_b = DictDataPool(data2)
    pool_chain = ChainedResoucePool([pool_a, pool_b])
    rlist = [
        "res://dog_age",
        "res://dog_name",
        "res://dog_failed",
        "ftp//invalid_uri",
    ]
    for uri in rlist:
        try:
            res = pool_chain.get_resource(uri)
            print(res)
        except ResourceError:
            print("Invalid uri error:", uri)
    print("Test default value:")
    uri = "res://dog_not_exist"
    value = pool_chain.get_resource(uri, default_value=None)
    print(f"Value for {uri} -> {value}")
