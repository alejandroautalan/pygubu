import tkinter.ttk as ttk

from pygubu.utils.widget import HideableMixin


class HideableFrame(HideableMixin, ttk.Frame):
    """A frame that can be easily hidden.
    Use hidden property to show or hide the frame.

    myframe.hidden = True
    """

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
