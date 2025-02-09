# encoding: utf-8
__all__ = ["ToolTip"]

import tkinter as tk
import tkinter.ttk as ttk
from contextlib import suppress


class TooltipBase:
    """Base class for tooltips using a Label widget."""

    tipwindows = {}
    label_class = tk.Label

    def __init__(self, widget: tk.Widget, /, **label_options):
        self.widget = widget
        self.x: int = 0
        self.y: int = 0
        self.label_options: dict = label_options
        self._bind_ids = (
            self.widget.bind("<Enter>", self.on_enter, add=True),
            self.widget.bind("<Leave>", self.on_leave, add=True),
        )
        # save reference for simple acces from wiget
        widget.stooltip = self

    # Add text property to mantain backward comatibility?
    @property
    def text(self):
        return self.label_options.get("text", "")

    @text.setter
    def text(self, value):
        self.label_options["text"] = value

    def inside_wbbox(self, rx, ry):
        bbox = self._calc_bbox(self.widget, True)
        inside = False
        if (bbox[0] <= rx <= bbox[2]) and (bbox[1] <= ry <= bbox[3]):
            inside = True
        return inside

    def _calc_bbox(self, widget: tk.Widget, screen=False):
        rx = widget.winfo_x()
        ry = widget.winfo_y()
        if screen:
            rx = widget.winfo_rootx()
            ry = widget.winfo_rooty()
        x2 = rx + widget.winfo_width()
        y2 = ry + widget.winfo_height()
        return (rx, ry, x2, y2)

    def _calc_final_pos(self, ttwidth, ttheight):
        rx, ry, rcx, rcy = self._calc_bbox(self.widget, True)
        w = rcx - rx
        h = rcy - ry
        sh = self.widget.winfo_screenheight()
        sw = self.widget.winfo_screenwidth()
        x = y = 0
        # final_region = None
        regions = (
            "se-al",
            "se-ar",
            "sw-al",
            "sw-ar",
            "nw-al",
            "nw-ar",
            "ne-al",
            "ne-ar",
        )
        for region in regions:
            if region == "ne-al":
                x = rx
                y = ry - ttheight
            elif region == "ne-ar":
                x = rx - ttwidth
                y = ry - ttheight
            elif region == "nw-al":
                x = rx + w
                y = ry - ttheight
            elif region == "nw-ar":
                x = rx + w - ttwidth
                y = ry - ttheight
            elif region == "se-al":
                x = rx
                y = ry + h
            elif region == "se-ar":
                x = rx - ttwidth
                y = ry + h
            elif region == "sw-al":
                x = rx + w
                y = ry + h
            elif region == "sw-ar":
                x = rx + w - ttwidth
                y = ry + h
            x2 = x + ttwidth
            y2 = y + ttheight
            if (x > 0 and x2 < sw) and (y > 0 and y2 < sh):
                # final_region = region
                break
        # print(final_region, x, x2, y, y2)
        return (x, y)

    def on_enter(self, event):
        self.showtip()

    def on_leave(self, event):
        self.hidetip()

    def __del__(self):
        with suppress(tk.TclError):
            if self.widget.winfo_exists():
                self.widget.unbind("<Enter>", self._bind_ids[0])
                self.widget.unbind("<Leave>", self._bind_ids[1])

    def _tipwindow_for(self, widget: tk.Widget) -> tk.Toplevel:
        root = widget.winfo_toplevel()
        root_id = id(root)
        tipwindow = self.tipwindows.get(root_id, None)
        if tipwindow is None:
            tipwindow = tk.Toplevel(root)
            tipwindow.wm_overrideredirect(1)
            with suppress(tk.TclError):
                # For Mac OS
                tipwindow.tk.call(
                    "::tk::unsupported::MacWindowStyle",
                    "style",
                    tipwindow._w,
                    "help",
                    "noActivates",
                )
            tipwindow.label = self._label_create(tipwindow)
            self.tipwindows[root_id] = tipwindow
        return tipwindow

    def _label_create(self, tipwindow: tk.Toplevel) -> tk.Widget:
        label = self.label_class(tipwindow)
        label.pack(expand=True, fill=tk.BOTH)
        return label

    def _label_config(self, label):
        label.configure(**self.label_options)

    def showtip(self):
        """Display text in tooltip window"""
        tipwindow = self._tipwindow_for(self.widget)
        label = tipwindow.label
        self._label_config(label)
        x, y = self._calc_final_pos(
            label.winfo_reqwidth(), label.winfo_reqheight()
        )
        tipwindow.wm_geometry(f"+{x}+{y}")
        tipwindow.deiconify()

    def hidetip(self):
        tipwindow = self._tipwindow_for(self.widget)
        tipwindow.withdraw()

    def configure(self, **kw):
        """Updates label options.
        Similar to configure method of tk widgets.
        """
        self.label_options.update(kw)


class Tooltip(TooltipBase):
    """A simple tooltip class based on tk.Label"""

    default_config = dict(
        text="undefined tooltip",
        font=("tahoma", "9", "normal"),
        background="#ffffe0",
        foreground="black",
        justify=tk.LEFT,
        wraplength="300p",
        relief=tk.SOLID,
        borderwidth="1p",
        padx="2p",
        pady="2p",
    )

    def __init__(self, widget: tk.Widget, /, **label_options):
        options = self.default_config.copy()
        options.update(label_options)
        super().__init__(widget, **options)


# Maintain old class name for now
ToolTip = Tooltip


class Tooltipttk(TooltipBase):
    """A simple tooltip class based on ttk.Label"""

    STYLE_NAME = "Tooltipttk.TLabel"
    STYLE_OPTIONS = dict()
    tipwindows = {}
    label_class = ttk.Label
    default_config = dict(style=STYLE_NAME)
    clear_config = dict(
        text="",
        font="",
        foreground="",
        background="",
        justify="left",
        wraplength="",
        relief="",
        borderwidth="",
        style=STYLE_NAME,
    )

    def __init__(self, widget: tk.Widget, /, **label_options):
        options = self.default_config.copy()
        options.update(label_options)
        super().__init__(widget, **options)

    def _label_config(self, label):
        label.configure(**self.clear_config)
        label.configure(**self.label_options)


def create(widget, text, **label_options):
    """Creates a Tooltip using a tk.Label."""
    label_options["text"] = text
    tooltip = Tooltip(widget, **label_options)
    return tooltip


def create_ttk(widget, text, **label_options):
    """Creates a Tooltip using a ttk.Label."""
    label_options["text"] = text
    tooltip = Tooltipttk(widget, **label_options)
    return tooltip


if __name__ == "__main__":

    def build_test(root, tk_options: dict = None, ttk_options: dict = None):
        tk_options = {} if tk_options is None else tk_options
        ttk_options = {} if ttk_options is None else ttk_options

        for idx in range(0, 2):
            b = tk.Button(root, text=f"Button({idx})")
            b.pack(pady="2p")
            text = f"A tooltip for button {idx}!!"
            create(b, text, **tk_options)

        for idx in range(2, 4):
            b = ttk.Button(root, text=f"Button({idx})")
            b.pack(pady="2p")
            text = f"A ttk tooltip for button {idx}!!"
            create_ttk(b, text, **ttk_options)

    root = tk.Tk()
    root.title("Root 1")
    root.minsize(300, 200)
    tk_options = {}  # dict(background="darkgreen", foreground="white")
    ttk_options = {}
    build_test(root)

    root2 = tk.Tk()
    root2.title("Root 2")
    root2.minsize(300, 200)

    s = ttk.Style(root2)
    s.configure(Tooltipttk.STYLE_NAME, foreground="white", background="red")
    ttk_options = dict()

    tk_options = dict(background="blue", foreground="white")
    build_test(root2, tk_options)

    root.mainloop()
