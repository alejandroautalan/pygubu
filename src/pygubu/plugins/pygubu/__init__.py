import os
from pygubu.api.v1 import BuilderLoaderPlugin
from pygubu.i18n import _
from ._config import nspygubu


class PygubuWidgetsLoader(BuilderLoaderPlugin):
    module_map = {
        "pygubu.plugins.pygubu.accordionframe_bo": (
            nspygubu.widgets.AccordionFrame,
            nspygubu.widgets.AccordionFrameGroup,
        ),
        "pygubu.plugins.pygubu.calendarframe_bo": (
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ),
        "pygubu.plugins.pygubu.colorinput_bo": (nspygubu.widgets.ColorInput,),
        "pygubu.plugins.pygubu.combobox_bo": (
            nspygubu.widgets.Combobox,
            nspygubu.builder_old.combobox,
        ),
        "pygubu.plugins.pygubu.dialog_bo": (
            nspygubu.widgets.Dialog,
            nspygubu.builder_old.dialog,
        ),
        "pygubu.plugins.pygubu.dockfw_bo": (
            nspygubu.widgets.dockframe,
            nspygubu.widgets.dockpane,
            nspygubu.widgets.dockwidget,
        ),
        "pygubu.plugins.pygubu.editabletreeview_bo": (
            nspygubu.widgets.EditableTreeview,
            nspygubu.builder_old.editabletreeview,
        ),
        "pygubu.plugins.pygubu.filterabletreeview_bo": (
            nspygubu.widgets.FilterableTreeview,
        ),
        "pygubu.plugins.pygubu.floodgauge_bo": (nspygubu.widgets.Floodgauge,),
        "pygubu.plugins.pygubu.fontinputbo": (nspygubu.widgets.FontInput,),
        # Forms are not finished so expect changes
        "pygubu.plugins.pygubu.forms.pygubuwidget_bo": (
            nspygubu.forms.pygubuwidget.PygubuCombobox,
            nspygubu.forms.pygubuwidget.FontInput,
            nspygubu.forms.pygubuwidget.ColorInput,
        ),
        "pygubu.plugins.pygubu.forms.tkwidget_bo": (
            nspygubu.forms.tkwidget.Text,
        ),
        "pygubu.plugins.pygubu.forms.ttkwidget_bo": (
            nspygubu.forms.ttkwidget.FrameFormBuilder,
            nspygubu.forms.ttkwidget.Label,
            nspygubu.forms.ttkwidget.Entry,
            nspygubu.forms.ttkwidget.LabelWidgetInfo,
            nspygubu.forms.ttkwidget.Combobox,
            nspygubu.forms.ttkwidget.Checkbutton,
        ),
        "pygubu.plugins.pygubu.hideableframe_bo": (
            nspygubu.widgets.hideableframe,
        ),
        "pygubu.plugins.pygubu.pathchooserinput_bo": (
            nspygubu.builder_old.pathchooserinput,
            nspygubu.widgets.PathChooserInput,
            nspygubu.widgets.PathChooserButton,
        ),
        "pygubu.plugins.pygubu.scrollbarhelper_bo": (
            nspygubu.builder_old.scrollbarhelper,
            nspygubu.widgets.ScrollbarHelper,
        ),
        "pygubu.plugins.pygubu.scrolledframe_bo": (
            nspygubu.builder_old.scrolledframe,
            nspygubu.widgets.ScrolledFrame,
        ),
        "pygubu.plugins.pygubu.simpletooltip_bo": (
            nspygubu.widgets.Tooltip,
            nspygubu.widgets.Tooltipttk,
        ),
        "pygubu.plugins.pygubu.tkscrollbarhelper_bo": (
            nspygubu.builder_old.tkscrollbarhelper,
            nspygubu.widgets.TkScrollbarHelper,
        ),
        "pygubu.plugins.pygubu.tkscrolledframe_bo": (
            nspygubu.builder_old.tkscrolledframe,
            nspygubu.widgets.TkScrolledFrame,
        ),
    }

    def do_activate(self) -> bool:
        return True

    def get_all_modules(self):
        return [m for m in self.module_map.keys()]

    def get_module_for(self, identifier: str) -> str:
        for module, identifiers in self.module_map.items():
            if identifier in identifiers:
                return module
        return None

    def can_load(self, identifier: str) -> bool:
        for module, builders in self.module_map.items():
            if identifier in builders:
                return True
        return False

    def get_designer_plugin(self):
        """Load class that implements IDesignerPlugin"""
        from .designer.designerplugin import PygubuDesignerPlugin

        return PygubuDesignerPlugin()
