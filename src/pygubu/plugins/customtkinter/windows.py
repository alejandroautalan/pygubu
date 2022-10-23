from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.i18n import _
from pygubu.plugins.tk.tkstdwidgets import TKToplevel as TKToplevelBO
from customtkinter import CTk, CTkToplevel

from ..customtkinter import _designer_tab_label, _plugin_uid
from .ctkbase import CTkBaseMixin


class CTkBO(TKToplevelBO):
    class_ = CTk

    def realize(self, parent):
        # Call realize from BuilderObject not Toplevel.
        return super(TKToplevelBO, self).realize(parent)


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
