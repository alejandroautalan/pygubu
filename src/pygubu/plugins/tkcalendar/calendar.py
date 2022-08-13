from pygubu.api.v1 import register_widget, register_custom_property
from tkcalendar import Calendar

from ..tkcalendar import _designer_tab_label, _plugin_uid
from .basecalendar import CalendarBaseBO, _base_prop_desc


class CalendarBO(CalendarBaseBO):
    class_ = Calendar
    OPTIONS_STANDARD = ("class_", "cursor")
    OPTIONS_SPECIFIC = ("borderwidth", "state")
    properties = (
        OPTIONS_STANDARD + OPTIONS_SPECIFIC + CalendarBaseBO.OPTIONS_CUSTOM
    )
    ro_properties = CalendarBaseBO.ro_properties + ("class_",)
    virtual_events = ("<<CalendarSelected>>", "<<CalendarMonthChanged>>")


_builder_id = f"{_plugin_uid}.Calendar"

register_widget(
    _builder_id,
    CalendarBO,
    "Calendar",
    ("ttk", _designer_tab_label),
)

for pname, editor, options in _base_prop_desc:
    register_custom_property(_builder_id, pname, editor, **options)
