from abc import ABC, abstractmethod


class BuilderLoader:
    @abstractmethod
    def get_module_path(self, identifier: str) -> str:
        ...

    @abstractmethod
    def can_load(self, identifier: str) -> bool:
        ...
