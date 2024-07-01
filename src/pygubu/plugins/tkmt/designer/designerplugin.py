from pygubu.api.v1 import IDesignerPlugin
from pygubu.utils.widget import crop_widget

# from pygubu.stockimage import StockRegistry, StockImageCache, StockImage
import pygubu.plugins.tkmt.designer.preview as preview
import pygubu.plugins.tkmt.designer.properties


class PygubuDesignerPlugin(IDesignerPlugin):
    def get_preview_builder(self, builder_uid: str):
        if builder_uid.startswith("tkmt."):
            notused, class_name = builder_uid.split(".")
            preview_name = f"{class_name}PreviewBO"
            if hasattr(preview, preview_name):
                return getattr(preview, preview_name)
            # else:
            #    print(f"Warning: {preview_name} NOT defined")
        return None

    #    def get_toplevel_preview_for(
    #        self, builder_uid: str, widget_id: str, builder, top_master
    #    ):
    #        top = None
    #        return top

    #    def configure_for_preview(self, builder_uid: str, widget):
    #        """Make widget just display with minimal functionality."""

    def ensure_visibility_in_preview(self, builder, selected_uid: str):
        """Ensure visibility of selected_uid in preview."""
        xpath = ".//object[@class='tkmt.NotebookTab']"
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
                tab_widget = tab_builder.widget
                notebook = tab_widget.nametowidget(tab_widget.winfo_parent())
                notebook.select(tab_widget)
                notebook.update()
                break
