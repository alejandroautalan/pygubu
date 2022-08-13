import importlib
from pygubu.i18n import _
from pygubu.api.v1 import BuilderLoaderPlugin

_designer_tab_label = _("ttkwidgets")
_plugin_uid = "ttkwidgets"


class TtkWidgetsLoader(BuilderLoaderPlugin):
    module_map = {
        "pygubu.plugins.ttkwidgets.calendar": (f"{_plugin_uid}.Calendar",),
        "pygubu.plugins.ttkwidgets.checkboxtreeview": (
            f"{_plugin_uid}.CheckboxTreeview",
        ),
        "pygubu.plugins.ttkwidgets.itemscanvas": (
            f"{_plugin_uid}.ItemsCanvas",
        ),
        "pygubu.plugins.ttkwidgets.linklabel": (f"{_plugin_uid}.LinkLabel",),
        "pygubu.plugins.ttkwidgets.scaleentry": (f"{_plugin_uid}.ScaleEntry",),
        "pygubu.plugins.ttkwidgets.scrolledlistbox": (
            f"{_plugin_uid}.ScrolledListbox",
        ),
        "pygubu.plugins.ttkwidgets.table": (f"{_plugin_uid}.Table",),
        "pygubu.plugins.ttkwidgets.tickscale": (f"{_plugin_uid}.TickScale",),
        "pygubu.plugins.ttkwidgets.frames": (
            f"{_plugin_uid}.ScrolledFrame",
            f"{_plugin_uid}.ToggledFrame",
        ),
        "pygubu.plugins.ttkwidgets.color": (
            f"{_plugin_uid}.AlphaBar",
            f"{_plugin_uid}.ColorSquare",
            f"{_plugin_uid}.GradientBar",
        ),
        "pygubu.plugins.ttkwidgets.autocomplete": (
            f"{_plugin_uid}.AutocompleteEntry",
            f"{_plugin_uid}.AutocompleteEntryListbox",
            f"{_plugin_uid}.AutocompleteCombobox",
        ),
        "pygubu.plugins.ttkwidgets.font": (
            f"{_plugin_uid}.FontFamilyDropdown",
            f"{_plugin_uid}.FontFamilyListbox",
            f"{_plugin_uid}.FontSelectFrame",
            f"{_plugin_uid}.FontPropertiesFrame",
            f"{_plugin_uid}.FontSizeDropdown",
        ),
    }

    def do_activate(self) -> bool:
        spec = importlib.util.find_spec("ttkwidgets")
        return True if spec is not None else False

    def get_module_for(self, identifier: str) -> str:
        for module, identifiers in self.module_map.items():
            if identifier in identifiers:
                return module
        return None

    def get_all_modules(self):
        return [m for m in self.module_map.keys()]

    def can_load(self, identifier: str) -> bool:
        return identifier.startswith("ttkwidgets.")
