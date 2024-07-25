# encoding: utf-8
from pygubu.api.v1 import register_widget
from pygubu.plugins.ttk.ttkstdwidgets import (
    TTKTreeviewBO,
    TTKTreeviewColumnBO,
)
from .scrollbarhelper_bo import TTKSBHelperBO
from pygubu.widgets.editabletreeview import EditableTreeview
from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid


class EditableTreeviewBO(TTKTreeviewBO):
    class_ = EditableTreeview
    virtual_events = TTKTreeviewBO.virtual_events + (
        "<<TreeviewInplaceEdit>>",
        "<<TreeviewCellEdited>>",
        "<<TreeviewEditorsUnfocused>>",
    )


_builder_uid = f"{_plugin_uid}.EditableTreeview"
if _builder_uid not in TTKTreeviewColumnBO.allowed_parents:
    TTKTreeviewColumnBO.add_allowed_parent(_builder_uid)
if _builder_uid not in TTKSBHelperBO.allowed_children:
    TTKSBHelperBO.add_allowed_child(_builder_uid)

register_widget(
    _builder_uid,
    EditableTreeviewBO,
    "EditableTreeview",
    (_tab_widgets_label, "ttk"),
)

# Register old name until removal
register_widget(
    "pygubu.builder.widgets.editabletreeview", EditableTreeviewBO, public=False
)
