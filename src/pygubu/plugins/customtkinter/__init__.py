import importlib
from pygubu.i18n import _
from pygubu.api.v1 import IPluginBase, IBuilderLoaderPlugin, IDesignerPlugin


_designer_tab_label = _("CustomTkinter")
_plugin_uid = "customtkinter"


class CTkBuilderLoader(IBuilderLoaderPlugin, IPluginBase):
    module_map = {
        "pygubu.plugins.customtkinter.windows": (
            f"{_plugin_uid}.CTkToplevel",
            f"{_plugin_uid}.CTk",
        ),
        "pygubu.plugins.customtkinter.widgets": (
            f"{_plugin_uid}.CTkFrame",
            f"{_plugin_uid}.CTkLabel",
            f"{_plugin_uid}.CTkProgressBar",
            f"{_plugin_uid}.CTkButton",
            f"{_plugin_uid}.CTkSlider",
            f"{_plugin_uid}.CTkEntry",
            f"{_plugin_uid}.CTkOptionMenu",
            f"{_plugin_uid}.CTkComboBox",
            f"{_plugin_uid}.CTkCheckBox",
            f"{_plugin_uid}.CTkRadioButton",
            f"{_plugin_uid}.CTkSwitch",
            f"{_plugin_uid}.CTkTextbox",
            f"{_plugin_uid}.CTkCanvas",
            f"{_plugin_uid}.CTkScrollbar",
            f"{_plugin_uid}.CTkTabview",
        ),
    }

    def do_activate(self) -> bool:
        spec = importlib.util.find_spec("customtkinter")
        return True if spec is not None else False

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
