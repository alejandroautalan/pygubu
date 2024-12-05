from pygubu.i18n import _
from pygubu.api.v1 import register_custom_property
from pygubu.plugins.awesometkinter import _plugin_uid


_builder_all = f"{_plugin_uid}.*"
_button3d = f"{_plugin_uid}.Button3d"
_radiobutton = f"{_plugin_uid}.Radiobutton"
_checkbutton = f"{_plugin_uid}.Checkbutton"
_frame3d = f"{_plugin_uid}.Frame3d"
_scrollableframe = f"{_plugin_uid}.ScrollableFrame"
_autowraplabel = f"{_plugin_uid}.AutoWrappingLabel"
_autofitlabel = f"{_plugin_uid}.AutofitLabel"
_radialpbar = f"{_plugin_uid}.RadialProgressbar"
_radialpbar3d = f"{_plugin_uid}.RadialProgressbar3d"
_segmentbar = f"{_plugin_uid}.Segmentbar"
_simplesbar = f"{_plugin_uid}.SimpleScrollbar"
_scrolledtext = f"{_plugin_uid}.ScrolledText"


plugin_properties = {
    "autoscroll": [
        dict(
            buid=_scrollableframe,
            editor="choice",
            values=("", "false", "true"),
            state="readonly",
            help=_("auto scroll to bottom if new items added to frame"),
        ),
        dict(
            buid=_scrolledtext,
            editor="choice",
            values=("", "false", "true"),
            state="readonly",
            help=_("automatic vertical scrolling"),
        ),
    ],
    "base_img": dict(
        buid=_radialpbar,
        editor="imageentry",
        help=_("base image for progressbar"),
    ),
    "check_mark_color": dict(
        buid=_checkbutton,
        editor="colorentry",
    ),
    "bd": dict(
        buid=_scrolledtext, editor="naturalnumber", help=_("border width")
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
        dict(
            buid=_radialpbar, editor="colorentry", help=_("color of base ring")
        ),
        dict(buid=[_segmentbar, _simplesbar], editor="colorentry"),
        dict(
            buid=_scrolledtext, editor="colorentry", help=_("background color")
        ),
    ],
    "box_color": dict(
        buid=_checkbutton,
        editor="colorentry",
    ),
    "fg": [
        dict(
            buid=[_button3d, _radiobutton],
            editor="colorentry",
            help=_("text color"),
        ),
        dict(
            buid=_radialpbar,
            editor="colorentry",
            help=_("color of indicator ring"),
        ),
        dict(buid=_radialpbar3d, editor="colorentry"),
        dict(buid=_segmentbar, editor="colorentry"),
        dict(
            buid=_scrolledtext, editor="colorentry", help=_("foreground color")
        ),
    ],
    "font": [
        dict(buid=_radiobutton, editor="fontentry"),
        dict(
            buid=_radialpbar,
            editor="fontentry",
            help=_("tkinter font for percentage text"),
        ),
    ],
    "font_size_ratio": dict(
        buid=_radialpbar,
        editor="spinbox",
        from_=0.1,
        to=1,
        increment=0.1,
        help=_(
            "font size to progressbar width ratio,"
             + "e.g. for a progressbar size 100 pixels, a 0.1 ratio means font size 10"
        ),
    ),
    "height": [
        dict(buid=_segmentbar, editor="dimensionentry"),
        dict(
            buid=[_frame3d, _scrollableframe],
            editor="dimensionentry",
            default_value=200,
        ),
    ],
    "hbar_width": [
        dict(
            buid=_scrollableframe,
            editor="dimensionentry",
            help=_("horizontal scrollbar width"),
        ),
        dict(
            buid=_scrolledtext,
            editor="naturalnumber",
            help=_("horizontal scrollbar width"),
        ),
    ],
    "hscroll": [
        dict(
            buid=_scrollableframe,
            editor="choice",
            values=("", "false", "true"),
            state="readonly",
            help=_("use horizontal scrollbar"),
        ),
        dict(
            buid=_scrolledtext,
            editor="choice",
            values=("", "false", "true"),
            state="readonly",
            help=_("include horizontal scrollbar"),
        ),
    ],
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
    "indicator_img": dict(
        buid=_radialpbar,
        editor="imageentry",
        help=_("indicator image for progressbar"),
    ),
    "max_chars": dict(
        buid=_scrolledtext,
        editor="naturalnumber",
        help=_(
            "maximum characters allowed in Text widget, "
             + "text will be truncated from the beginning to match the max chars"
        ),
    ),
    "parent_bg": dict(
        buid=_radialpbar,
        editor="colorentry",
        help=_("color of parent container"),
    ),
    "refresh_time": dict(
        buid=_autofitlabel,
        editor="naturalnumber",
        help=_("milliseconds"),
    ),
    "sbar_bg": dict(
        buid=[_scrollableframe, _scrolledtext],
        editor="colorentry",
        help=_("color of scrollbars' trough, default to frame's background"),
    ),
    "sbar_fg": dict(
        buid=[_scrollableframe, _scrolledtext],
        editor="colorentry",
        help=_("color of scrollbars' slider"),
    ),
    "slider_color": dict(buid=_simplesbar, editor="colorentry"),
    "text_color": dict(
        buid=_checkbutton,
        editor="colorentry",
    ),
    "text_bg": dict(buid=_radialpbar3d, editor="colorentry"),
    "text_fg": [
        dict(
            buid=_radialpbar,
            editor="colorentry",
            help=_("percentage text color"),
        ),
        dict(buid=_radialpbar3d, editor="colorentry"),
    ],
    "vscroll": [
        dict(
            buid=_scrollableframe,
            editor="choice",
            values=("", "false", "true"),
            state="readonly",
            help=_("use vertical scrollbar"),
        ),
        dict(
            buid=_scrolledtext,
            editor="choice",
            values=("", "false", "true"),
            state="readonly",
            help=_("include vertical scrollbar"),
        ),
    ],
    "vbar_width": [
        dict(
            buid=_scrollableframe,
            editor="dimensionentry",
            help=_("vertical scrollbar width"),
        ),
        dict(
            buid=_scrolledtext,
            editor="naturalnumber",
            help=_("vertical scrollbar width"),
        ),
    ],
    "width": [
        dict(buid=[_segmentbar, _simplesbar], editor="naturalnumber"),
        dict(
            buid=[_frame3d, _scrollableframe],
            editor="dimensionentry",
            default_value=200,
        ),
    ],
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
