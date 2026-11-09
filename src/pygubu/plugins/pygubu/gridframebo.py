#!/usr/bin/python3
"""
GridFrame

A container that arranges its child widgets in a grid.


UI source file: gridframe.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from pygubu.widgets.gridframe import GridFrame
from ._config import nspygubu, _section_containers, GCONTAINER

#
# Builder definition section
#
# widget_namespace = "gridframe"
# widget_classname = "GridFrame"
# builder_namespace = "custom_widgets"
# section_name = "Project Widgets"


class GridFrameBO(TTKFrame):
    class_ = GridFrame
    container = True
    container_layout = False
    children_layout_override = True
    children_layout_manager = "grid"
    properties = (
        "grid_anchor",
        "grid_dim_rows",
        "grid_dim_cols",
        "grid_propagate",
        "grid_flow",
        "grid_gap",
        "grid_expand",
        "grid_cell_hsizing",
        "grid_cell_vsizing",
    ) + TTKFrame.properties

    def add_child(self, bobject):
        self.widget.child_add(bobject.widget)

    def _process_property_value(self, pname, value):
        if pname in ("grid_expand", "grid_propagate"):
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def code_child_add(self, childid):
        return [f"{self.code_identifier()}.child_add({childid})"]


register_widget(
    nspygubu.widgets.GridFrame,
    GridFrameBO,
    "GridFrame",
    _section_containers,
    group=GCONTAINER - 1,
)
