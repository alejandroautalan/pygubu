# encoding: utf-8
import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.i18n import _
from pygubu.plugins.ttk.ttkstdwidgets import TTKButton
from pygubu.widgets.pathchooserinput import PathChooserInput, PathChooserButton


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


# common properties
_builder_id = "pygubu.widgets.PathChooser.*"
_help = _("Dialog type")
register_custom_property(
    _builder_id,
    "type",
    "choice",
    values=(PathChooserInput.FILE, PathChooserInput.DIR),
    state="readonly",
    default_value=PathChooserInput.FILE,
    help=_help,
)

_help = _("Initial path value.")
register_custom_property(_builder_id, "path", "entry", help=_help)

_help = _(
    "Dialog option. Determines if path must exist for directory and file dialogs. The default value is True."
)
register_custom_property(
    _builder_id,
    "mustexist",
    "choice",
    values=("", "true", "false"),
    state="readonly",
    default_value="true",
    help=_help,
)

_help = _("Dialog option. Sets initial directory.")
register_custom_property(_builder_id, "initialdir", "entry", help=_help)

_help = _("Dialog option. Sets dialog title.")
register_custom_property(_builder_id, "title", "entry", help=_help)

_help = _("Dialog option. Sets default file extension.")
register_custom_property(_builder_id, "defaultextension", "entry", help=_help)


class PathChooserInputBO(PathChooserBaseMixin, BuilderObject):
    class_ = PathChooserInput
    properties = PathChooserBaseMixin.base_properties + (
        "image",
        "textvariable",
        "state",
    )
    virtual_events = ("<<PathChooserPathChanged>>",)


_builder_id = "pygubu.widgets.PathChooserInput"
register_widget(
    _builder_id,
    PathChooserInputBO,
    "PathChooserInput",
    ("ttk", _("Pygubu Widgets")),
)
_old_bid = "pygubu.builder.widgets.pathchooserinput"
register_widget(
    _old_bid,
    PathChooserInputBO,
    public=False,
)

_help = _("Image for the button.")
register_custom_property(_builder_id, "image", "imageentry", help=_help)

_help = _("Tk variable associated to the path property.")
register_custom_property(_builder_id, "textvariable", "tkvarentry", help=_help)

_help = _("Path entry state.")
register_custom_property(
    _builder_id,
    "state",
    "choice",
    values=("", "normal", "disabled", "readonly"),
    state="readonly",
    help=_help,
)


class PathChooserButtonBO(PathChooserBaseMixin, BuilderObject):
    class_ = PathChooserButton
    properties = PathChooserBaseMixin.base_properties + tuple(
        set(TTKButton.properties) - set(("command", "default"))
    )
    virtual_events = ("<<PathChooserPathChanged>>",)


_builder_id = "pygubu.widgets.PathChooserButton"
register_widget(
    _builder_id,
    PathChooserButtonBO,
    "PathChooserButton",
    ("ttk", _("Pygubu Widgets")),
)

register_custom_property(_builder_id, "width", "integernumber")
