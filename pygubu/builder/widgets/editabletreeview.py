# encoding: utf8
from __future__ import unicode_literals
from pygubu.builder.builderobject import *
from pygubu.builder.ttkstdwidgets import TTKTreeviewBO, TTKTreeviewColBO
from pygubu.builder.widgets.scrollbarhelper import TTKSBHelperBO
from pygubu.widgets.editabletreeview import EditableTreeview


class EditableTreeviewBO(TTKTreeviewBO):
    class_ = EditableTreeview
    virtual_events = ('<<TreeviewInplaceEdit>>', '<<TreeviewCellEdited>>')


classid = 'pygubu.builder.widgets.editabletreeview'
if classid not in TTKTreeviewColBO.allowed_parents:
    TTKTreeviewColBO.allowed_parents = \
        TTKTreeviewColBO.allowed_parents + (classid, )
if classid not in TTKSBHelperBO.allowed_children:
    TTKSBHelperBO.allowed_children = \
        TTKSBHelperBO.allowed_children + (classid, )

register_widget('pygubu.builder.widgets.editabletreeview', EditableTreeviewBO,
                'EditableTreeview', ('Pygubu Widgets', 'ttk'))
