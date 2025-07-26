# encoding: utf-8
import tkinter.ttk as ttk


class Spinbox(ttk.Entry):
    def __init__(self, master=None, **kw):
        # Note:
        # ttk::Spinbox was added in tk 8.5.9 so it may fail in lower 8.5 patch versions
        ttk.Entry.__init__(self, master, "ttk::spinbox", **kw)

    def current(self, newindex=None):
        return self.tk.call(self._w, "current", newindex)

    def set(self, value):
        return self.tk.call(self._w, "set", value)
