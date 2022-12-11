from abc import ABC, ABCMeta, abstractmethod
from typing import Optional


class PluginRegistry(ABCMeta):
    plugins = []

    def __init__(cls, name, bases, attrs):
        if name not in (
            "IPluginBase",
            "BuilderLoaderPlugin",
        ):
            PluginRegistry.plugins.append(cls)


class IDesignerPlugin(ABC):
    def get_preview_builder(self, builder_uid: str):
        """Return a BuilderObject subclass used to build a preview
        for the target builder_uid"""
        return None

    def get_toplevel_preview_for(
        self, builder_uid: str, widget_id: str, builder, top_master
    ):
        """Return a Toplevel with the target widget_id rendered inside."""
        return None

    def configure_for_preview(self, builder_uid: str, widget):
        """Make widget just display with minimal functionality."""
        pass

    def ensure_visibility_in_preview(self, builder, selected_uid: str):
        """Ensure visibility of selected_uid in preview.
        Usage example:
            Activate a tab of a Notebook if the selected widget is
            inside the notebook.
        """
        pass


class IPluginBase(ABC, metaclass=PluginRegistry):
    @abstractmethod
    def do_activate(self) -> bool:
        "Initialize plugin and return if it is operational or not."
        ...

    def get_designer_plugin(self) -> Optional[IDesignerPlugin]:
        """Return class instance that implements IDesignerPlugin"""
        return None


class IBuilderLoaderPlugin(ABC):
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


class BuilderLoaderPlugin(IBuilderLoaderPlugin, IPluginBase):
    pass
