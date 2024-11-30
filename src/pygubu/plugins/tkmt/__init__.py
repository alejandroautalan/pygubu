import importlib
from pygubu.i18n import _
from pygubu.api.v1 import BuilderLoaderPlugin


_designer_tab_label = _("TkinterModernThemes")
_plugin_uid = "tkmt"


class TkmthemesLoader(BuilderLoaderPlugin):
    module_map = {
        "pygubu.plugins.tkmt.widgets": (f"{_plugin_uid}.ThemedTKinterFrame",),
    }

    def do_activate(self) -> bool:
        spec = importlib.util.find_spec("TKinterModernThemes")
        return spec is not None

    def get_module_for(self, identifier: str) -> str:
        for module, identifiers in self.module_map.items():
            if identifier in identifiers:
                return module
        return None

    def get_all_modules(self):
        return [m for m in self.module_map.keys()]

    def can_load(self, identifier: str) -> bool:
        for module, builders in self.module_map.items():
            if identifier in builders:
                return True
        return False

    def get_designer_plugin(self):
        """Load class that implements IDesignerPlugin"""
        from .designer.designerplugin import PygubuDesignerPlugin

        return PygubuDesignerPlugin()
