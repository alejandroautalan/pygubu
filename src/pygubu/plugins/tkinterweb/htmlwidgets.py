import tkinter as tk

# from pygubu.i18n import _
from pygubu.api.v1 import register_widget
from tkinterweb import HtmlLabel, HtmlFrame
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from ..tkinterweb import _designer_tab_label, _plugin_uid


class HtmlFrameBO(TTKFrame):
    class_ = HtmlFrame
    container = False
    OPTIONS_CUSTOM = (
        "messages_enabled",
        "vertical_scrollbar",
        "horizontal_scrollbar",
    )
    properties = (
        TTKFrame.OPTIONS_STANDARD + TTKFrame.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = OPTIONS_CUSTOM

    def _process_property_value(self, pname, value):
        if pname == "messages_enabled":
            return tk.getboolean(value)
        if pname in ("vertical_scrollbar", "horizontal_scrollbar"):
            return value if value == "auto" else tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def _code_process_property_value(self, targetid, pname, value):
        if pname in self.OPTIONS_CUSTOM:
            newval = self._process_property_value(pname, value)
            return newval if isinstance(newval, bool) else f"'{newval}'"
        return super()._code_process_property_value(targetid, pname, value)

    def code_imports(self):
        return (("tkinterweb", "HtmlFrame"),)


_builder_uid = f"{_plugin_uid}.HtmlFrame"
register_widget(
    _builder_uid,
    HtmlFrameBO,
    "HtmlFrame",
    ("ttk", _designer_tab_label),
    group=0,
)


class HtmlLabelBO(HtmlFrameBO):
    class_ = HtmlLabel
    OPTIONS_CUSTOM = ("messages_enabled", "text")
    properties = (
        HtmlFrameBO.OPTIONS_STANDARD
        + HtmlFrameBO.OPTIONS_SPECIFIC
        + OPTIONS_CUSTOM
    )
    ro_properties = OPTIONS_CUSTOM

    def code_imports(self):
        return (("tkinterweb", "HtmlLabel"),)


_builder_uid = f"{_plugin_uid}.HtmlLabel"
register_widget(
    _builder_uid,
    HtmlLabelBO,
    "HtmlLabel",
    ("ttk", _designer_tab_label),
    group=0,
)
