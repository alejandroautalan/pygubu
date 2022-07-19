from abc import ABC, ABCMeta, abstractmethod


class PluginRegistry(ABCMeta):
    plugins = []

    def __init__(cls, name, bases, attrs):
        if name not in ("BuilderLoaderPlugin",):
            PluginRegistry.plugins.append(cls)


class BuilderLoaderPlugin(ABC, metaclass=PluginRegistry):
    @abstractmethod
    def get_module_for(self, identifier: str) -> str:
        ...

    @abstractmethod
    def get_all_modules(self):
        ...

    @abstractmethod
    def can_load(self, identifier: str) -> bool:
        ...
