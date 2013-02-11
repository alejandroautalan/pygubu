#
# Copyright 2012 Alejandro Autalán
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

import tkinter
from tkinter import ttk

import pygubu
from . import util
from .util.stockimage import StockImage


class UIPreview():
    window_tag = 'window'
    indicators_tag = ('nw', 'ne', 'sw', 'se')

    def __init__(self, notebook):
        self.is_menu = False
        self.notebook = notebook
        self.builder = None
        self.canvas_window = None
        self.canvas = util.create_scrollable(self.notebook, tkinter.Canvas,
                background='white', highlightthickness=0)
        self.canvas.create_window(10, 10, anchor=tkinter.NW,
                tags=self.window_tag)
        self.notebook.add(self.canvas.frame, text='Preview', sticky=tkinter.NSEW)
        self.tab_id = self.canvas.frame

        #selected indicators
        self.indicators = []
        anchors = {'nw': tkinter.SE, 'ne': tkinter.SW,
                'sw': tkinter.NE, 'se': tkinter.NW}
        for sufix in self.indicators_tag:
            label = tkinter.Label(self.canvas,
                    image=StockImage.get('indicator_' + sufix))
            self.indicators.append(label)
            self.canvas.create_window(-10, -10, anchor=anchors[sufix],
                    window=label, tags=sufix)


    def show_selected(self, selected_id=None):
        canvas = self.canvas
        if selected_id is None or self.is_menu == True:
            for indicator in self.indicators:
                canvas.itemconfigure(indicator, state=tkinter.HIDDEN)
        else:
            canvas.update_idletasks()
            #canvas.itemconfigure(self.indicator_tag, state=tkinter.NORMAL)
            widget = self.builder.get_object(selected_id)
            for indicatorw in self.indicators:
                try:
                    indicatorw.lift(widget)
                except tkinter.TclError:
                    pass
            for tag in self.indicators_tag:
                x, y = self._calculate_indicator_coords(tag, widget)
                ox, oy = canvas.coords(tag)
                canvas.move(tag, x - ox, y - oy)


    def _calculate_indicator_coords(self, tag, widget):
        x = y = 0
        wx = widget.winfo_rootx()
        wy = widget.winfo_rooty()
        ww = widget.winfo_width()
        wh = widget.winfo_height()
        cx = self.canvas.winfo_rootx()
        cy = self.canvas.winfo_rooty()
        if tag == 'nw':
            x = wx - cx
            y = wy - cy
        if tag == 'ne':
            x = (wx - cx) + ww
            y = (wy - cy)
        if tag == 'sw':
            x = (wx - cx)
            y = (wy - cy) + wh
        if tag == 'se':
            x = (wx - cx) + ww
            y = (wy - cy) + wh
        return (x, y)

    def update(self, widget_id, xmlnode, is_menu=False):
        self.is_menu = is_menu
        #update tab text
        self.notebook.tab(self.tab_id, text=widget_id)

        #delete current preview
        #FIXME maybe do something to update preview without re-creating all ?
        del self.builder
        self.builder = None
        self.canvas.itemconfigure(self.window_tag, window='')
        if self.canvas_window:
            self.canvas_window.destroy()

        #Create preview
        self.builder = pygubu.Builder()
        self.builder.add_from_xmlnode(xmlnode)
        preview_widget = None
        if is_menu:
            menubutton = ttk.Menubutton(self.canvas, text='Menu preview')
            widget = self.builder.get_object(widget_id, menubutton)
            menubutton.configure(menu=widget)
            preview_widget = menubutton
        else:
            preview_widget = self.builder.get_object(widget_id, self.canvas)

        self.canvas_window = preview_widget
        self.canvas.itemconfigure(self.window_tag, window=preview_widget)
        self.canvas_window.bind('<Configure>', self._on_canvaswin_updated)


    def _on_canvaswin_updated(self, event):
            size = (self.canvas_window.winfo_reqwidth() + 10,
                self.canvas_window.winfo_reqheight() + 10)
            self.canvas.config(scrollregion="0 0 %s %s" % size)


class PreviewHelper:
    """Manages UI Preview"""

    def __init__(self, notebook):
        self.notebook = notebook
        self.builders = {}
        self.canvases = {}
        self.tabs = {}
        self.windows = {}
        self.preview_tag = 'previewwindow'


    def draw(self, identifier, widget_id, xmlnode, is_menu=False):
        preview = None
        if identifier not in self.tabs:
            preview = UIPreview(self.notebook)
            self.tabs[identifier] = preview
        else:
            preview = self.tabs[identifier]

        preview.update(widget_id, xmlnode, is_menu)


    def show_selected(self, identifier, selected_id):
        if identifier in self.tabs:
            self.tabs[identifier].show_selected(selected_id)


    def delete(self, identifier):
        preview = self.tabs[identifier]
        preview.canvas_window.destroy()
        del self.tabs[identifier]
        self.notebook.forget(preview.tab_id)


    def remove_all(self):
        for identifier in list(self.tabs.keys()):
            self.delete(identifier)


