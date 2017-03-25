# encoding: utf8
from __future__ import unicode_literals
from pygubu.builder.builderobject import *
from pygubu.widgets.scrollbarhelper import ScrollbarHelper


class TTKSBHelperBO(BuilderObject):
    class_ = ScrollbarHelper
    container = True
    maxchildren = 1
    allowed_children = ('tk.Entry', 'ttk.Entry', 'tk.Text', 'tk.Canvas',
                        'tk.Listbox', 'ttk.Treeview' )
    OPTIONS_STANDARD = ('class_', 'cursor', 'takefocus', 'style')
    OPTIONS_SPECIFIC = ('borderwidth', 'relief', 'padding', 'height', 'width')
    OPTIONS_CUSTOM = ('scrolltype', 'usemousewheel')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = ('class_', 'scrolltype')
    allow_bindings = False


    def add_child(self, bobject):
        cwidget = bobject.widget
        self.widget.add_child(cwidget)


register_widget('pygubu.builder.widgets.scrollbarhelper', TTKSBHelperBO,
    'ScrollbarHelper', ('Pygubu Helpers', 'ttk'))
