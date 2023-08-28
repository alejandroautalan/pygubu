import tkinter as tk
import tkinter.ttk as ttk
from collections import OrderedDict
from .slotframe import SlotFrame, SlotIndicator
from .framework import IDockFrame, IDockPane, IDockWidget
from .framework import DockingFramework


class DockFrame(SlotFrame, IDockFrame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        master = args[0]
        DockingFramework.init_binding(master)
        self.child_master = master.winfo_toplevel()

    def serialize(self):
        children = self.winfo_children()
        output = []
        if len(children) > 0:
            pane = self._serialize_pane(children[0])
            output.append(pane)
        return output

    def _serialize_pane(self, widget):
        pane = OrderedDict()
        if isinstance(widget, DockPane):
            pane["type"] = "dockpane"
            pane["config"] = OrderedDict()

            children = widget.winfo_children()
            if children:
                pane["children"] = pc = []
                for w in widget.winfo_children():
                    if not isinstance(w, ttk.Notebook):
                        child = self._serialize_pane(w)
                        pc.append(child)
        elif isinstance(widget, DockTab):
            pane["type"] = "docktab"
            pane["config"] = pconfig = OrderedDict()
            children = widget.winfo_children()
            if children:
                child = children[0]
                pconfig["widget_uid"] = child._name
        return pane


class DockPane(SlotFrame, IDockPane):
    def __init__(self, *args, orient="horizontal", **kw):
        super().__init__(*args, **kw)
        self.panedw = ttk.Panedwindow(self.fcenter, orient=orient)
        self.panedw.pack(expand=True, fill=tk.BOTH)


class DockTab(SlotFrame, IDockWidget):
    ...
