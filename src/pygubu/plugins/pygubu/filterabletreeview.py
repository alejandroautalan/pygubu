# encoding: utf-8
from pygubu.api.v1 import register_widget
from pygubu.plugins.ttk.ttkstdwidgets import (
    TTKTreeviewBO,
    TTKTreeviewColumnBO,
)
from .scrollbarhelper import TTKSBHelperBO
from pygubu.i18n import _
from pygubu.widgets.filterabletreeview import FilterableTreeview


class FilterableTreeviewBO(TTKTreeviewBO):
    class_ = FilterableTreeview
    # virtual_events = TTKTreeviewBO.virtual_events + (
    #     "<<FilterableTreeview:NoResults>>",
    # )


_builder_uid = "pygubu.widgets.FilterableTreeview"
if _builder_uid not in TTKTreeviewColumnBO.allowed_parents:
    TTKTreeviewColumnBO.add_allowed_parent(_builder_uid)
if _builder_uid not in TTKSBHelperBO.allowed_children:
    TTKSBHelperBO.add_allowed_child(_builder_uid)

register_widget(
    _builder_uid,
    FilterableTreeviewBO,
    "FilterableTreeview",
    (_("Pygubu Widgets"), "ttk"),
)
