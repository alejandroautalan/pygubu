import importlib
from pygubu.api.v1 import BuilderLoaderPlugin


class AwesometkinterLoader(BuilderLoaderPlugin):
    _module = "pygubu.plugins.awesometkinter.awesomebuilders"

    def do_activate(self) -> bool:
        spec = importlib.util.find_spec("awesometkinter")
        return True if spec is not None else False

    def get_module_for(self, identifier: str) -> str:
        return self._module

    def get_all_modules(self):
        return (self._module,)

    def can_load(self, identifier: str) -> bool:
        return identifier.startswith("awesometkinter.")
