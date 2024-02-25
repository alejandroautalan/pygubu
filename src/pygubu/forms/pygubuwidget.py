from pygubu.widgets.combobox import Combobox
from .ttkwidget import TtkVarBasedWidget


class PygubuCombobox(TtkVarBasedWidget, Combobox):
    tkvar_pname = "keyvariable"
