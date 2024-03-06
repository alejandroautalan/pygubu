import os
from pygubu.api.v1 import BuilderLoaderPlugin


class PygubuWidgetsLoader(BuilderLoaderPlugin):
    module_map = {
        "pygubu.plugins.pygubu.calendarframe": (
            "pygubu.builder.widgets.calendarframe",
        ),
        "pygubu.plugins.pygubu.combobox": ("pygubu.builder.widgets.combobox",),
        "pygubu.plugins.pygubu.dialog": ("pygubu.builder.widgets.dialog",),
        "pygubu.plugins.pygubu.editabletreeview": (
            "pygubu.builder.widgets.editabletreeview",
        ),
        "pygubu.plugins.pygubu.pathchooserinput": (
            "pygubu.builder.widgets.pathchooserinput",
            "pygubu.widgets.PathChooserInput",
            "pygubu.widgets.PathChooserButton",
        ),
        "pygubu.plugins.pygubu.scrollbarhelper": (
            "pygubu.builder.widgets.scrollbarhelper",
        ),
        "pygubu.plugins.pygubu.scrolledframe": (
            "pygubu.builder.widgets.scrolledframe",
        ),
        "pygubu.plugins.pygubu.tkinterscrolledtext": (
            "pygubu.builder.widgets.tkinterscrolledtext",
        ),
        "pygubu.plugins.pygubu.tkscrollbarhelper": (
            "pygubu.builder.widgets.tkscrollbarhelper",
        ),
        "pygubu.plugins.pygubu.tkscrolledframe": (
            "pygubu.builder.widgets.tkscrolledframe",
        ),
        "pygubu.plugins.pygubu.filterabletreeview": (
            "pygubu.widgets.FilterableTreeview",
        ),
        "pygubu.plugins.pygubu.accordionframe": (
            "pygubu.widgets.AccordionFrame",
        ),
        "pygubu.plugins.pygubu.dockfw": (
            "pygubu.widgets.dockframe",
            "pygubu.widgets.dockpane",
            "pygubu.widgets.dockwidget",
        ),
        "pygubu.plugins.pygubu.hideableframe": ("pygubu.widgets.hideableframe"),
        "pygubu.plugins.pygubu.colorinputbo": ("pygubu.widgets.ColorInput"),
        # Forms are not finished so expect changes
        "pygubu.plugins.pygubu.forms.ttkwidgetbo": (
            "pygubu.forms.ttkwidget.FrameFormBuilder",
            "pygubu.forms.ttkwidget.Label",
            "pygubu.forms.ttkwidget.Entry",
            "pygubu.forms.ttkwidget.LabelWidgetInfo",
        ),
        "pygubu.plugins.pygubu.forms.tkwidgetbo": (
            "pygubu.forms.tkwidget.Text",
        ),
        "pygubu.plugins.pygubu.forms.pygubuwidgetbo": (
            "pygubu.forms.pygubuwidget.PygubuCombobox"
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
