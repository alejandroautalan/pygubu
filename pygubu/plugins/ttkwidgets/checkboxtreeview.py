from pygubu.api.v1 import register_widget
from pygubu.plugins.ttk.ttkstdwidgets import TTKTreeviewBO, TTKTreeviewColumnBO
from pygubu.plugins.pygubu.scrollbarhelper import TTKSBHelperBO
from ttkwidgets.checkboxtreeview import CheckboxTreeview

from ..ttkwidgets import _designer_tab_label, _plugin_uid


class CheckboxTreeviewBO(TTKTreeviewBO):
    class_ = CheckboxTreeview
    allowed_children = ("ttk.Treeview.Column",)


_builder_uid = f"{_plugin_uid}.CheckboxTreeview"
register_widget(
    _builder_uid,
    CheckboxTreeviewBO,
    "CheckboxTreeview",
    ("ttk", _designer_tab_label),
)

TTKSBHelperBO.add_allowed_child(_builder_uid)
TTKTreeviewColumnBO.add_allowed_parent(_builder_uid)
