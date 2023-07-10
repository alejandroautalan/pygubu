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
    }

    def do_activate(self) -> bool:
        # Forms are not finished so include only for development
        forms = {
            "pygubu.plugins.pygubu.forms.ttkforms": (
                "pygubu.forms.ttk.FrameForm",
                "pygubu.forms.ttk.LabelField",
                "pygubu.forms.ttk.EntryField",
                "pygubu.forms.ttk.LabelFieldInfo",
            ),
            "pygubu.plugins.pygubu.forms.tkforms": (
                "pygubu.forms.tk.TextField",
            ),
            "pygubu.plugins.pygubu.forms.pwforms": (
                "pygubu.forms.pwforms.ComboboxField"
            ),
        }
        if os.getenv("PYGUBU_ENABLE_FORMS"):
            self.module_map.update(forms)
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
