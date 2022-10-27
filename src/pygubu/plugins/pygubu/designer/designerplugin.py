from pygubu.api.v1 import IDesignerPlugin
from .toplevelframe import ToplevelFramePreviewBO


class PygubuDesignerPlugin(IDesignerPlugin):
    def get_preview_builder(self, builder_uid: str):
        if builder_uid in ("tk.Toplevel", "pygubu.builder.widgets.dialog"):
            return ToplevelFramePreviewBO
        return None

    def get_toplevel_preview_for(
        self, builder_uid: str, widget_id: str, builder, top_master
    ):
        top = None
        if builder_uid == "tk.Toplevel":
            top = builder.get_object(widget_id, top_master)
        elif builder_uid == "pygubu.builder.widgets.dialog":
            dialog = builder.get_object(widget_id, top_master)
            dialog.run()
            top = dialog.toplevel
        return top

    def configure_for_preview(self, builder_uid: str, widget):
        """Make widget just display with minimal functionality."""
        pass
