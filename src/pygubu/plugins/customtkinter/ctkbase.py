import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.i18n import _

from pygubu.plugins.tk.tkstdwidgets import TKFrame as TKFrameBO

from customtkinter import CTkBaseClass
from ..customtkinter import _designer_tab_label, _plugin_uid


class CTkBaseMixin:
    def _process_property_value(self, pname, value):
        if pname in ("hover", "dynamic_resizing"):
            return tk.getboolean(value)
        if pname in (
            "border_width",
            "from_",
            "to",
            "corner_radius",
            "button_corner_radius",
            "button_length",
            "number_of_steps",
        ):
            return float(value)
        return super()._process_property_value(pname, value)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname in (
            "hover",
            "dynamic_resizing",
            "border_width",
            "from_",
            "to",
            "corner_radius",
            "button_corner_radius",
            "button_length",
            "number_of_steps",
        ):
            return super()._process_property_value(pname, value)
        return super()._code_process_property_value(targetid, pname, value)

    def code_imports(self):
        return [("customtkinter", self.class_.__name__)]


# I will register here all common properties used by customtkinter widgets
# so I don't have to repeat for each one (notice the .* at end of _builder_uid):
_builder_uid = f"{_plugin_uid}.*"
register_custom_property(
    _builder_uid,
    "bg_color",
    "colorentry",
    help=_("Color behind the widget if it has rounded corners."),
)
register_custom_property(_builder_uid, "border_color", "colorentry")
register_custom_property(_builder_uid, "border_width", "entry")
register_custom_property(_builder_uid, "button_color", "colorentry")
register_custom_property(_builder_uid, "button_hover_color", "colorentry")
register_custom_property(_builder_uid, "button_corner_radius", "entry")
register_custom_property(_builder_uid, "button_length", "entry")

register_custom_property(_builder_uid, "checkmark_color", "colorentry")
register_custom_property(_builder_uid, "command", "simplecommandentry")
register_custom_property(_builder_uid, "corner_radius", "entry")

register_custom_property(_builder_uid, "dropdown_color", "colorentry")
register_custom_property(_builder_uid, "dropdown_hover_color", "colorentry")
register_custom_property(_builder_uid, "dropdown_text_color", "colorentry")
register_custom_property(_builder_uid, "dropdown_text_font", "fontentry")
register_custom_property(
    _builder_uid,
    "dynamic_resizing",
    "choice",
    values=("", "True", "False"),
    state="readonly",
)

register_custom_property(
    _builder_uid, "fg_color", "colorentry", help=_("Main color of the widget.")
)

register_custom_property(_builder_uid, "height", "dimensionentry")
register_custom_property(
    _builder_uid,
    "hover",
    "choice",
    values=("", "True", "False"),
    state="readonly",
)
register_custom_property(_builder_uid, "hover_color", "colorentry")

register_custom_property(_builder_uid, "number_of_steps", "entry")

register_custom_property(_builder_uid, "placeholder_text", "entry")
register_custom_property(_builder_uid, "placeholder_text_color", "colorentry")
register_custom_property(_builder_uid, "progress_color", "colorentry")

register_custom_property(
    _builder_uid,
    "state",
    "choice",
    values=("", "normal", "active", "disabled"),
    state="readonly",
)

register_custom_property(_builder_uid, "text", "text")
register_custom_property(_builder_uid, "text_color", "colorentry")
register_custom_property(_builder_uid, "text_color_disabled", "colorentry")
register_custom_property(_builder_uid, "text_font", "fontentry")

register_custom_property(_builder_uid, "values", "entry")
register_custom_property(_builder_uid, "variable", "tkvarentry")

register_custom_property(_builder_uid, "width", "dimensionentry")

register_custom_property(
    _builder_uid,
    "appearance_mode",
    "choice",
    values=("", "dark", "light"),
    state="readonly",
)

register_custom_property(
    _builder_uid,
    "color_theme",
    "choice",
    values=("", "blue", "green", "dark-blue", "sweetkind"),
    state="readonly",
    help=_("Default color theme."),
)
