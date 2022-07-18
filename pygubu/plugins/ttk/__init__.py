from pygubu.api.v1 import BuilderLoader, register_loader


class StandardTTKWidgetsLoader(BuilderLoader):
    def get_module_path(self, identifier: str) -> str:
        return "pygubu.plugins.ttk.ttkstdwidgets"

    def can_load(self, identifier: str) -> bool:
        return identifier.startswith("ttk.")


register_loader(StandardTTKWidgetsLoader())
