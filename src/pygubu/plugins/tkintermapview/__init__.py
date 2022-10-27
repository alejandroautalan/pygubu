import importlib
from typing import Optional
from pygubu.i18n import _
from pygubu.api.v1 import BuilderLoaderPlugin, IDesignerPlugin


_designer_tab_label = _("TkinterMapView")
_plugin_uid = "tkintermapview"


class TkinterMapViewLoader(BuilderLoaderPlugin, IDesignerPlugin):
    _module = "pygubu.plugins.tkintermapview.mapview"

    #
    # IPluginBase interface methods
    #
    def do_activate(self) -> bool:
        spec = importlib.util.find_spec("tkintermapview")
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
        return identifier.startswith("tkintermapview.")

    #
    # IDesignerPlugin interface methods
    #
    def configure_for_preview(self, builder_uid: str, widget):
        """Make widget just display with minimal functionality."""
        if builder_uid.endswith(f"{_plugin_uid}.TkinterMapView"):

            def _no_op(event=None):
                pass

            seqlist = (
                "<B1-Motion>",
                "<Button-1>",
                "<Button-2>",
                "<Button-3>",
                "<Button-4>",
                "<Button-5>",
                "<ButtonRelease-1>",
                "<MouseWheel>",
            )
            for seq in seqlist:
                widget.canvas.bind(seq, _no_op)
            widget.button_zoom_in.command = _no_op
            widget.button_zoom_out.command = _no_op
