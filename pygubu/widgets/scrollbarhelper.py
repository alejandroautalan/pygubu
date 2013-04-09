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


class ScrollbarHelper(ttk.Frame):
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'
    BOTH = 'both'

    def __init__(self, master=None, **kw):
        self.scrolltype = kw.pop('scrolltype', self.VERTICAL)
        super(ScrollbarHelper, self).__init__(master, **kw)
        self._create_scrollbars()


    def _create_scrollbars(self):
        scrollbar_class = ttk.Scrollbar

        if self.scrolltype in (self.BOTH, self.VERTICAL):
            self.vsb = scrollbar_class(self, orient="vertical")
            #layout
            self.vsb.grid(column=1, row=0, sticky=tk.NS)

        if self.scrolltype in (self.BOTH, self.HORIZONTAL):
            self.hsb = scrollbar_class(self, orient="horizontal")
            self.hsb.grid(column=0, row=1, sticky=tk.EW)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def add_child(self, cwidget):
        cwidget.grid(column=0, row=0, sticky=tk.NSEW, in_=self)

        if self.scrolltype in (self.BOTH, self.VERTICAL):
            if hasattr(cwidget, 'yview'):
                self.vsb.configure(command=cwidget.yview)
                cwidget.configure(yscrollcommand=lambda f, l: _autoscroll(self.vsb, f, l))
            else:
                msg = "widget {} has no attribute 'yview'".format(str(cwidget))
                logger.warning(msg)

        if self.scrolltype in (self.BOTH, self.HORIZONTAL):
            if hasattr(cwidget, 'xview'):
                self.hsb.configure(command=cwidget.xview)
                cwidget.configure(xscrollcommand=lambda f, l: _autoscroll(self.hsb, f, l))
            else:
                msg = "widget {} has no attribute 'xview'".format(str(cwidget))
                logger.warning(msg)




class TTKSBHelperBO(BuilderObject):
    class_ = ScrollbarHelper
    container = True
    maxchildren = 1
    allowed_children = ('tk.Entry', 'ttk.Entry', 'tk.Text', 'tk.Canvas',
        'tk.Listbox', 'ttk.Treeview' )
    properties = ['scrolltype', 'cursor', 'height', 'padding',
            'relief', 'style', 'takefocus', 'width']
    ro_properties = ('scrolltype', )


    def add_child(self, cwidget):
        self.widget.add_child(cwidget)


__scrolltype_property = {
    'input_method': 'choice',
    'values': (ScrollbarHelper.BOTH, ScrollbarHelper.VERTICAL,
        ScrollbarHelper.HORIZONTAL),
    'default': ScrollbarHelper.HORIZONTAL }

register_property('scrolltype', __scrolltype_property)


register_widget('pygubu.widgets.scrollbarhelper', TTKSBHelperBO,
    'ScrollbarHelper', ('Pygubu Helpers', 'ttk'))

