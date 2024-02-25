import tkinter as tk
from .builder import FormBuilder
from .widget import FieldWidget, WidgetInfo


EMPTY_VALUES = (None, "", [], (), {})


class TkFormBuilder(FormBuilder):
    def scan_widgets(self):
        self.search_widgets(self)

    def search_widgets(self, master=None):
        if master is None:
            master = self
        for widget in master.winfo_children():
            if isinstance(widget, FieldWidget):
                self.widgets[widget.field_name] = widget
            elif isinstance(widget, WidgetInfo):
                self.widgets_info[widget.field_name] = widget
            else:
                self.search_widgets(widget)


class TkWidgetBase(FieldWidget):
    def wmark_invalid(self, state: bool):
        # Visually mark the widget as invalid depending on state parameter.
        cname = self.__class__.__name__
        print(f"TODO > {cname}: mark invalid state")

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
        else:
            raise ValueError("Incorrect type for data variable")

        super().__init__(*args, **kw)

    def configure(self, cnf=None, **kw):
        if self.tkvar_pname in kw:
            self._data_var = kw[self.tkvar_pname]
        return super().configure(cnf, **kw)

    def wset_value(self, value):
        if value in EMPTY_VALUES:
            value = ""
        # FIXME avoid TclErrors when using typed variables Int, Double, Boolean
        tk.Variable.set(self._data_var, value)

    def wget_value(self):
        # FIXME avoid TclErrors when using typed variables Int, Double, Boolean
        return tk.Variable.get(self._data_var)


class Text(TkWidgetBase, tk.Text):
    def wset_value(self, value):
        self.delete("0.0", tk.END)
        state = self.cget("state")
        if state == tk.DISABLED:
            self.configure(state=tk.NORMAL)
            self.insert("0.0", value)
            self.configure(state=tk.DISABLED)
        else:
            self.insert("0.0", value)

    def wget_value(self):
        return self.get("0.0", "end-1c")
