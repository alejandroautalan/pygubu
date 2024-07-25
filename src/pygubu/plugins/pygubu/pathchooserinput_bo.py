# encoding: utf-8
import tkinter as tk
from pygubu.api.v1 import BuilderObject, register_widget
from pygubu.plugins.ttk.ttkstdwidgets import TTKButton
from pygubu.widgets.pathchooserinput import PathChooserInput, PathChooserButton
from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid


class PathChooserBaseMixin:
    base_properties = (
        "type",
        "path",
        "initialdir",
        "mustexist",
        "title",
        "defaultextension",
    )

    def _process_property_value(self, pname, value):
        if pname == "mustexist":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname == "mustexist":
            return self._process_property_value(pname, value)
        return super()._code_process_property_value(targetid, pname, value)


class PathChooserInputBO(PathChooserBaseMixin, BuilderObject):
    class_ = PathChooserInput
    properties = PathChooserBaseMixin.base_properties + (
        "image",
        "textvariable",
        "state",
    )
    virtual_events = ("<<PathChooserPathChanged>>",)


_builder_id = f"{_plugin_uid}.PathChooserInput"
register_widget(
    _builder_id,
    PathChooserInputBO,
    "PathChooserInput",
    ("ttk", _tab_widgets_label),
)
_old_bid = "pygubu.builder.widgets.pathchooserinput"
register_widget(
    _old_bid,
    PathChooserInputBO,
    public=False,
)


class PathChooserButtonBO(PathChooserBaseMixin, BuilderObject):
    class_ = PathChooserButton
    properties = PathChooserBaseMixin.base_properties + tuple(
        set(TTKButton.properties) - set(("command", "default"))
    )
    virtual_events = ("<<PathChooserPathChanged>>",)


_builder_id = f"{_plugin_uid}.PathChooserButton"
register_widget(
    _builder_id,
    PathChooserButtonBO,
    "PathChooserButton",
    ("ttk", _tab_widgets_label),
)
