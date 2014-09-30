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

from pygubudesigner.widgets.propertyeditor import *


class ColorPropertyEditor(PropertyEditor):
    count = 0  # instance counter, to generate unike style name
    ttk_style = None  # style instance for all color instances
    btn_bgcolor = ''  # default background color picked from current theme
    style_name_tpl = 'ID{0}.ColorSelectorButton.Toolbutton'

    def _create_ui(self):
        cls = ColorPropertyEditor
        if cls.ttk_style is None:
            cls.ttk_style = ttk.Style()
            cls.btn_bgcolor = cls.ttk_style.lookup('Toolbutton', 'background')

        cls.count += 1

        self._entry = w = ttk.Entry(self, textvariable=self._variable)
        w.grid(sticky='ew')
        w.bind('<FocusOut>', self._on_variable_changed)
        w.bind('<KeyPress-Return>', self._on_variable_changed)
        w.bind('<KeyPress-KP_Enter>', self._on_variable_changed)

        selector_id = cls.count
        self._stylename = cls.style_name_tpl.format(selector_id)
        self._button = w = ttk.Button(self, text='…', style=self._stylename)
        w.grid(row=0, column=1, padx="5 0")
        w.configure(command=self._on_button_click)

        self.columnconfigure(0, weight=1)

    def _on_button_click(self):
        current = self._get_value()
        txtcolor = None
        try:
            _, txtcolor = tk.colorchooser.askcolor(color=current)
            if txtcolor is not None:
                self._set_value(txtcolor)
                self._on_variable_changed(event=None)
        except tk.TclError:
            pass
        self._change_color(txtcolor)

    def _change_color(self, newcolor):
        cls = ColorPropertyEditor
        if newcolor:
            try:
                rgb = self.winfo_rgb(newcolor)
                cls.ttk_style.configure(self._stylename,
                                        background=newcolor)
            except tk.TclError:
                pass
        else:
            cls.ttk_style.configure(self._stylename,
                                    background=cls.btn_bgcolor)

    def edit(self, value):
        PropertyEditor.edit(self, value)
        self._change_color(value)


register_editor('colorentry', ColorPropertyEditor)


if __name__ == '__main__':
    root = tk.Tk()
    editor = ColorPropertyEditor(root)
    editor.grid()
    editor.edit('red')

    def see_var(event=None):
        print(editor.value)

    editor.bind('<<PropertyChanged>>', see_var)
    root.mainloop()
