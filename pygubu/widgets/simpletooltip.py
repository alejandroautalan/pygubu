# encoding: utf8
__all__ = ['ToolTip']

try:
    import tkinter as tk
    from tkinter import ttk
except:
    import Tkinter as tk
    import ttk


class ToolTip(object):

    def __init__(self, widget, text=None, font=None,
                background=None, foreground=None,
                justify=None, wraplength=None):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.text = text if text is not None else '¿?'
        self.font = font if font is not None else ("tahoma", "9", "normal")
        self.background = background if background is not None else "#ffffe0"
        self.foreground = foreground if foreground is not None else "black"
        self.justify = justify if justify is not None else tk.LEFT
        self.wraplength = wraplength if wraplength is not None else 300
    
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
    
    def _calc_final_pos(self, ttwidth, ttheight):
        rx, ry, rcx, rcy = self._calc_bbox(self.widget, True)
        w = rcx-rx
        h = rcy-ry
        sh = self.widget.winfo_screenheight()
        sw = self.widget.winfo_screenwidth()
        x = y = 0
        #final_region = None
        regions = ('se-al','se-ar', 'sw-al', 'sw-ar',
                   'nw-al', 'nw-ar', 'ne-al', 'ne-ar')
        for region in regions:
            if region == 'ne-al':
                x = rx
                y = ry - ttheight
            elif region == 'ne-ar':
                x = rx - ttwidth
                y = ry - ttheight
            elif region == 'nw-al':
                x = rx + w
                y = ry - ttheight
            elif region == 'nw-ar':
                x = rx + w - ttwidth
                y = ry - ttheight
            elif region == 'se-al':
                x = rx
                y = ry + h
            elif region == 'se-ar':
                x = rx - ttwidth
                y = ry + h
            elif region == 'sw-al':
                x = rx + w
                y = ry + h
            elif region == 'sw-ar':
                x = rx + w - ttwidth
                y = ry + h
            x2 = x + ttwidth
            y2 = y + ttheight
            if (x > 0 and x2 < sw) and (y > 0 and y2 < sh):
                #final_region = region
                break
        #print(final_region, x, x2, y, y2)
        return (x, y)

    def showtip(self):
        "Display text in tooltip window"
        if self.tipwindow or not self.text:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except tk.TclError:
            pass
        label = tk.Label(tw, text=self.text, justify=self.justify,
                      background=self.background, foreground=self.foreground,
                      relief=tk.SOLID, borderwidth=1,
                      font=self.font, wraplength=self.wraplength)
        label.pack(ipadx=2)
        x, y = self._calc_final_pos(
            label.winfo_reqwidth(), label.winfo_reqheight())
        tw.wm_geometry("+{0}+{1}".format(x, y))

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def create(widget, text):
    toolTip = ToolTip(widget, text)
    def enter(event):
        toolTip.showtip()
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    return toolTip


if __name__ == '__main__':
    root = tk.Tk()
    for idx in range(0, 2):
        b = tk.Button(root, text='A button')
        b.grid()
        create(b, 'A tooltip !!')
    root.mainloop()
