import tkinter as tk
from .widgets import FieldWidget
from .validators import EMPTY_VALUES
from .fields import FieldBase, DisplayField


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
        #
        # Some widgets can use diferent variable types such as checkbutton
        elif isinstance(user_var, tk.Variable):
            self._data_var = user_var
            self.tkvar_class = type(user_var)
            print("using user variable:", user_var)
        else:
            raise ValueError("Incorrect type for data variable")

        super().__init__(*args, **kw)

    def configure(self, cnf=None, **kw):
        if self.tkvar_pname in kw:
            self._data_var = kw[self.tkvar_pname]
            print("user changed variable auto created")
        return super().configure(cnf, **kw)

    def wset_value(self, value):
        if value in EMPTY_VALUES:
            value = ""
        print(
            f"setting {self.field_name} value to:: {value}, type: {type(value)}"
        )
        # for now do not hide any error:
        self._data_var.set(value)

    def wget_value(self):
        return self._data_var.get()


class TextField(FieldBase, TkWidgetBase, tk.Text):
    def wset_value(self, value):
        state = self.cget("state")
        if state == tk.DISABLED:
            self.configure(state=tk.NORMAL)
            self.insert("0.0", value)
            self.configure(state=tk.DISABLED)
        else:
            self.insert("0.0", value)

    def wget_value(self):
        return self.get("0.0", "end-1c")
