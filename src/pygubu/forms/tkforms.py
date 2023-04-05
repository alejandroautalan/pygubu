import tkinter as tk
from .fields import FieldWidget
from .widgets import DataManager, ViewManager
from .validators import EMPTY_VALUES


class DefaultViewManager(ViewManager):
    def mark_invalid(self, state: bool):
        # Let user customize this ? Now, do Nothing
        pass

    def is_disabled(self) -> bool:
        return "disabled" == self._field.cget("state")


class TkVarBasedWidget(FieldWidget):
    tkvar_pname = "textvariable"
    tkvar_class = tk.StringVar

    class DataManager(DataManager):
        def set_value(self, value):
            if value in EMPTY_VALUES:
                value = ""
            print(
                f"setting {self._field.fname} value to:: {value}, type: {type(value)}"
            )
            self._field._data_var.set(value)

        def get_value(self):
            return self._field._data_var.get()

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


class TextWidget(FieldWidget, tk.Text):
    class DataManager(DataManager):
        def set_value(self, value):
            state = self._field.cget("state")
            if state == tk.DISABLED:
                self._field.configure(state=tk.NORMAL)
                self._field.insert("0.0", value)
                self._field.configure(state=tk.DISABLED)
            else:
                self._field.insert("0.0", value)

        def get_value(self):
            return self._field.get("0.0", "end-1c")

    class ViewManager(DefaultViewManager):
        pass
