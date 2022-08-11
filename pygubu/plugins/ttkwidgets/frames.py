import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from ttkwidgets.frames import ScrolledFrame, ToggledFrame
from ..ttkwidgets import _designer_tab_label, _plugin_uid


class ScrolledFrameBO(TTKFrame):
    class_ = ScrolledFrame
    container = True
    container_layout = True
    OPTIONS_CUSTOM = (
        "compound",
        "canvaswidth",
        "canvasheight",
        "canvasborder",
        "autohidescrollbar",
    )
    properties = (
        TTKFrame.OPTIONS_STANDARD + TTKFrame.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = TTKFrame.ro_properties + OPTIONS_CUSTOM

    def get_child_master(self):
        return self.widget.interior

    def _process_property_value(self, pname, value):
        if pname == "autohidescrollbar":
            return tk.getboolean(value)
        if pname == "compound":
            return tk.LEFT if value == "left" else tk.RIGHT
        return super(ScrolledFrameBO, self)._process_property_value(
            pname, value
        )

    def code_child_master(self):
        return f"{self.code_identifier()}.interior"

    def _code_process_property_value(self, targetid, pname, value):
        if pname == "autohidescrollbar":
            return tk.getboolean(value)
        return super()._code_process_property_value(targetid, pname, value)


_builder_uid = f"{_plugin_uid}.ScrolledFrame"
register_widget(
    _builder_uid,
    ScrolledFrameBO,
    "ScrolledFrame",
    ("ttk", _designer_tab_label),
    group=0,
)

register_custom_property(
    _builder_uid,
    "compound",
    "choice",
    default_value=tk.RIGHT,
    values=("", tk.LEFT, tk.RIGHT),
    state="readonly",
    help=_("side the scrollbar should be on"),
)
register_custom_property(
    _builder_uid, "canvaswidth", "dimensionentry", default_value=400
)
register_custom_property(
    _builder_uid, "canvasheight", "dimensionentry", default_value=400
)
register_custom_property(_builder_uid, "canvasborder", "dimensionentry")
register_custom_property(
    _builder_uid,
    "autohidescrollbar",
    "choice",
    values=("", "true", "false"),
    state="readonly",
)


class ToggledFrameBO(TTKFrame):
    class_ = ToggledFrame
    container = True
    OPTIONS_CUSTOM = (
        "compound",
        "width",
        "text",
    )
    properties = (
        TTKFrame.OPTIONS_STANDARD + TTKFrame.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = TTKFrame.ro_properties + OPTIONS_CUSTOM

    def get_child_master(self):
        return self.widget.interior

    def _process_property_value(self, pname, value):
        final_value = value
        if pname in ("autohidescrollbar",):
            final_value = tk.getboolean(value)
        else:
            final_value = super(ToggledFrameBO, self)._process_property_value(
                pname, value
            )
        return final_value

    def code_child_master(self):
        return f"{self.code_identifier()}.interior"


_builder_uid = f"{_plugin_uid}.ToggledFrame"
register_widget(
    _builder_uid,
    ToggledFrameBO,
    "ToggledFrame",
    ("ttk", _designer_tab_label),
    group=0,
)

register_custom_property(
    _builder_uid,
    "compound",
    "choice",
    default_value=tk.RIGHT,
    help=_("position of the toggle arrow compared to the text"),
    values=("", tk.TOP, tk.BOTTOM, tk.LEFT, tk.RIGHT, tk.CENTER, tk.NONE),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "width",
    "naturalnumber",
    help=_("width of the closed ToggledFrame (in characters)"),
)
register_custom_property(
    _builder_uid,
    "text",
    "entry",
    help=_("text to display next to the toggle arrow"),
)
