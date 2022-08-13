from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from ttkwidgets import Calendar

from ..ttkwidgets import _designer_tab_label, _plugin_uid


class CalendarBO(TTKFrame):
    class_ = Calendar
    container = False
    OPTIONS_CUSTOM = (
        "locale",
        "firstweekday",
        "year",
        "month",
        "selectbackground",
        "selectforeground",
    )
    properties = (
        TTKFrame.OPTIONS_STANDARD + TTKFrame.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    # FIXME: set all custom properties as readonly, there is a bug in the
    # ttkwidgets widget definition.
    ro_properties = TTKFrame.ro_properties + OPTIONS_CUSTOM

    def _process_property_value(self, pname, value):
        if pname in ("firstweekday", "year", "month"):
            return int(value)
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.Calendar"
register_widget(
    _builder_uid, CalendarBO, "Calendar", ("ttk", _designer_tab_label), group=2
)

register_custom_property(
    _builder_uid,
    "locale",
    "entry",
    help=_("calendar locale (defines the language, date formatting)"),
)
register_custom_property(
    _builder_uid,
    "firstweekday",
    "choice",
    values=("", 0, 1, 2, 3, 4, 5, 6),
    state="readonly",
    help=_("first day of the week, 0 is monday"),
)
register_custom_property(
    _builder_uid, "year", "integernumber", help=_("year to display")
)
register_custom_property(
    _builder_uid,
    "month",
    "choice",
    values=("", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
    state="readonly",
    help=_("month to display"),
)
register_custom_property(
    _builder_uid,
    "selectbackground",
    "colorentry",
    help=_("background color of the selected day"),
)
register_custom_property(
    _builder_uid,
    "selectforeground",
    "colorentry",
    help=_("selectforeground color of the selected day"),
)
