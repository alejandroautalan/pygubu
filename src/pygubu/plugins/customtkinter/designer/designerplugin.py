from pygubu.api.v1 import IPluginBase, IDesignerPlugin
from .preview import CTkToplevelPreviewBO, CTkPreviewBO


class CTkDesignerPlugin(IDesignerPlugin):
    def get_preview_builder(self, builder_uid: str):
        if builder_uid == "customtkinter.CTkToplevel":
            return CTkToplevelPreviewBO
        if builder_uid == "customtkinter.CTk":
            return CTkPreviewBO
        return None

    def get_toplevel_preview_for(
        self, builder_uid: str, widget_id: str, builder, top_master
    ):
        top = None
        toplevel_uids = ("customtkinter.CTkToplevel", "customtkinter.CTk")
        if builder_uid in toplevel_uids:
            top = builder.get_object(widget_id)
        return top
