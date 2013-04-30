import tkinter as tk
from tkinter import ttk

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


__scrolltype_property = {
    'input_method': 'choice',
    'values': (ScrollbarHelper.BOTH, ScrollbarHelper.VERTICAL,
        ScrollbarHelper.HORIZONTAL),
    'default': ScrollbarHelper.HORIZONTAL }

register_property('scrolltype', __scrolltype_property)


register_widget('pygubu.builder.widgets.scrollbarhelper', TTKSBHelperBO,
    'ScrollbarHelper', ('Pygubu Helpers', 'ttk'))

