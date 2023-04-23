"""Forms with pygubu widgets"""

from pygubu.widgets.combobox import Combobox
from .tkforms import TkVarBasedWidget
from .fields import FieldBase
from .config import ENTRY_MARK_INVALID_USING_VALIDATE


class ComboboxField(FieldBase, TkVarBasedWidget, Combobox):
    tkvar_pname = "keyvariable"

    def __init__(self, *args, **kw):
        kw["validate"] = kw.get("validate", "focusout")
        # kw["validatecommand"] = self._entry_validate
        super().__init__(*args, **kw)
