from abc import ABC, abstractmethod


class DataTransformer(ABC):
    @abstractmethod
    def transform(value):
        ...

    @abstractmethod
    def reversetransform(value):
        ...


class NoopTransfomer(DataTransformer):
    def transform(value):
        return value

    def reversetransform(value):
        return value
