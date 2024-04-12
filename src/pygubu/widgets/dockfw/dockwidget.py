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
        self.parent_pane: DockPane = None
        self.dw_options = {}

    def child_master(self):
        return self.fcenter

    def detach_from_parent(self):
        """Remove this widget as child of parent_pane."""
        if self.parent_pane:
            if self in self.parent_pane.dw_children:
                self.parent_pane.dw_children.remove(self)
            # the panedwindow of parent could be deleted
            exists = self.tk.call(
                "winfo", "exists", str(self.parent_pane.panedw)
            )
            if exists:
                if self in self.parent_pane.panedw.panes():
                    self.parent_pane.panedw.remove(self)
            self.parent_pane = None


class DockPane(DockWidgetBase, IDockPane):
    pcount = 0

    def __init__(self, *args, orient=tk.HORIZONTAL, **kw):
        uid = kw.get("uid", None)
        if uid is None:
            type(self).pcount += 1
            kw["uid"] = f"pane{self.pcount}"
        super().__init__(*args, **kw)
        self.panedw = ttk.Panedwindow(self.fcenter, orient=orient)
        self.panedw.pack(expand=True, fill=tk.BOTH)
        self.dw_children = []

    @property
    def orient(self):
        return str(self.panedw.cget("orient"))

    @property
    def count(self):
        return len(self.panedw.panes())

    @property
    def sorted_dw_children(self):
        wsorted = []
        for tkpane in self.panedw.panes():
            tkpane = self.nametowidget(tkpane)
            if isinstance(tkpane, ttk.Notebook):
                for tab in tkpane.tabs():
                    tab = self.nametowidget(tab)
                    if tab in self.dw_children:
                        wsorted.append(tab)
            else:
                if tkpane in self.dw_children:
                    wsorted.append(tkpane)
        return wsorted

    def add_pane(self, pane: "DockPane", **pane_kw):
        pane.dw_options.update(pane_kw)
        self.maindock._add_pane_to_pane(self, pane, **pane_kw)

    def add_widget(self, widget: "DockWidget", grouped=False, weight=1):
        widget.dw_options["weight"] = weight
        self.maindock._add_widget_to_pane(
            self, widget, grouped=grouped, weight=weight
        )

    def add_dwchild(self, dw: DockWidgetBase):
        """Add DockPane or DockWidget as child."""
        dw.parent_pane = self
        self.dw_children.append(dw)


class DockWidget(DockWidgetBase, IDockWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.noteb: ttk.Notebook = None
        self._title = None

    @property
    def is_grouped(self):
        grouped = False
        if self.noteb is not None:
            if len(self.noteb.tabs()) > 1:
                grouped = True
        return grouped

    @property
    def title(self):
        return self._title if self._title is not None else self.uid

    def configure(self, cnf=None, **kw):
        if cnf:
            return super().configure(cnf, **kw)
        key = "title"
        if key in kw:
            self._title = kw.pop(key)
        return super().configure(cnf, **kw)
