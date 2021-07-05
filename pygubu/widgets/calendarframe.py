# encoding: utf8
from __future__ import unicode_literals

__all__ = ['CalendarFrame']

import locale
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
    """ Allows to choose a date in a calendar.
    
    WIDGET-SPECIFIC OPTIONS
            locale, firstweekday, year, month
            calendarfg, calendarbg,
            headerfg, headerbg,
            selectbg, selectfg,
            markbg, markfg,
    Generates:
        <<CalendarFrameDateSelected>>
    """
    datetime = calendar.datetime.datetime
    timedelta = calendar.datetime.timedelta

    def __init__(self, master=None, **kw):
        self.__redraw_cb = None  # For redraw callback check.
        self.__markdays_cb = None  # For markdays callback check.

        sysloc = locale.getlocale(locale.LC_TIME)
        if None in sysloc:
            sysloc = None
        else:
            sysloc = '{0}.{1}'.format(*sysloc)

        self.__options = options = {
            'firstweekday': calendar.SUNDAY,
            'year': self.datetime.now().year,
            'month': self.datetime.now().month,
            'locale': sysloc,
            'calendarfg': 'black',
            'calendarbg': 'white',
            'headerfg': 'black',            
            'headerbg': 'grey90',
            'selectbg': '#8000FF',
            'selectfg': 'white',
            'state': 'normal',
            'markbg': 'white',
            'markfg': 'blue',
        }
        # remove custom options from kw before initialization ttk.Frame
        for k, v in options.items():
            options[k] = kw.pop(k, v)

        # Marked days
        self._marked_days = set()
        # Calendar variables
        self._date = self.datetime(options['year'], options['month'], 1)
        self._cal = get_calendar(options['locale'], options['firstweekday'])
        self._weeks = self._cal.monthdayscalendar(options['year'],
                                                  options['month'])
        self._selection = None
        
        # Canvas variables
        self._rheader = None
        self._theader = [ 0 for x in range(0, 7)]
        self._recmat = [ 0 for x in rowmajor(6, 7) ]
        self._txtmat = [0 for x in rowmajor(6, 7) ]
        
        # button bar variables
        self.__img_prev = None
        self.__img_next = None
        self._lmonth = None
        self._lyear = None

        ttk.Frame.__init__(self, master, **kw)
        
        #build ui
        self.__build_ui()
    
    def configure(self, cnf=None, **kw):
        args = tk._cnfmerge((cnf, kw))
        color_change = False
        for key in ('calendarfg', 'calendarbg', 'headerfg', 'headerbg',
                    'selectbg', 'selectfg', 'markbg', 'markfg'):
            if key in args:
                self.__options[key] = args.pop(key)
                color_change = True
        key = 'state'
        if key in args:
            value = args.pop(key)
            self.__options[key] = value
            self._canvas.config(state=value)
            for w in self._topframe.winfo_children():
                if w.winfo_class() == 'TButton':
                    w.config(state=value)
        
        calendar_change = False
        key = 'locale'
        if key in args:
            value = locale.normalize(args.pop(key))
            self.__options[key] = value
            calendar_change = True
        key = 'firstweekday'
        if key in args:
            value = args.pop(key)
            self.__options[key] = int(value)
            calendar_change = True
        if calendar_change:
            self._reconfigure_calendar()
        
        date_change = False
        for key in ('year', 'month'):
            if key in args:
                self.__options[key] = int(args.pop(key))
                date_change = True
        if date_change:
            self._reconfigure_date()
        
        if color_change or calendar_change or date_change:
            self._redraw_calendar()
        ttk.Frame.configure(self, args)

    config = configure

    def cget(self, key):
        if key in ('locale', 'firstweekday', 'calendarfg', 'calendarbg',
                   'headerfg', 'headerbg', 'selectbg', 'selectfg',
                   'markbg', 'markfg', 'state'):
            return self.__options[key]
        option = 'year'
        if key == option:
            return self._date.year
        option = 'month'
        if key == option:
            return self._date.month
        return ttk.Frame.cget(self, key)
    
    __getitem__ = cget
    
    def __build_ui(self):
        ## BUILD UI
        
        self.configure(height='200', width='200')
        self._topframe = ttk.Frame(self)
        self._topframe.configure(height='200', width='200')
        self.bpmonth = ttk.Button(self._topframe)
        self.bpmonth.configure(style='Toolbutton', text='L')
        self.bpmonth.pack(side='left')
        self.bnmonth = ttk.Button(self._topframe)
        self.bnmonth.configure(style='Toolbutton', text='R')
        self.bnmonth.pack(side='left')
        self._lmonth = ttk.Label(self._topframe)
        self._lmonth.configure(anchor='center', text='January')
        self._lmonth.pack(side='left')
        self.btoday = ttk.Button(self._topframe)
        self.btoday.configure(style='Toolbutton', text='Today')
        self.btoday.pack(expand='true', fill='x', side='left')
        self._lyear = ttk.Label(self._topframe)
        self._lyear.configure(text='2020')
        self._lyear.pack(side='left')
        self.bpyear = ttk.Button(self._topframe)
        self.bpyear.configure(style='Toolbutton', text='L')
        self.bpyear.pack(side='left')
        self.bnyear = ttk.Button(self._topframe)
        self.bnyear.configure(style='Toolbutton', text='R')
        self.bnyear.pack(side='left')
        self._topframe.pack(anchor='n', fill='x', side='top')
        self._canvas = tk.Canvas(self)
        self._canvas.configure(background='#ffffff', borderwidth='0', height='160', highlightthickness='0')
        self._canvas.configure(width='240')
        self._canvas.pack(anchor='center', expand='true', fill='both', side='top')
        
        
        self.__img_prev = imgp = tk.PhotoImage(data=imgp_data)
        self.__img_next = imgn = tk.PhotoImage(data=imgn_data)
        #self._lmonth = lmonth
        #self._lyear = lyear
        callback = lambda event=None: self._change_date('month', -1)
        self.bpmonth.configure(image=imgp, command=callback)
        callback = lambda event=None: self._change_date('month', 1)
        self.bnmonth.configure(image=imgn, command=callback)
        callback = lambda event=None: self._change_date('year', -1)
        self.bpyear.configure(image=imgp, command=callback)
        callback = lambda event=None: self._change_date('year', 1)
        self.bnyear.configure(image=imgn, command=callback)
        self.btoday.configure(command=self._go_today)
        self._canvas.bind('<Configure>', self._on_canvas_configure)
        #self._topframe = frame2
        #self._canvas = canvas
        self._draw_calendar(self._canvas)
        self._canvas.tag_bind('cell', '<Button-1>', self._on_cell_clicked)
        
    def _reconfigure_calendar(self):
        options = self.__options
        self._date = self.datetime(options['year'], options['month'], 1)
        self._cal = get_calendar(options['locale'], options['firstweekday'])
        self._weeks = self._cal.monthdayscalendar(options['year'],
                                                  options['month'])
    
    def _reconfigure_date(self):
        options = self.__options
        self._date = self.datetime(options['year'], options['month'], 1)
        self._weeks = self._cal.monthdayscalendar(options['year'],
                                                  options['month'])
        self._selection = None # Forget current selected day
        self._redraw_calendar()
    
    def _go_today(self, event=None):
        options = self.__options
        today = self.datetime.now()
        options['year'] = today.year
        options['month'] = today.month
        self._reconfigure_date()
        
    def _change_date(self, element, direction):
        options = self.__options
        newdate = None
        if element == 'month':
            if direction == -1:
                newdate = self._date - self.timedelta(days=1)
            else:
                year, month = self._date.year, self._date.month
                days = calendar.monthrange(year, month)[1] + 1
                newdate = self._date + self.timedelta(days=days)
        elif element == 'year':
            year = self._date.year + direction
            newdate = self.datetime(year, self._date.month, 1)
        options['year'] = newdate.year
        options['month'] = newdate.month
        self._reconfigure_date()
    
    def _on_cell_clicked(self, event=None):
        item = self._canvas.find_withtag('current')
        idx = self._recmat.index(item[0])
        weeks = self._weeks
        day = 0
        f, c = i2rc(idx, 7)
        if f < len(weeks):
            day = weeks[f][c]
            if day != 0:
                self.select_day(day, self._date.month, self._date.year)
    
    def _mark_days(self):
        options = self.__options
        year = self._date.year
        month = self._date.month
        weeks = self._weeks
        now = self.datetime.now()
        today = (now.year, now.month, now.day)
        for i, f, c in rowmajor(6,7):
            day = 0
            clear = True
            if f < len(weeks):
                day = weeks[f][c]
                key = (year, month, day)
                if ((None, None, day) in self._marked_days or
                   (None, month, day) in self._marked_days or
                   key in self._marked_days):
                    self._canvas.itemconfigure(self._recmat[i],
                                               fill=options['markbg'],
                                               outline=options['markbg'])
                    self._canvas.itemconfigure(self._txtmat[i],
                                               fill=options['markfg'])
                    clear = False
                if key == today:
                    self._canvas.itemconfigure(self._recmat[i],
                                               fill=options['selectfg'],
                                               outline=options['selectbg'])
                    self._canvas.itemconfigure(self._txtmat[i],
                                               fill=options['selectbg'])
                    clear = False
                if key == self._selection:
                    self._canvas.itemconfigure(self._recmat[i],
                                               fill=options['selectbg'],
                                               outline=options['selectbg'])
                    self._canvas.itemconfigure(self._txtmat[i],
                                               fill=options['selectfg'])
                    clear = False
            if clear:
                # clear day
                self._canvas.itemconfigure(self._recmat[i],
                                           fill=options['calendarbg'],
                                           outline=options['calendarbg'])
                self._canvas.itemconfigure(self._txtmat[i],
                                           fill=options['calendarfg'])
        self.__markdays_cb = None
    
    def _call_mark_days(self):
        if self.__markdays_cb is None:
            self.__markdays_cb = self.after_idle(self._mark_days)
        
    def _remark_date(self, day, month=None, year=None, highlight=True):
        key = (year, month, day)
        if highlight:
            self._marked_days.add(key)
        else:
            if key in self._marked_days:
                self._marked_days.remove(key)
        self._call_mark_days()
        
    def mark_day(self, day, month=None, year=None):
        """Marks the specified month day with a visual marker
        (typically by making the number bold).
        If only day is specified and the calendar month and year
        are changed, the marked day remain marked.
        You can be more specific setting month and year parameters.
        """
        self._remark_date(day, month, year, highlight=True)
    
    def unmark_day(self, day, month=None, year=None):
        self._remark_date(day, month, year, highlight=False)
    
    def clear_marks(self):
        """Clears all marked days"""
        self._marked_days.clear()
        self._call_mark_days()

    def _draw_calendar(self, canvas, redraw=False):
        """Draws calendar."""
        options = self.__options
        # Update labels:
        name = self._cal.formatmonthname(self._date.year, self._date.month, 0,
                                         withyear=False)
        self._lmonth.configure(text=name.title())
        self._lyear.configure(text=str(self._date.year))
        
        # Update calendar
        ch = canvas.winfo_height()
        cw = canvas.winfo_width()
        rowh = ch / 7.0
        colw = cw / 7.0
        # Header background
        if self._rheader is None:
            self._rheader = canvas.create_rectangle(0, 0, cw, rowh, width=0,
                                                    fill=options['headerbg'])
        else:
            canvas.itemconfigure(self._rheader, fill=options['headerbg'])
            canvas.coords(self._rheader, 0, 0, cw, rowh)
        # Header text
        ox = 0
        oy = rowh / 2.0
        coffset = colw / 2.0
        cols = self._cal.formatweekheader(3).split()
        for i in range(0, 7):
            x = ox + i * colw + coffset
            if redraw:
                item = self._theader[i]
                canvas.coords(item, x, oy)
                canvas.itemconfigure(item, text=cols[i],
                                     fill=options['headerfg'])
            else:
                self._theader[i] = canvas.create_text(x, oy, text=cols[i],
                                                      fill=options['headerbg'])
        
        # background matrix
        oy = rowh
        ox = 0
        for i, x, y, x1, y1 in matrix_coords(6, 7, rowh, colw, ox, oy):
            x1 -= 1
            y1 -= 1
            if redraw:
                rec = self._recmat[i]
                canvas.coords(rec, x, y, x1, y1)
                canvas.itemconfigure(rec, fill=options['calendarbg'])
            else:
                rec = canvas.create_rectangle(x, y, x1, y1, width=1,
                                          fill=options['calendarbg'],
                                          outline=options['calendarbg'],
                                          activeoutline=options['selectbg'],
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
        # Mark days
        self._mark_days()
    
    def _redraw_calendar(self):
        self._draw_calendar(self._canvas, redraw=True)
        # after idle callback trick
        self.__redraw_cb = None
    
    def _on_canvas_configure(self, event=None):
        if self.__redraw_cb is None:
            self.__redraw_cb = self.after_idle(self._redraw_calendar)

    @property
    def selection(self):
        """Return a datetime representing the current selected date."""
        if not self._selection:
            return None

        year, month = self._date.year, self._date.month
        return self.datetime(year, month, self._selection[2])
    
    def select_day(self, day, month=None, year=None):
        options = self.__options
        options['month'] = month = self._date.month if month is None else month
        options['year'] = year = self._date.year if year is None else year
        self._reconfigure_date()
        self._selection = (year, month, day)
        self._call_mark_days()
        self.event_generate('<<CalendarFrameDateSelected>>')


if __name__ == '__main__':
    import random
    
    locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
    root = tk.Tk()
    c = CalendarFrame(root)
    c.grid()
    
    # select day
    c.select_day(1)
    
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
