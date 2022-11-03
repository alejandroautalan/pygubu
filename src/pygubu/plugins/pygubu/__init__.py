from pygubu.api.v1 import BuilderLoaderPlugin


class PygubuWidgetsLoader(BuilderLoaderPlugin):
    builders = {
        "pygubu.builder.widgets.calendarframe": "pygubu.plugins.pygubu.calendarframe",
        "pygubu.builder.widgets.combobox": "pygubu.plugins.pygubu.combobox",
        "pygubu.builder.widgets.dialog": "pygubu.plugins.pygubu.dialog",
        "pygubu.builder.widgets.editabletreeview": "pygubu.plugins.pygubu.editabletreeview",
        "pygubu.builder.widgets.pathchooserinput": "pygubu.plugins.pygubu.pathchooserinput",
        "pygubu.builder.widgets.scrollbarhelper": "pygubu.plugins.pygubu.scrollbarhelper",
        "pygubu.builder.widgets.scrolledframe": "pygubu.plugins.pygubu.scrolledframe",
        "pygubu.builder.widgets.tkinterscrolledtext": "pygubu.plugins.pygubu.tkinterscrolledtext",
        "pygubu.builder.widgets.tkscrollbarhelper": "pygubu.plugins.pygubu.tkscrollbarhelper",
        "pygubu.builder.widgets.tkscrolledframe": "pygubu.plugins.pygubu.tkscrolledframe",
    }

    def do_activate(self) -> bool:
        return True

    def get_all_modules(self):
        return [m for m in self.builders.values()]

    def get_module_for(self, identifier: str) -> str:
        return self.builders[identifier]

    def can_load(self, identifier: str) -> bool:
        return identifier in self.builders

    def get_designer_plugin(self):
        """Load class that implements IDesignerPlugin"""
        from .designer.designerplugin import PygubuDesignerPlugin

        return PygubuDesignerPlugin()
