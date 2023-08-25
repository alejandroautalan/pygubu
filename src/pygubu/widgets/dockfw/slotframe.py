#!/usr/bin/python3
# Note: Template in development.
import tkinter as tk
import tkinter.ttk as ttk


class SlotIndicator(tk.Frame):
    def __init__(self, *args, side="n", **kw):
        super().__init__(*args, **kw)
        self.side = side


#
# Base class definition
#
class SlotFrameBase(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.fn = SlotIndicator(
            self, background="#003ed9", height=10, width=10, side="n", name="fn"
        )
        self.fn.grid(column=0, columnspan=3, row=0, sticky="ew")
        self.fs = SlotIndicator(
            self, background="#003ed9", height=10, width=10, side="n", name="fs"
        )
        self.fs.grid(column=0, columnspan=3, row=2, sticky="ew")
        self.fe = SlotIndicator(
            self, background="#003ed9", height=10, width=10, side="n", name="fe"
        )
        self.fe.grid(column=2, row=1, sticky="ns")
        self.fw = SlotIndicator(
            self, background="#003ed9", height=10, width=10, side="n", name="fw"
        )
        self.fw.grid(column=0, row=1, sticky="ns")
        self.fcenter = ttk.Frame(self, name="fcenter")
        self.fcenter.configure(height=20, width=20)
        self.fcenter.grid(column=1, row=1, sticky="nsew")
        self.configure(height=200, width=200)
        # self.pack(side="top")
        # self.grid_propagate(0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)


#
# Manual user code
#


class SlotFrame(SlotFrameBase):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for i in self.iter_indicators():
            i.grid_remove()

    def iter_indicators(self) -> tk.Widget:
        for fi in (self.fn, self.fs, self.fw, self.fe):
            yield fi

    def indicators_visible(self, visible: bool):
        for f in self.iter_indicators():
            if visible:
                f.grid()
            else:
                f.grid_remove()
