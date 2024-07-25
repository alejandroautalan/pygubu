from pygubu.api.v1 import BuilderLoaderPlugin


class StandardTKWidgetsLoader(BuilderLoaderPlugin):
    module_default = "pygubu.plugins.tk.tkstdwidgets"
    module_map = {
        module_default: tuple(),
        "pygubu.plugins.tk.scrolledtext_bo": (
            "tk.ScrolledText",
            "pygubu.builder.widgets.tkinterscrolledtext",  # old name
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
        return self.module_default

    def can_load(self, identifier: str) -> bool:
        for module, builders in self.module_map.items():
            if identifier in builders:
                return True
        return identifier.startswith("tk.")
