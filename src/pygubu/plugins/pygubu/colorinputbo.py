#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.widgets.colorinput import ColorInput
from pygubu.i18n import _


#
# Builder definition section
#


class ColorInputBO(BuilderObject):
    class_ = ColorInput


_builder_id = "pygubu.widgets.ColorInput"
register_widget(
    _builder_id, ColorInputBO, "ColorInput", ("ttk", _("Pygubu Widgets"))
)
