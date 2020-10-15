# encoding: utf8
from __future__ import unicode_literals

try:
    import tkinter as tk
    from tkinter.scrolledtext import ScrolledText
except:
    import Tkinter as tk
    from ScrolledText import ScrolledText


from pygubu.builder.builderobject import BuilderObject, register_widget
from pygubu.builder.tkstdwidgets import TKText


class TkinterScrolledTextBO(TKText):
    class_ = ScrolledText


register_widget('pygubu.builder.widgets.tkinterscrolledtext',
                TkinterScrolledTextBO,
                'ScrolledText', ('Control & Display', 'tk'))
