# encoding: utf8
from __future__ import unicode_literals

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubu.widgets.tkscrollbarhelper import ScrollbarHelperFactory

ScrollbarHelper = ScrollbarHelperFactory(ttk.Frame, ttk.Scrollbar)


