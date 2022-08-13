import importlib
from pygubu.i18n import _
from pygubu.api.v1 import BuilderLoaderPlugin

_designer_tab_label = _("AwesomeTkinter")
_plugin_uid = "awesometkinter"


class AwesometkinterLoader(BuilderLoaderPlugin):
    module_map = {
        "pygubu.plugins.awesometkinter.frame": (
            f"{_plugin_uid}.Frame3d",
            f"{_plugin_uid}.ScrollableFrame",
        ),
        "pygubu.plugins.awesometkinter.button": (
            f"{_plugin_uid}.Button3d",
            f"{_plugin_uid}.Radiobutton",
            f"{_plugin_uid}.Checkbutton",
        ),
        "pygubu.plugins.awesometkinter.label": (
            f"{_plugin_uid}.AutoWrappingLabel",
            f"{_plugin_uid}.AutofitLabel",
        ),
        "pygubu.plugins.awesometkinter.progressbar": (
            f"{_plugin_uid}.RadialProgressbar",
            f"{_plugin_uid}.RadialProgressbar3d",
            f"{_plugin_uid}.Segmentbar",
        ),
        "pygubu.plugins.awesometkinter.scrollbar": (
            f"{_plugin_uid}.SimpleScrollbar",
        ),
        "pygubu.plugins.awesometkinter.text": (f"{_plugin_uid}.ScrolledText",),
    }

    def do_activate(self) -> bool:
        spec = importlib.util.find_spec("awesometkinter")
        return True if spec is not None else False

    def get_module_for(self, identifier: str) -> str:
        for module, identifiers in self.module_map.items():
            if identifier in identifiers:
                return module
        return None

    def get_all_modules(self):
        return [m for m in self.module_map.keys()]

    def can_load(self, identifier: str) -> bool:
        return identifier.startswith("awesometkinter.")
