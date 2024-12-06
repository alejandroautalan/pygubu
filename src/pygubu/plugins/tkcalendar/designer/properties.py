from pygubu.i18n import _
from pygubu.api.v1 import register_custom_property
from pygubu.plugins.tkcalendar import _plugin_uid


_builder_all = f"{_plugin_uid}.*"
_calendar = f"{_plugin_uid}.Calendar"
_dateentry = f"{_plugin_uid}.DateEntry"

_none = {}
_base_prop_desc = (
    (
        "year",
        "naturalnumber",
        {"help": _("intinitially displayed year, default is current year.")},
    ),
    (
        "month",
        "naturalnumber",
        {"help": _("initially displayed month, default is current month.")},
    ),
    ("day", "naturalnumber", {"help": "initially selected day"}),
    (
        "firstweekday",
        "choice",
        {
            "values": ("", "monday", "sunday"),
            "state": "readonly",
            "help": _("first day of the week"),
        },
    ),
    (
        "mindate",
        "entry",
        {"help": _("minimum allowed date (string with format yyyy-mm-dd)")},
    ),
    (
        "maxdate",
        "entry",
        {"help": _("maximum allowed date (string with format yyyy-mm-dd)")},
    ),
    (
        "showweeknumbers",
        "choice",
        {
            "values": ("", "true", "false"),
            "state": "readonly",
            "help": _("whether to display week numbers"),
        },
    ),
    (
        "showothermonthdays",
        "choice",
        {
            "values": ("", "true", "false"),
            "state": "readonly",
            "help": _(
                "whether to display the last days of the previous month and the first of the next month."
            ),
        },
    ),
    (
        "date_pattern",
        "choice",
        {
            "values": (
                "",
                "dd/mm/yy",
                "dd/mm/yyyy",
                "mm/dd/yy",
                "mm/dd/yyyy",
                "yyyy/mm/dd",
            ),
            "state": "normal",
            "help": _("date pattern used to format the date as a string."),
        },
    ),
    (
        "selectmode",
        "choice",
        {"values": ("", "none", "day"), "state": "readonly"},
    ),
    (
        "textvariable",
        "tkvarentry",
        {"help": _("connect the currently selected date to the variable.")},
    ),
    ("background", "colorentry", _none),
    ("foreground", "colorentry", _none),
    ("disabledbackground", "colorentry", _none),
    ("disabledforeground", "colorentry", _none),
    ("bordercolor", "colorentry", _none),
    ("headersbackground", "colorentry", _none),
    ("headersforeground", "colorentry", _none),
    ("selectbackground", "colorentry", _none),
    ("selectforeground", "colorentry", _none),
    ("disabledselectbackground", "colorentry", _none),
    ("disabledselectforeground", "colorentry", _none),
    ("normalbackground", "colorentry", _none),
    ("normalforeground", "colorentry", _none),
    ("weekendbackground", "colorentry", _none),
    ("weekendforeground", "colorentry", _none),
    ("othermonthforeground", "colorentry", _none),
    ("othermonthbackground", "colorentry", _none),
    ("othermonthweforeground", "colorentry", _none),
    ("othermonthwebackground", "colorentry", _none),
    ("disableddaybackground", "colorentry", _none),
    ("disableddayforeground", "colorentry", _none),
    ("tooltipforeground", "colorentry", _none),
    ("tooltipbackground", "colorentry", _none),
    (
        "tooltipalpha",
        "spinbox",
        {
            "from_": 0.1,
            "to": 1,
            "increment": 0.1,
            "help": _("tooltip opacity between 0 and 1"),
        },
    ),
    (
        "tooltipdelay",
        "naturalnumber",
        {"help": _("delay in ms before displaying the tooltip")},
    ),
)


for pname, editor, options in _base_prop_desc:
    register_custom_property(_calendar, pname, editor, **options)
    register_custom_property(_dateentry, pname, editor, **options)

register_custom_property(
    _dateentry,
    "calendar_cursor",
    "cursorentry",
)
