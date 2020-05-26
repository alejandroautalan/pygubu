# encoding: utf8
__all__ = ['ToolTip']

try:
    import tkinter as tk
    from tkinter import ttk
except:
    import Tkinter as tk
    import ttk


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
    
    def inside_wbbox(self, rx , ry):
        bbox = self._calc_bbox(self.widget, True)
        inside = False
        if (bbox[0] <= rx <= bbox[2]) and (bbox[1] <= ry <= bbox[3]):
            inside = True
        return inside
        
    def _calc_bbox(self, widget, screen=False):
        rx = widget.winfo_x()
        ry = widget.winfo_y()
        if screen:
            rx = widget.winfo_rootx()
            ry = widget.winfo_rooty()
        x2 = rx + widget.winfo_width()
        y2 = ry + widget.winfo_height()
        return (rx, ry, x2, y2)
    
    def _calc_final_pos(self):
        rx, ry, rcx, rcy = self._calc_bbox(self.widget, True)
        w = rcx-rx
        h = rcy-ry
        sh = self.widget.winfo_screenheight() - 10
        sw = self.widget.winfo_screenwidth() - 10
        x = y = 0
        for region in ('bottom', 'right', 'top', 'left'):
            if region == 'bottom':
                x = rx + int(w//2 * 0.2)
                y = rcy + int(h//2 * 0.1)
            elif region == 'right':
                x = rcx + int(w//2 * 0.2)
                y = ry + int(h//2 * 0.1)
            elif region == 'top':
                x = rx - int(w//2 * 0.4)
                y = ry - int(h//2 * 0.4)
            elif region == 'left':
                x = rx
                y = ry - 20
            if x < sw and y < sh:
                break
        return (x, y)

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y = self._calc_final_pos()
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+{0}+{1}".format(x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except tk.TclError:
            pass
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", foreground="black",
                      relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "9", "normal"))
        label.pack(ipadx=2)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def create(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


if __name__ == '__main__':
    root = tk.Tk()
    for idx in range(0, 2):
        b = tk.Button(root, text='A button')
        b.grid()
        create(b, 'A tooltip !!')
    root.mainloop()
