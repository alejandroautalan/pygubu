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
        ...

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.data_manager = self.DataManager(self, variable=self._data_var)
        self.view_manager = self.ViewManager(self)
