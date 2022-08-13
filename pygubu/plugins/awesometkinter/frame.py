"""
Documentation, License etc.

@package pygubu.plugins.awesometkinter
"""
import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.tk.tkstdwidgets import TKFrame
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
import awesometkinter as atk

from ..awesometkinter import _designer_tab_label, _plugin_uid


class Frame3dBO(TTKFrame):
    OPTIONS_STANDARD = tuple(set(TTKFrame.OPTIONS_STANDARD) - set(("style",)))
    OPTIONS_CUSTOM = ("bg",)
    properties = OPTIONS_STANDARD + TTKFrame.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = TTKFrame.ro_properties + ("bg",)
    class_ = atk.Frame3d


_builder_uid = _plugin_uid + ".Frame3d"
register_widget(
    _builder_uid, Frame3dBO, "Frame3d", ("ttk", _designer_tab_label), group=0
)

register_custom_property(
    _builder_uid, "bg", "colorentry", help=_("color of frame")
)


class ScrollableFrameBO(TKFrame):
    OPTIONS_STANDARD = tuple()
    OPTIONS_SPECIFIC = tuple()
    OPTIONS_CUSTOM = (
        "vscroll",
        "hscroll",
        "autoscroll",
        "bg",
        "sbar_fg",
        "sbar_bg",
        "vbar_width",
        "hbar_width",
    )
    ro_properties = OPTIONS_CUSTOM
    class_ = atk.ScrollableFrame

    def _process_property_value(self, pname, value):
        if pname in ("vscroll", "hscroll", "autoscroll"):
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def _code_process_property_value(self, targetid, pname, value):
        if pname in ("vscroll", "hscroll", "autoscroll"):
            return tk.getboolean(value)
        return super()._code_process_property_value(targetid, pname, value)


_builder_uid = _plugin_uid + ".ScrollableFrame"
register_widget(
    _builder_uid,
    ScrollableFrameBO,
    "ScrollableFrame",
    ("ttk", _designer_tab_label),
    group=0,
)

register_custom_property(
    _builder_uid,
    "vscroll",
    "choice",
    values=("", "false", "true"),
    state="readonly",
    help=_("use vertical scrollbar"),
)

register_custom_property(
    _builder_uid,
    "hscroll",
    "choice",
    values=("", "false", "true"),
    state="readonly",
    help=_("use horizontal scrollbar"),
)

register_custom_property(
    _builder_uid,
    "autoscroll",
    "choice",
    values=("", "false", "true"),
    state="readonly",
    help=_("auto scroll to bottom if new items added to frame"),
)

register_custom_property(
    _builder_uid, "bg", "colorentry", help=_("background color")
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
    "dimensionentry",
    help=_("vertical scrollbar width"),
)

register_custom_property(
    _builder_uid,
    "hbar_width",
    "dimensionentry",
    help=_("vertical scrollbar width"),
)
