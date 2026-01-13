# encoding: utf-8
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from pygubu.widgets.calendarframe import CalendarFrame
from ._config import nspygubu, _designer_tabs_widgets_ttk


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


register_widget(
    nspygubu.widgets.CalendarFrame,
    CalendarFrameBuilder,
    "CalendarFrame",
    _designer_tabs_widgets_ttk,
)
# Register old name until removal
register_widget(
    nspygubu.builder_old.calendarframe, CalendarFrameBuilder, public=False
)
