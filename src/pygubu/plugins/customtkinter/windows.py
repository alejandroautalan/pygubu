from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.i18n import _
from pygubu.plugins.tk.tkstdwidgets import TKToplevel as TKToplevelBO
from customtkinter import (
    CTk,
    CTkToplevel,
    set_appearance_mode,
    set_default_color_theme,
)

from ..customtkinter import _designer_tab_label, _plugin_uid
from .ctkbase import CTkBaseMixin


class CTkBO(TKToplevelBO):
    class_ = CTk
    properties = TKToplevelBO.properties + (
        "appearance_mode",
        "color_theme",
        "fg_color",
    )
    ro_properties = TKToplevelBO.ro_properties + ("background", "fg_color")

    def realize(self, parent, extra_init_args: dict = None):
        # Call realize from BuilderObject not Toplevel.
        return super(TKToplevelBO, self).realize(parent, extra_init_args)

    def _set_property(self, target_widget, pname, value):
        if pname == "appearance_mode":
            set_appearance_mode(value)
        elif pname == "color_theme":
            set_default_color_theme(value)
        else:
            return super()._set_property(target_widget, pname, value)

    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == "appearance_mode":
            code_bag[pname] = (f'set_appearance_mode("{value}")',)
        elif pname == "color_theme":
            code_bag[pname] = (f'set_default_color_theme("{value}")',)
        else:
            super()._code_set_property(targetid, pname, value, code_bag)

    def code_imports(self):
        imports = ["CTk"]
        if "appearance_mode" in self.wmeta.properties:
            imports.append("set_appearance_mode")
        if "color_theme" in self.wmeta.properties:
            imports.append("set_default_color_theme")
        return [("customtkinter", name) for name in imports]


_builder_uid = f"{_plugin_uid}.CTk"
register_widget(
    _builder_uid,
    CTkBO,
    "CTk",
    ("ttk", _designer_tab_label),
    group=-1,
)

_maxsize_help = _("Set the maximum window size.")
_minsize_help = _("Set the minimum window size.")

register_custom_property(
    _builder_uid,
    "minsize",
    "whentry",
    help=_minsize_help,
)
register_custom_property(
    _builder_uid,
    "maxsize",
    "whentry",
    help=_maxsize_help,
)


class CTkToplevelBO(TKToplevelBO):
    class_ = CTkToplevel
    properties = TKToplevelBO.properties + ("fg_color",)
    ro_properties = TKToplevelBO.ro_properties + ("background", "fg_color")

    def realize(self, parent, extra_init_args: dict = None):
        # Call realize from BuilderObject not Toplevel.
        return super(TKToplevelBO, self).realize(parent, extra_init_args)

    def code_imports(self):
        return [("customtkinter", self.class_.__name__)]


_builder_uid = f"{_plugin_uid}.CTkToplevel"
register_widget(
    _builder_uid,
    CTkToplevelBO,
    "CTkToplevel",
    ("ttk", _designer_tab_label),
    group=-1,
)

register_custom_property(
    _builder_uid,
    "minsize",
    "whentry",
    help=_minsize_help,
)
register_custom_property(
    _builder_uid,
    "maxsize",
    "whentry",
    help=_maxsize_help,
)
