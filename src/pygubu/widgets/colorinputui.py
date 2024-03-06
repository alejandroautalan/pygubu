#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


#
# Base class definition
#
class ColorInputUI(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._frame = tk.Frame(self, name="_frame")
        self._frame.configure(borderwidth=0, height=10, relief="flat", width=24)
        self._frame.pack(fill="y", side="left")
        self._entry = ttk.Entry(self, name="_entry")
        self._entry.configure(validate="all")
        self._entry.pack(expand=True, fill="both", padx=2, side="left")
        self._entry.bind("<FocusOut>", self.on_focusout, add="")
        self._entry.bind("<KeyPress>", self.on_keypress, add="")
        self._button = ttk.Button(self, name="_button")
        self._button.configure(
            compound="center",
            style="Toolbutton",
            takefocus=True,
            text="…",
            width=-2,
        )
        self._button.pack(fill="both", side="left")
        self._button.configure(command=self.on_picker_clicked)
        self.configure(height=25, width=100)
        # self.pack(side="top")

    def on_focusout(self, event=None):
        pass

    def on_keypress(self, event=None):
        pass

    def on_picker_clicked(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = ColorInputUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
