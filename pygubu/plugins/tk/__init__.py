from pygubu.api.v1 import BuilderLoader, register_loader


class StandardTKWidgetsLoader(BuilderLoader):
    def get_module_path(self, identifier: str) -> str:
        return "pygubu.plugins.tk.tkstdwidgets"

    def can_load(self, identifier: str) -> bool:
        return identifier.startswith("tk.")


register_loader(StandardTKWidgetsLoader())
