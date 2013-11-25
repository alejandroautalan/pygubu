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
    import tkinter.colorchooser
except:
    import Tkinter as tk
    import ttk
    import tkColorChooser
    tk.colorchooser = tkColorChooser

from pygubudesigner.widgets.compoundpropertyeditor import CompoundPropertyEditor
#from compoundpropertyeditor import CompoundPropertyEditor


class ColorEntry(CompoundPropertyEditor):
    count = 0
    ttk_style = None
    btn_bgcolor = ''

    def __init__(self, master=None, **kw):
        CompoundPropertyEditor.__init__(self, master, **kw)
        
        if ColorEntry.ttk_style is None:
            ColorEntry.ttk_style = ttk.Style()
            ColorEntry.btn_bgcolor = ColorEntry.ttk_style.lookup('Toolbutton', 'background')

        ColorEntry.count += 1

        self._entryvar = tk.StringVar()
        self.entry = w = ttk.Entry(self, textvariable=self._entryvar)
        w.grid(sticky='ew')
        w.bind('<FocusOut>', self._on_entry_changed)
        w.bind('<KeyPress-Return>', self._on_entry_changed)
        w.bind('<KeyPress-KP_Enter>', self._on_entry_changed)
        selector_id = ColorEntry.count
        self.stylename = 'ID{0}.ColorSelectorButton.Toolbutton'.format(selector_id)
        self.button = w = ttk.Button(self, text='…', style=self.stylename)
        w.grid(row=0, column=1, padx="5 0")
        w.configure(command=self._on_button_click)
        
        self.columnconfigure(0, weight=1)

    def _on_button_click(self):
        current = self._entryvar.get()
        txtcolor = None
        try:
            _, txtcolor = tk.colorchooser.askcolor(color=current)
        except tk.TclError:
            pass
        self._change_color(txtcolor)


    def _change_color(self, newcolor, gen_event=True):
        if newcolor:
            try:
                rgb = self.winfo_rgb(newcolor)
                ColorEntry.ttk_style.configure(self.stylename, background=newcolor)
            except tk.TclError as e:
                pass
        else:
            ColorEntry.ttk_style.configure(self.stylename,
                background=ColorEntry.btn_bgcolor)
            newcolor = ''
        self._disable_cb()
        self._variable.set(newcolor)
        self._entryvar.set(newcolor)
        self._enable_cb()
        if gen_event:
            self.event_generate('<<ColorEntryChanged>>')

    def _on_entry_changed(self, event=None):
        color = self._entryvar.get()
        self._change_color(color)

    def _on_variable_changed(self, varname, elementname, mode):
        color = self._variable.get()
        self._change_color(color, gen_event=False)

    
    
if __name__ == '__main__':
    root = tk.Tk()
    var = tk.StringVar()
    
    def see_var():
        print(var.get())

    entry = ColorEntry(root, textvariable=var)
    entry.grid()
    entry.configure(textvariable=var)
    var.set('red')
    
    btn = ttk.Button(root, text='Value', command=see_var)
    btn.grid(row=0, column=1)

    root.mainloop()

