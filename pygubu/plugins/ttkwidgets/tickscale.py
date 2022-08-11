import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.ttk.ttkstdwidgets import TTKScale
from ttkwidgets.tickscale import TickScale

from ..ttkwidgets import _designer_tab_label, _plugin_uid


class TickScaleBO(TTKScale):
    class_ = TickScale
    OPTIONS_CUSTOM = (
        "digits",
        "labelpos",
        "resolution",
        "showvalue",
        "tickinterval",
        "tickpos",
    )
    properties = (
        TTKScale.OPTIONS_STANDARD + TTKScale.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = TTKScale.ro_properties + ("from_", "to")

    def _process_property_value(self, pname, value):
        final_value = value
        if pname in ("digits",):
            final_value = int(value)
        elif pname in ("from", "to_", "resolution", "tickinterval"):
            final_value = float(value)
        else:
            final_value = super(TickScaleBO, self)._process_property_value(
                pname, value
            )
        return final_value


_builder_uid = f"{_plugin_uid}.TickScale"

register_widget(
    _builder_uid,
    TickScaleBO,
    "TickScale",
    ("ttk", _designer_tab_label),
    group=3,
)

register_custom_property(_builder_uid, "digits", "naturalnumber")
register_custom_property(
    _builder_uid,
    "resolution",
    "realnumber",
    help=_(
        "increment by which the slider can be moved. 0 means continuous sliding."
    ),
)
register_custom_property(
    _builder_uid,
    "tickinterval",
    "realnumber",
    help=_("if not 0, display ticks with the given interval"),
)
register_custom_property(
    _builder_uid,
    "showvalue",
    "choice",
    values=("", "true", "false"),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "labelpos",
    "choice",
    help="if showvalue is True, position of the label",
    values=("", tk.N, tk.S, tk.E, tk.W),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "tickpos",
    "choice",
    help=_("if tickinterval is not 0, position of the ticks"),
    values=("", tk.N, tk.S, tk.E, tk.W),
    state="readonly",
)
