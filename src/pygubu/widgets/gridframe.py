#!/usr/bin/python3
"""
GridFrame

A container that arranges its child widgets in a grid.


UI source file: gridframe.ui
"""
# <MODULE_IMPORTS>
from enum import StrEnum, auto
from pygubu.utils.widget import WidgetConfigureMixin

# </MODULE_IMPORTS>
import tkinter as tk
import tkinter.ttk as ttk


# <CLASS_DEFINITION>
class Alignment(StrEnum):
    BEGIN = auto()
    CENTER = auto()
    END = auto()


class Sizing(StrEnum):
    FILL = auto()
    SHRINK_BEGIN = auto()
    SHRINK_CENTER = auto()
    SHRINK_END = auto()


class Direction(StrEnum):
    ROW = auto()
    COLUMN = auto()


class _FlexGrid(ttk.Frame):

    STICKY_HMAP = {
        Sizing.FILL: tk.W + tk.E,
        Sizing.SHRINK_BEGIN: tk.W,
        Sizing.SHRINK_CENTER: "",
        Sizing.SHRINK_END: tk.E,
    }
    STICKY_VMAP = {
        Sizing.FILL: tk.N + tk.S,
        Sizing.SHRINK_BEGIN: tk.N,
        Sizing.SHRINK_CENTER: "",
        Sizing.SHRINK_END: tk.S,
    }

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self._anchor = tk.CENTER
        self._rows = (-1, ())
        self._cols = (-1, ())
        self._flow = Direction.ROW
        self._gap = [0, 0]
        self._grid_expand = False
        self._cell_hsizing = Sizing.SHRINK_CENTER
        self._cell_vsizing = Sizing.SHRINK_CENTER
        self._realize_layout_cbid = None

    def _parse_dim(self, value) -> tuple:
        fdim = -1
        weights = tuple()
        if isinstance(value, int):
            fdim = value
        elif isinstance(value, (list, tuple)):
            fdim = len(value)
            weights = value
        elif isinstance(value, str):
            if value == "auto":
                fdim = -1
            elif "," in value:
                weights = value.split(",")
                fdim = len(weights)
            else:
                fdim = int(value)
        return fdim, weights

    def _parse_gap(self, value) -> tuple:
        fgap = (0, 0)
        if isinstance(value, (list, tuple)):
            fgap = value
        elif isinstance(value, str):
            values = tuple(value.split(maxsplit=1))
            if len(values) == 2:
                fgap = values
            else:
                fgap = (values[0], values[0])
        # print(f"{type(value)=} {value=} {fgap=}")
        return fgap

    def _adjust_dimensions(self, widget_count: int) -> tuple[int, int]:
        """Recalculate dimensions when the number of widgets
        exceeds the row and column configuration."""
        flat_dim = widget_count if widget_count > 0 else widget_count + 1
        row_dim = self._rows[0] if self._rows[0] > 0 else flat_dim
        col_dim = self._cols[0] if self._cols[0] > 0 else flat_dim
        last_row, last_col = self.index2rc(widget_count - 1, col_dim)
        return (max(row_dim, last_row + 1), max(col_dim, last_col + 1))

    def _grid_clear(self, widgets):
        for child in widgets:
            child.grid_forget()
        rows, cols = self.grid_size()
        for r in range(0, rows):
            self.rowconfigure(r, minsize=0, weight=0, uniform="", pad=0)
        for c in range(0, cols):
            self.rowconfigure(c, minsize=0, weight=0, uniform="", pad=0)

    def apply_layout(self):
        if self._realize_layout_cbid is not None:
            self.after_cancel(self._realize_layout_cbid)
        self._realize_layout_cbid = self.after(100, self._realize_layout)

    def _realize_layout(self):
        # breakpoint()
        widgets = [self.nametowidget(child) for child in self.children]
        self._grid_clear(widgets)

        # grid position
        self.grid_anchor(self._anchor)

        # cells setup
        sticky = (
            self.STICKY_HMAP[self._cell_hsizing]
            + self.STICKY_VMAP[self._cell_vsizing]
        )
        child_grid = dict(
            column=0,
            row=0,
            padx=0,
            pady=0,
            sticky=sticky,
        )

        gap_none = (0, 0)
        gap_row, gap_col = self._gap
        gap_x = (0, gap_col)
        gap_y = (0, gap_row)
        # row_dim = self._rows if self._rows > 0 else 1000
        # col_dim = self._cols if self._cols > 0 else 1000
        # adjust dimensions if there are more widgets than configured dimensions.
        row_dim, col_dim = self._adjust_dimensions(len(widgets))
        skip_row = row_dim - 1
        skip_col = col_dim - 1
        for index, child in enumerate(widgets):
            padx = gap_x
            pady = gap_y
            if self._flow == Direction.ROW:
                row_next, col_next = self.index2rc(index, col_dim)
            else:
                col_next, row_next = self.index2rc(index, row_dim)
            if row_next == skip_row:
                pady = gap_none
            if col_next == skip_col:
                padx = gap_none
            child_grid["row"] = row_next
            child_grid["column"] = col_next
            child_grid["padx"] = padx
            child_grid["pady"] = pady
            # print(
            #     f"---\n{row_dim=} {col_dim=}\n{skip_row=} {skip_col=}\n{row_next=} {col_next=}"
            #     f"\n{gap_row=} {gap_col=}\n{child_grid}"
            # )
            child.grid(**child_grid)

        # streching for all rows and cols
        weight_all = 1 if self._grid_expand else 0
        self.rowconfigure("all", weight=weight_all)
        self.columnconfigure("all", weight=weight_all)
        # individual row and col streching
        for row, weight in enumerate(self._rows[1]):
            self.rowconfigure(row, weight=weight)
        for col, weight in enumerate(self._cols[1]):
            self.columnconfigure(col, weight=weight)

        self._layout_cbid = None

    def index2rc(self, i, coldim):
        """Index to (row, column) coords"""
        c = i % coldim
        r = (i - c) // coldim
        return (r, c)

    def child_add(self, widget):
        self.apply_layout()


class GridFrame(WidgetConfigureMixin, _FlexGrid):
    """Your widget direct subclass.

    Only simple properties will be configured.
    No commands, no bindings.
    """

    PROP_GRID_ANCHOR = "grid_anchor"
    PROP_GRID_ROWS = "grid_dimrows"
    PROP_GRID_COLS = "grid_dimcols"
    PROP_GRID_PROPAGATE = "grid_propagate"
    PROP_GRID_FLOW = "grid_flow"
    PROP_GRID_GAP = "grid_gap"
    PROP_GRID_EXPAND = "grid_expand"
    PROP_GRID_HSIZING = "grid_chsizing"
    PROP_GRID_VSIZING = "grid_cvsizing"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        # </CLASS_DEFINITION>
        # widget setup
        self.configure(height=200, width=200)
        # Layout for 'frame1' skipped in custom widget template.
        # <CLASS_BODY>
        self.apply_layout()

    # WidgetConfigureMixin

    def _widget_cget(self, option):
        if option == self.PROP_GRID_ANCHOR:
            return self._anchor
        if option == self.PROP_GRID_ROWS:
            return self._rows
        elif option == self.PROP_GRID_COLS:
            return self._cols
        elif option == self.PROP_GRID_PROPAGATE:
            return bool(self.grid_propagate())
        elif option == self.PROP_GRID_FLOW:
            return self._flow
        elif option == self.PROP_GRID_GAP:
            return self._gap
        elif option == self.PROP_GRID_EXPAND:
            return self._grid_expand
        elif option == self.PROP_GRID_HSIZING:
            return self._cell_hsizing
        elif option == self.PROP_GRID_VSIZING:
            return self._cell_vsizing
        return super()._widget_cget(option)

    def _configure_set(self, **kw):
        apply_layout = False
        if self.PROP_GRID_ANCHOR in kw:
            self._anchor = kw.pop(self.PROP_GRID_ANCHOR)
            apply_layout = True
        if self.PROP_GRID_ROWS in kw:
            self._rows = self._parse_dim(kw.pop(self.PROP_GRID_ROWS))
            apply_layout = True
        if self.PROP_GRID_COLS in kw:
            self._cols = self._parse_dim(kw.pop(self.PROP_GRID_COLS))
            apply_layout = True
        if self.PROP_GRID_PROPAGATE in kw:
            value = bool(kw.pop(self.PROP_GRID_PROPAGATE))
            self.grid_propagate(value)
        if self.PROP_GRID_FLOW in kw:
            self._flow = Direction(kw.pop(self.PROP_GRID_FLOW))
            apply_layout = True
        if self.PROP_GRID_GAP in kw:
            self._gap = self._parse_gap(kw.pop(self.PROP_GRID_GAP))
            apply_layout = True
        if self.PROP_GRID_EXPAND in kw:
            self._grid_expand = bool(kw.pop(self.PROP_GRID_EXPAND))
            apply_layout = True
        if self.PROP_GRID_HSIZING in kw:
            self._cell_hsizing = Sizing(kw.pop(self.PROP_GRID_HSIZING))
            apply_layout = True
        if self.PROP_GRID_VSIZING in kw:
            self._cell_vsizing = Sizing(kw.pop(self.PROP_GRID_VSIZING))
            apply_layout = True
        if apply_layout:
            self.apply_layout()
        return super()._configure_set(**kw)

    def _configure_get(self, option):
        # Option information:
        # (argvName, dbName, dbClass, defValue, current value)
        if option == self.PROP_GRID_ANCHOR:
            return (self.PROP_GRID_ANCHOR, None, None, tk.Center, self._anchor)
        if option == self.PROP_GRID_ROWS:
            return (self.PROP_GRID_ROWS, None, None, -1, self._rows)
        elif option == self.PROP_GRID_COLS:
            return (self.PROP_GRID_COLS, None, None, -1, self._cols)
        elif option == self.PROP_GRID_PROPAGATE:
            return (
                self.PROP_GRID_PROPAGATE,
                None,
                None,
                True,
                bool(self.grid_propagate()),
            )
        elif option == self.PROP_GRID_FLOW:
            return (
                self.PROP_GRID_FLOW,
                None,
                None,
                False,
                self._flow,
            )
        elif option == self.PROP_GRID_GAP:
            return (self.PROP_GRID_GAP, None, None, (0, 0), self._gap)
        elif option == self.PROP_GRID_EXPAND:
            return (self.PROP_GRID_EXPAND, None, None, False, self._grid_expand)
        elif option == self.PROP_GRID_HSIZING:
            return (
                self.PROP_GRID_HSIZING,
                None,
                None,
                Sizing.SHRINK_CENTER,
                self._cell_hsizing,
            )
        elif option == self.PROP_GRID_VSIZING:
            return (
                self.PROP_GRID_VSIZING,
                None,
                None,
                Sizing.SHRINK_CENTER,
                self._cell_vsizing,
            )

        return super()._configure_get(option)

    # End WidgetConfigureMixin
    # </CLASS_BODY>


# <MODULE_BODY>
if __name__ == "__main__":
    root = tk.Tk()
    widget = GridFrame(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
# </MODULE_BODY>
