from pygubu.api.v1 import IPluginBase, IDesignerPlugin
from pygubu.utils.widget import crop_widget
from .preview import (
    CTkToplevelPreviewBO,
    CTkPreviewBO,
    CTkFramePreviewBO,
    CTkTabviewForPreviewBO,
    CTkSegmentedButtonForPreviewBO,
)
from ..ctkbase import _plugin_uid


class CTkDesignerPlugin(IDesignerPlugin):
    def get_preview_builder(self, builder_uid: str):
        if builder_uid == f"{_plugin_uid}.CTkToplevel":
            return CTkToplevelPreviewBO
        if builder_uid == f"{_plugin_uid}.CTk":
            return CTkPreviewBO
        if builder_uid == f"{_plugin_uid}.CTkFrame":
            return CTkFramePreviewBO
        if builder_uid == f"{_plugin_uid}.CTkTabview":
            return CTkTabviewForPreviewBO
        if builder_uid == f"{_plugin_uid}.CTkSegmentedButton":
            return CTkSegmentedButtonForPreviewBO
        return None

    def get_toplevel_preview_for(
        self, builder_uid: str, widget_id: str, builder, top_master
    ):
        top = None
        toplevel_uids = ("customtkinter.CTkToplevel", "customtkinter.CTk")
        if builder_uid in toplevel_uids:
            top = builder.get_object(widget_id)
        return top

    def configure_for_preview(self, builder_uid: str, widget):
        """Make widget just display with minimal functionality."""

        if not builder_uid.startswith(f"{_plugin_uid}."):
            return

        #
        # do recursive cropping
        #
        crop_widget(widget, recursive=True)

        #
        # Remove default bindings
        #
        def _no_op(event=None):
            pass

        widget_canvas = widget._canvas
        if builder_uid.endswith(".CTKEntry"):
            seqlist = ("<FocusOut>", "<FocusIn>")
            for seq in seqlist:
                widget_canvas.bind(seq, _no_op)
        elif builder_uid.endswith(".CTkSlider"):
            seqlist = ("<Enter>", "<Leave>", "<Button-1>", "<B1-Motion>")
            for seq in seqlist:
                widget_canvas.bind(seq, _no_op)
        elif builder_uid.endswith(".CTkOptionMenu"):
            seqlist = ("<Enter>", "<Leave>", "<Button-1>")
            for seq in seqlist:
                widget_canvas.bind(seq, _no_op)
                widget._text_label.bind(seq, _no_op)
        elif builder_uid.endswith(".CTkComboBox"):
            widget_canvas.tag_bind("right_parts", "<Enter>", _no_op)
            widget_canvas.tag_bind("dropdown_arrow", "<Enter>", _no_op)
            widget_canvas.tag_bind("right_parts", "<Leave>", _no_op)
            widget_canvas.tag_bind("dropdown_arrow", "<Leave>", _no_op)
            widget_canvas.tag_bind("right_parts", "<Button-1>", _no_op)
            widget_canvas.tag_bind("dropdown_arrow", "<Button-1>", _no_op)

    def ensure_visibility_in_preview(self, builder, selected_uid: str):
        """Ensure visibility of selected_uid in preview."""
        xpath = ".//object[@class='customtkinter.CTkTabview.Tab']"
        # find all tabs
        tabs = builder.uidefinition.root.findall(xpath)
        if tabs is None:
            return

        for tab in tabs:
            tab_id = tab.get("id")
            activate_tab = False
            # Check if this tab was clicked
            if tab_id == selected_uid:
                activate_tab = True
            else:
                # check if selected_uid is inside this tab
                xpath = f".//object[@id='{selected_uid}']"
                o = tab.find(xpath)
                if o is not None:
                    activate_tab = True
            if activate_tab:
                tab_builder = builder.objects[tab_id]
                top = tab_builder.widget.winfo_toplevel()
                tabview = top.nametowidget(tab_builder.widget.winfo_parent())
                tabname = tab_builder.wmeta.properties.get("label")
                current = tabview.get()
                if current != tabname:
                    tabview.set(tabname)
                    top.update()
                break
