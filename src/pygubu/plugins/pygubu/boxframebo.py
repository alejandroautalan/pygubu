#!/usr/bin/python3
"""
BoxFrame

A container that arranges its child widgets horizontally or vertically.

Subclass of ttk.Frame and uses grid manager.


UI source file: boxframe.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.widgets.boxframe import BoxFrame
from ._config import nspygubu, _section_containers, GCONTAINER
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame

#
# Builder definition section
#
# widget_namespace = "pygubu.widgets.boxcontainer"
# widget_classname = "BoxContainer"
# builder_namespace = "pygubu.widgets"
# section_name = "Project Widgets"


class BoxFrameBO(TTKFrame):
    class_ = BoxFrame
    children_layout_override = True
    properties = (
        "box_direction",
        "box_alignment",
        "box_expand",
        "box_hsizing",
        "box_gap",
        "box_vsizing",
    ) + TTKFrame.properties

    def add_child(self, bobject):
        self.widget.child_add(bobject.widget)

    def _process_property_value(self, pname, value):
        if pname == "box_expand":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)


register_widget(
    nspygubu.widgets.BoxFrame,
    BoxFrameBO,
    "BoxFrame",
    _section_containers,
    group=GCONTAINER,
)
