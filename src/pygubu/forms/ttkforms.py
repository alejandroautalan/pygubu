import tkinter as tk
import tkinter.ttk as ttk

from pygubu.utils.widget import HideableMixin
from .exceptions import ValidationError
from .forms import FormWidget, FieldInfo, FormInfo
from .tkforms import TkVarBasedWidget
from .config import ENTRY_MARK_INVALID_USING_VALIDATE
from .fields import FieldBase, DisplayField


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


class EntryField(FieldBase, TkVarBasedWidget, ttk.Entry):
    pass


class LabelField(DisplayField, TkVarBasedWidget, ttk.Label):
    """A Display only field using ttk.Label"""

    def __init__(self, *args, **kw):
        self.original_data = None
        super().__init__(*args, **kw)

    def to_python(self, value):
        if self.original_data is None:
            return value
        return self.original_data

    def wset_value(self, value):
        self.original_data = value
        super().wset_value(str(value))
