import tkinter as tk
import tkinter.ttk as ttk

from pygubu.utils.widget import HideableMixin
from .exceptions import ValidationError
from .forms import FormWidget, FieldInfo, FormInfo
from .widgets import ChoiceWidget
from .tkforms import TkVarBasedWidget, TextWidget, DefaultViewManager
from .config import ENTRY_MARK_INVALID_USING_VALIDATE
from .fields import (
    CharField,
    FieldWidget,
    IntegerField,
    FloatField,
    BooleanField,
    ChoiceField,
    DisplayField,
)


class FrameForm(FormWidget, ttk.Frame):
    pass


class LabelFieldInfo(FieldInfo, HideableMixin, ttk.Label):
    """Used to display help and errors messages for the associated form field."""

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def show_error(self, error):
        self.hidden = False
        self.configure(text=error.message)

    def show_help(self, message):
        self.hidden = False
        self.configure(text=message)

    def clear(self):
        self.configure(text="")
        self.hidden = True


class LabelDisplayField(DisplayField, TkVarBasedWidget, ttk.Label):
    """A Display only field using ttk.Label"""

    class DataManager(TkVarBasedWidget.DataManager):
        def __init__(self, *args, **kw):
            self.original_data = None
            super().__init__(*args, **kw)

        def to_python(self, value):
            if self.original_data is None:
                return value
            return self.original_data

        def set_value(self, value):
            self.original_data = value
            super().set_value(str(value))

    class ViewManager(DefaultViewManager):
        ...


class EntryCharWidget(TkVarBasedWidget, ttk.Entry):
    class ViewManager(DefaultViewManager):
        def mark_invalid(self, state: bool):
            if ENTRY_MARK_INVALID_USING_VALIDATE:
                print("Validating ....")
                ttk.Entry.validate(self._field)

    def __init__(self, *args, **kw):
        if ENTRY_MARK_INVALID_USING_VALIDATE:
            kw["validate"] = kw.get("validate", "focusout")
            kw["validatecommand"] = self._entry_validate
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


class EntryCharField(CharField, EntryCharWidget):
    pass


class EntryIntegerField(IntegerField, EntryCharWidget):
    pass


class EntryFloatField(FloatField, EntryCharWidget):
    pass


class TextCharField(CharField, TextWidget):
    pass


class CheckbuttonBoolWidget(TkVarBasedWidget, ttk.Checkbutton):
    tkvar_pname = "variable"
    tkvar_class = tk.BooleanVar

    class ViewManager(DefaultViewManager):
        pass


class CheckbuttonBoolField(BooleanField, CheckbuttonBoolWidget):
    pass


class ComboboxChoiceWidget(ChoiceWidget, TkVarBasedWidget, ttk.Combobox):
    class ViewManager(DefaultViewManager):
        def mark_invalid(self, state: bool):
            if ENTRY_MARK_INVALID_USING_VALIDATE:
                ttk.Combobox.validate(self._field)

    def __init__(self, *args, **kw):
        if ENTRY_MARK_INVALID_USING_VALIDATE:
            kw["validate"] = kw.get("validate", "focusout")
            kw["validatecommand"] = self._entry_validate
        state = kw.get("state", "readonly")
        state = state if state != "normal" else "readonly"
        kw["state"] = state
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

    def _set_choices(self, value):
        super()._set_choices(value)
        self.configure(values=self._choices)


class ComboboxChoiceField(ChoiceField, ComboboxChoiceWidget):
    pass


#
# Default classes
#
CharField = EntryCharField
IntegerField = EntryIntegerField
FloatField = EntryFloatField
ChoiceField = ComboboxChoiceField
