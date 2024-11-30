import tkinter as tk
import tkinter.ttk as ttk
import logging

from pygubu.widgets.dockfw.dockwidget import (
    DockWidgetBase,
    DockPane,
    DockWidget,
)
from pygubu.widgets.dockfw.framework import (
    DockingFramework,
    IDockFrame,
)


logger = logging.getLogger(__name__)


class DockFrame(DockWidgetBase, IDockFrame):
    """A Dock Frame, where user can configure the layout
    of the frames within a window.
    Based on https://wiki.tcl-lang.org/page/Docking+framework

    Generates <<DocFrame::LayoutChanged>> event when the user
    changes the layout.
    """

    EVENT_LAYOUT_CHANGED = "<<DocFrame::LayoutChanged>>"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.dock_widgets: dict[str, DockWidget] = {}
        self._main_pane = None
        self._emit_cbid = None

    def indicators_visible(self, visible: bool):
        if self._main_pane:
            self._main_pane.indicators_visible(visible)

    @property
    def main_pane(self):
        return self._main_pane

    def _add_pane_to_pane(
        self, topane: DockPane, newpane: DockPane, position=tk.END, **pane_kw
    ):
        # remove newpane as child of current pane if any
        newpane.detach_from_parent()

        topane.panedw.insert(position, newpane, **pane_kw)
        newpane.parent_pane = topane
        topane.add_dwchild(newpane)

    def _add_widget_to_pane(
        self, topane, widget, grouped=False, position=tk.END, weight=1
    ):
        nb = None
        if grouped:
            panes = topane.panedw.panes()
            if panes:
                nb = self.nametowidget(panes[-1])
        if nb is None:
            nb = ttk.Notebook(self, padding=0)
            DockingFramework.init_binding(nb)
            # topane.panedw.add(nb, weight=1)
            topane.panedw.insert(position, nb, weight=weight)
        nb.add(widget, text=widget.title)
        widget.tkraise()
        widget.detach_from_parent()
        topane.add_dwchild(widget)
        # widget.parent_pane = topane
        widget.noteb = nb
        self.dock_widgets[widget.uid] = widget

    def new_pane(self, *, main_pane=False, **pane_kw) -> DockPane:
        """Creates new DockPane locked to this DockFrame."""
        pane = DockPane(self, maindock=self, **pane_kw)
        if main_pane:
            self.set_main_pane(pane)
        return pane

    def set_main_pane(self, pane):
        pane.pack(in_=self.fcenter, expand=True, fill=tk.BOTH)
        self._main_pane = pane

    def new_widget(self, **widget_kw) -> DockWidget:
        """Creates new DockWidget locked to this DockFrame."""
        widget = DockWidget(self, maindock=self, **widget_kw)
        return widget

    def _add_widget_to_group(
        self, tgroup, swidget: DockWidget, position=tk.END
    ):
        nb: ttk.Notebook = tgroup.noteb
        nb.insert(position, swidget, text=swidget.title)
        nb.select(position)
        swidget.noteb = nb
        if tgroup != swidget:
            swidget.detach_from_parent()
            tgroup.parent_pane.add_dwchild(swidget)
        # swidget.parent_pane = tgroup.parent_pane
        swidget.tkraise()
        self.dock_widgets[swidget.uid] = swidget

    def _move_into_widget_group(self, twidget, swidget, position):
        noteb = swidget.noteb
        pane = swidget.parent_pane
        self._add_widget_to_group(twidget, swidget, position)
        self._clear_notebook(noteb)
        self._clear_pane(pane)
        self._emit_layout_changed()

    def _move_into_pane_side(self, swidget, tpane, side, position=None):
        logger.debug("Move to into pane side. position %s", position)

        move_in_same_pane = swidget.parent_pane == tpane
        simple_sides = "ns" if tpane.orient == tk.VERTICAL else "we"

        noteb = swidget.noteb
        pane = swidget.parent_pane
        if position is None:
            position = 0 if side in "nw" else tk.END

        if move_in_same_pane:
            if side in simple_sides:
                # if widget is in a group, must detach and re-insert widget
                if swidget.is_grouped:
                    self._add_widget_to_pane(tpane, swidget, position=position)
                elif tpane.count > 1:
                    # pane has more than the moving widget
                    # reposition widget in same pane
                    logger.debug(
                        "Reposition widget in same pane. position %s", position
                    )
                    tpane.panedw.insert(position, noteb)
                else:
                    logger.debug("No need to move")
            else:
                self._move_into_pane_side_complex(
                    swidget, tpane, side, position
                )
        else:
            if side in simple_sides:
                self._add_widget_to_pane(tpane, swidget, position=position)
            else:
                self._move_into_pane_side_complex(
                    swidget, tpane, side, position
                )
        self._clear_notebook(noteb)
        self._clear_pane(pane)
        self._emit_layout_changed()

    def _move_into_pane_side_complex(self, swidget, tpane, side, position=None):
        move_to_new_pane = True
        # check if parent pane is in sync
        parent_pane = tpane.parent_pane
        if parent_pane:
            in_sync = side in (
                "ns" if parent_pane.orient == tk.VERTICAL else "we"
            )
            if in_sync:
                logger.debug("Parent pane in sync, adding into parent.")
                index = self._get_position_in_pane(tpane)
                logger.debug("Pane position: %s side: %s", index, side)
                if side not in "nw":
                    index += 1
                    index = tk.END if index >= parent_pane.count else index
                logger.debug("final index: %s", index)
                self._add_widget_to_pane(parent_pane, swidget, position=index)
                move_to_new_pane = False
        if move_to_new_pane:
            logger.debug("Moving to new pane.")
            self._move_to_new_pane(swidget, tpane, side)

    def _move_to_new_pane(self, swidget: DockWidget, tpane: DockPane, side):
        """Move DockWidget 'swidget' to a new pane inside target pane 'tpane'."""
        logger.debug("Move to new pane.")
        new_orient = (
            tk.HORIZONTAL if tpane.orient == tk.VERTICAL else tk.VERTICAL
        )
        main_pane = tpane == self._main_pane
        new_pane = self.new_pane(main_pane=main_pane, orient=new_orient)
        parent_pane = tpane.parent_pane
        self._add_pane_to_pane(new_pane, tpane)
        if parent_pane:
            self._add_pane_to_pane(parent_pane, new_pane)
        new_pos = 0 if side in "nw" else tk.END
        self._add_widget_to_pane(new_pane, swidget, position=new_pos)
        self._raise_panes(new_pane)

    def _move_to_widget_side(
        self, swidget: DockWidget, twidget: DockWidget, side
    ):
        """Move 'swidget' to one side of 'twidget'."""
        logger.debug("Move to widget side: %s", side)
        if swidget == twidget:
            logger.debug("No move needed.")
            return

        tpane = twidget.parent_pane
        # move_in_same_pane = swidget.parent_pane == tpane
        simple_sides = "ns" if tpane.orient == tk.VERTICAL else "we"

        if side in simple_sides:
            index = self._get_position_in_pane(twidget)
            if side not in "nw":
                index += 1
                index = tk.END if index >= tpane.count else index
            self._move_into_pane_side(swidget, tpane, side, position=index)
        else:
            new_orient = (
                tk.HORIZONTAL if tpane.orient == tk.VERTICAL else tk.VERTICAL
            )
            self._replace_widget_with_pane(twidget, new_orient)
            self._move_into_pane_side(swidget, twidget.parent_pane, side)

    def _get_position_in_pane(self, widget):
        index = tk.END
        if isinstance(widget, DockWidget):
            pane = widget.parent_pane
            if pane:
                panes: tuple = pane.panedw.panes()
                index = panes.index(str(widget.noteb))
        elif isinstance(widget, DockPane):
            pane = widget.parent_pane
            if pane:
                panes: tuple = pane.panedw.panes()
                index = panes.index(str(widget))
        return index

    def _replace_widget_with_pane(self, widget: DockWidget, orient):
        """Creates new pane, move widget inside it and
        puts the pane in the current position of widget.
        """
        parent_pane = widget.parent_pane
        widget_pos = self._get_position_in_pane(widget)
        new_pane = self.new_pane(orient=orient)
        self._add_pane_to_pane(parent_pane, new_pane, position=widget_pos)
        side = "n" if orient == tk.VERTICAL else "w"
        self._move_into_pane_side(widget, new_pane, side, position=tk.END)

    def _raise_panes(self, widget):
        if isinstance(widget, DockPane):
            widget.tkraise()
            for w in widget.panedw.panes():
                self._raise_panes(widget.nametowidget(w))
        elif isinstance(widget, ttk.Notebook):
            widget.tkraise()
            for tab in widget.tabs():
                self._raise_panes(widget.nametowidget(tab))
        elif not isinstance(widget, tk.Canvas):
            widget.tkraise()

    def _clear_notebook(self, nb: ttk.Notebook):
        """Destroy notebook if does not have children."""
        if not nb.tabs():
            nb.destroy()

    def _clear_pane(self, pane: DockPane):
        """If pane does not have children, destroys it.
        Otherwise tries to simplificate it.
        """
        if pane.count == 0:
            pane.detach_from_parent()
            pane.destroy()
            return
        logger.debug("Simplify pane for: %s parent: %s", pane, pane.parent_pane)
        if pane.parent_pane:
            parent = pane.parent_pane
            if parent.orient == pane.orient:
                # FIXME: Pane can be simplified, try moving content to parent pane.?
                logger.debug(
                    "Pane can be simplified, try moving content to parent pane."
                )
            else:
                logger.debug(
                    "Pane orients differ: %s %s", parent.orient, pane.orient
                )
                if pane.count == 1:
                    logger.debug(
                        "Pane can be simplified, pane has only one child."
                    )
                    widget = pane.nametowidget(pane.panedw.panes()[0])
                    if isinstance(widget, ttk.Notebook):
                        tabs = widget.tabs()
                        if len(tabs) > 1:
                            # FIXME: simplify a pane with grouped widgets.
                            logger.warn("Grouped widgets not managed yet.")
                            logger.warn("Aborting simplification.")
                            return
                        widget = pane.nametowidget(widget.tabs()[0])
                    side = "n" if parent.orient == tk.VERTICAL else "w"
                    pos = self._get_position_in_pane(pane)
                    logger.debug("Trying to move: %s", widget)
                    if isinstance(widget, DockPane):
                        self._add_pane_to_pane(parent, widget, position=pos)
                    else:
                        self._move_into_pane_side(
                            widget, parent, side, position=pos
                        )

    def save_layout(self):
        """Return a dictionary with information of current layout."""
        config = {}
        if self.main_pane:
            layout = {}
            self._create_layout(self.main_pane, layout)
            config = {
                "ver": 1,
                "main": self.main_pane.uid,
                "layout": layout,
                "dwl": [dw_uid for dw_uid in self.dock_widgets],
            }
        return config

    def load_layout(self, config: dict):
        """Restore layout from previusly saved config dictionary."""
        if not self._layout_config_valid(config):
            raise ValueError("Invalid layout configuration.")
        self._remove_layout()
        main_uid = config["main"]
        pane = self._build_layout(main_uid, config["layout"])
        self.set_main_pane(pane)

    def _emit_layout_changed(self):
        """Schedule a notify of layout changed."""
        if self._emit_cbid is not None:
            self.after_cancel(self._emit_cbid)
        self._emit_cbid = self.after(800, self._notify_layout_changed)

    def _notify_layout_changed(self):
        self.event_generate(self.EVENT_LAYOUT_CHANGED)
        self._emit_cbid = None

    def _layout_config_valid(self, config):
        valid = True
        # validate "version"
        if config.get("ver", 0) != 1:
            valid = False
        # validate widgets exists
        if valid and "dwl" in config:
            for uid in config["dwl"]:
                if uid not in self.dock_widgets:
                    valid = False
                    break
        else:
            valid = False

        return valid

    def _create_layout(self, pane: DockPane, layout: dict):
        conf = {"orient": pane.orient}
        children = []
        layout[pane.uid] = {
            "cnf": conf,
            "ch": children,
        }
        # if len(pane.panedw.panes()) > 1:
        #    print(">>>", pane.uid),
        #    print(">>>", pane.panedw.sashpos(0))
        for child in pane.sorted_dw_children:
            if isinstance(child, DockPane):
                children.append(child.uid)
                self._create_layout(child, layout)
            else:
                dw = {
                    "uid": child.uid,
                    "grouped": child.is_grouped,
                    "weight": int(child.dw_options.get("weight", 1)),
                }
                children.append(dw)

    def _build_layout(self, pane_uid, layout):
        pane = self.new_pane(uid=pane_uid, **layout[pane_uid]["cnf"])
        for widget_or_pane in layout[pane_uid]["ch"]:
            if isinstance(widget_or_pane, dict):
                child_uid = widget_or_pane["uid"]
                grouped = widget_or_pane["grouped"]
                weight = widget_or_pane["weight"]
                if child_uid in self.dock_widgets:
                    pane.add_widget(
                        self.dock_widgets[child_uid],
                        grouped=grouped,
                        weight=weight,
                    )
            else:
                child_pane = self._build_layout(widget_or_pane, layout)
                pane.add_pane(child_pane)
        return pane

    def _remove_layout(self):
        """Remove all panes and set main pane to None"""

        def _recursive_remove(pane):
            for child in pane.dw_children:
                if isinstance(child, DockPane):
                    _recursive_remove(child)
                else:
                    child.detach_from_parent()
            pane.detach_from_parent()
            pane.destroy()

        if self.main_pane:
            _recursive_remove(self.main_pane)
            self._main_pane = None
