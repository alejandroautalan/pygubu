from pygubu.widgets.combobox import Combobox
from pygubu.widgets.fontinput import FontInput
from pygubu.widgets.colorinput import ColorInput

from .ttkwidget import TtkVarBasedWidget


class PygubuCombobox(TtkVarBasedWidget, Combobox):
    tkvar_pname = "keyvariable"


class FontInputFW(TtkVarBasedWidget, FontInput):
    """A FontInput form field widget."""

    tkvar_pname = "variable"


class ColorInputFW(TtkVarBasedWidget, ColorInput):
    """A ColorInput form field widget."""

    tkvar_pname = "textvariable"

    def wset_value(self, value):
        ColorInput.configure(self, value=value)

    def wis_disabled(self) -> bool:
        return self.view_manager.is_disabled(self._entry)
