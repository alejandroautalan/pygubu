# encoding: utf-8
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from pygubu.i18n import _
from pygubu.widgets.calendarframe import CalendarFrame


class CalendarFrameBuilder(BuilderObject):
    class_ = CalendarFrame
    OPTIONS_STANDARD = TTKFrame.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = TTKFrame.OPTIONS_SPECIFIC
    OPTIONS_CUSTOM = (
        "firstweekday",
        "year",
        "month",
        "calendarfg",
        "calendarbg",
        "headerfg",
        "headerbg",
        "selectbg",
        "selectfg",
        "state",
        "markbg",
        "markfg",
    )
    ro_properties = TTKFrame.ro_properties
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    virtual_events = ("<<CalendarFrameDateSelected>>",)


_builder_id = "pygubu.builder.widgets.calendarframe"
register_widget(
    _builder_id,
    CalendarFrameBuilder,
    "CalendarFrame",
    ("ttk", _("Pygubu Widgets")),
)

register_custom_property(
    _builder_id,
    "state",
    "choice",
    values=("", "normal", "disabled"),
    state="readonly",
)
register_custom_property(
    _builder_id,
    "firstweekday",
    "choice",
    values=("0", "6"),
    state="readonly",
    default_value="6",
)
register_custom_property(_builder_id, "year", "entry")
register_custom_property(
    _builder_id,
    "month",
    "choice",
    values=("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"),
    state="readonly",
    default_value="1",
)
register_custom_property(_builder_id, "calendarfg", "colorentry")
register_custom_property(_builder_id, "calendarbg", "colorentry")
register_custom_property(_builder_id, "headerfg", "colorentry")
register_custom_property(_builder_id, "headerbg", "colorentry")
register_custom_property(_builder_id, "selectbg", "colorentry")
register_custom_property(_builder_id, "selectfg", "colorentry")
register_custom_property(_builder_id, "markbg", "colorentry")
register_custom_property(_builder_id, "markfg", "colorentry")
