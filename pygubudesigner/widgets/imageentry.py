# encoding: UTF-8
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

from __future__ import unicode_literals
import os
try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.filedialog
except:
    import Tkinter as tk
    import ttk
    import tkFileDialog
    tk.filedialog = tkFileDialog

from pygubu.stockimage import *
from pygubudesigner.widgets.compoundpropertyeditor import CompoundPropertyEditor
#from compoundpropertyeditor import CompoundPropertyEditor


class ImageEntry(CompoundPropertyEditor):

    def __init__(self, master=None, **kw):
        CompoundPropertyEditor.__init__(self, master, **kw)
        
        self._entryvar = tk.StringVar()
        self.entry = w = ttk.Entry(self, textvariable=self._entryvar)
        w.grid(sticky='ew')
        w.bind('<FocusOut>', self._on_entry_changed)
        w.bind('<KeyPress-Return>', self._on_entry_changed)
        w.bind('<KeyPress-KP_Enter>', self._on_entry_changed)
        self.button = w = ttk.Button(self, text='…',
            style='ImageSelectorButton.Toolbutton')
        w.grid(row=0, column=1, padx="5 0")
        w.configure(command=self._on_button_click)
        
        self.columnconfigure(0, weight=1)

    def _on_button_click(self):
        ext = ['*.gif', '*.pgm', '*.ppm']
        if tk.TkVersion >= 8.6:
            ext.append('*.png')
        options = {
            'filetypes':[('All Images', ' '.join(ext))] }

        fname = tk.filedialog.askopenfilename(**options)
        if fname:
            base, name = os.path.split(fname)
            if not StockImage.is_registered(name):
                StockImage.register(name, fname)
            self._disable_cb()
            self._variable.set(name)
            self._entryvar.set(name)
            self._enable_cb()
            self.event_generate('<<ImageEntryChanged>>')

    def _on_entry_changed(self, event=None):
        imagename = self._entryvar.get()
        self._disable_cb()
        self._variable.set(imagename)
        self._enable_cb()
        self.event_generate('<<ImageEntryChanged>>')

    def _on_variable_changed(self, varname, elementname, mode):
        imagename = self._variable.get()
        self._entryvar.set(imagename)

    
    
if __name__ == '__main__':
    root = tk.Tk()
    var = tk.StringVar()
    
    def see_var():
        print(var.get())

    entry = ImageEntry(root, textvariable=var)
    entry.grid()
    entry.configure(textvariable=var)
    var.set('red')
    
    btn = ttk.Button(root, text='Value', command=see_var)
    btn.grid(row=0, column=1)

    root.mainloop()

