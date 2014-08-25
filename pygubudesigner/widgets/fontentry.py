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

from __future__ import unicode_literals

import os
try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.font
except:
    import Tkinter as tk
    import ttk
    import tkFont
    tk.font = tkFont


import sys
project_basedir = '/home/alejandro2/codigofuente/python/pygubu'
if project_basedir not in sys.path:
    sys.path.insert(0, project_basedir)

from pygubu.stockimage import StockImage, StockImageException
from pygubudesigner.widgets.propertyeditor import *


FILE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(FILE_DIR, "..", "images", "widgets", "fontentry")
IMAGES_DIR = os.path.abspath(IMAGES_DIR)
StockImage.register_from_dir(IMAGES_DIR)


class FontPropertyEditor(PropertyEditor):

    def _create_ui(self):
        self._sep = '|'
        self._sep2 = ' '

        w = ttk.Label(self, text='name:', font='TkSmallCaptionFont')
        w.grid(row=0, column=0)
        self._name = w = ChoicePropertyEditor(self)
        w.grid(row=0, column=1, sticky='we')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)

        w = ttk.Label(self, text='size:', font='TkSmallCaptionFont')
        w.grid(row=1, column=0)

        container1 = ttk.Frame(self)
        container1.grid(row=1, column=1, sticky='we')

        self._size = w = ChoicePropertyEditor(container1)
        w.parameters(width=4)
        w.grid(row=0, column=0, sticky='w')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)

        w = ttk.Label(container1, text='style:', font='TkSmallCaptionFont')
        w.grid(row=0, column=1, sticky='w', padx=5)

        container2 = ttk.Frame(container1)
        container2.grid(row=0, column=2, sticky='w')

        self._bold = w = CheckbuttonPropertyEditor(container2)
        img = StockImage.get('format-text-bold')
        w.parameters(style='Toolbutton', text='B', image=img,
                     onvalue='bold', offvalue='')
        w.grid(row=0, column=0, sticky='we')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)

        self._italic = w = CheckbuttonPropertyEditor(container2)
        img = StockImage.get('format-text-italic')
        w.parameters(style='Toolbutton', text='I', image=img,
                     onvalue='italic', offvalue='')
        w.grid(row=0, column=1, sticky='we')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)

        self._underline = w = CheckbuttonPropertyEditor(container2)
        img = StockImage.get('format-text-underline')
        w.parameters(style='Toolbutton', text='U', image=img,
                     onvalue='underline', offvalue='')
        w.grid(row=0, column=2, sticky='we')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)

        self._overstrike = w = CheckbuttonPropertyEditor(container2)
        img = StockImage.get('format-text-strikethrough')
        w.parameters(style='Toolbutton', text='S', image=img,
                     onvalue='overstrike', offvalue='')
        w.grid(row=0, column=3, sticky='we')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)

        self.columnconfigure(1, weight=1)
        self._populate_options()

    def _get_value(self):
        value = ''
        if self._name.value:
            name = self._name.value
            size = self._size.value if self._size.value else '0'
            value = '{1}{0}{2}'.format(self._sep, name, size)
            modifiers = []
            if self._bold.value:
                modifiers.append(self._bold.value)
            if self._italic.value:
                modifiers.append(self._italic.value)
            if self._underline.value:
                modifiers.append(self._underline.value)
            if self._overstrike.value:
                modifiers.append(self._overstrike.value)
            modifiers = self._sep2.join(modifiers)
            value = '{1}{0}{2}'.format(self._sep, value, modifiers)
        else:
            self._clear_editors()
            
        return value

    def _set_value(self, value):
        parts = value.split(self._sep)
        count = len(parts)
        value = parts[0]
        self._name.edit(value)
        if not value:
            self._clear_editors()
        if count >= 2:
            self._size.edit(parts[1])
        if count == 3:
            modifiers = parts[2]
            modifiers = modifiers.split(self._sep2)
            for m in modifiers:
                if m == 'bold':
                    self._bold.edit(m)
                if m == 'italic':
                    self._italic.edit(m)
                if m == 'underline':
                    self._underline.edit(m)
                if m == 'overstrike':
                    self._overstrike.edit(m)

    def _clear_editors(self):
        self._size.edit('')
        self._bold.edit('')
        self._italic.edit('')
        self._underline.edit('')
        self._overstrike.edit('')

    def _populate_options(self):
        sizes = (6, 8, 9, 10, 11, 12, 14, 16, 20, 24, 36, 48, 72)
        self._size.parameters(values=sizes)
        
        stdfonts = (
            '', 'TkDefaultFont', 'TkTextFont', 'TkFixedFont',
            'TkMenuFont', 'TkHeadingFont', 'TkCaptionFont',
            'TkSmallCaptionFont', 'TkIconFont', 'TkTooltipFont')
        families = tuple(sorted(tk.font.families()))
        self._name.parameters(values=stdfonts+families)


register_editor('fontentry', FontPropertyEditor)


if __name__ == '__main__':
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    editor = FontPropertyEditor(root)
    editor.grid(sticky='nsew')
    #editor.edit('Anonymous Pro|-50|bold,italic')
    editor.edit('Anonymous Pro|-50|bold,italic')

    def see_var():
        print(editor.value)

    btn = ttk.Button(root, text='Value', command=see_var)
    btn.grid(row=0, column=1)
    lbl = ttk.Label(root, text='Lorem ipsum dolor sit amet.')
    lbl.grid(row=1, column=0)
    
    def font_cb(event=None):
        font = editor.value.split('|')
        lbl.configure(font=font)
    
    editor.bind('<<PropertyChanged>>', font_cb)

    root.mainloop()
