import tkinter as tk
import tkinter.ttk as ttk
from collections import defaultdict
from .themes import STANDARD_THEMES
from .builder import ThemeDefinition, BootstrapThemeBuilder


class Style(ttk.Style):
    """Style class to manage bootstrap themes."""

    bs_names = []
    bs_definitions = {}
    bs_builders = {}
    bs_themes_loaded = False
    bs_configured_roots = defaultdict(list)

    def __init__(self, master=None):
        root = None if master is None else master.winfo_toplevel()
        super().__init__(root)
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

    def theme_names(self, bs_themes_only=False):
        if bs_themes_only:
            return tuple(self.bs_names)
        return super().theme_names() + tuple(self.bs_names)

    def theme_use(self, themename=None):
        if themename is None:
            return super().theme_use()
        if themename not in self.bs_names:
            # raise ValueError(f"Bootstrap theme '{themename}' not found.")
            return super().theme_use(themename)
        current_theme = super().theme_use()
        if current_theme == themename:
            # Already using theme: themename
            # Do nothing
            return
        builder = type(self).bs_builders.get(themename, None)
        if builder is None:
            builder = BootstrapThemeBuilder(self.bs_definitions[themename])
            type(self).bs_builders[themename] = builder
        if themename not in self.bs_configured_roots[self.master]:
            builder.create(self.master)
            builder.apply(self.master)
            self.bs_configured_roots[self.master].append(themename)
        else:
            builder.apply(self.master)
        builder.update_current_widgets(self.master)

    @classmethod
    def get_generated_styles(cls):
        return list(BootstrapThemeBuilder.generated_styles)
