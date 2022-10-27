from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.i18n import _
from pygubu.plugins.tk.tkstdwidgets import TKToplevel as TKToplevelBO
from customtkinter import CTk, CTkToplevel, set_appearance_mode

from ..customtkinter import _designer_tab_label, _plugin_uid
from .ctkbase import CTkBaseMixin


class CTkBO(TKToplevelBO):
    class_ = CTk
    properties = TKToplevelBO.properties + ("appearance_mode", "fg_color")
    ro_properties = TKToplevelBO.ro_properties + ("background", "fg_color")

    def realize(self, parent):
        # Call realize from BuilderObject not Toplevel.
        return super(TKToplevelBO, self).realize(parent)

    def _set_property(self, target_widget, pname, value):
        if pname == "appearance_mode":
            set_appearance_mode(value)
        else:
            return super()._set_property(target_widget, pname, value)

    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == "appearance_mode":
            line = f'set_apearance_mode("{value}")'
            code_bag[pname] = (line,)

    def code_imports(self):
        return (("customtkinter", "CTk"), ("customtkinter", "appearance_mode"))


_builder_uid = f"{_plugin_uid}.CTk"
register_widget(
    _builder_uid,
    CTkBO,
    "CTk",
    ("ttk", _designer_tab_label),
    group=-1,
)


class CTkToplevelBO(TKToplevelBO):
    class_ = CTkToplevel
    properties = TKToplevelBO.properties + ("fg_color",)
    ro_properties = TKToplevelBO.ro_properties + ("background", "fg_color")

    def realize(self, parent):
        # Call realize from BuilderObject not Toplevel.
        return super(TKToplevelBO, self).realize(parent)


_builder_uid = f"{_plugin_uid}.CTkToplevel"
register_widget(
    _builder_uid,
    CTkToplevelBO,
    "CTkToplevel",
    ("ttk", _designer_tab_label),
    group=-1,
)
