#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)

from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid
from pygubu.widgets.fontinput import FontInput


#
# Builder definition section
#


class FontInputBO(BuilderObject):
    class_ = FontInput
    virtual_events = (FontInput.EVENT_FONT_CHANGED,)


_wname = "FontInput"
_builder_id = f"{_plugin_uid}.{_wname}"

register_widget(_builder_id, FontInputBO, _wname, ("ttk", _tab_widgets_label))
