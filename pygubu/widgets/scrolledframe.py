# encoding: utf8
from __future__ import unicode_literals

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk


from pygubu.widgets.tkscrolledframe import ScrolledFrameFactory

ScrolledFrame = ScrolledFrameFactory(ttk.Frame, ttk.Scrollbar)
