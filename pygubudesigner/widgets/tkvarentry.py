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
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubudesigner.widgets.compoundpropertyeditor import CompoundPropertyEditor
#from compoundpropertyeditor import CompoundPropertyEditor


class TkVarEntry(CompoundPropertyEditor):
    
    def __init__(self, master=None, **kw):
        CompoundPropertyEditor.__init__(self, master, **kw)
        
        self._entryvar = tk.StringVar()
        self._cboxvar = var2 = tk.StringVar()
        var2.trace(mode="w", callback=self.__on_cbox_changed)
        self.entry = entry = ttk.Entry(self, textvariable=self._entryvar)
        entry.bind('<FocusOut>', self.__on_entry_changed)
        entry.bind('<KeyPress-Return>', self.__on_entry_changed)
        entry.bind('<KeyPress-KP_Enter>', self.__on_entry_changed)
        self.entry.grid(sticky='ew')
        
        self.default_vtype = 'string'
        cbox_values = ('string', 'int', 'double', 'boolean')
        self._cboxvar.set(cbox_values[0])
        self.cbox = ttk.Combobox(self, textvariable=self._cboxvar,
            state='readonly', values=cbox_values, width=6)
        self.cbox.grid(row=0, column=1)
        
        self.columnconfigure(0, weight=1)
        
    def __on_cbox_changed(self, varname, elementname, mode):
        self._on_value_changed_by_user()

    def __on_entry_changed(self, event=None):
        self._on_value_changed_by_user()

    def _on_value_changed_by_user(self):
        value = self._entryvar.get()
        if value:
            value = self._cboxvar.get() + ':' + value
        else:
            value = ''
        self._disable_cb()
        self._variable.set(value)
        self._enable_cb()
        self.event_generate('<<TkVarEntryChanged>>')
        
    def _on_variable_changed(self, varname, elementname, mode):
        vtype = self.default_vtype
        value = self._variable.get()
        if ':' in value:
            vtype, value = value.split(':')
        self._cboxvar.set(vtype)
        self._entryvar.set(value)

    
    
if __name__ == '__main__':
    root = tk.Tk()
    var = tk.StringVar()
    
    def see_var():
        print(var.get())

    entry = TkVarEntry(root, textvariable=var)
    entry.grid()
    entry.configure(textvariable=var)
    var.set('Double:mydouble')
    
    btn = ttk.Button(root, text='Value', command=see_var)
    btn.grid(row=0, column=1)

    root.mainloop()

    
