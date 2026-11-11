from tkinter.scrolledtext import ScrolledText

from pygubu.api.v1 import register_widget
from pygubu.plugins.tk.tkstdwidgets import TKText
from pygubu.i18n import _
from pygubu.plugins import GINPUT


class TkinterScrolledTextBO(TKText):
    class_ = ScrolledText


register_widget(
    "tk.ScrolledText",
    TkinterScrolledTextBO,
    "tk.ScrolledText",
    (_("Control & Display"), "tk"),
    group=GINPUT,
)

_builder_old = "pygubu.builder.widgets.tkinterscrolledtext"
register_widget(
    _builder_old,
    TkinterScrolledTextBO,
    public=False,
)
