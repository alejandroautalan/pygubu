import tkinter as tk
import tkinter.ttk as ttk
import weakref
from abc import ABC, ABCMeta, abstractmethod
from collections import defaultdict
from contextlib import suppress
from dataclasses import dataclass, field
from typing import Optional, DefaultDict


class StyleDefinitionMeta(ABCMeta):
    managers = []
    instances = weakref.WeakKeyDictionary()

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if name != "IStyleManager":
            StyleDefinitionMeta.managers.append(cls)

    def __call__(cls, *args, **kwargs):
        inst = super().__call__(*args, **kwargs)
        StyleDefinitionMeta.instances[inst] = None

        return inst


@dataclass
class RootInfo:
    current_theme: Optional[str] = None
    configured_themes: DefaultDict[str, list] = field(
        default_factory=lambda: defaultdict(list)
    )  # theme > [definitions]


class StyleManager:
    CONFIGURED_THEMES = {}
    EVENT_THEME_CHANGED = "<<StyleManager:ThemeChanged>>"
    STYLE_CLASS = ttk.Style

    @classmethod
    def definition_exists(cls, definition_uid: str, root: tk.Tk):
        curr_theme = root.tk.eval("return $ttk::currentTheme")
        exists = False
        info: RootInfo = cls.CONFIGURED_THEMES.get(root, None)
        if info and definition_uid in info.configured_themes[curr_theme]:
            exists = True

        return exists

    @classmethod
    def register_root(cls, definition_uid: str, root: tk.Tk, curr_theme: str):
        if root not in cls.CONFIGURED_THEMES:
            info = RootInfo(curr_theme)
            info.configured_themes[curr_theme].append(definition_uid)
            cls.CONFIGURED_THEMES[root] = info

            root.bind_class(
                "TFrame",
                "<<ThemeChanged>>",
                lambda e, r=root: cls._theme_change_monitor(root),
                add=True,
            )

    @classmethod
    def _theme_change_monitor(cls, root: tk.Tk):
        info: RootInfo = cls.CONFIGURED_THEMES[root]
        curr_theme = root.tk.eval("return $ttk::currentTheme")
        # print(f"{curr_theme=} root {id(root)=}")
        if info.current_theme != curr_theme:
            info.current_theme = curr_theme
            cls.reconfigure_all(root, info)
            root.event_generate(cls.EVENT_THEME_CHANGED)
        return "break"

    @classmethod
    def reconfigure_all(cls, root: tk.Tk, info: RootInfo):
        """Call reconfigure for all definitions in root.
        The call is done only if definition was no applied
        previously in current theme.
        """
        definitions = info.configured_themes[info.current_theme]
        style = cls.STYLE_CLASS(root)
        for instance in StyleDefinitionMeta.instances:
            if instance.UID not in definitions:
                instance.reconfigure(style)


class IStyleDefinition(ABC, metaclass=StyleDefinitionMeta):
    """Helps to manage a custom style definition."""

    @property
    @abstractmethod
    def UID() -> str:
        """This property will be supplied by the inheriting
        classes individually.
        It is an unique identifier for the style or group of
        styles that will manage.
        """
        ...

    def __init__(self):
        self.style_managed_externally = False

    def is_managed_externally(self, master: tk.Widget):
        """Determine if style was defined externally.
        Default implementation returns False.

        If style is managed externally, this class just
        drop management of this definition.
        """
        return False

    def initialize(self, master: tk.Widget):
        root = master.winfo_toplevel()
        initialized = StyleManager.definition_exists(self.UID, root)

        if initialized or self.style_managed_externally:
            return

        if self.is_managed_externally(master):
            self.style_managed_externally = True
            return

        style = StyleManager.STYLE_CLASS(root)
        self.setup(style)

        StyleManager.register_root(self.UID, root, style.theme_use())

    def reconfigure(self, style: ttk.Style) -> None:
        """Reconfigure style in current theme.
        For simple styles just call style_setup again (default)
        For complex styles, redefine method in the subclass.
        """
        if self.style_managed_externally:
            return
        self.setup(style)

    @abstractmethod
    def setup(self, style: ttk.Style) -> None:
        """Setup your custom style here."""
        ...
