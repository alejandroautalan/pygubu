import tkinter as tk
from datetime import datetime
from pygubu.api.v1 import BuilderObject


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
