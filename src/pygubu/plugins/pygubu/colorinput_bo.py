#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.widgets.colorinput import ColorInput
from ._config import nspygubu, _designer_tabs_widgets_ttk, GINPUT


#
# Builder definition section
#


class ColorInputBO(BuilderObject):
    class_ = ColorInput
    virtual_events = (ColorInput.EVENT_COLOR_CHANGED,)
    properties = ("value", "textvariable")


register_widget(
    nspygubu.widgets.ColorInput,
    ColorInputBO,
    "ColorInput",
    _designer_tabs_widgets_ttk,
    group=GINPUT,
)
