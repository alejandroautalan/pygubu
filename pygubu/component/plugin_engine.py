from abc import ABC, ABCMeta, abstractmethod


class PluginRegistry(ABCMeta):
    plugins = []

    def __init__(cls, name, bases, attrs):
        if name not in (
            "IPluginBase",
            "BuilderLoaderPlugin",
        ):
            PluginRegistry.plugins.append(cls)


class IPluginBase(ABC, metaclass=PluginRegistry):
    @abstractmethod
    def do_activate(self) -> bool:
        "Initialize plugin and return if it is operational or not."
        ...


class BuilderLoaderPlugin(IPluginBase):
    @abstractmethod
    def get_module_for(self, identifier: str) -> str:
        "Return module name for specified identifier."
        ...

    @abstractmethod
    def get_all_modules(self):
        "Return an iterable with module names of all builders."
        ...

    @abstractmethod
    def can_load(self, identifier: str) -> bool:
        "Return if this loader can manage specified identifier."
        ...
