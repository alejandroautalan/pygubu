# encoding: utf-8
import tkinter as tk
from pygubu.api.v1 import BuilderObject, register_widget
from pygubu.plugins.ttk.ttkstdwidgets import TTKButton
from pygubu.widgets.pathchooserinput import PathChooserInput, PathChooserButton
from ._config import nspygubu, _designer_tabs_widgets_ttk, GINPUT


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


register_widget(
    nspygubu.widgets.PathChooserInput,
    PathChooserInputBO,
    "PathChooserInput",
    _designer_tabs_widgets_ttk,
    group=GINPUT,
)
register_widget(
    nspygubu.builder_old.pathchooserinput,
    PathChooserInputBO,
    public=False,
)


class PathChooserButtonBO(PathChooserBaseMixin, BuilderObject):
    class_ = PathChooserButton
    properties = PathChooserBaseMixin.base_properties + tuple(
        set(TTKButton.properties) - set(("command", "default"))
    )
    virtual_events = ("<<PathChooserPathChanged>>",)


register_widget(
    nspygubu.widgets.PathChooserButton,
    PathChooserButtonBO,
    "PathChooserButton",
    _designer_tabs_widgets_ttk,
    group=GINPUT,
)
