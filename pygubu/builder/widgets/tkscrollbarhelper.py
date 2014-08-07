# encoding: utf8

from __future__ import unicode_literals
from pygubu.builder.builderobject import *
from pygubu.widgets.tkscrollbarhelper import TkScrollbarHelper


class TKSBHelperBO(BuilderObject):
    class_ = TkScrollbarHelper
    container = False
    maxchildren = 1
    allowed_children = ('tk.Entry', 'ttk.Entry', 'tk.Text', 'tk.Canvas',
                        'tk.Listbox', 'ttk.Treeview')
    OPTIONS_STANDARD = ('borderwidth', 'cursor', 'highlightbackground',
                        'highlightcolor', 'highlightthickness',
                        'padx', 'pady', 'relief', 'takefocus')
    OPTIONS_SPECIFIC = ('background',  'class_', 'container',
                        'height', 'width')
    OPTIONS_CUSTOM = ('scrolltype',)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = ('class_', 'scrolltype', )
    allow_bindings = False

    def add_child(self, bobject):
        cwidget = bobject.widget
        self.widget.add_child(cwidget)


register_widget('pygubu.builder.widgets.tkscrollbarhelper', TKSBHelperBO,
                'ScrollbarHelper', ('Pygubu Helpers', 'tk'))
