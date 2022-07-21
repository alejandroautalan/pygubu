import importlib
from pygubu.api.v1 import BuilderLoaderPlugin


class AwesometkinterLoader(BuilderLoaderPlugin):
    builders = {
        "awesometkinter.frame3d": "pygubu.plugins.awesometkinter.frame",
        "awesometkinter.scrollable_frame": "pygubu.plugins.awesometkinter.frame",
        "awesometkinter.radialprogressbar": "pygubu.plugins.awesometkinter.frame",
        "awesometkinter.radialprogressbar3d": "pygubu.plugins.awesometkinter.frame",
        "awesometkinter.segmentbar": "pygubu.plugins.awesometkinter.frame",
        "awesometkinter.button3d": "pygubu.plugins.awesometkinter.button",
        "awesometkinter.radiobutton": "pygubu.plugins.awesometkinter.button",
        "awesometkinter.checkbutton": "pygubu.plugins.awesometkinter.button",
    }

    def do_activate(self) -> bool:
        spec = importlib.util.find_spec("awesometkinter")
        return True if spec is not None else False

    def get_module_for(self, identifier: str) -> str:
        return self.builders[identifier]

    def get_all_modules(self):
        return [m for m in self.builders.values()]

    def can_load(self, identifier: str) -> bool:
        return identifier.startswith("awesometkinter.")
