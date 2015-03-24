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
from pygubudesigner.util.selecttool import SelectTool


class StickyPropertyEditor(PropertyEditor):
    DIM = 3

    def _create_ui(self):
        self._label_var = v = tk.StringVar()
        self._label = w = ttk.Label(self, textvariable=v, width=4)
        w.grid(row=0, column=1)
        
        self._map = {
            '' : [0 , 0, 0, 0 , 1, 0, 0 , 0, 0],

            'n' : [0 , 1, 0, 0 , 0, 0, 0 , 0, 0],
            's' : [0 , 0, 0, 0 , 0, 0, 0 , 1, 0],
            'e' : [0 , 0, 0, 0 , 0, 1, 0 , 0, 0],
            'w' : [0 , 0, 0, 1 , 0, 0, 0 , 0, 0],
            
            'nw' : [1 , 0, 0, 0 , 0, 0, 0 , 0, 0],
            'ne' : [0 , 0, 1, 0 , 0, 0, 0 , 0, 0],
            'sw' : [0 , 0, 0, 0 , 0, 0, 1 , 0, 0],
            'se' : [0 , 0, 0, 0 , 0, 0, 0 , 0, 1],
            
            'new': [1 , 1, 1, 0 , 0, 0, 0 , 0, 0],
            'ew': [0 , 0, 0, 1 , 1, 1, 0 , 0, 0],
            'sew': [0 , 0, 0, 0 , 0, 0, 1 , 1, 1],
            'nsw' : [1 , 0, 0, 1 , 0, 0, 1 , 0, 0],
            'ns' : [0 , 1, 0, 0 , 1, 0, 0 , 1, 0],
            'nse' : [0 , 0, 1, 0 , 0, 1, 0 , 0, 1],
            'nsew' : [1 , 1, 1, 1 , 1, 1, 1 , 1, 1],
            }
        self._items = {}
        self._c = w = tk.Canvas(self, bg='#ffffff', borderwidth=0,
                                highlightthickness=0, width=50, height=50)
        w.bind('<Configure>', self._on_canvas_configure)
        w.bind('<<RegionSelected>>', self._on_region_selected)
        w.grid(row=0, column=0, sticky='w')

        self._tool = t = SelectTool(w)
        
        w.bind('<Button-1>', t.click_handler)
        w.bind('<ButtonRelease-1>', t.release_handler)
        w.bind('<Motion>', t.motion_handler)

        self._on_canvas_configure()
    
    def _set_value(self, value):
        self._variable.set(value)
        self._label_var.set(value)
        self._set_state(value)
    
    def _set_state(self, state):
        self._clear()
        if state in self._map:
            self._paint_state(self._map[state])
        else:
            self._paint_state(self._map[''])

    def _on_canvas_configure(self, event=None):
        # Draw grid
        canvas = self._c
        ch, cw = canvas.winfo_height()-1, canvas.winfo_width()-1
        rw = cw / self.DIM
        rh = ch / self.DIM
        # k = f * DIM + c
        if not self._items:
            for k in range(0, self.DIM * self.DIM):
                f = k % self.DIM
                c = k // self.DIM
                x0 = f * rw
                y0 = c * rh
                x1 = x0 + rw
                y1 = y0 + rh
                item = canvas.create_rectangle(x0, y0, x1, y1, fill='white',
                                               outline='gray')
                self._items[item] = k
        else:
            for item in self._items:
                k = self._items[item]
                f = k % self.DIM
                c = k // self.DIM
                x0 = f * rw
                y0 = c * rh
                x1 = x0 + rw
                y1 = y0 + rh
                canvas.coords(item, x0, y0, x1, y1)
    
    def _on_region_selected(self, event=None):
        canvas = self._c
        region = canvas.region_selected
        items = canvas.find_overlapping(*region)
        self._activate(items)
        
    def _clear(self):
        self._paint(self._items)
    
    def _paint(self, items, color='white'):
        for item in items:
            self._c.itemconfigure(item, fill=color)
    
    def _paint_state(self, state, color='#9999cc'):
        for item in self._items:
            pos = self._items[item]
            if state[pos]:
                self._c.itemconfigure(item, fill=color)
    
    def _activate(self, items):
        self._paint(self._items.keys())
        state = [0] * (self.DIM * self.DIM)
        for item in items:
            pos = self._items[item]
            state[pos] = 1
        # check valid state
        found = ''
        for k, v in self._map.items():
            if v == state:
                found = k
                break
        self._paint_state(self._map[found], color='#9999cc')
        self._set_value(found)
        self._on_variable_changed()


register_editor('stickyentry', StickyPropertyEditor)

if __name__ == '__main__':
    root = tk.Tk()
    editor = StickyPropertyEditor(root)
    editor.grid()
    editor.edit('nsew')

    def see_var(event=None):
        print(editor.value)

    editor.bind('<<PropertyChanged>>', see_var)
    root.mainloop()
