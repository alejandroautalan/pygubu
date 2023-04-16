import tkinter as tk
from .widgets import FieldWidget
from .validators import EMPTY_VALUES


class TkWidgetBase(FieldWidget):
    def wmark_invalid(self, state: bool):
        # Visually mark the widget as invalid depending on state parameter.
        print("TODO > mark invalid state")

    def wis_disabled(self) -> bool:
        return "disabled" == self.cget("state")


class TkVarBasedWidget(TkWidgetBase):
    tkvar_pname = "textvariable"
    tkvar_class = tk.StringVar

    def __init__(self, *args, **kw):
        user_var = kw.get(self.tkvar_pname, None)
        if user_var is None:
            self._data_var = self.tkvar_class()
            kw[self.tkvar_pname] = self._data_var
        elif isinstance(user_var, self.tkvar_class):
            self._data_var = user_var
        else:
            raise ValueError("Incorrect type for data variable")

        super().__init__(*args, **kw)

    def wset_value(self, value):
        if value in EMPTY_VALUES:
            value = ""
        print(f"setting {self.fname} value to:: {value}, type: {type(value)}")
        try:
            self._data_var.set(value)
        except tk.TclError:
            pass

    def wget_value(self):
        return self._data_var.get()
