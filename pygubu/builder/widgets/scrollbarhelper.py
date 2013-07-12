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
    properties = ['scrolltype', 'cursor', 'height', 'padding',
            'relief', 'style', 'takefocus', 'width']
    ro_properties = ('scrolltype', )
    allow_bindings = False


    def add_child(self, bobject):
        cwidget = bobject.widget
        self.widget.add_child(cwidget)


register_widget('pygubu.builder.widgets.scrollbarhelper', TTKSBHelperBO,
    'ScrollbarHelper', ('Pygubu Helpers', 'ttk'))
