import os
from pygubu.api.v1 import BuilderLoaderPlugin
from pygubu.i18n import _


_tab_widgets_label = _("Pygubu Widgets")
_tab_helpers_label = _("Pygubu Helpers")
_plugin_uid = "pygubu.widgets"


class PygubuWidgetsLoader(BuilderLoaderPlugin):
    module_map = {
        "pygubu.plugins.pygubu.accordionframe_bo": (
            f"{_plugin_uid}.AccordionFrame",
        ),
        "pygubu.plugins.pygubu.calendarframe_bo": (
            f"{_plugin_uid}.CalendarFrame",
            "pygubu.builder.widgets.calendarframe",
        ),
        "pygubu.plugins.pygubu.colorinput_bo": (f"{_plugin_uid}.ColorInput",),
        "pygubu.plugins.pygubu.combobox_bo": (
            f"{_plugin_uid}.Combobox",
            "pygubu.builder.widgets.combobox",
        ),
        "pygubu.plugins.pygubu.dialog_bo": (
            f"{_plugin_uid}.Dialog",
            "pygubu.builder.widgets.dialog",
        ),
        "pygubu.plugins.pygubu.dockfw_bo": (
            f"{_plugin_uid}.dockframe",
            f"{_plugin_uid}.dockpane",
            f"{_plugin_uid}.dockwidget",
        ),
        "pygubu.plugins.pygubu.editabletreeview_bo": (
            f"{_plugin_uid}.EditableTreeview",
            "pygubu.builder.widgets.editabletreeview",
        ),
        "pygubu.plugins.pygubu.filterabletreeview_bo": (
            f"{_plugin_uid}.FilterableTreeview",
        ),
        "pygubu.plugins.pygubu.floodgauge_bo": (f"{_plugin_uid}.Floodgauge",),
        # Forms are not finished so expect changes
        "pygubu.plugins.pygubu.forms.pygubuwidget_bo": (
            "pygubu.forms.pygubuwidget.PygubuCombobox"
        ),
        "pygubu.plugins.pygubu.forms.tkwidget_bo": (
            "pygubu.forms.tkwidget.Text",
        ),
        "pygubu.plugins.pygubu.forms.ttkwidget_bo": (
            "pygubu.forms.ttkwidget.FrameFormBuilder",
            "pygubu.forms.ttkwidget.Label",
            "pygubu.forms.ttkwidget.Entry",
            "pygubu.forms.ttkwidget.LabelWidgetInfo",
        ),
        "pygubu.plugins.pygubu.hideableframe_bo": (
            f"{_plugin_uid}.hideableframe",
        ),
        "pygubu.plugins.pygubu.pathchooserinput_bo": (
            "pygubu.builder.widgets.pathchooserinput",
            "pygubu.widgets.PathChooserInput",
            f"{_plugin_uid}.PathChooserButton",
        ),
        "pygubu.plugins.pygubu.scrollbarhelper_bo": (
            "pygubu.builder.widgets.scrollbarhelper",
            f"{_plugin_uid}.ScrollbarHelper",
        ),
        "pygubu.plugins.pygubu.scrolledframe_bo": (
            "pygubu.builder.widgets.scrolledframe",
            f"{_plugin_uid}.ScrolledFrame",
        ),
        "pygubu.plugins.pygubu.tkscrollbarhelper_bo": (
            "pygubu.builder.widgets.tkscrollbarhelper",
            f"{_plugin_uid}.TkScrollbarHelper",
        ),
        "pygubu.plugins.pygubu.tkscrolledframe_bo": (
            "pygubu.builder.widgets.tkscrolledframe",
            f"{_plugin_uid}.TkScrolledFrame",
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
