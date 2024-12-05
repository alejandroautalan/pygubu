import importlib
from pygubu.i18n import _
from pygubu.api.v1 import BuilderLoaderPlugin


_designer_tab_label = _("TkinterWeb")
_plugin_uid = "tkinterweb"


class TkinterwebLoader(BuilderLoaderPlugin):
    module_map = {
        "pygubu.plugins.tkinterweb.htmlwidgets": (
            f"{_plugin_uid}.HtmlFrame",
            f"{_plugin_uid}.HtmlLabel",
        ),
        "pygubu.plugins.tkinterweb.extrawidgets": (
            f"{_plugin_uid}.Notebook",
            f"{_plugin_uid}.ColourSelector",
        ),
    }

    def do_activate(self) -> bool:
        spec = importlib.util.find_spec("tkinterweb")
        return spec is not None

    def get_module_for(self, identifier: str) -> str:
        for module, identifiers in self.module_map.items():
            if identifier in identifiers:
                return module
        return None

    def get_all_modules(self):
        return [m for m in self.module_map.keys()]

    def can_load(self, identifier: str) -> bool:
        return identifier.startswith("tkinterweb.")

    def get_designer_plugin(self):
        """Load class that implements IDesignerPlugin"""

        # Just load the module for properties definitions.
        from .designer.designerplugin import TkinterwebPlugin

        return None
