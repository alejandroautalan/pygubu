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

class Textentry(CompoundPropertyEditor):
    def __init__(self, master=None, cnf={}, **kw):
        CompoundPropertyEditor.__init__(self, master, **kw)
        self.text = w = tk.Text(self)
        w.grid(sticky='nsew')
        w.bind('<FocusOut>', self._on_focus_out)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def _on_focus_out(self, event=None):
        value = (self.text.get('0.0', tk.END))[:-1]
        if self._variable is not None:
            self._disable_cb()
            self._variable.set(value)
            self._enable_cb()
            self.event_generate('<<TextentryChanged>>')

    def _on_variable_changed(self, varname, elementname, mode):
        self.text.delete('0.0', tk.END)
        self.text.insert('0.0', self._variable.get())

