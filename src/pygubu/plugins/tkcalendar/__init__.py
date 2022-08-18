import importlib
from pygubu.i18n import _
from pygubu.api.v1 import BuilderLoaderPlugin


_designer_tab_label = _("tkcalendar")
_plugin_uid = "tkcalendar"


class TkcalendarLoader(BuilderLoaderPlugin):
    module_map = {
        "pygubu.plugins.tkcalendar.calendar": (f"{_plugin_uid}.Calendar",),
        "pygubu.plugins.tkcalendar.dateentry": (f"{_plugin_uid}.DateEntry",),
    }

    def do_activate(self) -> bool:
        spec = importlib.util.find_spec("tkcalendar")
        return True if spec is not None else False

    def get_module_for(self, identifier: str) -> str:
        for module, identifiers in self.module_map.items():
            if identifier in identifiers:
                return module
        return None

    def get_all_modules(self):
        return [m for m in self.module_map.keys()]

    def can_load(self, identifier: str) -> bool:
        return identifier.startswith("tkcalendar.")
