import tkinter as tk
import tkinter.ttk as ttk
import pygubu.forms.validators as validators
import pygubu.forms.fields as fields
import pygubu.forms.fieldinfo as fieldinfo
import pygubu.forms.fieldm as fieldm
from pygubu.utils.widget import HideableMixin
from .exceptions import ValidationError
from .forms import BaseFormMixin


class Form(BaseFormMixin, ttk.Frame):
    ...


class LabelField(fields.TkVariableBasedField, ttk.Label):
    class DataManager(fieldm.TkvarFDM):
        def to_python(self, value):
            """Return a string."""
            if value not in self.field.empty_values:
                value = str(value)
            else:
                value = ""
            return value

    class ViewManager(fieldm.FieldViewManager):
        ...

    def __init__(self, *args, **kw):
        kw["required"] = False
        super().__init__(*args, **kw)

        self.data_manager = self.DataManager(self, variable=self._data_var)
        self.view_manager = self.ViewManager(self)

    def has_changed(self, initial):
        """Return True if data differs from initial."""
        return self.data_manager.to_python(
            initial
        ) != self.data_manager.to_python(self.data)


class CharField(fields.CharFieldMixin, fields.TkVariableBasedField, ttk.Entry):
    class DataManager(fieldm.TkvarFDM):
        def to_python(self, value):
            """Return a string."""
            if value not in self.field.empty_values:
                value = str(value)
                if self.field.strip:
                    value = value.strip()
            if value in self.field.empty_values:
                return self.field.empty_value
            return value

    class ViewManager(fieldm.FieldViewManager):
        def mark_invalid(self, state: bool):
            ttk.Entry.validate(self.field)

    def __init__(self, *args, **kw):
        kw["validate"] = kw.get("validate", "focusout")
        kw["validatecommand"] = self._entry_validate
        print("CharField init")
        super().__init__(*args, **kw)

        self.data_manager = self.DataManager(self, variable=self._data_var)
        self.view_manager = self.ViewManager(self)

    def _entry_validate(self):
        """Tcl command to validate entry and mark it as invalid.
        If using ttkbootstrap, this will add visual error hint for entry.
        """
        try:
            self.clean(self.data)
            return True
        except ValidationError:
            return False


class CharComboField(
    fields.ChoiceFieldMixin,
    fields.CharFieldMixin,
    fields.TkVariableBasedField,
    ttk.Combobox,
):
    class DataManager(CharField.DataManager):
        ...

    class ViewManager(fieldm.FieldViewManager):
        def mark_invalid(self, state: bool):
            ttk.Combobox.validate(self.field)

    def __init__(self, *args, **kw):
        kw["validate"] = kw.get("validate", "focusout")
        kw["validatecommand"] = self._entry_validate
        super().__init__(*args, **kw)

        self.data_manager = self.DataManager(self, variable=self._data_var)
        self.view_manager = self.ViewManager(self)

        self.configure(values=self._choices)

    def _entry_validate(self):
        """Tcl command to validate entry and mark it as invalid.
        If using ttkbootstrap, this will add visual error hint for entry.
        """
        try:
            self.clean(self.data_manager.data)
            return True
        except ValidationError:
            return False


class ChoiceField(
    fields.ChoiceFieldMixin, fields.TkVariableBasedField, ttk.Combobox
):
    class DataManager(fieldm.TkvarFDM):
        def validate(self, value):
            self.field.validate_choice(value)

    class ViewManager(fieldm.FieldViewManager):
        def mark_invalid(self, state: bool):
            ttk.Combobox.validate(self.field)

    def __init__(self, *args, **kw):
        state = kw.get("state", "readonly")
        state = state if state != "normal" else "readonly"
        kw["state"] = state
        kw["validate"] = kw.get("validate", "focusout")
        kw["validatecommand"] = self._entry_validate

        super().__init__(*args, **kw)

        self.data_manager = self.DataManager(self, variable=self._data_var)
        self.view_manager = self.ViewManager(self)

        self.configure(values=self._choices)

    def _entry_validate(self):
        """Tcl command to validate entry and mark it as invalid.
        If using ttkbootstrap, this will add visual error hint for entry.
        """
        try:
            self.clean(self.data_manager.data)
            return True
        except ValidationError:
            return False


class TextField(fields.Field, tk.Text):
    class DataManager(fieldm.FieldDataManager):
        def set_value(self, value):
            state = self.field.cget("state")
            if state == tk.DISABLED:
                self.field.configure(state=tk.NORMAL)
                self.field.insert("0.0", value)
                self.field.configure(state=tk.DISABLED)
            else:
                self.field.insert("0.0", value)

        def get_value(self):
            return self.field.get("0.0", "end")

    class ViewManager(fieldm.FieldViewManager):
        def mark_invalid(self, state: bool):
            pass

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.data_manager = self.DataManager(self)
        self.view_manager = self.ViewManager(self)


class BooleanCheckboxField(fields.TkVariableBasedField, ttk.Checkbutton):
    tkvar_pname = "variable"
    tkvar_class = tk.BooleanVar

    class DataManager(fieldm.TkvarFDM):
        def to_python(self, value):
            # will return a python object representation of value"
            # should raise ValidationError if value can't be conveted.
            if isinstance(value, str) and value.lower() in ("false", "0"):
                value = False
            else:
                value = bool(value)
            return value

        def set_value(self, value):
            super().set_value(self.to_python(value))

    class ViewManager(fieldm.FieldViewManager):
        def mark_invalid(self, state: bool):
            pass

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.data_manager = self.DataManager(self, variable=self._data_var)
        self.view_manager = self.ViewManager(self)


class LabelFieldInfo(fieldinfo.FieldInfoDisplay, HideableMixin, ttk.Label):
    """Used to display help and errors messages for the associated form field."""

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def show_error(self, error):
        self.hidden = False
        self.configure(text=error.message)

    def clear(self):
        self.configure(text="")
        self.hidden = True
