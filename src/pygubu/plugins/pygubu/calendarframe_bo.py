# encoding: utf-8
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from pygubu.widgets.calendarframe import CalendarView, CalendarFrame
from ._config import nspygubu, _section_widgets, GDISPLAY


class CalendarViewBO(BuilderObject):
    class_ = CalendarView
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
    virtual_events = (CalendarView.EVENT_DATE_SELECTED,)


register_widget(
    nspygubu.widgets.CalendarView,
    CalendarViewBO,
    "CalendarView",
    _section_widgets,
    group=GDISPLAY,
)


class CalendarFrameBO(CalendarViewBO):
    class_ = CalendarFrame
    virtual_events = (CalendarFrame.EVENT_DATE_SELECTED,)


# Register deprecated name until removal
register_widget(
    nspygubu.widgets.CalendarFrame,
    CalendarFrameBO,
    "CalendarFrame",
    _section_widgets,
    group=GDISPLAY,
    public=False,
)
# Register old name until removal
register_widget(
    nspygubu.builder_old.calendarframe, CalendarFrameBO, public=False
)
