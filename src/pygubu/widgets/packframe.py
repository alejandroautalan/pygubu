#!/usr/bin/python3
"""
PackFrame

A container that arranges its child widgets horizontally or vertically.

Subclass of ttk.Frame and uses grid manager.


UI source file: packframe.ui
"""
# <MODULE_IMPORTS>
from enum import StrEnum, auto
from pygubu.utils.widget import WidgetConfigureMixin
from pygubu.widgets.gridframe import _FlexGrid, Alignment, Sizing, Direction

# </MODULE_IMPORTS>
import tkinter as tk
import tkinter.ttk as ttk


# <CLASS_DEFINITION>


class PackFrame(WidgetConfigureMixin, _FlexGrid):
    """Your widget direct subclass.

    Only simple properties will be configured.
    No commands, no bindings.
    """

    PROP_PACK_ALIGNMENT = "pack_alignment"
    PROP_PACK_DIRECTION = "pack_direction"
    PROP_PACK_GAP = "pack_gap"
    PROP_PACK_EXPAND = "pack_expand"
    PROP_PACK_HSIZING = "pack_chsizing"
    PROP_PACK_VSIZING = "pack_cvsizing"
    PROP_PACK_PROPAGATE = "pack_propagate"

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

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._pack_alignment: Alignment = (
            Alignment.BEGIN
        )  # ty: ignore[invalid-assignment]
        # </CLASS_DEFINITION>
        # widget setup
        self.configure(height=200, width=200)
        # Layout for 'frame1' skipped in custom widget template.
        # <CLASS_BODY>
        self.apply_layout()

    # WidgetConfigureMixin

    def _widget_cget(self, option):
        if option == self.PROP_PACK_GAP:
            return (
                self._gap[0] if self._flow == Direction.COLUMN else self._gap[1]
            )
        elif option == self.PROP_PACK_EXPAND:
            return self._grid_expand
        elif option == self.PROP_PACK_ALIGNMENT:
            return self._pack_alignment
        elif option == self.PROP_PACK_DIRECTION:
            return self._flow
        elif option == self.PROP_PACK_HSIZING:
            return self._cell_hsizing
        elif option == self.PROP_PACK_VSIZING:
            return self._cell_vsizing
        elif option == self.PROP_PACK_PROPAGATE:
            return bool(self.grid_propagate())
        return super()._widget_cget(option)

    def _configure_set(self, **kw):
        apply_layout = False
        if self.PROP_PACK_DIRECTION in kw:
            self._flow = Direction(kw.pop(self.PROP_PACK_DIRECTION))
            apply_layout = True
        if self.PROP_PACK_ALIGNMENT in kw:
            self._pack_alignment = Alignment(kw.pop(self.PROP_PACK_ALIGNMENT))
            self._anchor = self.ANCHOR_MAP[self._flow][self._pack_alignment]
            apply_layout = True
        if self.PROP_PACK_GAP in kw:
            gap = self._parse_gap(kw.pop(self.PROP_PACK_GAP))[0]
            self._gap = (0, gap)  # horizontal -> gap in cols
            if self._flow == Direction.COLUMN:
                self._gap = (gap, 0)  # vertical -> gap in rows
            apply_layout = True
        if self.PROP_PACK_EXPAND in kw:
            self._grid_expand = bool(kw.pop(self.PROP_PACK_EXPAND))
            apply_layout = True
        if self.PROP_PACK_HSIZING in kw:
            self._cell_hsizing = Sizing(kw.pop(self.PROP_PACK_HSIZING))
            apply_layout = True
        if self.PROP_PACK_VSIZING in kw:
            self._cell_vsizing = Sizing(kw.pop(self.PROP_PACK_VSIZING))
            apply_layout = True
        if self.PROP_PACK_PROPAGATE in kw:
            value = bool(kw.pop(self.PROP_PACK_PROPAGATE))
            self.grid_propagate(value)
        if apply_layout:
            self.apply_layout()
        return super()._configure_set(**kw)

    def _configure_get(self, option):
        if option == self.PROP_PACK_GAP:
            # Option information:
            # (argvName, dbName, dbClass, defValue, current value)
            return (
                self.PROP_PACK_GAP,
                None,
                None,
                0,
                (
                    self._gap[0]
                    if self._flow == Direction.COLUMN
                    else self._gap[1]
                ),
            )
        elif option == self.PROP_PACK_EXPAND:
            return (self.PROP_PACK_EXPAND, None, None, False, self._grid_expand)
        elif option == self.PROP_PACK_HSIZING:
            return (
                self.PROP_PACK_HSIZING,
                None,
                None,
                Sizing.SHRINK_CENTER,
                self._cell_hsizing,
            )
        elif option == self.PROP_PACK_HSIZING:
            return (
                self.PROP_PACK_VSIZING,
                None,
                None,
                Sizing.SHRINK_CENTER,
                self._cell_vsizing,
            )
        elif option == self.PROP_PACK_PROPAGATE:
            return (
                self.PROP_PACK_PROPAGATE,
                None,
                None,
                True,
                bool(self.grid_propagate()),
            )
        return super()._configure_get(option)

    # End WidgetConfigureMixin
    # </CLASS_BODY>


# <MODULE_BODY>
if __name__ == "__main__":
    root = tk.Tk()
    widget = PackFrame(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
# </MODULE_BODY>
