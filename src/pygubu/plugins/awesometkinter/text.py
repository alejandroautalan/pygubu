import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.tk.tkstdwidgets import TKText
import awesometkinter as atk

from ..awesometkinter import _plugin_uid, _designer_tabs


class ScrolledTextBO(TKText):
    OPTIONS_CUSTOM = TKText.OPTIONS_CUSTOM + (
        "bg",
        "fg",
        "bd",
        "vscroll",
        "hscroll",
        "autoscroll",
        "max_chars",
        "sbar_fg",
        "sbar_bg",
        "vbar_width",
        "hbar_width",
    )
    properties = (
        TKText.OPTIONS_STANDARD + TKText.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = tuple(
        (set(TKText.ro_properties) | set(OPTIONS_CUSTOM) | set(("wrap",)))
        - set(("text",))
    )
    class_ = atk.text.ScrolledText

    def _process_property_value(self, pname, value):
        if pname in ("vscroll", "hscroll", "autoscroll"):
            return tk.getboolean(value)
        if pname in ("max_chars", "vbar_width", "hbar_width"):
            return int(value)
        return super()._process_property_value(pname, value)

    def _code_process_property_value(self, targetid, pname, value):
        if pname in ("vscroll", "hscroll", "autoscroll"):
            return tk.getboolean(value)
        return super()._code_process_property_value(targetid, pname, value)


_builder_uid = f"{_plugin_uid}.ScrolledText"
register_widget(
    _builder_uid,
    ScrolledTextBO,
    "ScrolledText",
    _designer_tabs,
    group=1,
)
