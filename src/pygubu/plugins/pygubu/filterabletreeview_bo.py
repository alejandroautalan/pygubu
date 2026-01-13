# encoding: utf-8
from pygubu.api.v1 import register_widget
from pygubu.plugins.ttk.ttkstdwidgets import (
    TTKTreeviewBO,
    TTKTreeviewColumnBO,
)
from .scrollbarhelper_bo import TTKSBHelperBO
from pygubu.widgets.filterabletreeview import FilterableTreeview
from ._config import nspygubu, _designer_tabs_widgets_ttk


class FilterableTreeviewBO(TTKTreeviewBO):
    class_ = FilterableTreeview
    # virtual_events = TTKTreeviewBO.virtual_events + (
    #     "<<FilterableTreeview:NoResults>>",
    # )


_builder_uid = nspygubu.widgets.FilterableTreeview
if _builder_uid not in TTKTreeviewColumnBO.allowed_parents:
    TTKTreeviewColumnBO.add_allowed_parent(_builder_uid)
if _builder_uid not in TTKSBHelperBO.allowed_children:
    TTKSBHelperBO.add_allowed_child(_builder_uid)

register_widget(
    _builder_uid,
    FilterableTreeviewBO,
    "FilterableTreeview",
    _designer_tabs_widgets_ttk,
)
