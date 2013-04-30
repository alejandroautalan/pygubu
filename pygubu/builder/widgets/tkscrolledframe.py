import types
import tkinter as tk

from pygubu.builder.builderobject import *
from pygubu.widgets.tkscrolledframe import TkScrolledFrame


class TKScrolledFrameBO(BuilderObject):
    class_ = TkScrolledFrame
    container = True
    maxchildren = 1
    allowed_children = ('tk.Frame', 'ttk.Frame' )
    properties = ['background', 'borderwidth', 'cursor', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'padx', 'pady', 'relief', 'takefocus', 'width']
    ro_properties = ro_properties = ('class_',)

    def get_child_master(self):
        return self.widget.innerframe

register_widget('pygubu.builder.widgets.tkscrolledframe', TKScrolledFrameBO,
    'ScrolledFrame', ('Pygubu Widgets', 'tk'))

