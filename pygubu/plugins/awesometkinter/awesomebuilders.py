"""
Documentation, License etc.

@package pygubu.plugins.awesometkinter
"""
import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.plugins.tk.tkstdwidgets import TKFrame, TKCheckbutton
from pygubu.plugins.ttk.ttkstdwidgets import TTKButton, TTKFrame, TTKRadiobutton
import awesometkinter as atk

designer_tab_label = _("AwesomeTkinter")
module_uid = "awesometkinter"


class Frame3dBO(TTKFrame):
    OPTIONS_STANDARD = tuple(set(TTKFrame.OPTIONS_STANDARD) - set(("style",)))
    OPTIONS_CUSTOM = ("bg",)
    properties = OPTIONS_STANDARD + TTKFrame.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = TTKFrame.ro_properties + ("bg",)
    class_ = atk.Frame3d


_builder_uid = module_uid + ".frame3d"
register_widget(_builder_uid, Frame3dBO, "Frame3d", ("ttk", designer_tab_label))

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


_builder_uid = module_uid + ".scrollable_frame"
register_widget(
    _builder_uid,
    ScrollableFrameBO,
    "ScrollableFrame",
    ("ttk", designer_tab_label),
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


class Button3dBO(TTKButton):
    OPTIONS_STANDARD = tuple(set(TTKButton.OPTIONS_STANDARD) - set(("style",)))
    OPTIONS_CUSTOM = ("bg", "fg")
    properties = OPTIONS_STANDARD + TTKButton.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = TTKButton.ro_properties + ("bg", "fg")
    class_ = atk.Button3d


_builder_uid = module_uid + ".button3d"
register_widget(
    _builder_uid, Button3dBO, "Button3d", ("ttk", designer_tab_label)
)
register_custom_property(
    _builder_uid, "bg", "colorentry", help=_("button color")
)

register_custom_property(_builder_uid, "fg", "colorentry", help=_("text color"))


class RadiobuttonBO(TTKRadiobutton):
    OPTIONS_STANDARD = tuple(
        set(TTKRadiobutton.OPTIONS_STANDARD) - set(("style",))
    )
    OPTIONS_CUSTOM = (
        "bg",
        "fg",
        "ind_bg",
        "ind_mark_color",
        "ind_outline_color",
        "font",
    )
    properties = (
        OPTIONS_STANDARD + TTKRadiobutton.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = (
        TTKRadiobutton.ro_properties + OPTIONS_CUSTOM + ("text", "value")
    )
    class_ = atk.Radiobutton


_builder_uid = module_uid + ".radiobutton"
register_widget(
    _builder_uid, RadiobuttonBO, "Radiobutton", ("ttk", designer_tab_label)
)
register_custom_property(
    _builder_uid,
    "bg",
    "colorentry",
    help=_('background color "should match parent bg"'),
)
register_custom_property(_builder_uid, "fg", "colorentry", help=_("text color"))
register_custom_property(
    _builder_uid,
    "ind_bg",
    "colorentry",
    help=_('indicator ring background "fill color"'),
)
register_custom_property(
    _builder_uid,
    "ind_outline_color",
    "colorentry",
    help=_("indicator outline / ring color"),
)
register_custom_property(
    _builder_uid, "ind_mark_color", "colorentry", help=_("check mark color")
)
register_custom_property(
    _builder_uid,
    "font",
    "fontentry",
)


class CheckbuttonBO(TKCheckbutton):
    class_ = atk.Checkbutton


_builder_uid = module_uid + ".checkbutton"
register_widget(
    _builder_uid, CheckbuttonBO, "Checkbutton", ("ttk", designer_tab_label)
)


class RadialProgressbarBO(BuilderObject):
    class_ = atk.RadialProgressbar


_builder_uid = module_uid + ".radialprogressbar"
register_widget(
    _builder_uid,
    RadialProgressbarBO,
    "RadialProgressbar",
    ("ttk", designer_tab_label),
)


class RadialProgressbar3dBO(BuilderObject):
    class_ = atk.RadialProgressbar3d


_builder_uid = module_uid + ".radialprogressbar3d"
register_widget(
    _builder_uid,
    RadialProgressbar3dBO,
    "RadialProgressbar3d",
    ("ttk", designer_tab_label),
)


class SegmentbarBO(BuilderObject):
    class_ = atk.Segmentbar


_builder_uid = module_uid + ".Segmentbar"
register_widget(
    _builder_uid, SegmentbarBO, "Segmentbar", ("ttk", designer_tab_label)
)
