import tkinter.ttk as ttk
from pygubu.utils.widget import HideableMixin
from .builder import FormBuilder
from .widget import FieldWidget, WidgetInfo, FormInfo
from .tkwidget import TkFormBuilder, TkVarBasedWidget


class FrameFormBuilder(TkFormBuilder, ttk.Frame):
    ...


class TtkVarBasedWidget(TkVarBasedWidget):
    def wmark_invalid(self, state: bool):
        style: str = self.cget("style")
        if style:
            style = style.removeprefix("Error.")
            if state:
                style = f"Error.{style}"
            self.configure(style=style)


class LabelWidgetInfo(WidgetInfo, HideableMixin, ttk.Label):
    """Used to display help and errors messages for the associated form field."""

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def _set_style(self, mode: str):
        style: str = self.cget("style")
        if style:
            style = style.removeprefix("Error.")
            style = style.removeprefix("Help.")
            style = f"{mode}.{style}"
            self.configure(style=style)

    def show_error(self, error):
        self.hidden = False
        self.configure(text=error.message)
        self._set_style("Error")

    def show_help(self, message):
        self.hidden = False
        self.configure(text=message)
        self._set_style("Help")

    def clear(self):
        self.configure(text="")
        self.hidden = True


class Entry(TtkVarBasedWidget, ttk.Entry):
    pass


class Label(TtkVarBasedWidget, ttk.Label):
    """A Display only field using ttk.Label"""

    def __init__(self, *args, **kw):
        self.original_data = None
        super().__init__(*args, **kw)

    def wget_value(self):
        return self.original_data

    def wset_value(self, value):
        self.original_data = value
        super().wset_value(str(value))


class Checkbutton(TtkVarBasedWidget, ttk.Checkbutton):
    tkvar_pname = "variable"


class Combobox(TtkVarBasedWidget, ttk.Combobox):
    pass
