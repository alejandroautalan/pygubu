# encoding: utf-8
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from pygubu.widgets.calendarframe import CalendarFrame
from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid


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
        "linewidth",
    )
    ro_properties = TTKFrame.ro_properties
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    virtual_events = ("<<CalendarFrameDateSelected>>",)


_builder_id = f"{_plugin_uid}.CalendarFrame"
register_widget(
    _builder_id,
    CalendarFrameBuilder,
    "CalendarFrame",
    ("ttk", _tab_widgets_label),
)
# Register old name until removal
register_widget(
    "pygubu.builder.widgets.calendarframe", CalendarFrameBuilder, public=False
)
