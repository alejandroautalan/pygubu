import tkinter as tk
import tkinter.ttk as ttk
from collections import defaultdict

from pygubu.widgets.dockfw.slotframe import SlotFrame
from pygubu.widgets.dockfw.framework import (
    DockingFramework,
    IDockWidget,
    IDockFrame,
    IDockPane,
)


class DockWidgetBase(SlotFrame):
    def __init__(self, *args, maindock=None, uid=None, **kw):
        super().__init__(*args, **kw)
        self.maindock = maindock
        self.uid = uid
        self.parent_pane = None

    def child_master(self):
        return self.fcenter


class DockPane(DockWidgetBase, IDockPane):
    pcount = 0

    def __init__(self, *args, orient=tk.HORIZONTAL, **kw):
        uid = kw.get("uid", None)
        if uid is None:
            self.pcount += 1
            kw["uid"] = f"pane{self.pcount}"
        super().__init__(*args, **kw)
        self.panedw = ttk.Panedwindow(self.fcenter, orient=orient)
        self.panedw.pack(expand=True, fill=tk.BOTH)

    @property
    def orient(self):
        return str(self.panedw.cget("orient"))

    @property
    def count(self):
        return len(self.panedw.panes())

    def add_pane(self, pane):
        self.maindock._add_pane_to_pane(self, pane)

    def add_widget(self, widget, as_tab=False):
        self.maindock._add_widget_to_pane(self, widget, as_tab=as_tab)


class DockWidget(DockWidgetBase, IDockWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.noteb: ttk.Notebook = None

    @property
    def is_grouped(self):
        grouped = False
        if self.noteb is not None:
            if len(self.noteb.tabs()) > 1:
                grouped = True
        return grouped
