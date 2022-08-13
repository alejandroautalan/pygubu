import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.tk.tkstdwidgets import TKText
import awesometkinter as atk

from ..awesometkinter import _designer_tab_label, _plugin_uid


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


_builder_uid = _plugin_uid + ".ScrolledText"
register_widget(
    _builder_uid,
    ScrolledTextBO,
    "ScrolledText",
    ("ttk", _designer_tab_label),
    group=1,
)
register_custom_property(
    _builder_uid, "bg", "colorentry", help=_("background color")
)
register_custom_property(
    _builder_uid, "fg", "colorentry", help=_("foreground color")
)
register_custom_property(
    _builder_uid, "bd", "naturalnumber", help=_("border width")
)
register_custom_property(
    _builder_uid,
    "vscroll",
    "choice",
    values=("", "false", "true"),
    state="readonly",
    help=_("include vertical scrollbar"),
)
register_custom_property(
    _builder_uid,
    "hscroll",
    "choice",
    values=("", "false", "true"),
    state="readonly",
    help=_("include horizontal scrollbar"),
)
register_custom_property(
    _builder_uid,
    "autoscroll",
    "choice",
    values=("", "false", "true"),
    state="readonly",
    help=_("automatic vertical scrolling"),
)
register_custom_property(
    _builder_uid,
    "max_chars",
    "naturalnumber",
    help=_(
        "maximum characters allowed in Text widget, text will be truncated from the beginning to match the max chars"
    ),
)
register_custom_property(
    _builder_uid, "sbar_fg", "colorentry", help=_("color of scrollbars' slider")
)
register_custom_property(
    _builder_uid,
    "sbar_bg",
    "colorentry",
    help=_("color of scrollbars' trough, default to frame's background"),
)
register_custom_property(
    _builder_uid,
    "vbar_width",
    "naturalnumber",
    help=_("vertical scrollbar width"),
)
register_custom_property(
    _builder_uid,
    "hbar_width",
    "naturalnumber",
    help=_("horizontal scrollbar width"),
)
