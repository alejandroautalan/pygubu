#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from fontinput import FontInput


#
# Builder definition section
#


class FontInputBO(BuilderObject):
    class_ = FontInput


_builder_id = "projectcustom.FontInput"
register_widget(
    _builder_id, FontInputBO, "FontInput", ("ttk", "Project Widgets")
)
