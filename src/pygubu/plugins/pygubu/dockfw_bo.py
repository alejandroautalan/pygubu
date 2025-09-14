import tkinter as tk
import tkinter.ttk as ttk

from pygubu.api.v1 import (
    register_widget,
    BuilderObject,
)

import pygubu.widgets.dockfw.widgets as widgets
from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid


class DockWidgetBaseBO(BuilderObject):
    def __init__(self, builder, wmeta):
        self.main_pane = None  # store main pane for code generation
        super().__init__(builder, wmeta)

    def _get_init_args(self, extra_init_args: dict = None):
        args = super()._get_init_args(extra_init_args)
        if "uid" not in args:
            args["uid"] = self.wmeta.identifier
        return args

    def _code_get_init_args(self, code_identifier):
        args = super()._code_get_init_args(code_identifier)
        if "uid" not in args:
            args["uid"] = self.code_escape_str(self.wmeta.identifier)
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

    def code_realize(self, boparent, code_identifier=None):
        self.parent_bo = boparent
        if code_identifier is not None:
            self._code_identifier = code_identifier

        this_pane = self.code_identifier()
        dockframe = boparent.code_child_master()
        args = self._code_get_init_args(this_pane)

        if not self.parent_bo.main_pane:
            args["main_pane"] = True
            self.parent_bo.main_pane = self

        pweight = args.pop("weight", 1)
        kwargs = self.code_make_kwargs_str(args)

        lines = [f"{this_pane} = {dockframe}.new_pane({kwargs})"]
        if isinstance(boparent, DockPaneBO):
            main_pane = self.parent_bo.main_pane.code_identifier()
            main_pane = self.code_escape_str(main_pane)
            line = f"{main_pane}.add_pane({this_pane}, weight={pweight})"
            lines.append(line)
        return lines

    def code_configure(self, targetid=None):
        return []

    def code_layout(self, targetid=None, parentid=None):
        return []


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

    def code_child_master(self):
        return f"{self.code_identifier()}.fcenter"

    def code_realize(self, boparent, code_identifier=None):
        self.parent_bo = boparent
        if code_identifier is not None:
            self._code_identifier = code_identifier

        dockframe = boparent.parent_bo.code_child_master()
        pane = boparent.code_child_master()
        this_widget = self.code_identifier()
        args = self._code_get_init_args(this_widget)
        grouped = args.pop("grouped", False)
        weight = args.pop("weight", 1)
        kwargs = self.code_make_kwargs_str(args)
        lines = [f"{this_widget} = {dockframe}.new_widget({kwargs})"]
        lines.extend(super().code_configure(this_widget))
        line = f"{pane}.add_widget({this_widget}, grouped={grouped}, weight={weight})"
        lines.append(line)
        return lines

    def code_configure(self, targetid=None):
        return []

    def code_layout(self, targetid=None, parentid=None):
        return []


_builder_id = f"{_plugin_uid}.dockwidget"
DockPaneBO.add_allowed_child(_builder_id)

register_widget(
    _builder_id, DockWidgetBO, "DockWidget", ("ttk", _tab_widgets_label)
)
