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
import sys
import re
try:
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.font
except:
    import Tkinter as tk
    import ttk
    import tkFont
    tk.font = tkFont

from pygubu.stockimage import StockImage, StockImageException
from pygubudesigner.widgets.propertyeditor import *

RE_FONT = re.compile("(?P<family>\{\w+(\w|\s)*\}|\w+)\s?(?P<size>-?\d+)?\s?(?P<modifiers>\{\w+(\w|\s)*\}|\w+)?")
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(FILE_DIR, "..", "images", "widgets", "fontentry")
IMAGES_DIR = os.path.abspath(IMAGES_DIR)
StockImage.register_from_dir(IMAGES_DIR)

PREDEFINED_FONTS = [
    'TkDefaultFont', 'TkTextFont', 'TkFixedFont',
    'TkMenuFont', 'TkHeadingFont', 'TkCaptionFont',
    'TkSmallCaptionFont', 'TkIconFont', 'TkTooltipFont']
WIN_FONTS = (
    'system', 'ansi', 'device', 'systemfixed', 'ansifixed', 'oemfixed')
MAC_FONTS = (
    'system','application','menu',
    'systemSystemFont', 'systemEmphasizedSystemFont', 'systemSmallSystemFont',
    'systemSmallEmphasizedSystemFont', 'systemApplicationFont',
    'systemLabelFont', 'systemViewsFont', 'systemMenuTitleFont',
    'systemMenuItemFont', 'systemMenuItemMarkFont', 'systemMenuItemCmdKeyFont',
    'systemWindowTitleFont', 'systemPushButtonFont',
    'systemUtilityWindowTitleFont', 'systemAlertHeaderFont',
    'systemToolbarFont', 'systemMiniSystemFont', 'systemDetailSystemFont',
    'systemDetailEmphasizedSystemFont')

_sp = sys.platform
if _sp in ('win32', 'cygwin'):
    PREDEFINED_FONTS.extend(WIN_FONTS)
if _sp == 'darwin':
    PREDEFINED_FONTS.extend(MAC_FONTS)


class FontPropertyEditor(PropertyEditor):

    def _create_ui(self):
        self._dsize = '12'  # default font size

        self._name = w = ChoicePropertyEditor(self)
        w.grid(row=0, column=0, sticky='we')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)
        w.bind('<<PropertyChanged>>', self._on_fontname_changed, add=True)

        self._optionsframe = container1 = ttk.Frame(self)
        container1.grid(row=1, column=0, sticky='we')

        w = ttk.Label(container1, text='size:', font='TkSmallCaptionFont')
        w.grid(row=0, column=0)
        self._size = w = ChoicePropertyEditor(container1)
        w.parameters(width=4)
        w.grid(row=0, column=1, sticky='w')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)

        w = ttk.Label(container1, text='style:', font='TkSmallCaptionFont')
        w.grid(row=0, column=2, sticky='w', padx=5)

        self._bold = w = CheckbuttonPropertyEditor(container1)
        img = StockImage.get('format-text-bold')
        w.parameters(style='Toolbutton', text='B', image=img,
                     onvalue='bold', offvalue='')
        w.grid(row=0, column=3, sticky='we')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)

        self._italic = w = CheckbuttonPropertyEditor(container1)
        img = StockImage.get('format-text-italic')
        w.parameters(style='Toolbutton', text='I', image=img,
                     onvalue='italic', offvalue='')
        w.grid(row=0, column=4, sticky='we')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)

        self._underline = w = CheckbuttonPropertyEditor(container1)
        img = StockImage.get('format-text-underline')
        w.parameters(style='Toolbutton', text='U', image=img,
                     onvalue='underline', offvalue='')
        w.grid(row=0, column=5, sticky='we')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)

        self._overstrike = w = CheckbuttonPropertyEditor(container1)
        img = StockImage.get('format-text-strikethrough')
        w.parameters(style='Toolbutton', text='S', image=img,
                     onvalue='overstrike', offvalue='')
        w.grid(row=0, column=6, sticky='we')
        w.bind('<<PropertyChanged>>', self._on_variable_changed)

        self.columnconfigure(0, weight=1)
        self._populate_options()

    def _get_value(self):
        value = ''
        name = self._name.value
        if name:
            if name in PREDEFINED_FONTS:
                value = name
            else:
                size = self._size.value if self._size.value else self._dsize
                modifiers = []
                if self._bold.value:
                    modifiers.append(self._bold.value)
                if self._italic.value:
                    modifiers.append(self._italic.value)
                if self._underline.value:
                    modifiers.append(self._underline.value)
                if self._overstrike.value:
                    modifiers.append(self._overstrike.value)
                modifiers = ' '.join(modifiers)
                tkformat = '{{{0}}} {1} {{{2}}}'
                value = tkformat.format(name, size, modifiers)
        else:
            self._clear_editors()
            
        return value

    def _set_value(self, value):
        family = value
        size = None
        modifiers = ''

        s = RE_FONT.search(value)
        if s:
            g = s.groupdict()
            family = g['family'].replace('{', '').replace('}','')
            size = g['size']
            modifiers = g['modifiers']
            if  modifiers is not None:
                modifiers = modifiers.replace('{', '').replace('}','')
            else:
                modifiers = ''
        self._name.edit(family)
        if size:
            self._size.edit(size)
        if modifiers:
            modifiers = modifiers.split(' ')
            for m in modifiers:
                if m == 'bold':
                    self._bold.edit(m)
                if m == 'italic':
                    self._italic.edit(m)
                if m == 'underline':
                    self._underline.edit(m)
                if m == 'overstrike':
                    self._overstrike.edit(m)

    def edit(self, value):
        self._clear_editors()
        PropertyEditor.edit(self, value)
        self._on_fontname_changed()

    def _on_fontname_changed(self, event=None):
#        print('_on_fontname_changed', event, self._name.value)
        if self._name.value in PREDEFINED_FONTS:
            self._optionsframe.grid_remove()
        else:
            self._optionsframe.grid()
            if self._name.value and not self._size.value:
                self._size.edit(self._dsize)

    def _clear_editors(self):
        self._size.edit('')
        self._bold.edit('')
        self._italic.edit('')
        self._underline.edit('')
        self._overstrike.edit('')

    def _populate_options(self):
        sizes = (6, 8, 9, 10, 11, 12, 14, 16, 20, 24, 36, 48, 72)
        self._size.parameters(values=sizes)

        families = sorted(tk.font.families())
        values = [''] + PREDEFINED_FONTS + families
        self._name.parameters(values=values)


register_editor('fontentry', FontPropertyEditor)


if __name__ == '__main__':
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    editor = FontPropertyEditor(root)
    editor.grid(sticky='nsew')
    #editor.edit('Anonymous Pro|-50|bold,italic')
    editor.edit('Anonymous Pro|12|bold,italic')

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
