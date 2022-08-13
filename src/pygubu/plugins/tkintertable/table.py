import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.utils.font import tkfontstr_to_tuple
from tkintertable import TableCanvas
from ..tkintertable import _designer_tab_label, _plugin_uid


class TableCanvasBuilder(BuilderObject):
    class_ = TableCanvas
    OPTIONS_CUSTOM = (
        "read_only",
        "width",
        "height",
        "bgcolor",
        "fgcolor",
        "rows",
        "cols",
        "cellwidth",
        "maxcellwidth",
        "rowheight",
        "horizlines",
        "vertlines",
        "alternaterows",
        "autoresizecols",
        "linewidth",
        "rowheaderwidth",
        "showkeynamesinheader",
        "thefont",
        "entrybackgr",
        "grid_color",
        "selectedcolor",
        "rowselectedcolor",
        "multipleselectioncolor",
    )
    ro_properties = OPTIONS_CUSTOM
    layout_required = False

    def _process_property_value(self, pname, value):
        if pname in (
            "rows",
            "cols",
            "cellwidth",
            "maxcellwidth",
            "rowheight",
            "rowheaderwidth",
        ):
            value = int(value)
        elif pname == "linewidth":
            value = float(value)
        elif pname in ("read_only", "showkeynamesinheader"):
            value = tk.getboolean(value)
        elif pname == "thefont":
            value = tkfontstr_to_tuple(value)
        elif pname in (
            "horizlines",
            "vertlines",
            "alternaterows",
            "autoresizecols",
        ):
            value = int(tk.getboolean(value))
        return value

    def layout(self, target=None, configure_gridrc=True):
        self.widget.show()

    def code_layout(self, targetid=None, parentid=None):
        if targetid is None:
            targetid = self.code_identifier()
        return [f"{targetid}.show()"]

    def _code_process_property_value(self, targetid, pname, value: str):
        pvalue = self._process_property_value(pname, value)
        if pname in ("thefont", "showkeynamesinheader"):
            return pvalue
        pvalue = f"{pvalue}"
        return super()._code_process_property_value(targetid, pname, pvalue)


_builder_uid = f"{_plugin_uid}.TableCanvas"
register_widget(
    _builder_uid,
    TableCanvasBuilder,
    "TableCanvas",
    ("ttk", _designer_tab_label),
)

register_custom_property(
    _builder_uid,
    "read_only",
    "choice",
    values=("", "true", "false"),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "width",
    "dimensionentry",
)
register_custom_property(
    _builder_uid,
    "height",
    "dimensionentry",
)
register_custom_property(
    _builder_uid,
    "bgcolor",
    "colorentry",
)
register_custom_property(
    _builder_uid,
    "fgcolor",
    "colorentry",
)
register_custom_property(
    _builder_uid,
    "rows",
    "naturalnumber",
)
register_custom_property(
    _builder_uid,
    "cols",
    "naturalnumber",
)
register_custom_property(
    _builder_uid,
    "cellwidth",
    "naturalnumber",
)
register_custom_property(
    _builder_uid,
    "maxcellwidth",
    "naturalnumber",
)
register_custom_property(
    _builder_uid,
    "rowheight",
    "naturalnumber",
)
register_custom_property(
    _builder_uid,
    "horizlines",
    "choice",
    values=("", "true", "false"),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "vertlines",
    "choice",
    values=("", "true", "false"),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "alternaterows",
    "choice",
    values=("", "true", "false"),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "autoresizecols",
    "choice",
    values=("", "true", "false"),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "linewidth",
    "realnumber",
)
register_custom_property(
    _builder_uid,
    "rowheaderwidth",
    "naturalnumber",
)
register_custom_property(
    _builder_uid,
    "showkeynamesinheader",
    "choice",
    values=("", "true", "false"),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "thefont",
    "fontentry",
)
register_custom_property(
    _builder_uid,
    "entrybackgr",
    "colorentry",
)
register_custom_property(
    _builder_uid,
    "grid_color",
    "colorentry",
)
register_custom_property(
    _builder_uid,
    "selectedcolor",
    "colorentry",
)
register_custom_property(
    _builder_uid,
    "rowselectedcolor",
    "colorentry",
)
register_custom_property(
    _builder_uid,
    "multipleselectioncolor",
    "colorentry",
)
