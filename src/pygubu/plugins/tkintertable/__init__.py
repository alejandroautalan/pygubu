import importlib
from typing import Optional
from pygubu.i18n import _
from pygubu.api.v1 import BuilderLoaderPlugin, IDesignerPlugin


_designer_tab_label = _("tkintertable")
_plugin_uid = "tkintertable"


class StandardTKWidgetsLoader(BuilderLoaderPlugin, IDesignerPlugin):
    _module = "pygubu.plugins.tkintertable.table"

    #
    # IPluginBase interface methods
    #
    def do_activate(self) -> bool:
        spec = importlib.util.find_spec("tkintertable")
        return True if spec is not None else False

    def get_designer_plugin(self) -> Optional[IDesignerPlugin]:
        return self

    #
    # IBuilderLoaderPlugin interface methods
    #
    def get_module_for(self, identifier: str) -> str:
        return self._module

    def get_all_modules(self):
        return (self._module,)

    def can_load(self, identifier: str) -> bool:
        return identifier.startswith("tkintertable.")

    #
    # IDesignerPlugin interface methods
    #
    def configure_for_preview(self, builder_uid: str, widget):
        """Make widget just display with minimal functionality."""
        if builder_uid.endswith(f"{_plugin_uid}.TableCanvas"):

            def _no_op(event=None):
                pass

            seqlist = (
                "<Button-1>",
                "<Button-2>",
                "<Button-3>",
                "<Button-4>",
                "<Button-5>",
                "<MouseWheel>" "<Double-Button-1>",
                "<Control-Button-1>",
                "<Shift-Button-1>",
                "<B1-Motion>",
            )
            for seq in seqlist:
                widget.bind(seq, _no_op)
