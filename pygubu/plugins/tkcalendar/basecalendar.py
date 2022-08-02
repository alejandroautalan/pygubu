import tkinter as tk
from datetime import datetime
from pygubu.api.v1 import BuilderObject
from pygubu.i18n import _


class CalendarBaseBO(BuilderObject):
    OPTIONS_CUSTOM = (
        "year",
        "month",
        "day",
        "firstweekday",
        "mindate",
        "maxdate",
        "showweeknumbers",
        "showothermonthdays",
        "date_pattern",
        "selectmode",
        "textvariable",
        "background",
        "foreground",
        "disabledbackground",
        "disabledforeground",
        "bordercolor",
        "headersbackground",
        "headersforeground",
        "selectbackground",
        "selectforeground",
        "disabledselectbackground",
        "disabledselectforeground",
        "normalbackground",
        "normalforeground",
        "weekendbackground",
        "weekendforeground",
        "othermonthforeground",
        "othermonthbackground",
        "othermonthweforeground",
        "othermonthwebackground",
        "disableddaybackground",
        "disableddayforeground",
        "tooltipforeground",
        "tooltipbackground",
        "tooltipalpha",
        "tooltipdelay",
    )
    ro_properties = ("year", "month", "day")

    def _process_property_value(self, pname, value):
        if pname in ("year", "month", "day", "tooltipdelay"):
            return int(value)
        if pname in ("showweeknumbers", "showothermonthdays"):
            return tk.getboolean(value)
        if pname == "tooltipalpha":
            return float(value)
        if pname in ("mindate", "maxdate"):
            return datetime.strptime(value, "%Y-%m-%d")
        return super()._process_property_value(pname, value)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname in ("showweeknumbers", "showothermonthdays"):
            return self._process_property_value(pname, value)
        if pname in ("mindate", "maxdate"):
            return f"""Calendar.datetime.strptime("{value}", "%Y-%m-%d")"""
        return super()._code_process_property_value(targetid, pname, value)


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
