# encoding: utf8
from __future__ import unicode_literals

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk


from pygubu.widgets.tkscrolledframe import ScrolledFrameBase


class TTKScrolledFrameFactory(type):
    def __new__(cls, clsname, superclasses, attrs):
        return type.__new__(cls, clsname, superclasses, attrs)


ScrolledFrame = TTKScrolledFrameFactory('ScrolledFrame',
                                       (ScrolledFrameBase, ttk.Frame, object),
                                       {'_framecls':ttk.Frame,
                                        '_sbarcls': ttk.Scrollbar}) 
