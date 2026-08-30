import importlib
from typing import List
from pygubu.i18n import _
from pygubu.api.v1 import IPluginBase, IBuilderLoaderPlugin, IDesignerPlugin
from ._config import namespace, nsctk


class CTkBuilderLoader(IBuilderLoaderPlugin, IPluginBase):
    module_map = {
        "pygubu.plugins.customtkinter.windows": (
            nsctk.CTkToplevel,
            nsctk.CTk,
        ),
        "pygubu.plugins.customtkinter.widgets": (
            nsctk.CTkFrame,
            nsctk.CTkLabel,
            nsctk.CTkProgressBar,
            nsctk.CTkButton,
            nsctk.CTkSlider,
            nsctk.CTkEntry,
            nsctk.CTkOptionMenu,
            nsctk.CTkComboBox,
            nsctk.CTkCheckBox,
            nsctk.CTkRadioButton,
            nsctk.CTkSwitch,
            nsctk.CTkTextbox,
            nsctk.CTkCanvas,
            nsctk.CTkScrollbar,
            nsctk.CTkScrollableFrame,
        ),
        "pygubu.plugins.customtkinter.tabview": (nsctk.CTkTabview,),
        "pygubu.plugins.customtkinter.scrollableframe": (
            nsctk.CTkScrollableFrame,
        ),
    }

    @classmethod
    def get_uid(cls) -> str:
        """Return plugin unique ID."""
        return "pygubu_customtkinter"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        """Return a list of required plugins UID."""
        return ["pygubu"]

    def do_activate(self) -> bool:
        spec = importlib.util.find_spec("customtkinter")
        return spec is not None

    def get_module_for(self, identifier: str) -> str:
        for module, identifiers in self.module_map.items():
            if identifier in identifiers:
                return module
        return None

    def get_all_modules(self):
        return [m for m in self.module_map.keys()]

    def can_load(self, identifier: str) -> bool:
        return identifier.startswith("customtkinter.")

    def get_designer_plugin(self):
        """Load class that implements IDesignerPlugin"""
        from .designer.designerplugin import CTkDesignerPlugin

        return CTkDesignerPlugin()
