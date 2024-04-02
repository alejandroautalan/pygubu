import tkinter as tk
import tkinter.ttk as ttk
from .themes import STANDARD_THEMES
from .builder import ThemeDefinition, BootstrapThemeBuilder


class Style(ttk.Style):
    """Style class to manage bootstrap themes."""

    bs_names = []
    bs_definitions = {}
    bs_builders = {}
    bs_themes_loaded = False

    def __init__(self, master=None):
        super().__init__(master)
        self._load_standard_themes()

    def _load_standard_themes(self):
        if not self.bs_themes_loaded:
            for name, definition in STANDARD_THEMES.items():
                self.register_theme(
                    ThemeDefinition(
                        name=name,
                        theme_type=definition["type"],
                        colors=definition["colors"],
                    )
                )
            type(self).bs_themes_loaded = True

    @classmethod
    def register_theme(cls, definition: ThemeDefinition):
        cls.bs_names.append(definition.name)
        cls.bs_definitions[definition.name] = definition

    def theme_names(self):
        return self.bs_names

    def theme_use(self, themename=None):
        if themename is None:
            return super().theme_use()
        if themename not in self.bs_names:
            raise ValueError(f"Bootstrap theme '{themename}' not found.")
        current_theme = super().theme_use()
        if current_theme == themename:
            # Already using theme: themename
            # Do nothing
            return
        if themename not in self.bs_builders:
            builder = BootstrapThemeBuilder(self.bs_definitions[themename])
            builder.create(self.master)
            builder.apply(self.master)
            type(self).bs_builders[themename] = builder
        else:
            self.bs_builders[themename].apply(self.master)
        self.bs_builders[themename].update_current_widgets(self.master)

    @classmethod
    def get_generated_styles(cls):
        return list(BootstrapThemeBuilder.generated_styles)
