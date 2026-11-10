#!/usr/bin/python3
"""
PackFrame

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
from pygubu.widgets.packframe import PackFrame
from ._config import nspygubu, _section_containers, GCONTAINER
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame

#
# Builder definition section
#
# widget_namespace = "pygubu.widgets.boxcontainer"
# widget_classname = "BoxContainer"
# builder_namespace = "pygubu.widgets"
# section_name = "Project Widgets"


class PackFrameBO(TTKFrame):
    class_ = PackFrame
    children_layout_override = True
    container_layout = False
    properties = (
        "pack_alignment",
        "pack_direction",
        "pack_expand",
        "pack_gap",
        "pack_chsizing",
        "pack_cvsizing",
        "pack_propagate",
    ) + TTKFrame.properties

    def add_child(self, bobject):
        self.widget.child_add(bobject.widget)

    def _process_property_value(self, pname, value):
        if pname in ("pack_expand", "pack_propagate"):
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def code_child_add(self, childid):
        return [f"{self.code_identifier()}.child_add({childid})"]


register_widget(
    nspygubu.widgets.PackFrame,
    PackFrameBO,
    "PackFrame",
    _section_containers,
    group=GCONTAINER - 1,
)
