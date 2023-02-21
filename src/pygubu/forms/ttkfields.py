import tkinter as tk
import tkinter.ttk as ttk
import pygubu.forms.validators as validators
import pygubu.forms.fields as fields
from .exceptions import ValidationError
from .forms import BaseFormMixin


class Form(BaseFormMixin, ttk.Frame):
    ...


class LabelField(fields.TkVariableBasedField, ttk.Label):
    def __init__(self, *args, **kw):
        kw["required"] = False
        super().__init__(*args, **kw)

    def to_python(self, value):
        """Return a string."""
        if value not in self.empty_values:
            value = str(value)
        else:
            value = ""
        return value

    def has_changed(self, initial):
        """Return True if data differs from initial."""
        return self.to_python(initial) != self.to_python(self.data)

    def mark_invalid(self):
        pass

    def clear_invalid(self):
        pass


class CharField(fields.CharFieldMixin, fields.TkVariableBasedField, ttk.Entry):
    def __init__(self, *args, **kw):
        kw["validate"] = kw.get("validate", "focusout")
        kw["validatecommand"] = self._entry_validate
        print("CharField init")
        super().__init__(*args, **kw)

    def _entry_validate(self):
        """Tcl command to validate entry and mark it as invalid.
        If using ttkbootstrap, this will add visual error hint for entry.
        """
        try:
            self.clean(self.data)
            return True
        except ValidationError:
            return False

    def mark_invalid(self):
        ttk.Entry.validate(self)

    def clear_invalid(self):
        ttk.Entry.validate(self)


class CharComboField(
    fields.ChoiceFieldMixin,
    fields.CharFieldMixin,
    fields.TkVariableBasedField,
    ttk.Combobox,
):
    def __init__(self, *args, **kw):
        kw["validate"] = kw.get("validate", "focusout")
        kw["validatecommand"] = self._entry_validate
        super().__init__(*args, **kw)
        self.configure(values=self._choices)

    def validate(self, value):
        return fields.TkVariableBasedField.validate(self, value)

    def _entry_validate(self):
        """Tcl command to validate entry and mark it as invalid.
        If using ttkbootstrap, this will add visual error hint for entry.
        """
        try:
            self.clean(self.data)
            return True
        except ValidationError:
            return False

    def mark_invalid(self):
        ttk.Combobox.validate(self)

    def clear_invalid(self):
        ttk.Combobox.validate(self)


class ChoiceField(
    fields.ChoiceFieldMixin, fields.TkVariableBasedField, ttk.Combobox
):
    def __init__(self, *args, **kw):
        state = kw.get("state", "readonly")
        state = state if state != "normal" else "readonly"
        kw["state"] = state
        kw["validate"] = kw.get("validate", "focusout")
        kw["validatecommand"] = self._entry_validate
        super().__init__(*args, **kw)
        self.configure(values=self._choices)

    def _entry_validate(self):
        """Tcl command to validate entry and mark it as invalid.
        If using ttkbootstrap, this will add visual error hint for entry.
        """
        try:
            self.clean(self.data)
            return True
        except ValidationError:
            return False

    def mark_invalid(self):
        ttk.Combobox.validate(self)

    def clear_invalid(self):
        ttk.Combobox.validate(self)


class LabelFieldInfo(fields.FieldInfoDisplay, ttk.Label):
    """Used to display help and errors messages for the associated form field."""

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._is_hidden = None
        self._layout = None
        self._layout_info = None

    def _hide(self):
        if self._is_hidden is None:
            self._layout = m = self.winfo_manager()
            if m == "pack":
                self._layout_info = self.pack_info()
                self._layout_info.pop("in", None)
                parent = self.nametowidget(self.winfo_parent())
                wlist = parent.pack_slaves()
                total = len(wlist)
                self_index = wlist.index(self)
                print("Iam in position:", self_index)
                if total > 1:
                    if self_index == 0:
                        self._layout_info["before"] = wlist[1]
                    else:
                        self._layout_info["after"] = wlist[self_index - 1]

            elif m == "place":
                self._layout_info = info = self.place_info()
                info.pop("in", None)
                # FIXME: ttkbootstrap issue with localization ??
                for key in ("relx", "rely", "relwidth", "relheight"):
                    info[key] = str(info[key]).replace(",", ".")
                print("saving place info:", self._layout_info)
            self._is_hidden = False

        if self._is_hidden is False:
            if self._layout == "pack":
                self.pack_forget()
            elif self._layout == "grid":
                self.grid_remove()
            elif self._layout == "place":
                self.place_forget()
            self._is_hidden = True

    def _show(self):
        if self._is_hidden:
            layout = self._layout
            if layout == "pack":
                self.pack(**self._layout_info)
            elif layout == "grid":
                self.grid()
            elif layout == "place":
                self.place(**self._layout_info)
            self._is_hidden = False

    def show_error(self, error):
        self._show()
        self.configure(text=error.message)

    def clear(self):
        self.configure(text="")
        self._hide()
