"""Pygubu widgets as form fields"""

import pygubu.forms.validators as validators
import pygubu.forms.fields as fields
from pygubu.forms.forms import BaseFormMixin
from pygubu.forms.exceptions import ValidationError

from pygubu.widgets.combobox import Combobox


class ComboboxField(fields.TkVariableBasedField, Combobox):
    tkvar_pname = "keyvariable"
