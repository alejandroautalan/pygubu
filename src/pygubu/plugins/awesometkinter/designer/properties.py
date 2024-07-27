from pygubu.i18n import _
from pygubu.api.v1 import register_custom_property
from pygubu.plugins.awesometkinter import _plugin_uid


_builder_all = f"{_plugin_uid}.*"
_button3d = f"{_plugin_uid}.Button3d"
_radiobutton = f"{_plugin_uid}.Radiobutton"
_checkbutton = f"{_plugin_uid}.Checkbutton"
_frame3d = f"{_plugin_uid}.Frame3d"
_scrollableframe = f"{_plugin_uid}.ScrollableFrame"


plugin_properties = {
    "autoscroll": dict(
        buid=_scrollableframe,
        editor="choice",
        values=("", "false", "true"),
        state="readonly",
        help=_("auto scroll to bottom if new items added to frame"),
    ),
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
        dict(buid=_frame3d, editor="colorentry", help=_("color of frame")),
        dict(
            buid=_scrollableframe,
            editor="colorentry",
            help=_("background color"),
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
    "hbar_width": dict(
        buid=_scrollableframe,
        editor="dimensionentry",
        help=_("horizontal scrollbar width"),
    ),
    "hscroll": dict(
        buid=_scrollableframe,
        editor="choice",
        values=("", "false", "true"),
        state="readonly",
        help=_("use horizontal scrollbar"),
    ),
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
    "sbar_bg": dict(
        buid=_scrollableframe,
        editor="colorentry",
        help=_("color of scrollbars' trough, default to frame's background"),
    ),
    "sbar_fg": dict(
        buid=_scrollableframe,
        editor="colorentry",
        help=_("color of scrollbars' slider"),
    ),
    "text_color": dict(
        buid=_checkbutton,
        editor="colorentry",
    ),
    "vscroll": dict(
        buid=_scrollableframe,
        editor="choice",
        values=("", "false", "true"),
        state="readonly",
        help=_("use vertical scrollbar"),
    ),
    "vbar_width": dict(
        buid=_scrollableframe,
        editor="dimensionentry",
        help=_("vertical scrollbar width"),
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
