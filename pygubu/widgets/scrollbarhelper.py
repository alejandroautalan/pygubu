import tkinter as tk
from tkinter import ttk

from ..builderobject import *


def _autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed.
    Code from Joe English (JE) at http://wiki.tcl.tk/950"""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


class ScrollbarHelper(BuilderObject):
    class_ = None
    scrollbar_class = None
    container = True
    maxchildren = 1
    allowed_children = ('tk.Entry', 'ttk.Entry', 'tk.Text', 'tk.Canvas',
        'tk.Listbox', 'ttk.Treeview' )
    properties = ['scrolltype']
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'
    BOTH = 'both'

    def configure(self):
        scrolltype = self.properties.get('scrolltype', self.BOTH)
        if scrolltype in (self.BOTH, self.VERTICAL):
            self.widget.vsb = self.scrollbar_class(self.widget,
                orient="vertical")
            #layout
            self.widget.vsb.grid(column=1, row=0, sticky=tk.NS)

        if scrolltype in (self.BOTH, self.HORIZONTAL):
            self.widget.hsb = self.scrollbar_class(self.widget,
                orient="horizontal")
            self.widget.hsb.grid(column=0, row=1, sticky=tk.EW)

        self.widget.grid_columnconfigure(0, weight=1)
        self.widget.grid_rowconfigure(0, weight=1)

    def add_child(self, cwidget):
        cwidget.grid(column=0, row=0, sticky=tk.NSEW, in_=self.widget)
        scrolltype = self.properties.get('scrolltype', self.BOTH)

        if scrolltype in (self.BOTH, self.VERTICAL):
            if hasattr(cwidget, 'yview'):
                self.widget.vsb.configure(command=cwidget.yview)
                cwidget.configure(yscrollcommand=lambda f, l: _autoscroll(self.widget.vsb, f, l))
            else:
                msg = "widget {} has no attribute 'yview'".format(str(cwidget))
                logger.warning(msg)

        if scrolltype in (self.BOTH, self.HORIZONTAL):
            if hasattr(cwidget, 'xview'):
                self.widget.hsb.configure(command=cwidget.xview)
                cwidget.configure(xscrollcommand=lambda f, l: _autoscroll(self.widget.hsb, f, l))
            else:
                msg = "widget {} has no attribute 'xview'".format(str(cwidget))
                logger.warning(msg)


__scrolltype_property = {
    'input_method': 'choice',
    'values': (ScrollbarHelper.BOTH, ScrollbarHelper.VERTICAL,
        ScrollbarHelper.HORIZONTAL),
    'default': ScrollbarHelper.HORIZONTAL }

register_property('scrolltype', __scrolltype_property)


class TTKScrollbarHelper(ScrollbarHelper):
    class_ = ttk.Frame
    scrollbar_class = ttk.Scrollbar

register_widget('pygubu.widgets.scrollbarhelper', TTKScrollbarHelper,
    'ScrollbarHelper', ('Pygubu Utilities', 'ttk'))

