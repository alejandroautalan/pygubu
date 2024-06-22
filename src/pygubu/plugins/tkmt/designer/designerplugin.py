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
