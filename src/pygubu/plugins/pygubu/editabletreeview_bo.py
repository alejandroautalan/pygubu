# encoding: utf-8
from pygubu.api.v1 import register_widget
from pygubu.plugins.ttk.ttkstdwidgets import (
    TTKTreeviewBO,
    TTKTreeviewColumnBO,
)
from .scrollbarhelper_bo import TTKSBHelperBO
from pygubu.widgets.editabletreeview import EditableTreeview
from ._config import nspygubu, _designer_tabs_widgets_ttk, GDISPLAY


class EditableTreeviewBO(TTKTreeviewBO):
    class_ = EditableTreeview
    virtual_events = TTKTreeviewBO.virtual_events + (
        "<<TreeviewInplaceEdit>>",
        "<<TreeviewCellEdited>>",
        "<<TreeviewEditorsUnfocused>>",
    )


_builder_uid = nspygubu.widgets.EditableTreeview
if _builder_uid not in TTKTreeviewColumnBO.allowed_parents:
    TTKTreeviewColumnBO.add_allowed_parent(_builder_uid)
if _builder_uid not in TTKSBHelperBO.allowed_children:
    TTKSBHelperBO.add_allowed_child(_builder_uid)

register_widget(
    _builder_uid,
    EditableTreeviewBO,
    "EditableTreeview",
    _designer_tabs_widgets_ttk,
    group=GDISPLAY,
)

# Register old name until removal
_old_name = nspygubu.builder_old.editabletreeview
register_widget(_old_name, EditableTreeviewBO, public=False)
if _old_name not in TTKTreeviewColumnBO.allowed_parents:
    TTKTreeviewColumnBO.add_allowed_parent(_old_name)
if _old_name not in TTKSBHelperBO.allowed_children:
    TTKSBHelperBO.add_allowed_child(_old_name)
