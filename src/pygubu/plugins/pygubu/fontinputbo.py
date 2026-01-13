#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)

from pygubu.widgets.fontinput import FontInput
from ._config import nspygubu, _designer_tabs_widgets_ttk


#
# Builder definition section
#


class FontInputBO(BuilderObject):
    class_ = FontInput
    virtual_events = (FontInput.EVENT_FONT_CHANGED,)


register_widget(
    nspygubu.widgets.FontInput,
    FontInputBO,
    "FontInput",
    _designer_tabs_widgets_ttk,
)
