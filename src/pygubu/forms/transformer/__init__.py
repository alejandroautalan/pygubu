from abc import ABC, abstractmethod


"""
Model transformers:

        transform(): "model data" => "norm data"
        reverseTransform(): "norm data" => "model data"

View transformers:

        transform(): "norm data" => "view data"
        reverseTransform(): "view data" => "norm data


 Model data     <|
 |               |
 | transform     | reverse transform
 |               |
 |>              |
    Norm data
 |              <|
 | transform     |
 |>              | reverse transform
    View data    |
"""


class DataTransformer(ABC):
    @abstractmethod
    def transform(self, value):
        ...

    @abstractmethod
    def reversetransform(self, value):
        ...


class NoopTransfomer(DataTransformer):
    def transform(self, value):
        return value

    def reversetransform(self, value):
        return value


class TransformationError(Exception):
    ...
