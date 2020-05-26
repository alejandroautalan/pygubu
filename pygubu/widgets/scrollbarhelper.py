# encoding: utf8
from __future__ import unicode_literals

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubu.widgets.tkscrollbarhelper import ScrollbarHelperBase


class TTKScrollbarHelperFactory(type):
    def __new__(cls, clsname, superclasses, attrs):
        return type.__new__(cls, str(clsname), superclasses, attrs)


ScrollbarHelper = TTKScrollbarHelperFactory('ScrollbarHelper',
                                       (ScrollbarHelperBase, ttk.Frame, object),
                                       {'_framecls': ttk.Frame,
                                        '_sbarcls': ttk.Scrollbar})
