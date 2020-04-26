# encoding: utf8
from __future__ import unicode_literals

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk


from pygubu.widgets.tkscrolledframe import (ScrolledFrameBase,
                                            ScrolledFrameFactory)


ScrolledFrame = ScrolledFrameFactory('ScrolledFrame',
                                       (ScrolledFrameBase, ttk.Frame, object),
                                       {'_framecls':tk.Frame,
                                        '_sbarcls': ttk.Scrollbar}) 