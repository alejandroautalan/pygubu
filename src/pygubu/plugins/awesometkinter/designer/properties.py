from pygubu.i18n import _
from pygubu.api.v1 import register_custom_property
from pygubu.plugins.awesometkinter import _plugin_uid


_builder_all = f"{_plugin_uid}.*"
_button3d = f"{_plugin_uid}.Button3d"
_radiobutton = f"{_plugin_uid}.Radiobutton"
_checkbutton = f"{_plugin_uid}.Checkbutton"

plugin_properties = {
    "check_mark_color": dict(
        buid=_checkbutton,
        editor="colorentry",
    ),
    "bg": [
        dict(buid=_button3d, editor="colorentry", help=_("button color")),
        dict(
            buid=_radiobutton,
            editor="colorentry",
            help=_('background color "should match parent bg"'),
        ),
    ],
    "box_color": dict(
        buid=_checkbutton,
        editor="colorentry",
    ),
    "fg": dict(
        buid=[_button3d, _radiobutton],
        editor="colorentry",
        help=_("text color"),
    ),
    "font": dict(buid=_radiobutton, editor="fontentry"),
    "ind_bg": dict(
        buid=_radiobutton,
        editor="colorentry",
        help=_('indicator ring background "fill color"'),
    ),
    "ind_mark_color": dict(
        buid=_radiobutton, editor="colorentry", help=_("check mark color")
    ),
    "ind_outline_color": dict(
        buid=_radiobutton,
        editor="colorentry",
        help=_("indicator outline / ring color"),
    ),
    "text_color": dict(
        buid=_checkbutton,
        editor="colorentry",
    ),
}

for prop in plugin_properties:
    definitions = plugin_properties[prop]
    if isinstance(definitions, dict):
        definitions = [definitions]
    for definition in definitions:
        builders = definition.pop("buid", _builder_all)
        if isinstance(builders, str):
            builders = [builders]
        editor = definition.pop("editor", "entry")
        for builder_uid in builders:
            register_custom_property(builder_uid, prop, editor, **definition)
