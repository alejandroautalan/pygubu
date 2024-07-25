#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.widgets.colorinput import ColorInput
from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid


#
# Builder definition section
#


class ColorInputBO(BuilderObject):
    class_ = ColorInput
    virtual_events = (ColorInput.EVENT_COLOR_CHANGED,)
    properties = ("value", "textvariable")


_builder_id = f"{_plugin_uid}.ColorInput"
register_widget(
    _builder_id, ColorInputBO, "ColorInput", ("ttk", _tab_widgets_label)
)
