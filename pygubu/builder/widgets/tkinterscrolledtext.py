# encoding: utf8
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from pygubu.builder.builderobject import register_widget
from pygubu.builder.tkstdwidgets import TKText


class TkinterScrolledTextBO(TKText):
    class_ = ScrolledText


register_widget('pygubu.builder.widgets.tkinterscrolledtext',
                TkinterScrolledTextBO,
                'ScrolledText', ('Control & Display', 'tk'))
