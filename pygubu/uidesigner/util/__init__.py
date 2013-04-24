#
# Copyright 2012-2013 Alejandro Autalán
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  http://pygubu.web.here
import os

import tkinter as tk
from tkinter import ttk
import tkinter.colorchooser
import tkinter.filedialog

from pygubu.stockimage import *


class BaseFrame(ttk.Frame):
    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        self.master = master
        self.widgets = {}
        self._init_before()
        self._create_ui()
        self._init_after()

    def _init_before(self):
        pass

    def _create_ui(self):
        pass

    def _init_after(self):
        pass


class AppFrame(BaseFrame):
    """Base class for an application"""

    def run(self):
        """Ejecutes the main loop"""

        self.master.protocol("WM_DELETE_WINDOW", self.__on_window_close)
        self.master.mainloop()

    def set_resizable(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

    def set_title(self, title):
        """Sets the window title"""
        if self.master:
            self.master.title(title)

    def set_menu(self, menu):
        """Sets the main menu"""
        self.master.config(menu=menu)

    def __on_window_close(self):
        """Manage WM_DELETE_WINDOW protocol"""
        if self.on_close_execute():
            self.master.destroy()

    def on_close_execute(self):
        """Returns True if the app is ready for quit"""
        return True

    def quit(self):
        """Exits the app if it is ready for quit"""
        self.__on_window_close()

    def set_size(self, geom):
        self.master.geometry(geom)

Application = AppFrame


def _autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed.
    Code from Joe English (JE) at http://wiki.tcl.tk/950"""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


def create_scrollable(master, wclass, **kw):
    """Creates a widget of class wclass and makes it scrollable.
    The widget is created inside a frame in the master.
    widget.frame.grid(*) should be used to grid it.
    Params: master, widget_class
    """
    frame = ttk.Frame(master)
    widget = wclass(frame, **kw)
    widget.vsb = ttk.Scrollbar(frame, orient="vertical", command=widget.yview)
    widget.hsb = ttk.Scrollbar(frame, orient="horizontal", command=widget.xview)
    widget.frame = frame

    widget.configure(yscrollcommand=lambda f, l: _autoscroll(widget.vsb, f, l))
    widget.configure(xscrollcommand=lambda f, l: _autoscroll(widget.hsb, f, l))

    #packing
    widget.grid(column=0, row=0, sticky='nswe', in_=frame)
    widget.update()
    widget.vsb.grid(column=1, row=0, sticky='ns')
    widget.hsb.grid(column=0, row=1, sticky='ew')

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    return widget


_selector_id = 0
_ttk_style = None

def make_color_selector(master, textvariable):
    global _selector_id
    global _ttk_style

    if _ttk_style is None:
        _ttk_style = ttk.Style()

    frame = ttk.Frame(master)
    entry = ttk.Entry(frame, textvariable=textvariable)
    _selector_id += 1
    stylename = 'ID{0}.ColorSelectorButton.TButton'.format(_selector_id)
    button = ttk.Button(frame, text='…', style=stylename)
    btn_bgcolor = _ttk_style.lookup('TButton', 'background')

    def on_entry_changed(varname, element, mode):
        color = textvariable.get()
        stylename = button.cget('style')
        if color:
            try:
                _ttk_style.configure(stylename, background=color)
            except Exception as e:
                pass
        else:
            #set button to the default color
            _ttk_style.configure(stylename, background=btn_bgcolor)

    def on_button_click():
        current = entry.get()
        _, txtcolor = tk.colorchooser.askcolor(color=current)
        if txtcolor is not None:
            textvariable.set(txtcolor)

    button.configure(command=on_button_click)
    textvariable.trace('w', on_entry_changed)
    entry.grid()
    button.grid(row=0, column=1)

    return (frame, entry, button)


def make_image_selector(master, textvariable):
    frame = ttk.Frame(master)
    entry = ttk.Entry(frame, textvariable=textvariable)
    button = ttk.Button(frame, text='…', style='ImageSelectorButton.TButton')

    def on_button_click():
        options = {
            'filetypes':[('GIF', '*.gif'), ('PGM', '*.pgm'), ('PPM', '*.ppm')] }
        if tk.TkVersion >= 8.6:
            options['filetypes'].append(('PNG', '*.png'))

        fname = tk.filedialog.askopenfilename(**options)
        if fname:
            base, name = os.path.split(fname)
            if not StockImage.is_registered(name):
                StockImage.register(name, fname)
            textvariable.set(name)

    button.configure(command=on_button_click)
    entry.grid()
    button.grid(row=0, column=1)

    return (frame, entry, button)


class ArrayVar(tk.Variable):
    '''A variable that works as a Tcl array variable'''

    _default = {}
    _elementvars = {}

    def __del__(self):
        self._tk.globalunsetvar(self._name)
        for elementvar in self._elementvars:
            del elementvar


    def __setitem__(self, elementname, value):
        if elementname not in self._elementvars:
            v = ArrayElementVar(varname=self._name,
            elementname=elementname, master=self._master)
            self._elementvars[elementname] = v
        self._elementvars[elementname].set(value)


    def __getitem__(self, name):
        if name in self._elementvars:
            return self._elementvars[name].get()
        return None


    def __call__(self, elementname):
        '''Create a new StringVar as an element in the array'''
        if elementname not in self._elementvars:
            v = ArrayElementVar(varname=self._name, elementname=elementname,
                master=self._master)
            self._elementvars[elementname] = v
        return self._elementvars[elementname]


    def set(self, dictvalue):
        # this establishes the variable as an array
        # as far as the Tcl interpreter is concerned
        self._master.eval("array set {%s} {}" % self._name)

        for (k, v) in dictvalue.items():
            self._tk.call("array", "set", self._name, k, v)

    initialize = set


    def get(self):
        '''Return a dictionary that represents the Tcl array'''
        value = {}
        for (elementname, elementvar) in self._elementvars.items():
            value[elementname] = elementvar.get()
        return value


class ArrayElementVar(tk.StringVar):
    '''A StringVar that represents an element of an array'''
    _default = ""

    def __init__(self, varname, elementname, master):
        self._master = master
        self._tk = master.tk
        self._name = "%s(%s)" % (varname, elementname)
        self.set(self._default)

    def __del__(self):
        """Unset the variable in Tcl."""
        self._tk.globalunsetvar(self._name)

