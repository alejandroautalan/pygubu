#!/usr/bin/python3
import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.widgets.floodgauge import Floodgauge
from pygubu.plugins.ttk.ttkstdwidgets import TTKProgressbar
from ._config import nspygubu, _designer_tabs_widgets_ttk

#
# Builder definition section
#


class FloodgaugeBO(TTKProgressbar):
    class_ = Floodgauge
    properties = TTKProgressbar.properties + ("mask", "text", "textvariable")


register_widget(
    nspygubu.widgets.Floodgauge,
    FloodgaugeBO,
    "Floodgauge",
    _designer_tabs_widgets_ttk,
)
