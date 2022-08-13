from pygubu.api.v1 import BuilderLoaderPlugin


class StandardTKWidgetsLoader(BuilderLoaderPlugin):
    _module = "pygubu.plugins.tk.tkstdwidgets"

    def do_activate(self) -> bool:
        return True

    def get_module_for(self, identifier: str) -> str:
        return self._module

    def get_all_modules(self):
        return (self._module,)

    def can_load(self, identifier: str) -> bool:
        return identifier.startswith("tk.")
