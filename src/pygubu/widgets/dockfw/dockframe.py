import tkinter as tk
import tkinter.ttk as ttk

from pygubu.widgets.dockfw.dockwidget import (
    DockWidgetBase,
    DockPane,
    DockWidget,
)
from pygubu.widgets.dockfw.framework import (
    DockingFramework,
    IDockFrame,
)


class DockFrame(DockWidgetBase, IDockFrame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.dock_widgets: dict[str, DockWidget] = {}
        self._main_pane = None

    def indicators_visible(self, visible: bool):
        if self._main_pane:
            self._main_pane.indicators_visible(visible)

    @property
    def main_pane(self):
        return self._main_pane

    def _add_pane_to_pane(self, topane, newpane, position=tk.END):
        topane.panedw.insert(position, newpane)
        newpane.parent_pane = topane

    def _add_widget_to_pane(
        self, topane, widget, as_tab=False, position=tk.END
    ):
        nb = None
        if as_tab:
            panes = topane.panedw.panes()
            if panes:
                nb = self.nametowidget(panes[-1])
        if nb is None:
            nb = ttk.Notebook(self)
            DockingFramework.init_binding(nb)
            # topane.panedw.add(nb, weight=1)
            topane.panedw.insert(position, nb, weight=1)
        nb.add(widget, text=widget.uid)
        widget.tkraise()
        widget.parent_pane = topane
        widget.noteb = nb
        self.dock_widgets[widget.uid] = widget

    def new_pane(self, *, main_pane=False, **pane_kw):
        pane = DockPane(self, maindock=self, **pane_kw)
        if main_pane:
            self.set_main_pane(pane)
        return pane

    def set_main_pane(self, pane):
        pane.pack(in_=self.fcenter, expand=True, fill=tk.BOTH)
        self._main_pane = pane

    def new_widget(self, **widget_kw):
        widget = DockWidget(self, maindock=self, **widget_kw)
        return widget

    def find_pane_for(self, dock_widget):
        target = None
        for uid, widget in self.dock_widgets.items():
            if widget == dock_widget:
                if widget.parent_pane:
                    target = widget.parent_pane
                    break
        return target

    def _add_widget_to_group(self, tgroup, swidget, position=tk.END):
        nb: ttk.Notebook = tgroup.noteb
        nb.insert(position, swidget, text=swidget.uid)
        nb.select(position)
        swidget.noteb = nb
        swidget.parent_pane = tgroup.parent_pane
        swidget.tkraise()
        self.dock_widgets[swidget.uid] = swidget

    def _move_into_widget_group(self, twidget, swidget, position):
        noteb = swidget.noteb
        pane = swidget.parent_pane
        self._add_widget_to_group(twidget, swidget, position)
        self._clear_notebook(noteb)
        self._clear_pane(pane)

    def _move_into_pane_side(self, swidget, tpane, side, position=None):
        print("Move to into pane side. position=", position)

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
                    print("Reposition widget in same pane. position=", position)
                    tpane.panedw.insert(position, noteb)
                else:
                    print("No need to move")
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

    def _move_into_pane_side_complex(self, swidget, tpane, side, position=None):
        move_to_new_pane = True
        # check if parent pane is in sync
        parent_pane = tpane.parent_pane
        if parent_pane:
            in_sync = side in (
                "ns" if parent_pane.orient == tk.VERTICAL else "we"
            )
            if in_sync:
                print("Parent pane in sync, adding into parent")
                index = self._get_position_in_pane(tpane)
                print("Pane position:", index, "side:", side)
                if side not in "nw":
                    index += 1
                    index = tk.END if index >= parent_pane.count else index
                print("final index:", index)
                self._add_widget_to_pane(parent_pane, swidget, position=index)
                move_to_new_pane = False
        if move_to_new_pane:
            print("Moving to new pane.")
            self._move_to_new_pane(swidget, tpane, side)

    def _move_to_new_pane(self, swidget, tpane, side):
        print("Move to new pane")
        new_orient = (
            tk.HORIZONTAL if tpane.orient == tk.VERTICAL else tk.VERTICAL
        )
        main_pane = True if tpane == self._main_pane else False
        new_pane = self.new_pane(main_pane=main_pane, orient=new_orient)
        parent_pane = tpane.parent_pane
        self._add_pane_to_pane(new_pane, tpane)
        if parent_pane:
            panes = parent_pane.panedw.panes()
            print("panes in parent pane:", panes)
            self._add_pane_to_pane(parent_pane, new_pane)
        new_pos = 0 if side in "nw" else tk.END
        self._add_widget_to_pane(new_pane, swidget, position=new_pos)
        self._raise_panes(new_pane)

    def _move_to_widget_side(self, swidget, twidget, side):
        print("Move to widget side", side)
        if swidget == twidget:
            print("No move needed")
            return

        tpane = twidget.parent_pane
        # move_in_same_pane = swidget.parent_pane == tpane
        simple_sides = "ns" if tpane.orient == tk.VERTICAL else "we"

        if side in simple_sides:
            index = self._get_position_in_pane(twidget)
            if side not in "nw":
                index += 1
                index = tk.END if index >= tpane.count else index
            print("index:", index, "count:", tpane.count)
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
                # if index == 0 and len(panes) > 0:
                #    index = tk.END
        return index

    def _replace_widget_with_pane(self, widget, orient):
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
        if not nb.tabs():
            nb.destroy()

    def _clear_pane(self, pane):
        if pane.count == 0:
            pane.destroy()
        else:
            print("Simplify pane for:", pane, "parent:", pane.parent_pane)
            # simplified = False
            if pane.parent_pane:
                parent = pane.parent_pane
                if parent.orient == pane.orient:
                    # FIXME: Pane can be simplified, try moving content to parent pane.?
                    print(
                        "Pane can be simplified, try moving content to parent pane."
                    )
                else:
                    print("Pane orients differ: ", parent.orient, pane.orient)
                    if pane.count == 1:
                        print("Pane can be simplified, pane has only one child")
                        widget = pane.nametowidget(pane.panedw.panes()[0])
                        if isinstance(widget, ttk.Notebook):
                            tabs = widget.tabs()
                            if len(tabs) > 1:
                                print("WARNING: multiple tabs not managed yet.")
                                print("Aborting simplification.")
                                return
                            widget = pane.nametowidget(widget.tabs()[0])
                        side = "n" if parent.orient == tk.VERTICAL else "w"
                        pos = self._get_position_in_pane(pane)
                        print("Trying to move:", widget)
                        if isinstance(widget, DockPane):
                            self._add_pane_to_pane(parent, widget, position=pos)
                        else:
                            self._move_into_pane_side(
                                widget, parent, side, position=pos
                            )
