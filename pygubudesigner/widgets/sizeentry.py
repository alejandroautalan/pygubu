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
import re
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubudesigner.widgets.compoundpropertyeditor import CompoundPropertyEditor

DIMENSION = r'[1-9]\d*[cimp]?'
DIMENSION_RE = re.compile(DIMENSION)


class SizeEntry(CompoundPropertyEditor):

    def __init__(self, master=None, **kw):
        CompoundPropertyEditor.__init__(self, master, **kw)
        self._mode = ''
        self._dvar = tk.StringVar()
        self._dentry = w = ttk.Entry(self, textvariable=self._dvar)
        w.bind('<FocusOut>', self._on_entry_changed)
        w.bind('<KeyPress-Return>', self._on_entry_changed)
        w.bind('<KeyPress-KP_Enter>', self._on_entry_changed)
        w.grid(row=0, column=0, sticky='ew')

        self._whframe = f = ttk.Frame(self)
        f.grid(row=1, column=0, sticky='ew')
        f.columnconfigure(1, weight=1)
        f.columnconfigure(3, weight=1)
        l = ttk.Label(f, text='w:')
        l.grid(row=0, column=0)
        self._wvar = tk.StringVar()
        self._wentry = w = ttk.Entry(f, textvariable=self._wvar, width=9)
        w.grid(row=0, column=1, sticky='ew')
        w.bind('<FocusOut>', self._on_entry_changed)
        w.bind('<KeyPress-Return>', self._on_entry_changed)
        w.bind('<KeyPress-KP_Enter>', self._on_entry_changed)

        l = ttk.Label(f, text='h:')
        l.grid(row=0, column=2)
        self._hvar = tk.StringVar()
        self._hentry = w = ttk.Entry(f, textvariable=self._hvar, width=9)
        w.grid(row=0, column='3', sticky='ew')
        w.bind('<FocusOut>', self._on_entry_changed)
        w.bind('<KeyPress-Return>', self._on_entry_changed)
        w.bind('<KeyPress-KP_Enter>', self._on_entry_changed)
        self.set_mode()


    def set_mode(self, mode=''):
        self._mode = mode
        if mode == '':
            self._dentry.grid()
            self._whframe.grid_remove()
        if mode == 'whsize':
            self._dentry.grid_remove()
            self._whframe.grid()


    def _on_entry_changed(self, event=None):
        if self._mode == '':
            dvalue = self._dvar.get()
            self._change_value(dvalue)

        elif self._mode == 'whsize':
            wvalue = self._wvar.get()
            hvalue = self._hvar.get()
            valid = False
            empty = False
            if wvalue and hvalue and wvalue.isnumeric() and hvalue.isnumeric():
                valid = True
            elif wvalue == hvalue == '':
                valid = True
                empty = True
            if valid:
                newvalue = ''
                if not empty:
                    newvalue = '{0}|{1}'.format(wvalue, hvalue)
                self._change_value(newvalue)

    def _on_variable_changed(self, varname, elementname, mode):
        newvalue = self._variable.get()
        self._change_value(newvalue, gen_event=False)

    def _change_value(self, newvalue, gen_event=True):
        self._disable_cb()
        if self._mode == '':
            self._variable.set(newvalue)
        elif self._mode == 'whsize':
            w = h = ''
            if '|' in newvalue:
                w, h = newvalue.split('|')
                self._wvar.set(w)
                self._hvar.set(h)
                self._variable.set(newvalue)
            else:
                self._variable.set('')
        self._enable_cb()
        if gen_event:
            self.event_generate('<<SizeEntryChanged>>')


if __name__ == '__main__':
    root = tk.Tk()
    var = tk.StringVar()

    def see_var():
        print(var.get())

    entry = DimensionEntry(root, textvariable=var)
    entry.grid()
    entry.configure(textvariable=var)
    #entry.set_mode('whsize')
    var.set('100|70')

    btn = ttk.Button(root, text='Value', command=see_var)
    btn.grid(row=0, column=1)

    root.mainloop()
