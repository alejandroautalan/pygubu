"""Pygubu widgets as form fields"""

import pygubu.forms.validators as validators
import pygubu.forms.fields as fields
import pygubu.forms.fieldm as fieldm

from pygubu.forms.forms import BaseFormMixin
from pygubu.forms.exceptions import ValidationError
from pygubu.widgets.combobox import Combobox


class ComboboxField(fields.TkVariableBasedField, Combobox):
    tkvar_pname = "keyvariable"

    class DataManager(fieldm.TkvarFDM):
        ...

    class ViewManager(fieldm.FieldViewManager):
        def mark_invalid(self, state: bool):
            Combobox.validate(self.field)

    def __init__(self, *args, **kw):
        kw["validate"] = kw.get("validate", "focusout")
        kw["validatecommand"] = self._entry_validate
        super().__init__(*args, **kw)

        self.data_manager = self.DataManager(self, variable=self._data_var)
        self.view_manager = self.ViewManager(self)

    def _entry_validate(self):
        """Tcl command to validate entry and mark it as invalid.
        If using ttkbootstrap, this will add visual error hint for entry.
        """
        try:
            self.clean(self.data_manager.data)
            return True
        except ValidationError:
            return False
