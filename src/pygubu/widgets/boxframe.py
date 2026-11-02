#!/usr/bin/python3
"""
BoxFrame

A container that arranges its child widgets horizontally or vertically.

Subclass of ttk.Frame and uses pack manager.


UI source file: boxcontainer.ui
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


class BoxFrame(WidgetConfigureMixin, ttk.Frame):
    """Your widget direct subclass.

    Only simple properties will be configured.
    No commands, no bindings.
    """

    PROP_BOX_ALIGNMENT = "box_alignment"
    PROP_BOX_DIRECTION = "box_direction"
    PROP_BOX_GAP = "box_gap"
    PROP_BOX_EXPAND = "box_expand"
    PROP_BOX_HSIZING = "box_hsizing"
    PROP_BOX_VSIZING = "box_vsizing"

    ANCHOR_MAP = {
        Direction.ROW: {  # Horizontal
            Alignment.BEGIN: tk.W,
            Alignment.CENTER: tk.CENTER,
            Alignment.END: tk.E,
        },
        Direction.COLUMN: {  # Vertical
            Alignment.BEGIN: tk.N,
            Alignment.CENTER: tk.CENTER,
            Alignment.END: tk.S,
        },
    }

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

    def __init__(self, *args, box_direction=Direction.ROW, **kw):
        super().__init__(*args, **kw)
        self._box_alignment: Alignment = (
            Alignment.BEGIN
        )  # ty: ignore[invalid-assignment]
        self._box_gap = 0
        self._box_expand = False
        self._box_hsizing = Sizing.SHRINK_CENTER
        self._box_vsizing = Sizing.SHRINK_CENTER
        self._box_direction = box_direction
        self.ordering = []
        self._layout_cbid = None
        # </CLASS_DEFINITION>
        # widget setup
        self.configure(height=100, width=100)
        # Layout for 'frame1' skipped in custom widget template.

    # <CLASS_BODY>

    # WidgetConfigureMixin

    def _widget_cget(self, option):
        if option == self.PROP_BOX_GAP:
            return self._box_gap
        elif option == self.PROP_BOX_EXPAND:
            return self._box_expand
        elif option == self.PROP_BOX_ALIGNMENT:
            return self._box_alignment
        elif option == self.PROP_BOX_DIRECTION:
            return self._box_direction
        elif option == self.PROP_BOX_HSIZING:
            return self._box_hsizing
        elif option == self.PROP_BOX_VSIZING:
            return self._box_vsizing
        return super()._widget_cget(option)

    def _configure_set(self, **kw):
        apply_layout = False
        if self.PROP_BOX_ALIGNMENT in kw:
            self._box_alignment = Alignment(kw.pop(self.PROP_BOX_ALIGNMENT))
            apply_layout = True
        if self.PROP_BOX_DIRECTION in kw:
            self._box_direction = Direction(kw.pop(self.PROP_BOX_DIRECTION))
            apply_layout = True
        if self.PROP_BOX_GAP in kw:
            self._box_gap = kw.pop(self.PROP_BOX_GAP)
            apply_layout = True
        if self.PROP_BOX_EXPAND in kw:
            self._box_expand = bool(kw.pop(self.PROP_BOX_EXPAND))
            apply_layout = True
        if self.PROP_BOX_HSIZING in kw:
            self._box_hsizing = Sizing(kw.pop(self.PROP_BOX_HSIZING))
            apply_layout = True
        if self.PROP_BOX_VSIZING in kw:
            self._box_vsizing = Sizing(kw.pop(self.PROP_BOX_VSIZING))
            apply_layout = True
        if apply_layout:
            self._schedule_layout()
        return super()._configure_set(**kw)

    def _configure_get(self, option):
        if option == self.PROP_BOX_GAP:
            # Option information:
            # (argvName, dbName, dbClass, defValue, current value)
            return (self.PROP_BOX_GAP, None, None, 0, self._box_gap)
        elif option == self.PROP_BOX_EXPAND:
            return (self.PROP_BOX_EXPAND, None, None, False, self._box_expand)
        elif option == self.PROP_BOX_HSIZING:
            return (
                self.PROP_BOX_HSIZING,
                None,
                None,
                Sizing.SHRINK_CENTER,
                self._box_hsizing,
            )
        elif option == self.PROP_BOX_HSIZING:
            return (
                self.PROP_BOX_VSIZING,
                None,
                None,
                Sizing.SHRINK_CENTER,
                self._box_vsizing,
            )
        return super()._configure_get(option)

    # End WidgetConfigureMixin

    def _apply_layout(self):
        widgets = self.ordering.copy()

        for child in widgets:
            child.grid_forget()

        grid_anchor = self.ANCHOR_MAP[self._box_direction][self._box_alignment]

        # default horizontal
        gap = self._box_gap if self._box_gap else 0
        child_padx = gap
        child_pady = 0
        direction = "column"  # In grid terms (horizontal: increment columns)

        sticky = (
            self.STICKY_HMAP[self._box_hsizing]
            + self.STICKY_VMAP[self._box_vsizing]
        )
        child_grid = dict(
            column=0,
            row=0,
            padx=0,
            pady=0,
            sticky=sticky,
        )

        if self._box_direction == Direction.COLUMN:
            child_padx = 0
            child_pady = gap
            direction = "row"
        skip_indexes = (len(widgets) - 1,)
        gap_none = (0, 0)
        gap_x = (0, child_padx)
        gap_y = (0, child_pady)
        for index, child in enumerate(widgets):
            padx = gap_x
            pady = gap_y
            if index in skip_indexes:
                padx = gap_none
                pady = gap_none
            child_grid[direction] = index
            child_grid["padx"] = padx
            child_grid["pady"] = pady
            child.grid(**child_grid)
        if self._box_expand:
            self.rowconfigure("all", weight=1)
            self.columnconfigure("all", weight=1)

        self.grid_anchor(grid_anchor)
        self._layout_cbid = None

    def _schedule_layout(self):
        if self._layout_cbid is not None:
            self.after_cancel(self._layout_cbid)
        self._layout_cbid = self.after(10, self._apply_layout)

    def child_add(self, widget):
        self.ordering.append(widget)
        self._schedule_layout()

    # </CLASS_BODY>


# <MODULE_BODY>
if __name__ == "__main__":
    root = tk.Tk()
    widget = BoxFrame(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
# </MODULE_BODY>
