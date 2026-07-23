"""Toggleswitch

This module provides a fallback class to use ttk::toggleswitch from tk 9.1
until is added to tkinter.
"""

import tkinter.ttk as ttk


class Toggleswitch(ttk.Widget):

    def __init__(self, master=None, **kw):
        """Construct a ttk toggleswitch with parent master.

        STANDARD OPTIONS

            class, ,cursor, style, takefocus

        WIDGET-SPECIFIC OPTIONS

            command, offvalue, onvalue, size, variable
        """
        super().__init__(master, "ttk::toggleswitch", kw)

    def toggle(self):
        """Invokes the command associated with the button."""
        return self.tk.call(self._w, "toggle")

    def switchstate(self, newstate: bool = None):
        if newstate is None:
            return self.tk.call(self._w, "switchstate")
        return self.tk.call(self._w, "switchstate", newstate)
