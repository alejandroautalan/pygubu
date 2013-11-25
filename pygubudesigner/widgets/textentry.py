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


class Textentry(tk.Text):
    def __init__(self, master=None, cnf={}, **kw):
        self.__variable = None
        self.__cbhandler = None

        if 'textvariable' in kw:
            self.__configure_variable(kw.pop('textvariable'))

        tk.Text.__init__(self, master, *cnf, **kw)
        self.bind('<FocusOut>', self._on_focus_out)

    def configure(self, cnf=None, **kw):
        if 'textvariable' in kw:
            self.__configure_variable(kw.pop('textvariable'))
        tk.Text.configure(self, cnf, **kw)

    config = configure

    def _on_focus_out(self, event):
        value = (self.get('0.0', tk.END))[:-1]
        if self.__variable is not None:
            self.__disable_cb()
            self.__variable.set(value)
            self.__enable_cb()

    def _on_variable_changed(self, varname, elementname, mode):
        self.delete('0.0', tk.END)
        self.insert('0.0', self.__variable.get())

    def __configure_variable(self, variable):
        self.__disable_cb()
        self.__variable = variable
        self.__enable_cb()

    def __enable_cb(self):
        if self.__variable is not None:
            self.__cbhandler = self.__variable.trace(
                mode="w", callback=self._on_variable_changed)

    def __disable_cb(self):
        if self.__cbhandler is not None:
            self.__variable.trace_vdelete("w", self.__cbhandler)
            self.__cbhandler = None
