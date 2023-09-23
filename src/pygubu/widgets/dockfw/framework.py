import tkinter as tk
import tkinter.ttk as ttk

from pygubu.utils.widget import iter_to_toplevel
from pygubu.widgets.dockfw.slotframe import SlotIndicator


class IDockFrame:
    ...


class IDockPane:
    ...


class IDockWidget:
    ...


def tab_below_mouse(noteb: ttk.Notebook, rootx: int, rooty: int):
    # Is calculated this way because mouse motion events
    # return negative values with respect to where the drag started.
    x = rootx - noteb.winfo_rootx()
    y = rooty - noteb.winfo_rooty()
    tab_index = noteb.tk.call(noteb._w, "identify", "tab", x, y)
    if not isinstance(tab_index, int):
        tab_index = None
    return tab_index


class DockingFramework:
    initialized = False
    curr_dockf = None
    curr_dpane = None
    curr_dwidget = None
    source_dwidget = None
    moving = False
    indicator_active = None
    cursor_moving = "fleur"
    cursor_tab_target = "sb_down_arrow"
    indicator_bg_color = "#989cec"

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
    def get_targets(cls, event: tk.Event):
        dock = None
        pane = None
        widget = None

        widget_below = event.widget.winfo_containing(event.x_root, event.y_root)

        for w in iter_to_toplevel(widget_below):
            if isinstance(w, IDockFrame) and dock is None:
                dock = w
                break
            if isinstance(w, IDockPane) and pane is None:
                pane = w
            if isinstance(w, IDockWidget) and widget is None:
                widget = w
            if isinstance(w, ttk.Notebook) and widget is None:
                selected = None
                if event.type == tk.EventType.ButtonPress:
                    tab_clicked = w.tk.call(
                        w._w, "identify", "tab", event.x, event.y
                    )
                    if isinstance(tab_clicked, int):
                        tab_id = w.tabs()[tab_clicked]
                        selected = w.nametowidget(tab_id)
                nb_tabs = w.tabs()
                if selected is None and nb_tabs:
                    tab_id = nb_tabs[0]
                    selected = w.nametowidget(tab_id)
                if isinstance(selected, IDockWidget):
                    widget = selected
        if dock and widget and pane is None:
            pane = widget.parent_pane
        return (dock, pane, widget)

    @classmethod
    def drag_start(cls, event: tk.Event):
        cls.curr_dockf, cls.curr_dpane, cls.curr_dwidget = cls.get_targets(
            event
        )
        cls.source_dwidget = cls.curr_dwidget

    @classmethod
    def drag_motion(cls, event: tk.Event):
        if cls.moving is False:
            cls.curr_dockf.indicators_visible(True)
            cls.curr_dpane.indicators_visible(True)
            # cls.curr_dwidget.indicators_visible(True)
            cls.moving = True

        widget_below = event.widget.winfo_containing(event.x_root, event.y_root)
        if not widget_below:
            return
        _, below_dpane, below_dwidget = cls.get_targets(event)

        if below_dpane is not None and cls.curr_dpane != below_dpane:
            if (
                cls.curr_dpane is not None
                and cls.curr_dpane != cls.curr_dockf.main_pane
            ):
                cls.curr_dpane.indicators_visible(False)
            cls.curr_dpane = below_dpane
            below_dpane.indicators_visible(True)
        if below_dwidget is not None and cls.curr_dwidget != below_dwidget:
            cls.curr_dwidget.indicators_visible(False)
            cls.curr_dwidget = below_dwidget
            below_dwidget.indicators_visible(True)

        last_indicator = cls.indicator_active
        cls.indicator_active = None
        if isinstance(widget_below, SlotIndicator):
            cls.indicator_active = widget_below

        indicator = cls.indicator_active
        if indicator:
            if not hasattr(indicator, "_ocolor"):
                indicator._ocolor = indicator.cget("background")
            indicator.configure(background=cls.indicator_bg_color)
            cls.curr_dockf.configure(cursor=indicator.cget("cursor"))
        else:
            cls.curr_dockf.configure(cursor=cls.cursor_moving)
        if (
            last_indicator
            and last_indicator != indicator
            and last_indicator.winfo_exists()
        ):
            last_indicator.configure(background=last_indicator._ocolor)

    @classmethod
    def drag_end(cls, event):
        if cls.curr_dockf:
            if cls.moving:
                cls.curr_dockf.indicators_visible(False)
                if cls.curr_dpane:
                    cls.curr_dpane.indicators_visible(False)
                cls.curr_dwidget.indicators_visible(False)

                relative_to = None
                side = None
                if cls.indicator_active:
                    side = cls.indicator_active.side
                    target = cls.indicator_active.nametowidget(
                        cls.indicator_active.winfo_parent()
                    )
                    relative_to = (
                        "pane" if isinstance(target, IDockPane) else "widget"
                    )

                    # TODO: check for tab moves later here
                    cls.apply_move(
                        cls.source_dwidget,
                        cls.curr_dpane,
                        cls.curr_dwidget,
                        relative_to,
                        side,
                    )
            cls.curr_dockf.configure(cursor="arrow")
        cls.moving = False
        cls.curr_dwidget = None

    @classmethod
    def apply_move(
        cls, src_dwidget, target_pane, target_widget, relative_to, side
    ):
        dock = src_dwidget.maindock
        if relative_to == "pane":
            dock._move_into_pane_side(src_dwidget, target_pane, side)
        else:
            dock._move_to_widget_side(src_dwidget, target_widget, side)
