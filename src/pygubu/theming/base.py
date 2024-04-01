import tkinter as tk
import tkinter.ttk as ttk
from abc import ABC, ABCMeta, abstractmethod


class IThemeBuilder(ABC):
    @abstractmethod
    def theme_name(self) -> str:
        ...

    @abstractmethod
    def theme_parent(self) -> str:
        ...

    @abstractmethod
    def theme_settings(self):
        ...

    @abstractmethod
    def db_settings(self):
        ...

    @abstractmethod
    def tk_palette(self):
        ...

    def create(self, master):
        style = ttk.Style(master)
        name = self.theme_name()
        parent = self.theme_parent()
        if name not in style.theme_names():
            theme_settings = self.theme_settings()
            style.theme_create(name, parent, theme_settings)
        else:
            raise ValueError("Theme name already exists.")

    def apply(self, master: tk.Widget):
        # master.option_clear()

        palette = self.tk_palette()
        if palette:
            master.tk_setPalette(**palette)

        db_settings = self.db_settings()
        for pattern, options in db_settings.items():
            for option, value in options.items():
                fpattern = f"{pattern}{option}"
                master.option_add(fpattern, value, "widgetDefault")
        style = ttk.Style(master)
        style.theme_use(self.theme_name())
