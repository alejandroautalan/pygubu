# encoding: utf-8
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from pygubu.builder.builderobject import register_widget
from pygubu.builder.tkstdwidgets import TKText
from pygubu.i18n import _


class TkinterScrolledTextBO(TKText):
    class_ = ScrolledText


register_widget(
    "pygubu.builder.widgets.tkinterscrolledtext",
    TkinterScrolledTextBO,
    "ScrolledText",
    (_("Control & Display"), "tk"),
)
