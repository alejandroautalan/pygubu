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

from pygubudesigner.widgets.propertyeditor import *


class TkVarPropertyEditor(PropertyEditor):

    def _create_ui(self):
        self._entry = w = EntryPropertyEditor(self)
        w.grid(sticky='we')
        self._cbox = w = ChoicePropertyEditor(self)
        w.grid(row=0, column=1, sticky='we')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._entry.bind('<<PropertyChanged>>', self._on_variable_changed)
        self._cbox.bind('<<PropertyChanged>>', self._on_variable_changed)
        cbvalues = ('string', 'int', 'double', 'boolean')
        self._cbox.parameters(width=8, values=cbvalues, state='readonly')

    def _get_value(self):
        value = ''
        if self._entry.value != '':
            value = '{0}:{1}'.format(self._cbox.value, self._entry.value)
        return value

    def _set_value(self, value):
        if ':' in value:
            type_, name = value.split(':')
            self._entry.edit(name)
            self._cbox.edit(type_)
        else:
            self._entry.edit('')
            self._cbox.edit('string')


register_editor('tkvarentry', TkVarPropertyEditor)


if __name__ == '__main__':
    root = tk.Tk()
    editor = TkVarPropertyEditor(root)
    editor.grid()
    editor.edit('double:mydouble')

    def see_var():
        print(editor.value)

    btn = ttk.Button(root, text='Value', command=see_var)
    btn.grid(row=0, column=1)

    root.mainloop()
