from pygubu.api.v1 import register_widget
from pygubu.plugins.ttk.ttkstdwidgets import TTKEntry
from tkcalendar import DateEntry

from ..tkcalendar import _designer_tab_label, _plugin_uid
from .basecalendar import CalendarBaseBO


class DateEntryBO(CalendarBaseBO, TTKEntry):
    class_ = DateEntry
    OPTIONS_CUSTOM = CalendarBaseBO.OPTIONS_CUSTOM + ("calendar_cursor",)
    properties = (
        TTKEntry.OPTIONS_STANDARD + TTKEntry.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = CalendarBaseBO.ro_properties + ("calendar_cursor",)
    virtual_events = ("<<DateEntrySelected>>",)


_builder_id = f"{_plugin_uid}.DateEntry"

register_widget(
    _builder_id,
    DateEntryBO,
    "DateEntry",
    ("ttk", _designer_tab_label),
)
