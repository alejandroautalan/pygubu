import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.tk.tkstdwidgets import TKListbox
from ttkwidgets.scrolledlistbox import ScrolledListbox

from ..ttkwidgets import _designer_tab_label, _plugin_uid


class ScrolledListboxBO(TKListbox):
    class_ = ScrolledListbox
    container = False
    OPTIONS_CUSTOM = ("compound", "autohidescrollbar")
    properties = (
        TKListbox.OPTIONS_STANDARD + TKListbox.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = TKListbox.ro_properties + OPTIONS_CUSTOM

    def configure(self, target=None):
        super(ScrolledListboxBO, self).configure(self.widget.listbox)

    def _process_property_value(self, pname, value):
        final_value = value
        if pname in ("autohidescrollbar",):
            final_value = tk.getboolean(value)
        elif pname == "compound":
            final_value = tk.RIGHT
            values = {"left": tk.LEFT, "right": tk.RIGHT}
            if value in values:
                final_value = values[value]
        else:
            final_value = super(
                ScrolledListboxBO, self
            )._process_property_value(pname, value)
        return final_value

    def code_configure(self, targetid=None):
        if targetid is None:
            targetid = self.code_identifier()
        newtarget = f"{targetid}.listbox"
        return super(ScrolledListboxBO, self).code_configure(newtarget)


_builder_uid = f"{_plugin_uid}.ScrolledListbox"
register_widget(
    _builder_uid,
    ScrolledListboxBO,
    "ScrolledListbox",
    ("ttk", _designer_tab_label),
    group=3,
)

register_custom_property(
    _builder_uid,
    "compound",
    "choice",
    default_value=tk.RIGHT,
    help="side for the Scrollbar to be on",
    values=("", tk.LEFT, tk.RIGHT),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "autohidescrollbar",
    "choice",
    values=("", "true", "false"),
    state="readonly",
)
