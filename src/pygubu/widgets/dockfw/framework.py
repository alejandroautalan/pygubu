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
    source_tab = None
    moving = False
    indicator_active = None

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
        cls.current_dw = below_dock
        cls.current_pane = below_pane
        cls.current_tab = below_tab
        cls.source_tab = below_tab

    @classmethod
    def drag_motion(cls, event: tk.Event):
        if cls.moving is False:
            cls.moving = True
            cls.current_dw.indicators_visible(True)
            if cls.current_pane is not None:
                cls.current_pane.indicators_visible(True)
            if (
                cls.current_tab is not None
                and cls.current_tab != cls.source_tab
            ):
                cls.current_tab.indicators_visible(True)

        # print(".", end="")
        widget_below = event.widget.winfo_containing(event.x_root, event.y_root)
        if not widget_below:
            return
        below_dock, below_pane, below_tab = cls._get_panes(widget_below)
        # if cls.current_dw != below_dock:
        #    cls.current_dw = below_dock
        #    print("changed to dock:", below_dock, flush=True)
        if cls.current_pane != below_pane and below_pane is not None:
            cls.current_pane.indicators_visible(False)
            cls.current_pane = below_pane
            below_pane.indicators_visible(True)
            print("changed to pane:", below_pane, flush=True)
        if (
            cls.current_tab != below_tab
            and below_tab is not None
            and below_tab != cls.source_tab
        ):
            cls.current_tab.indicators_visible(False)
            cls.current_tab = below_tab
            below_tab.indicators_visible(True)
            print("changed to tab:", below_tab, flush=True)

        last_indicator = cls.indicator_active
        cls.indicator_active = None
        if isinstance(widget_below, SlotIndicator):
            cls.indicator_active = widget_below

        indicator = cls.indicator_active
        if indicator:
            if not hasattr(indicator, "_ocolor"):
                indicator._ocolor = indicator.cget("background")
            indicator.configure(background="#989cec")
            cls.current_dw.configure(cursor=indicator.cget("cursor"))
        else:
            cls.current_dw.configure(cursor="fleur")
        if last_indicator and last_indicator != indicator:
            last_indicator.configure(background=last_indicator._ocolor)

    @classmethod
    def drag_end(cls, event):
        if cls.moving:
            cls.current_dw.indicators_visible(False)
            cls.current_pane.indicators_visible(False)
            cls.current_tab.indicators_visible(False)
        if cls.indicator_active:
            source_dock, source_pane, source_tab = cls._get_panes(
                cls.source_tab
            )
            target_dock, target_pane, target_tab = cls._get_panes(
                cls.indicator_active
            )
            cls.apply_move(
                source_dock,
                source_pane,
                source_tab,
                target_dock,
                target_pane,
                target_tab,
                cls.indicator_active.side,
            )

        cls.current_dw.configure(cursor="arrow")
        cls.moving = False
        cls.current_tab = None
        cls.current_pane = None
        cls.current_dw = None

    @classmethod
    def apply_move(
        cls,
        source_dock,
        source_pane,
        source_tab,
        target_dock,
        target_pane,
        target_tab,
        side,
    ):
        print("-" * 10)
        print("source_dock", source_dock)
        print("source_pane", source_pane)
        print("source_tab", source_tab)
        print("target_dock", target_dock)
        print("target_pane", target_pane)
        print("target_tab", target_tab)
        print("-" * 10)
        if source_pane == target_pane:
            print("Move in Same pane, position:", side)
        if target_tab:
            if side in "ew":
                print(
                    "Move Inside tab, position:",
                    side,
                )
            else:
                print(
                    "Move relative to a tab, position:",
                    side,
                )
        if target_tab is None and target_pane is None:
            print(
                "Move relative to docframe, position:",
                side,
            )

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
