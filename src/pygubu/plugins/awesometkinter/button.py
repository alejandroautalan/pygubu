import awesometkinter as atk
from pygubu.api.v1 import register_widget
from pygubu.plugins.tk.tkstdwidgets import TKCheckbutton
from pygubu.plugins.ttk.ttkstdwidgets import TTKButton, TTKRadiobutton
from ..awesometkinter import _plugin_uid, _designer_tabs


class Button3dBO(TTKButton):
    OPTIONS_STANDARD = tuple(set(TTKButton.OPTIONS_STANDARD) - set(("style",)))
    OPTIONS_CUSTOM = ("bg", "fg")
    properties = OPTIONS_STANDARD + TTKButton.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = TTKButton.ro_properties + ("bg", "fg")
    class_ = atk.Button3d


_builder_uid = f"{_plugin_uid}.Button3d"
register_widget(_builder_uid, Button3dBO, "Button3d", _designer_tabs, group=2)


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


_builder_uid = f"{_plugin_uid}.Radiobutton"
register_widget(
    _builder_uid,
    RadiobuttonBO,
    "Radiobutton",
    _designer_tabs,
    group=2,
)


class CheckbuttonBO(TKCheckbutton):
    OPTIONS_CUSTOM = (
        "box_color",
        "check_mark_color",
        "text_color",
    )
    properties = (
        TKCheckbutton.OPTIONS_STANDARD
        + TKCheckbutton.OPTIONS_SPECIFIC
        + OPTIONS_CUSTOM
    )
    ro_properties = TKCheckbutton.ro_properties + OPTIONS_CUSTOM
    class_ = atk.Checkbutton


_builder_uid = f"{_plugin_uid}.Checkbutton"
register_widget(
    _builder_uid,
    CheckbuttonBO,
    "Checkbutton",
    _designer_tabs,
    group=2,
)
