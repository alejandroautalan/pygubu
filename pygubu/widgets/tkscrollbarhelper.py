import tkinter as tk
from tkinter import ttk

from ..builderobject import *
from .scrollbarhelper import ScrollbarHelper


class TKScrollbarHelper(ScrollbarHelper):
    class_ = tk.Frame
    scrollbar_class = tk.Scrollbar

register_widget('pygubu.widgets.tkscrollbarhelper', TKScrollbarHelper,
    'ScrollbarHelper', ('Pygubu Utilities', 'tk'))
