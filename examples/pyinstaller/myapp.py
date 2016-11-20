#file: myapp.py
import sys
import os
import random
import math

try:
    import Tkinter as tk
    import ttk
    import tkMessageBox as tkmb
    tk.messagebox = tkmb
except:
    import tkinter as tk
    import tkinter.messagebox
    import tkinter.ttk as ttk

import pygubu


try:
    DATA_DIR = os.path.abspath(os.path.dirname(__file__))
except NameError:
    DATA_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

DEG2RAD = 4 * math.atan(1) * 2 / 360


class MyApplication:

    def __init__(self):
        self.about_dialog = None
        
        self.builder = b = pygubu.Builder()
        b.add_from_file(os.path.join(DATA_DIR, 'myapp.ui'))
        b.add_resource_path(os.path.join(DATA_DIR, 'imgs'))
        
        self.mainwindow = b.get_object('mainwindow')
        self.mainmenu = b.get_object('mainmenu', self.mainwindow)
        self.btn_menu = b.get_object('btn_menu')
        #self.mainwindow['menu'] = menu
        self.canvas = b.get_object('main_canvas')
        
        # Connect to Delete event
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.quit)
        
        b.connect_callbacks(self)

    def on_mainmenu_action(self, option_id=None):
        if option_id == 'mm_clear':
            self.canvas.delete('all')
        if option_id == 'mm_about':
            self.show_about_dialog()
        if option_id == 'mm_quit':
            self.mainwindow.quit()
    
    def btn_menu_clicked(self):
        # this is ugly but I don't want to use menubutton :(
        x, y = (self.btn_menu.winfo_rootx(), self.btn_menu.winfo_rooty())
        y = y + self.btn_menu.winfo_height()
        try:
            self.mainmenu.tk_popup(x, y, '')
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.mainmenu.grab_release()
    
    def show_about_dialog(self):
        if self.about_dialog is None:
            dialog = self.builder.get_object('dlg_about', self.mainwindow)
            self.about_dialog = dialog
            
            def dialog_btnclose_clicked():
                dialog.close()
            
            btnclose = self.builder.get_object('about_btnclose')
            btnclose['command'] = dialog_btnclose_clicked
            
            dialog.run()
        else:
            self.about_dialog.show()
    
    def btn_square_clicked(self):
        self._draw_figure('square')
    
    def btn_cross_clicked(self):
        self._draw_figure('cross')
        
    def btn_circle_clicked(self):
        self._draw_figure('circle')
        
    def btn_triangle_clicked(self):
        self._draw_figure('triangle')
        
    def quit(self, event=None):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()
    
    def _draw_figure(self, figure):
        canvas = self.canvas
        max_iterations = random.randint(3, 10)
        
        for i in range(0, max_iterations):
            canvasw = canvas.winfo_width()
            canvash = canvas.winfo_height()
            borderw = random.randint(1, 5)
            max_width = int(canvas.winfo_width()*0.25)
            w = random.randint(20, max_width)
            x = random.randint(0, canvasw) - int(max_width * 0.5)
            y = random.randint(0, canvash) - int(max_width * 0.5)
            start = random.randint(0, 180)
            
            if figure == 'circle':
                canvas.create_oval(x, y, x+w, y+w, outline='#FF6666', width=borderw)
            if figure == 'square':
                self.create_regpoly(x, y, x+w, y+w,
                                    sides=4, start=start,
                                    outline='#ED9DE9', width=borderw, fill='')
            if figure == 'triangle':
                self.create_regpoly(x, y, x+w, y+w,
                                    sides=3, start=start,
                                    outline='#40E2A0', width=borderw, fill='')
            if figure == 'cross':
                self.create_regpoly(x, y, x+w, y+w,
                                    sides=2, start=start,
                                    outline='#80B3E7', width=borderw, fill='')
                self.create_regpoly(x, y, x+w, y+w,
                                    sides=2, start=start+90,
                                    outline='#80B3E7', width=borderw, fill='')
                
    def create_regpoly(self, x0, y0, x1, y1, sides=0, start=90, extent=360, **kw):
        """Create a regular polygon"""
        coords = self.__regpoly_coords(x0, y0, x1, y1, sides, start, extent)
        return self.canvas.create_polygon(*coords, **kw)

    def __regpoly_coords(self, x0, y0, x1, y1, sides, start, extent):
        """Create the coordinates of the regular polygon specified"""

        coords = []
        if extent == 0:
            return coords

        xm = (x0 + x1) / 2.
        ym = (y0 + y1) / 2.
        rx = xm - x0
        ry = ym - y0

        n = sides
        if n == 0: # 0 sides => circle
            n = round((rx + ry) * .5)
            if n < 2:
                n = 4

        # Extent can be negative
        dirv = 1 if extent > 0 else -1
        if abs(extent) > 360:
            extent = dirv * abs(extent) % 360

        step = dirv * 360 / n
        numsteps = 1 + extent / float(step)
        numsteps_int = int(numsteps)

        i = 0
        while i < numsteps_int:
            rad = (start - i * step) * DEG2RAD
            x = rx * math.cos(rad)
            y = ry * math.sin(rad)
            coords.append((xm+x, ym-y))
            i += 1

        # Figure out where last segment should end
        if numsteps != numsteps_int:
            # Vecter V1 is last drawn vertext (x,y) from above
            # Vector V2 is the edge of the polygon
            rad2 = (start - numsteps_int * step) * DEG2RAD
            x2 = rx * math.cos(rad2) - x
            y2 = ry * math.sin(rad2) - y

            # Vector V3 is unit vector in direction we end at
            rad3 = (start - extent) * DEG2RAD
            x3 = math.cos(rad3)
            y3 = math.sin(rad3)

            # Find where V3 crosses V1+V2 => find j s.t.  V1 + kV2 = jV3
            j = (x*y2 - x2*y) / (x3*y2 - x2*y3)

            coords.append((xm + j * x3, ym - j * y3))

        return coords


if __name__ == '__main__':
    app = MyApplication()
    app.run();

