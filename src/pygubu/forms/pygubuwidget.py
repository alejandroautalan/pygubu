from pygubu.widgets.combobox import Combobox
from pygubu.widgets.fontinput import FontInput

from .ttkwidget import TtkVarBasedWidget


class PygubuCombobox(TtkVarBasedWidget, Combobox):
    tkvar_pname = "keyvariable"


class FontInputFW(TtkVarBasedWidget, FontInput):
    """A FontInput form field widget."""

    tkvar_pname = "variable"
