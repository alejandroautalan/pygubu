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
    
    
class CompoundPropertyEditor(ttk.Frame):
    def __init__(self, master=None, **kw):
        self._variable = None
        self.__cbhandler = None
        
        if 'textvariable' in kw:
            self._configure_variable(kw.pop('textvariable'))
        ttk.Frame.__init__(self, master, **kw)
        
    def configure(self, cnf=None, **kw):
        if 'textvariable' in kw:
            self._configure_variable(kw.pop('textvariable'))
        ttk.Frame.configure(self, cnf, **kw)

    config = configure
        
    def _configure_variable(self, variable):
        self._disable_cb()
        self._variable = variable
        self._enable_cb()

    def _enable_cb(self):
        if self._variable is not None:
            self.__cbhandler = self._variable.trace(
                mode="w", callback=self._on_variable_changed)

    def _disable_cb(self):
        if self.__cbhandler is not None:
            self._variable.trace_vdelete("w", self.__cbhandler)
            self.__cbhandler = None
            
    def _on_variable_changed(self, varname, elementname, mode):
        pass
