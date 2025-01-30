# encoding: utf-8
__all__ = ["ToolTip"]

import tkinter as tk
from contextlib import suppress


class TooltipBase:
    tipwindows = {}

    def __init__(self, widget: tk.Widget, /, text: str):
        self.widget = widget
        self.text = text
        self.x: int = 0
        self.y: int = 0
        self._bind_ids = (
            self.widget.bind("<Enter>", self.on_enter, add=True),
            self.widget.bind("<Leave>", self.on_leave, add=True),
        )

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
        label = tk.Label(tipwindow)
        label.pack(ipadx="2p")
        return label

    def _label_config(self, label, **kw):
        label.configure(text=self.text, **kw)

    def showtip(self):
        "Display text in tooltip window"
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


class Tooltip(TooltipBase):
    def __init__(
        self,
        widget: tk.Widget,
        /,
        text: str = None,
        font=None,
        background=None,
        foreground=None,
        justify=None,
        wraplength=None,
        relief=None,
    ):
        text = "undefined tooltip" if text is None else text
        self.font = ("tahoma", "9", "normal") if font is None else font
        self.background = "#ffffe0" if background is None else background
        self.foreground = "black" if foreground is None else foreground
        self.justify = tk.LEFT if justify is None else justify
        self.wraplength = "300p" if wraplength is None else wraplength
        self.relief = tk.SOLID if relief is None else relief
        super().__init__(widget, text=text)

    def _label_config(self, label, **kw):
        label.configure(
            text=self.text,
            font=self.font,
            background=self.background,
            foreground=self.foreground,
            wraplength=self.wraplength,
            justify=self.justify,
            relief=self.relief,
            borderwidth="1p",
        )


# Maintain old class name for now
ToolTip = Tooltip


def create(widget, text, **kw):
    """Creates a Tooltip using a tk.Label."""
    tooltip = Tooltip(widget, text, **kw)
    return tooltip


if __name__ == "__main__":
    root = tk.Tk()
    for idx in range(0, 2):
        b = tk.Button(root, text=f"Button({idx})")
        b.grid(pady="2p")
        text = f"A tooltip for button {idx}!!"
        create(b, text)

    root2 = tk.Tk()
    tip_options = dict(background="blue", foreground="white")
    for idx in range(0, 2):
        b = tk.Button(root2, text=f"Button({idx})")
        b.grid(pady="2p")
        text = f"A tooltip for button {idx}!!"
        create(b, text, **tip_options)

    root.mainloop()
