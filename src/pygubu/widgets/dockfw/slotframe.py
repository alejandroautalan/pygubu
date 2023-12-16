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
            self,
            cursor="top_side",
            background="#003ed9",
            height=15,
            width=15,
            side="n",
            name="fn",
        )
        self.fn.grid(column=0, columnspan=3, row=0, sticky="ew")
        self.fs = SlotIndicator(
            self,
            cursor="bottom_side",
            background="#003ed9",
            height=15,
            width=10,
            side="s",
            name="fs",
        )
        self.fs.grid(column=0, columnspan=3, row=2, sticky="ew")
        self.fe = SlotIndicator(
            self,
            cursor="right_side",
            background="#003ed9",
            height=15,
            width=15,
            side="e",
            name="fe",
        )
        self.fe.grid(column=2, row=1, sticky="ns")
        self.fw = SlotIndicator(
            self,
            cursor="left_side",
            background="#003ed9",
            height=15,
            width=15,
            side="w",
            name="fw",
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
        self._indicators_visible = False

    def iter_indicators(self) -> tk.Widget:
        for fi in (self.fn, self.fs, self.fw, self.fe):
            yield fi

    def indicators_visible(self, visible: bool):
        if self._indicators_visible != visible:
            self._indicators_visible = visible
            if visible:
                self.configure(padding=4)
            else:
                self.configure(padding=0)

            for f in self.iter_indicators():
                if visible:
                    f.grid()
                else:
                    f.grid_remove()
