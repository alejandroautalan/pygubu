import tkinter.ttk as ttk
from pygubu.utils.widget import HideableMixin
from .builder import FormBuilder
from .widget import FieldWidget, WidgetInfo, FormInfo
from .tkwidget import TkFormBuilder, TkVarBasedWidget, TkWidgetViewManager


class FrameFormBuilder(TkFormBuilder, ttk.Frame):
    ...


class TtkWidgetViewManager(TkWidgetViewManager):
    """Default view manager for ttk widgets

    To mark widget as invalid, combines the word "Error."
    with the widget style class.
    """

    def mark_invalid(self, widget: ttk.Widget, state: bool):
        style: str = widget.cget("style")
        if style:
            # remove prefix if exists.
            prefix = "Error."
            if style.startswith(prefix):
                style = style[len(prefix) :]
            if state:
                style = f"{prefix}{style}"
            widget.configure(style=style)


class TtkVarBasedWidget(TkVarBasedWidget):
    view_manager = TtkWidgetViewManager()


class TtkWidgetInfoViewManager:
    def _set_style(self, widget, mode: str):
        style: str = widget.cget("style")
        if style:
            # remove prefix if exists
            prefix = "Error."
            if style.startswith(prefix):
                style = style[len(prefix) :]
            # remove prefix if exists
            prefix = "Help."
            if style.startswith(prefix):
                style = style[len(prefix) :]
            style = f"{mode}.{style}"
            widget.configure(style=style)

    def show_error(self, widget: ttk.Widget):
        self._set_style(widget, "Error")

    def show_help(self, widget: ttk.Widget):
        self._set_style(widget, "Help")


class LabelWidgetInfo(WidgetInfo, HideableMixin, ttk.Label):
    """Used to display help and errors messages for the associated form field."""

    view_manager = TtkWidgetInfoViewManager()

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def show_error(self, error):
        self.hidden = False
        self.configure(text=error.message)
        self.view_manager.show_error(self)

    def show_help(self, message):
        self.hidden = False
        self.configure(text=message)
        self.view_manager.show_help(self)

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
