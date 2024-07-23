import tkinter as tk
from pygubu.api.v1 import register_custom_property
from pygubu.plugins.pygubu import _designer_tab_label, _plugin_uid


_builder_uid = f"{_plugin_uid}.*"
_AccordionFrame = f"{_plugin_uid}.AccordionFrame"
_AccordionFrameGroup = f"{_plugin_uid}.AccordionFrameGroup"
_CalendarFrame = f"{_plugin_uid}.CalendarFrame"

plugin_properties = {
    "calendarfg": dict(buid=_CalendarFrame, editor="colorentry"),
    "calendarbg": dict(buid=_CalendarFrame, editor="colorentry"),
    "compound": dict(
        buid=_AccordionFrameGroup,
        editor="choice",
        values=(
            "",
            tk.LEFT,
            tk.RIGHT,
            tk.NONE,
        ),
        state="readonly",
    ),
    "firstweekday": dict(
        buid=_CalendarFrame,
        editor="choice",
        values=("0", "6"),
        state="readonly",
        default_value="6",
    ),
    "headerbg": dict(buid=_CalendarFrame, editor="colorentry"),
    "headerfg": dict(buid=_CalendarFrame, editor="colorentry"),
    "height": dict(
        buid=_AccordionFrame, editor="dimensionentry", default_value="200"
    ),
    "img_expand": dict(editor="imageentry"),
    "img_collapse": dict(editor="imageentry"),
    "label": dict(buid=_AccordionFrameGroup),
    "linewidth": dict(
        buid=_CalendarFrame,
        editor="choice",
        values=("1", "2", "3", "4"),
        state="readonly",
        default_value="1",
    ),
    "mask": dict(buid=f"{_plugin_uid}.Floodgauge"),
    "markbg": dict(buid=_CalendarFrame, editor="colorentry"),
    "markfg": dict(buid=_CalendarFrame, editor="colorentry"),
    "month": dict(
        buid=_CalendarFrame,
        editor="choice",
        values=(
            "",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        ),
        state="readonly",
    ),
    "selectbg": dict(buid=_CalendarFrame, editor="colorentry"),
    "selectfg": dict(buid=_CalendarFrame, editor="colorentry"),
    "state": dict(
        buid=_CalendarFrame,
        editor="choice",
        values=("", "normal", "disabled"),
        state="readonly",
    ),
    "style": dict(
        buid=_AccordionFrameGroup,
        editor="ttkstylechoice",
        default_value="Toolbutton",
    ),
    "expanded": dict(
        buid=_AccordionFrameGroup,
        editor="choice",
        values=("", "false", "true"),
        state="readonly",
    ),
    "width": dict(
        buid=_AccordionFrame, editor="dimensionentry", default_value="200"
    ),
    "year": dict(buid=_CalendarFrame, editor="naturalnumber"),
}

for prop in plugin_properties:
    definitions = plugin_properties[prop]
    if isinstance(definitions, dict):
        definitions = [definitions]
    for definition in definitions:
        builder_uid = definition.pop("buid", _builder_uid)
        editor = definition.pop("editor", "entry")
        register_custom_property(builder_uid, prop, editor, **definition)
