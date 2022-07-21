import awesometkinter as atk
from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.tk.tkstdwidgets import TKCheckbutton
from pygubu.plugins.ttk.ttkstdwidgets import TTKButton, TTKRadiobutton
from .config import designer_tab_label, module_uid


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
