# encoding: utf-8
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.i18n import _
from pygubu.widgets.pathchooserinput import PathChooserInput


class PathChooserInputBuilder(BuilderObject):
    class_ = PathChooserInput
    OPTIONS_CUSTOM = (
        "type",
        "path",
        "image",
        "textvariable",
        "state",
        "initialdir",
        "mustexist",
        "title",
    )
    properties = OPTIONS_CUSTOM
    virtual_events = ("<<PathChooserPathChanged>>",)

    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == "type":
            code_bag[pname] = '"{0}"'.format(value)
        elif pname in ("initialdir", "mustexist", "title"):
            code_bag[pname] = '"{0}"'.format(value)
        elif pname == "textvariable":
            code_bag[pname] = self._code_set_tkvariable_property(pname, value)
        else:
            super(PathChooserInputBuilder, self)._code_set_property(
                targetid, pname, value, code_bag
            )


_builder_id = "pygubu.builder.widgets.pathchooserinput"
register_widget(
    _builder_id,
    PathChooserInputBuilder,
    "PathChooserInput",
    ("ttk", _("Pygubu Widgets")),
)

_help = "Dialog type"
register_custom_property(
    _builder_id,
    "type",
    "choice",
    values=(PathChooserInput.FILE, PathChooserInput.DIR),
    state="readonly",
    default_value=PathChooserInput.FILE,
    help=_help,
)

_help = "Initial path value."
register_custom_property(_builder_id, "path", "entry", help=_help)

_help = "Image for the button."
register_custom_property(_builder_id, "image", "imageentry", help=_help)

_help = "Tk variable associated to the path property."
register_custom_property(_builder_id, "textvariable", "tkvarentry", help=_help)

_help = "Path entry state."
register_custom_property(
    _builder_id,
    "state",
    "choice",
    values=("", "normal", "disabled", "readonly"),
    state="readonly",
    help=_help,
)

_help = "Dialog option. Determines if path must exist for directory dialog."
register_custom_property(
    _builder_id,
    "mustexist",
    "choice",
    values=("", "false", "true"),
    state="readonly",
    help=_help,
)

_help = "Dialog option. Sets initial directory."
register_custom_property(_builder_id, "initialdir", "entry", help=_help)

_help = "Dialog option. Sets dialog title."
register_custom_property(_builder_id, "title", "entry", help=_help)
