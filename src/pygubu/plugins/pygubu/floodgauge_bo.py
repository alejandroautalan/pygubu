#!/usr/bin/python3
import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.widgets.floodgauge import Floodgauge
from pygubu.plugins.ttk.ttkstdwidgets import TTKProgressbar
from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid

#
# Builder definition section
#


class FloodgaugeBO(TTKProgressbar):
    class_ = Floodgauge
    properties = TTKProgressbar.properties + ("mask", "text", "textvariable")


_builder_uid = f"{_plugin_uid}.Floodgauge"
register_widget(
    _builder_uid,
    FloodgaugeBO,
    "Floodgauge",
    ("ttk", _tab_widgets_label),
)
