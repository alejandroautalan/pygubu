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
