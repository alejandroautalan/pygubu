import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.ttk.ttkstdwidgets import TTKTreeviewBO, TTKTreeviewColumnBO
from pygubu.plugins.pygubu.scrollbarhelper import TTKSBHelperBO
from ttkwidgets.table import Table

from ..ttkwidgets import _designer_tab_label, _plugin_uid


class TableBO(TTKTreeviewBO):
    class_ = Table
    OPTIONS_SPECIFIC = ("height", "padding", "selectmode")
    OPTIONS_CUSTOM = ("drag_cols", "drag_rows", "sortable")
    properties = (
        TTKTreeviewBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )

    def _process_property_value(self, pname, value):
        final_value = value
        if pname in ("drag_cols", "drag_rows", "sortable"):
            final_value = tk.getboolean(value)
        else:
            final_value = super(TableBO, self)._process_property_value(
                pname, value
            )
        return final_value


_builder_uid = _table_uid = f"{_plugin_uid}.Table"
register_widget(
    _builder_uid, TableBO, "Table", ("ttk", _designer_tab_label), group=6
)

register_custom_property(
    _builder_uid,
    "drag_cols",
    "choice",
    values=("", "true", "false"),
    default_value="true",
    help=_("whether columns are draggable"),
)
register_custom_property(
    _builder_uid,
    "drag_rows",
    "choice",
    values=("", "true", "false"),
    default_value="true",
    help=_("whether rows are draggable"),
)
register_custom_property(
    _builder_uid,
    "sortable",
    "choice",
    values=("", "true", "false"),
    default_value="true",
    help=_(
        "whether columns are sortable by clicking on their headings. The sorting order depends on the type of data (str, float, ...) which can be set with the column method."
    ),
)

TTKSBHelperBO.add_allowed_child(_table_uid)


class TableColumnBO(TTKTreeviewColumnBO):
    OPTIONS_CUSTOM = ("type",)
    properties = (
        TTKTreeviewBO.OPTIONS_STANDARD
        + TTKTreeviewBO.OPTIONS_SPECIFIC
        + OPTIONS_CUSTOM
    )
    allowed_parents = (_table_uid,)

    def _get_column_properties(self, props):
        colprop = super(TableColumnBO, self)._get_column_properties(props)
        type_value = props.get("type", None)
        if type_value is not None:
            final_value = str
            if type_value in ("str", "int", "float", "bool"):
                final_value = eval(type_value)
            colprop["type"] = final_value
        # Setup required anchor
        if colprop["anchor"] == "":
            colprop["anchor"] = "nw"
        return colprop


_builder_uid = f"{_plugin_uid}.Table.Column"

TableBO.add_allowed_child(_builder_uid)

register_widget(
    _builder_uid,
    TableColumnBO,
    "Table.Column",
    ("ttk", _designer_tab_label),
    group=6,
)

register_custom_property(
    _builder_uid,
    "type",
    "choice",
    values=("", "str", "int", "float", "bool"),
    state="readonly",
)
