import tkinter as tk
import tkinter.ttk as ttk
from dataclasses import dataclass, field

from pygubu.utils.widget import iter_to_toplevel
from .slotframe import SlotIndicator

# DockFrame
#     DockArea: vertical u orizontal (panedwindow)
#         DockPane: ??


class IDockFrame:
    ...


class IDockPane:
    ...


class IDockWidget:
    ...


class DockingFramework:
    initialized = False
    current_tab = None
    current_pane = None
    current_dw = None

    @classmethod
    def init_binding(cls, master: tk.Widget):
        if cls.initialized:
            return
        master.bind_class("TNotebook", "<Button-1>", cls.drag_start, add=True)
        master.bind_class("TNotebook", "<B1-Motion>", cls.drag_motion, add=True)
        master.bind_class(
            "TNotebook", "<ButtonRelease-1>", cls.drag_end, add=True
        )
        cls.initialized = True

    @classmethod
    def _get_panes(cls, widget):
        dock = None
        pane = None
        tab = None
        if isinstance(widget, ttk.Notebook):
            tab_sel = widget.select()
            tab = widget.nametowidget(tab_sel)

        for w in iter_to_toplevel(widget):
            if isinstance(w, IDockWidget) and tab is None:
                tab = w
            if isinstance(w, IDockPane) and pane is None:
                pane = w
            if isinstance(w, IDockFrame) and dock is None:
                dock = w
                break
        return (dock, pane, tab)

    @classmethod
    def drag_start(cls, event: tk.Event):
        print("drag_start")
        widget_below = event.widget
        below_dock, below_pane, below_tab = cls._get_panes(widget_below)
        cls.current_tab = below_tab
        cls.current_pane = below_pane
        cls.current_dw = below_dock
        p = f"""current_tab = {cls.current_tab}
        current_pane = {cls.current_pane}
        current_dw = {cls.current_dw}"""
        print(p)

    @classmethod
    def drag_motion(cls, event: tk.Event):
        # print(".", end="")
        widget_below = event.widget.winfo_containing(event.x_root, event.y_root)
        if not widget_below:
            return
        prev_dock = cls.current_dw
        below_dock, below_pane, below_tab = cls._get_panes(widget_below)
        if cls.current_dw != below_dock:
            cls.current_dw = below_dock
            print("changed to dock:", below_dock, flush=True)
        if cls.current_pane != below_pane:
            cls.current_pane = below_pane
            print("changed to pane:", below_pane, flush=True)
        if cls.current_tab != below_tab:
            cls.current_tab = below_tab
            print("changed to tab:", below_tab, flush=True)

        if prev_dock:
            prev_dock.indicators_visble(False)
        if cls.current_dw:
            cls.current_dw.indicators_visble(True)
        widget_below.update()

    @classmethod
    def drag_end(cls, event):
        print("drag_end")
        if cls.current_dw:
            cls.current_dw.indicators_visble(False)
        cls.current_tab = None
        cls.current_pane = None
        cls.current_dw = None

    @classmethod
    def raise_tree(cls, widget: tk.Widget):
        widget.tkraise()
        class_ = str(widget.winfo_class())
        if class_ == "TNotebook":
            for tab in widget.tabs():
                cls.raise_tree(widget.nametowidget(tab))
        elif class_ == "TPanedwindow":
            for pane in widget.panes():
                cls.raise_tree(widget.nametowidget(pane))
