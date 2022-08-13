import importlib
from pygubu.i18n import _
from pygubu.api.v1 import BuilderLoaderPlugin


_designer_tab_label = _("tksheet")
_plugin_uid = "tksheet"


class TksheetLoader(BuilderLoaderPlugin):
    _module = "pygubu.plugins.tksheet.sheet"

    def do_activate(self) -> bool:
        spec = importlib.util.find_spec("tksheet")
        return True if spec is not None else False

    def get_module_for(self, identifier: str) -> str:
        return self._module

    def get_all_modules(self):
        return (self._module,)

    def can_load(self, identifier: str) -> bool:
        return identifier.startswith("tksheet.")
