# encoding: utf8
from __future__ import unicode_literals

import calendar
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk


imgp_data = ('R0lGODlhDAAMAIABAAAAAP///yH+EUNyZWF0ZWQgd2l0aCBHSU1QACH5BAEK'
            +'AAEALAAAAAAMAAwAAAIVjI+JoMsdgIRyqmoTfrfCmDWh+DUFADs=')
imgn_data = ('R0lGODlhDAAMAIABAAAAAP///yH+EUNyZWF0ZWQgd2l0aCBHSU1QACH5BAEK'
            +'AAEALAAAAAAMAAwAAAIUjI8ZoAnczINtUmdrVpu/uFwcSBYAOw==')

def get_calendar(locale, fwday):
    # instantiate proper calendar class
    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)

def i2rc(i, coldim):
    c = i % coldim
    f = (i - c) // coldim
    return (f, c)

def rowmajor(rows, cols):
    size = rows * cols
    for i in range(0, size):
        c = i % cols
        f = (i - c) // cols
        yield (i, f, c)

def matrix_coords(rows, cols, rowh, colw, ox=0, oy=0):
    "Generate coords for a matrix of rects"
    for i, f, c in rowmajor(rows, cols):
        x = ox + c * colw
        y = oy + f * rowh
        x1 = x + colw
        y1 = y + rowh
        yield (i, x, y, x1, y1)


class CalendarFrame(ttk.Frame):
    """ Allows to choose a file or directory.
    
    Generates:
        <<CalendarDaySelected>>
        <<CalendarMonthChanged>>
        <<CalendarYearChanged>>
    
    """
    datetime = calendar.datetime.datetime
    timedelta = calendar.datetime.timedelta

    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        
        self._sel_bg = '#ecffc4'
        self._sel_fg = '#05640e'
        
        self.__cb = None
        #calendar variables
        year = 2015
        month = 9
        self._date = self.datetime(year, month, 1)
        self._cal = get_calendar(None, calendar.MONDAY)
        self._weeks = self._cal.monthdayscalendar(year, month)
        
        #Canvas variables
        self._rheader = None
        self._theader = [ 0 for x in range(0, 7)]
        self._recmat = [ 0 for x in rowmajor(6, 7) ]
        self._txtmat = [0 for x in rowmajor(6, 7) ]
        self._selected_day_idx = None
        
        #build ui
        self.__build_ui()
    
    def __build_ui(self):
        # BUILD UI
        # mainframe widget
        mainframe = self
        mainframe.configure(width='200', height='200', padding='2')
        # frame2 widget
        frame2 = ttk.Frame(mainframe)
        frame2.configure(width='200', height='200')
        # bpmonth widget
        bpmonth = ttk.Button(frame2)
        bpmonth.configure(style='Toolbutton', width='2', text='L')
        bpmonth.grid(column='0', row='0')
        bpmonth.propagate(True)
        # lmonth widget
        lmonth = ttk.Label(frame2)
        lmonth.configure(anchor='center', text='Enero')
        lmonth.grid(ipadx='5', row='0', column='1', sticky='ew')
        lmonth.propagate(True)
        # bnmonth widget
        bnmonth = ttk.Button(frame2)
        bnmonth.configure(style='Toolbutton', width='2', text='R')
        bnmonth.grid(column='2', row='0')
        bnmonth.propagate(True)
        # bpyear widget
        bpyear = ttk.Button(frame2)
        bpyear.configure(style='Toolbutton', width='2', text='L')
        bpyear.grid(padx='5', column='4', row='0')
        bpyear.propagate(True)
        # lyear widget
        lyear = ttk.Label(frame2)
        lyear.configure(anchor='center', text='2015')
        lyear.grid(ipadx='5', row='0', column='5', sticky='ew')
        lyear.propagate(True)
        # bnyear widget
        bnyear = ttk.Button(frame2)
        bnyear.configure(style='Toolbutton', width='2', text='R')
        bnyear.grid(column='6', row='0')
        bnyear.propagate(True)
        frame2.grid(row='0', column='0', sticky='ew')
        frame2.propagate(True)
        frame2.columnconfigure(3, minsize='20', weight='1')
        # canvas widget
        canvas = tk.Canvas(mainframe)
        canvas.configure(highlightthickness='0', borderwidth='0', background='#ffffff', height='180')
        canvas.configure(width='260')
        canvas.grid(row='1', column='0', sticky='nsew')
        canvas.propagate(True)
        mainframe.grid(row='0', column='0', sticky='nsew')
        mainframe.propagate(True)
        mainframe.rowconfigure(1, weight='1')
        mainframe.rowconfigure(0, weight='0')
        mainframe.columnconfigure(0, weight='1')
        
        self.__img_prev = imgp = tk.PhotoImage(data=imgp_data)
        self.__img_next = imgn = tk.PhotoImage(data=imgn_data)
        bpmonth.configure(image=imgp)
        bnmonth.configure(image=imgn)
        bpyear.configure(image=imgp)
        bnyear.configure(image=imgn)
        canvas.bind('<Configure>', self._on_canvas_configure)
        self._canvas = canvas
        self._draw_canvas(canvas)
        self._canvas.tag_bind('cell', '<Button-1>', self._on_cell_clicked)
        
    def _on_cell_clicked(self, event=None):
        if self._selected_day_idx is not None:
            self._draw_day(self._selected_day_idx, marked=False)
        item = self._canvas.find_withtag('current')
        idx = self._recmat.index(item[0])

        weeks = self._weeks
        day = 0
        f, c = i2rc(idx, 7)
        if f < len(weeks):
            day = weeks[f][c]
        if day != 0:
            self._selected_day_idx = idx
            self._draw_day(idx)
    
    def _draw_day(self, idx, marked=True):
        if marked:
            self._canvas.itemconfigure(self._recmat[idx], fill=self._sel_bg)
            self._canvas.itemconfigure(self._txtmat[idx], fill=self._sel_fg)
        else:
            self._canvas.itemconfigure(self._recmat[idx], fill='white')
            self._canvas.itemconfigure(self._txtmat[idx], fill='black')

    def _draw_canvas(self, canvas, redraw=False):
        ch = canvas.winfo_height()
        cw = canvas.winfo_width()
        rowh = ch / 7.0
        colw = cw / 7.0
        # Header
        if self._rheader is None:
            self._rheader = canvas.create_rectangle(0, 0, cw, rowh, width=0,
                                                    fill='grey90')
        else:
            canvas.coords(self._rheader, 0, 0, cw, rowh)
        ox = 0
        oy = rowh / 2.0
        coffset = colw / 2.0
        cols = self._cal.formatweekheader(3).split()
        for i in range(0, 7):
            x = ox + i * colw + coffset
            if redraw:
                item = self._theader[i]
                canvas.coords(item, x, oy)
                canvas.itemconfigure(item, text=cols[i])
            else:
                self._theader[i] = canvas.create_text(x, oy, text=cols[i])
        
        # background matrix
        oy = rowh
        ox = 0
        for i, x, y, x1, y1 in matrix_coords(6, 7, rowh, colw, ox, oy):
            x1 -= 1
            y1 -= 1
            if redraw:
                rec = self._recmat[i]
                canvas.coords(rec, x, y, x1, y1)
            else:
                rec = canvas.create_rectangle(x, y, x1, y1, width=1,
                                          fill='white', outline='white',
                                          activeoutline='blue',
                                          activewidth=1, tags='cell')
                self._recmat[i] = rec
        
        # text matrix
        weeks = self._weeks
        xoffset = colw / 2.0
        yoffset = rowh / 2.0
        oy = rowh
        ox = 0
        for i, x, y, x1, y1 in matrix_coords(6, 7, rowh, colw, ox, oy):
            x += coffset
            y += yoffset
            # day text
            txt = ""
            f, c = i2rc(i, 7)
            if f < len(weeks):
                day = weeks[f][c]
                txt = "{0}".format(day) if day != 0 else ""
            if redraw:
                item = self._txtmat[i]
                canvas.coords(item, x, y)
                canvas.itemconfigure(item, text=txt)
            else:
                self._txtmat[i] = canvas.create_text(x, y, text=txt,
                                                     state=tk.DISABLED)
    
    def _redraw(self):
        self._draw_canvas(self._canvas, redraw=True)
        # after idle callback trick
        self.__cb = None
    
    def _on_canvas_configure(self, event=None):
        print('on_canvas_configure')
        if self.__cb is None:
            self.__cb = self.after_idle(self._redraw)

    def configure(self, cnf=None, **kw):
        args = tk._cnfmerge((cnf, kw))
        key = 'type'
        if key in args:
            self._choose = args[key]
            del args[key]
        ttk.Frame.configure(self, args)

    config = configure

    def cget(self, key):
        option = 'type'
        if key == option:
            return self._choose
        return ttk.Frame.cget(self, key)
        
    def mark_day():
        pass
    
    def unmark_day():
        pass

if __name__ == '__main__':
    root = tk.Tk()
    c = CalendarFrame(root)
    c.grid()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
