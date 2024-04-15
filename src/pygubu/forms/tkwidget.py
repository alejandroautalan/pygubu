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


class WidgetViewManager:
    """A class to provide default behavior and allow user to inject
    custom code."""

    def mark_invalid(self, widget, state: bool):
        ...

    def is_disabled(self, widget) -> bool:
        ...


class TkWidgetViewManager(WidgetViewManager):
    """Default view manager for tk widgets

    To mark widget as invalid, uses option database
    to get color information:
       form_error_bg: background color
       form_error_fg: foreground color
    If color information is not found, does nothing.
    """

    def mark_invalid(self, widget: tk.Widget, state: bool):
        class_ = widget.winfo_class()
        error_bg = widget.option_get("form_error_bg", class_)
        error_fg = widget.option_get("form_error_fg", class_)

        if not all((error_bg, error_fg)):
            # no configuration found, do nothing
            return
        if not hasattr(widget, "_oldbg"):
            widget._oldbg = None
            widget._oldfg = None
        if state:
            widget._oldbg = widget.cget("background")
            widget._oldfg = widget.cget("foreground")
            widget.configure(background=error_bg, foreground=error_fg)
        elif widget._oldbg is not None:
            widget.configure(background=widget._oldbg, foreground=widget._oldfg)

    def is_disabled(self, widget) -> bool:
        return "disabled" == widget.cget("state")


class TkWidgetBase(FieldWidget):
    view_manager = TkWidgetViewManager()

    def wis_disabled(self) -> bool:
        return self.view_manager.is_disabled(self)

    def wmark_invalid(self, state: bool):
        self.view_manager.mark_invalid(self, state)


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
