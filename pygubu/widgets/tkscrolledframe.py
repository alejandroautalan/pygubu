import tkinter as tk
from tkinter import ttk

from ..builderobject import *
from .scrolledframe import ScrolledFrame

class TKScrolledFrame(ScrolledFrame):
    class_ = tk.Frame
    scrollbar_class = tk.Scrollbar
    properties = ['background', 'borderwidth', 'cursor', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'padx', 'pady', 'relief', 'takefocus', 'width']

register_widget('pygubu.widgets.tkscrolledframe', TKScrolledFrame,
    'ScrolledFrame', ('Pygubu Utilities', 'tk'))
