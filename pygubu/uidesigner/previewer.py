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


class UIPreview():
    window_tag = 'window'


    def __init__(self, notebook):
        self.notebook = notebook
        self.builder = None
        self.canvas_window = None
        self.canvas = canvas = util.create_scrollable(self.notebook,
                tkinter.Canvas, background='white', highlightthickness=0)
        canvas.create_window(5, 5, anchor=tkinter.NW,
                tags=self.window_tag)
        self.notebook.add(canvas.frame, text='Preview', sticky=tkinter.NSEW)
        self.tab_id = canvas.frame


    def update(self, widget_id, xmlnode, is_menu=False):
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


    def delete(self, identifier):
        preview = self.tabs[identifier]
        preview.canvas_window.destroy()
        del self.tabs[identifier]
        self.notebook.forget(preview.tab_id)


    def remove_all(self):
        for identifier in self.tabs:
            self.delete(identifier)


