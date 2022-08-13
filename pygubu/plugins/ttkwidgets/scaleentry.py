import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from ttkwidgets.scaleentry import ScaleEntry

from ..ttkwidgets import _designer_tab_label, _plugin_uid


class ScaleEntryBO(TTKFrame):
    class_ = ScaleEntry
    container = False
    OPTIONS_CUSTOM = (
        "scalewidth",
        "entrywidth",
        "from_",
        "to",
        "orient",
        "compound",
        "entryscalepad",
    )
    properties = (
        TTKFrame.OPTIONS_STANDARD + TTKFrame.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )

    def _process_property_value(self, pname, value):
        final_value = value
        if pname in (
            "scalewidth",
            "entrywidth",
            "from_",
            "to",
            "entryscalepad",
        ):
            final_value = int(value)
        elif pname == "compound":
            final_value = tk.RIGHT
            values = {
                "top": tk.TOP,
                "bottom": tk.BOTTOM,
                "left": tk.LEFT,
                "right": tk.RIGHT,
            }
            if value in values:
                final_value = values[value]
        else:
            final_value = super(ScaleEntryBO, self)._process_property_value(
                pname, value
            )
        return final_value


_builder_uid = f"{_plugin_uid}.ScaleEntry"
register_widget(
    _builder_uid,
    ScaleEntryBO,
    "ScaleEntry",
    ("ttk", _designer_tab_label),
    group=3,
)

register_custom_property(
    _builder_uid,
    "compound",
    "choice",
    default_value=tk.RIGHT,
    help=_("side the Entry must be on."),
    values=("", tk.TOP, tk.BOTTOM, tk.LEFT, tk.RIGHT),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "orient",
    "choice",
    default_value=tk.HORIZONTAL,
    help=_("scale orientation"),
    values=("", tk.HORIZONTAL, tk.VERTICAL),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "scalewidth",
    "naturalnumber",
    help=_("width of the Scale in pixels"),
)
register_custom_property(
    _builder_uid,
    "entrywidth",
    "naturalnumber",
    help=_("width of the Entry in characters"),
)
register_custom_property(
    _builder_uid, "from_", "naturalnumber", help=_("start value of the scale")
)
register_custom_property(
    _builder_uid, "to", "naturalnumber", help=_("end value of the scale")
)
register_custom_property(
    _builder_uid,
    "entryscalepad",
    "naturalnumber",
    help=_("space between the entry and the scale"),
)
