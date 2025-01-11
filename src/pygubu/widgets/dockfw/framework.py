import tkinter as tk
import tkinter.ttk as ttk
import logging

from pygubu.utils.widget import iter_to_toplevel
from pygubu.widgets.dockfw.slotframe import SlotIndicator


logger = logging.getLogger(__name__)


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
    source_tab_clicked = None
    moving = False
    indicator_active = None
    cursor_default = "arrow"
    cursor_moving = "hand1"
    cursor_tab_target = "sb_down_arrow"
    cursor_showing = None
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
        # Only start movement if a tab is clicked
        cls.source_tab_clicked = tab_below_mouse(
            event.widget, event.x_root, event.y_root
        )
        if cls.source_tab_clicked is not None:
            cls.get_targets_below_mouse(event)
            cls.curr_dock = cls.bmouse_dock
            cls.curr_dpane = cls.bmouse_dpane
            cls.curr_dwidget = cls.bmouse_dwidget

    @classmethod
    def drag_motion(cls, event: tk.Event):
        if cls.curr_dock is None:
            # avoid errors on pygubu-designer preview
            return

        show_cursor = cls.cursor_moving
        cls._handle_cursor_moving()

        # If drag ends in a menu, a key error is produced.
        widget_below = None
        try:
            widget_below = event.widget.winfo_containing(
                event.x_root, event.y_root
            )
        except KeyError:
            pass
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
            and cls.curr_dwidget is not None
            and cls.curr_dwidget != cls.bmouse_dwidget
        ):
            cls.curr_dwidget.indicators_visible(False)
            cls.curr_dwidget = cls.bmouse_dwidget
            if cls.curr_dwidget != cls.source_dwidget:
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
            show_cursor = indicator.cget("cursor")
        if (
            last_indicator
            and last_indicator != indicator
            and last_indicator.winfo_exists()
        ):
            last_indicator.configure(background=last_indicator._ocolor)

        show_cursor = cls._handle_nootbook(event, widget_below, show_cursor)

        if cls.cursor_showing != show_cursor:
            cls.curr_dock.configure(cursor=show_cursor)

    @classmethod
    def _handle_cursor_moving(cls):
        if cls.moving is False:
            cls.source_dwidget = cls.curr_dwidget
            cls.curr_dock.indicators_visible(True)
            cls.curr_dpane.indicators_visible(True)
            cls.moving = True

    @classmethod
    def _handle_nootbook(cls, event, widget_below, show_cursor):
        if cls.bmouse_dwidget and isinstance(widget_below, ttk.Notebook):
            tab_clicked = tab_below_mouse(
                widget_below, event.x_root, event.y_root
            )
            if cls.bmouse_dwidget == cls.source_dwidget:
                if (
                    tab_clicked is not None
                    and tab_clicked != cls.source_tab_clicked
                ):
                    show_cursor = show_cursor = cls.cursor_tab_target
            elif tab_clicked is not None:
                show_cursor = cls.cursor_tab_target
        return show_cursor

    @classmethod
    def drag_end(cls, event):
        if cls.curr_dock:
            if cls.moving:
                cls.curr_dock.indicators_visible(False)
                if cls.curr_dpane:
                    cls.curr_dpane.indicators_visible(False)
                if cls.curr_dwidget:
                    cls.curr_dwidget.indicators_visible(False)
                # Execute move if any
                if cls.source_dwidget is not None:
                    cls.execute_move(event)

            cls.curr_dock.configure(cursor=cls.cursor_default)
        cls.moving = False
        cls.curr_dwidget = None

    @classmethod
    def execute_move(cls, event: tk.Event):
        widget_below = None
        # If drag ends in a menu, a key error is produced.
        try:
            widget_below = event.widget.winfo_containing(
                event.x_root, event.y_root
            )
        except KeyError:
            pass
        dock = cls.source_dwidget.maindock
        relative_to = None
        side = None
        if cls.indicator_active:
            side = cls.indicator_active.side
            target = cls.indicator_active.nametowidget(
                cls.indicator_active.winfo_parent()
            )
            relative_to = "pane" if isinstance(target, IDockPane) else "widget"
            if relative_to == "pane":
                dock._move_into_pane_side(
                    cls.source_dwidget, cls.curr_dpane, side
                )
            else:
                dock._move_to_widget_side(
                    cls.source_dwidget, cls.curr_dwidget, side
                )
            return
        if cls.curr_dwidget and isinstance(widget_below, ttk.Notebook):
            move_inside = True
            tab_below = tab_below_mouse(
                widget_below, event.x_root, event.y_root
            )
            if tab_below is None:
                # No move
                logger.debug("No move posible.")
                return
            if cls.curr_dwidget == cls.source_dwidget:
                # Move in same pane
                if tab_below == cls.source_tab_clicked:
                    move_inside = False
            if move_inside:
                logger.debug(
                    "Move %s into group of %s, position %s",
                    cls.source_dwidget,
                    cls.curr_dwidget,
                    tab_below,
                )
                dock._move_into_widget_group(
                    cls.curr_dwidget, cls.source_dwidget, tab_below
                )
