import tkinter as tk
import tkinter.ttk as ttk

from pygubu.api.v1 import (
    register_widget,
    BuilderObject,
)

import pygubu.widgets.dockfw.widgets as widgets
from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid


class DockWidgetBaseBO(BuilderObject):
    def _get_init_args(self, extra_init_args: dict = None):
        args = super()._get_init_args(extra_init_args)
        if "uid" not in args:
            args["uid"] = self.wmeta.identifier
        return args


class DockFrameBO(DockWidgetBaseBO):
    class_ = widgets.DockFrame
    container = True
    container_layout = False
    maxchildren = 1
    virtual_events = (widgets.DockFrame.EVENT_LAYOUT_CHANGED,)


_builder_id = dockframe_uid = f"{_plugin_uid}.dockframe"
register_widget(
    _builder_id, DockFrameBO, "DockFrame", ("ttk", _tab_widgets_label)
)


class DockPaneBO(DockWidgetBaseBO):
    class_ = widgets.DockPane
    container = True
    container_layout = False
    layout_required = False
    properties = ("orient", "weight")
    ro_properties = properties
    allowed_parents = (dockframe_uid,)

    @classmethod
    def canbe_child_of(cls, parent_builder, classname):
        allowed = False
        if parent_builder in (DockFrameBO, DockPaneBO):
            allowed = True
        return allowed

    def __init__(self, builder, wmeta):
        super().__init__(builder, wmeta)
        self.pane_widget = None

    def realize(self, parent, extra_init_args: dict = None):
        self.widget: widgets.DockFrame = parent.widget
        args = self._get_init_args(extra_init_args)
        if not self.widget.main_pane:
            args["main_pane"] = True
        pweight = args.pop("weight", 1)
        self.pane_widget = self.widget.new_pane(**args)
        if isinstance(parent, DockPaneBO):
            parent.pane_widget.add_pane(self.pane_widget, weight=pweight)
        return self.widget

    def configure(self, target=None):
        pass

    def layout(self, target=None, *, forget=False):
        pass


_builder_id = dockpane_uid = f"{_plugin_uid}.dockpane"
DockPaneBO.add_allowed_child(_builder_id)

register_widget(
    _builder_id, DockPaneBO, "DockPane", ("ttk", _tab_widgets_label)
)


class DockWidgetBO(DockWidgetBaseBO):
    class_ = widgets.DockWidget
    container = True
    container_layout = True
    layout_required = False
    properties = ("grouped", "weight", "title")
    ro_properties = ("grouped", "weight")
    allowed_parents = (dockframe_uid, dockpane_uid)

    @classmethod
    def canbe_child_of(cls, parent_builder, classname):
        allowed = False
        if parent_builder is DockPaneBO:
            allowed = True
        return allowed

    def _process_property_value(self, pname, value):
        if pname == "grouped":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def realize(self, parent, extra_init_args: dict = None):
        dock = parent.pane_widget.maindock
        args: dict = self._get_init_args(extra_init_args)
        grouped = args.pop("grouped", False)
        weight = args.pop("weight", 1)
        self.widget = dock.new_widget(**args)
        super().configure(target=self.widget)  # hack used here
        parent.pane_widget.add_widget(
            self.widget, grouped=grouped, weight=weight
        )

    def get_child_master(self):
        return self.widget.fcenter

    def configure(self, target=None):
        pass


_builder_id = f"{_plugin_uid}.dockwidget"
DockPaneBO.add_allowed_child(_builder_id)

register_widget(
    _builder_id, DockWidgetBO, "DockWidget", ("ttk", _tab_widgets_label)
)
