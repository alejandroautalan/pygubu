# encoding: utf-8
from pygubu.api.v1 import register_widget
from pygubu.plugins.ttk.ttkstdwidgets import (
    TTKTreeviewBO,
    TTKTreeviewColumnBO,
)
from .scrollbarhelper import TTKSBHelperBO
from pygubu.i18n import _
from pygubu.widgets.editabletreeview import EditableTreeview


class EditableTreeviewBO(TTKTreeviewBO):
    class_ = EditableTreeview
    virtual_events = TTKTreeviewBO.virtual_events + (
        "<<TreeviewInplaceEdit>>",
        "<<TreeviewCellEdited>>",
    )


classid = "pygubu.builder.widgets.editabletreeview"
if classid not in TTKTreeviewColumnBO.allowed_parents:
    TTKTreeviewColumnBO.add_allowed_parent(classid)
if classid not in TTKSBHelperBO.allowed_children:
    TTKSBHelperBO.add_allowed_child(classid)

register_widget(
    "pygubu.builder.widgets.editabletreeview",
    EditableTreeviewBO,
    "EditableTreeview",
    (_("Pygubu Widgets"), "ttk"),
)
