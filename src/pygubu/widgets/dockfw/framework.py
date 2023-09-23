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
    curr_dock = None
    curr_dpane = None
    curr_dwidget = None
    bmouse_dock = None
    bmouse_dpane = None
    bmouse_dwidget = None
    source_dwidget = None
    moving = False
    indicator_active = None
    cursor_default = "arrow"
    cursor_moving = "fleur"
    cursor_tab_target = "sb_down_arrow"
    indicator_bg_color = "#989cec"

    @classmethod
    def init_binding(cls, widget: tk.Widget):
        widget.bind("<Button-1>", cls.drag_start, add=True)
        widget.bind("<B1-Motion>", cls.drag_motion, add=True)
        widget.bind("<ButtonRelease-1>", cls.drag_end, add=True)

    @classmethod
    def get_targets_below_mouse(cls, event: tk.Event):
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
        cls.bmouse_dock = dock
        cls.bmouse_dpane = pane
        cls.bmouse_dwidget = widget

    @classmethod
    def drag_start(cls, event: tk.Event):
        cls.get_targets_below_mouse(event)
        cls.curr_dock = cls.bmouse_dock
        cls.curr_dpane = cls.bmouse_dpane
        cls.curr_dwidget = cls.bmouse_dwidget

    @classmethod
    def drag_motion(cls, event: tk.Event):
        if cls.moving is False:
            cls.source_dwidget = cls.curr_dwidget
            cls.curr_dock.indicators_visible(True)
            cls.curr_dpane.indicators_visible(True)
            # cls.curr_dwidget.indicators_visible(True)
            cls.moving = True

        widget_below = event.widget.winfo_containing(event.x_root, event.y_root)
        if not widget_below:
            return

        cls.get_targets_below_mouse(event)
        if cls.bmouse_dpane is not None and cls.curr_dpane != cls.bmouse_dpane:
            if (
                cls.curr_dpane is not None
                and cls.curr_dpane != cls.curr_dock.main_pane
            ):
                cls.curr_dpane.indicators_visible(False)
            cls.curr_dpane = cls.bmouse_dpane
            cls.curr_dpane.indicators_visible(True)
        if (
            cls.bmouse_dwidget is not None
            and cls.curr_dwidget != cls.bmouse_dwidget
            and cls.bmouse_dwidget != cls.source_dwidget
        ):
            cls.curr_dwidget.indicators_visible(False)
            cls.curr_dwidget = cls.bmouse_dwidget
            cls.curr_dwidget.indicators_visible(True)

        last_indicator = cls.indicator_active
        cls.indicator_active = None
        if isinstance(widget_below, SlotIndicator):
            cls.indicator_active = widget_below

        indicator = cls.indicator_active
        if indicator:
            if not hasattr(indicator, "_ocolor"):
                indicator._ocolor = indicator.cget("background")
            indicator.configure(background=cls.indicator_bg_color)
            cls.curr_dock.configure(cursor=indicator.cget("cursor"))
        else:
            cls.curr_dock.configure(cursor=cls.cursor_moving)
        if (
            last_indicator
            and last_indicator != indicator
            and last_indicator.winfo_exists()
        ):
            last_indicator.configure(background=last_indicator._ocolor)

    @classmethod
    def drag_end(cls, event):
        if cls.curr_dock:
            if cls.moving:
                cls.curr_dock.indicators_visible(False)
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
            cls.curr_dock.configure(cursor=cls.cursor_default)
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
