import tkinter as tk
from TKinterModernThemes.WidgetFrame import WidgetFrame, Notebook, PanedWindow


def tkmt_to_tkwidget(widget):
    """Get underline tk widget."""
    if isinstance(widget, tk.Widget):
        return widget
    if isinstance(widget, WidgetFrame):
        return widget.master
    if isinstance(widget, Notebook):
        return widget.notebook
    if isinstance(widget, PanedWindow):
        return widget.panedwindow
    return None


# Groups for ordering buttons in designer palette.
GROUP_CONTAINER = 0
GROUP_DISPLAY = 1
GROUP_INPUT = 2


class CommandProxy:
    def __init__(self):
        self.command = None

    @property
    def __name__(self):
        return f"CommandProxy({self.command})"

    def __call__(self, *args):
        if self.command is not None:
            self.command(*args)
