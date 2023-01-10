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
    properties = (
        "cursor",
        "padx",
        "pady",
        "relief",
        "takefocus",
        "class_",
        "height",
        "width",
        # CUSTOM OPTIONS,
        "title",
        "geometry",
        "overrideredirect",
        "minsize",
        "maxsize",
        "resizable",
        "iconbitmap",
        "iconphoto",
        # CUSTOMTKINTER options,
        "appearance_mode",
        "color_theme",
        "fg_color",
    )
    ro_properties = ("container", "fg_color")

    def realize(self, parent, extra_init_args: dict = None):
        args = self._get_init_args(extra_init_args)
        # master = parent.get_child_master()
        fg_color = args.pop("fg_color", None)
        self.widget = self.class_(fg_color, **args)
        return self.widget

    def _set_property(self, target_widget, pname, value):
        if pname == "appearance_mode":
            set_appearance_mode(value)
        elif pname == "color_theme":
            set_default_color_theme(value)
        else:
            return super()._set_property(target_widget, pname, value)

    #
    # Code generation methods
    #

    def code_realize(self, boparent, code_identifier=None):
        if code_identifier is not None:
            self._code_identifier = code_identifier
        lines = []
        # master = boparent.code_child_master()
        init_args = self._code_get_init_args(self.code_identifier())
        fg_color = init_args.pop("fg_color", None)
        bag = []
        for pname, value in init_args.items():
            bag.append(f"{pname}={value}")
        kwargs = ""
        if bag:
            kwargs = f""", {", ".join(bag)}"""
        s = f"{self.code_identifier()} = {self._code_class_name()}({fg_color}{kwargs})"
        lines.append(s)
        return lines

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
    properties = (
        "borderwidth",
        "cursor",
        "takefocus",
        "class_",
        "height",
        "width",
        "highlightbackground",
        "highlightthickness",
        # CUSTOM OPTIONS,
        "title",
        "geometry",
        "overrideredirect",
        "minsize",
        "maxsize",
        "resizable",
        "iconbitmap",
        "iconphoto",
        # CUSTOMTKINTER options,
        "fg_color",
    )
    ro_properties = ("fg_color",)

    def realize(self, parent, extra_init_args: dict = None):
        kwargs = self._get_init_args(extra_init_args)
        fg_color = kwargs.pop("fg_color", None)
        master = parent.get_child_master()
        self.widget = self.class_(master, fg_color=fg_color, **kwargs)
        return self.widget

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
