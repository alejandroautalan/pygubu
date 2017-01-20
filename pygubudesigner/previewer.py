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
from collections import OrderedDict
import sys
import xml.etree.ElementTree as ET
import re
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

import pygubu
from pygubu.stockimage import StockImage
import pygubudesigner.widgets.toplevelframe

try:
    basestring
except NameError:
    basestring = str


RE_FONT = re.compile("(?P<family>\{\w+(\w|\s)*\}|\w+)\s?(?P<size>-?\d+)?\s?(?P<modifiers>\{\w+(\w|\s)*\}|\w+)?")


class BuilderForPreview(pygubu.Builder):
    def _pre_process_data(self, data):
        super(BuilderForPreview, self)._pre_process_data(data)
        cname = data['class']
        
        #  Do not resize main window when
        #  Sizegrip is dragged on preview panel.
        if cname == 'ttk.Sizegrip':
            data['properties']['class_'] = 'DUMMY_CLASS'


class Preview(object):

    def __init__(self, id_, canvas, x=0, y=0, rpaths=None):
        self.id = 'preview_{0}'.format(id_)
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.min_w = self.w
        self.min_h = self.h
        self.resizer_h = 10
        self.canvas = canvas
        self.shapes = {}
        self._create_shapes()
        # --------
        self.builder = None
        self.canvas_window = None
        self._resource_paths = rpaths if rpaths is not None else []

    def width(self):
        return self.w

    def height(self):
        return self.h + self.resizer_h
        
    def _create_builder(self):
        b = BuilderForPreview()
        for p in self._resource_paths:
            b.add_resource_path(p)
        return b

    def _create_shapes(self):
        # Preview box
        c = self.canvas
        x, y, x2, y2 = (-1001, -1000, -1001, -1000)
        s1 = c.create_rectangle(x, y, x2, y2,
                                width=2, outline='blue', tags=self.id)
        s2 = c.create_rectangle(x, y, x2, y2, fill='blue', outline='blue',
                                tags=(self.id, 'resizer'))
        s3 = c.create_text(x, y, text='widget_id', anchor=tk.NW,
                           fill='white', tags=self.id)
        s4 = c.create_window(x, y, anchor=tk.NW, tags=self.id)
        self.shapes = {
            'outline': s1,
            'resizer': s2,
            'text': s3,
            'window': s4
        }
        self.draw()

    def erase(self):
        self.canvas_window.destroy()
        for key, sid in self.shapes.items():
            self.canvas.delete(sid)

    def draw(self):
        c = self.canvas
        x, y, x2, y2 = (self.x, self.y, self.x + self.w, self.y + self.h)
        c.coords(self.shapes['outline'], x, y, x2, y2)
        tbbox = c.bbox(self.shapes['text'])
        tw, th = tbbox[2] - tbbox[0] + 10, tbbox[3] - tbbox[1] + 6
        self.resizer_h = th
        rx2 = self.x + self.w
        ry2 = self.y + self.h + self.resizer_h
        rx = rx2 - tw
        ry = self.y + self.h
        c.coords(self.shapes['resizer'], rx, ry, rx2, ry2)
        tx = rx + 5
        ty = ry + 3
        c.coords(self.shapes['text'], tx, ty)
        c.coords(self.shapes['window'], x, y)

    def move_by(self, dx, dy):
        self.x += dx
        self.y += dy
        self.draw()

    def resize_to(self, w, h):
        self.resize_by(w - self.w, h - self.h)

    def resize_by(self, dw, dh):
        new_w = self.w + dw
        new_h = self.h + dh
        changed = False
        if new_w >= self.min_w:
            self.w = new_w
            changed = True
        if new_h >= self.min_h:
            self.h = new_h
            changed = True
        if changed:
            self.draw()
            self._resize_preview_window()

    def _resize_preview_window(self):
        if self.canvas_window:
            self.canvas_window.configure(width=self.w, height=self.h)

    def update(self, widget_id, xmlnode):
        # delete current preview
        # FIXME maybe do something to update preview without re-creating all ?
        del self.builder
        self.builder = None
        self.canvas.itemconfigure(self.shapes['window'], window='')
        if self.canvas_window:
            self.canvas_window.destroy()

        # Create preview
        canvas_window = ttk.Frame(self.canvas)
        canvas_window.rowconfigure(0, weight=1)
        canvas_window.columnconfigure(0, weight=1)

        self.canvas.itemconfigure(self.shapes['text'], text=widget_id)

        self._preview_widget = \
            self.create_preview_widget(canvas_window, widget_id, xmlnode)

        self.canvas_window = canvas_window
        self.canvas.itemconfigure(self.shapes['window'], window=canvas_window)
        canvas_window.update_idletasks()
        canvas_window.grid_propagate(0)
        self.min_w = self._get_wreqwidth()
        self.min_h = self._get_wreqheight()
        self.w = self.min_w * 2
        self.h = self.min_h * 2
        self.resize_to(self.min_w, self.min_h)

    def create_preview_widget(self, parent, widget_id, xmlnode):
        self.builder = self._create_builder()
        self.builder.add_from_xmlnode(xmlnode)
        widget = self.builder.get_object(widget_id, parent)
        return widget

    def get_widget_by_id(self, widget_id):
        return self.builder.get_object(widget_id)

    def create_toplevel(self, widget_id, xmlnode):
        # Create preview
        builder = pygubu.Builder()
        builder.add_from_xmlnode(xmlnode)
        top = tk.Toplevel(self.canvas)
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)
        builder.get_object(widget_id, top)
        return top

    def _get_wreqwidth(self):
        return self._preview_widget.winfo_reqwidth()

    def _get_wreqheight(self):
        return self._preview_widget.winfo_reqheight()


class DefaultMenuPreview(Preview):

    def create_preview_widget(self, parent, widget_id, xmlnode):
        self.builder = self._create_builder()
        self.builder.add_from_xmlnode(xmlnode)
        menubutton = ttk.Menubutton(parent, text='Menu preview')
        menubutton.grid()
        widget = self.builder.get_object(widget_id, menubutton)
        menubutton.configure(menu=widget)
        return menubutton

    def create_toplevel(self, widget_id, xmlnode):
        # Create preview
        builder = pygubu.Builder()
        builder.add_from_xmlnode(xmlnode)
        top = tk.Toplevel(self.canvas)
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

        menu = builder.get_object(widget_id, top)
        top['menu'] = menu
        return top

    def resize_by(self, dw, hw):
        return


class OnCanvasMenuPreview(Preview):
    fonts = {}

    def __init__(self, id_, canvas, x=0, y=0, rpaths=None):
        super(OnCanvasMenuPreview, self).__init__(id_, canvas, x, y, rpaths)
        self._menu = None
        self._cwidth = 0
        self._cheight = 0

    def _get_wreqwidth(self):
        return self._cwidth

    def _get_wreqheight(self):
        return self._cheight

    def _get_font(self, font):
        fontname = family = 'TkMenuFont'
        size = 12
        modifiers = ''
        tclobject = False

        if font and isinstance(font, basestring):
            fontname = family = font
        elif isinstance(font, tk._tkinter.Tcl_Obj):
            fontname = family = str(font)
            tclobject = True
        elif isinstance(font, tuple):
            fontname = str(font[4])
            tclobject = True
        if tclobject:
            s = RE_FONT.search(fontname)
            if s:
                g = s.groupdict()
                family = g['family'].replace('{', '').replace('}', '')
                size = g['size']
                modifiers = g['modifiers'] if g['modifiers'] else ''
        if fontname not in OnCanvasMenuPreview.fonts:
            weight = 'bold' if 'bold' in modifiers else 'normal'
            slant = 'italic' if 'italic' in modifiers else 'roman'
            underline = '1' if 'underline' in modifiers else '0'
            overstrike = '1' if 'overstrike' in modifiers else '0'
            kw = {'family': family, 'weight': weight, 'slant': slant,
                  'underline': underline, 'overstrike': overstrike}
            if size:
                kw['size'] = size
            OnCanvasMenuPreview.fonts[fontname] = tk.font.Font(**kw)
        return OnCanvasMenuPreview.fonts[fontname]

    def _calculate_menu_wh(self):
        """ Calculate menu widht and height."""
        w = iw = 50
        h = ih = 0
        # menu.index returns None if there are no choices
        index = self._menu.index(tk.END)
        index = index if index is not None else 0
        count = index + 1

        # First calculate using the font paramters of root menu:
        font = self._menu.cget('font')
        font = self._get_font(font)
        for i in range(0, count):
            mtype = self._menu.type(i)
            if mtype == 'tearoff':
                continue
            label = 'default'
            ifont = 'TkMenuFont'
            if mtype != 'separator':
                label = self._menu.entrycget(i, 'label')
                ifont = self._menu.entrycget(i, 'font')
            wpx = font.measure(label)
            hpx = font.metrics('linespace')
            w += wpx
            if hpx > h:
                h = hpx * 2
            # Calculate using font configured for each subitem
            ifont = self._get_font(ifont)
            wpx = ifont.measure(label)
            hpx = ifont.metrics('linespace')
            iw += wpx
            if hpx > ih:
                ih = hpx * 2
        # Then compare 2 sizes and use the greatest
        w = max(w, iw, 100)
        h = max(h, ih, 25)
        self._cwidth = w + int(w * 0.25)
        self._cheight = h + int(h * 0.25)

    def create_preview_widget(self, parent, widget_id, xmlnode):
        container = tk.Frame(parent, container=True, height=50)
        container.grid(sticky='nswe')
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self._top = top = tk.Toplevel(parent, use=container.winfo_id())
        top.maxsize(2048, 50)
        top.resizable(width=True, height=False)
        top.update()

        self.builder = self._create_builder()
        self.builder.add_from_xmlnode(xmlnode)
        self._menu = widget = self.builder.get_object(widget_id, top)
        top.configure(menu=widget)
        self._calculate_menu_wh()
        return parent

    def create_toplevel(self, widget_id, xmlnode):
        # Create preview
        builder = pygubu.Builder()
        builder.add_from_xmlnode(xmlnode)
        top = tk.Toplevel(self.canvas)
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

        menu = builder.get_object(widget_id, top)
        top['menu'] = menu
        return top


MenuPreview = DefaultMenuPreview
if sys.platform == 'linux':
    MenuPreview = OnCanvasMenuPreview


class ToplevelPreview(Preview):

    def create_preview_widget(self, parent, widget_id, xmlnode):
        xmlnode.set('class', 'pygubudesigner.ToplevelFramePreview')
        layout = ET.Element('layout')
        for n, v in (('row', '0'), ('column', '0'), ('sticky', 'nsew')):
            p = ET.Element('property')
            p.set('name', n)
            p.text = v
            layout.append(p)
        xmlnode.append(layout)
        # print(ET.tostring(xmlnode))
        self.builder = self._create_builder()
        self.builder.add_from_xmlnode(xmlnode)
        widget = self.builder.get_object(widget_id, parent)
        return widget

    def create_toplevel(self, widget_id, xmlnode):
        # Create preview
        builder = pygubu.Builder()
        builder.add_from_xmlnode(xmlnode)
        top = builder.get_object(widget_id, self.canvas)
        return top


class DialogPreview(ToplevelPreview):
    def create_toplevel(self, widget_id, xmlnode):
        top = super(DialogPreview, self).create_toplevel(widget_id, xmlnode)
        top.run()
        return top


#    def get_widget_by_id(self, widget_id):
#        return self.canvas_window


class PreviewHelper:
    indicators_tag = ('nw', 'ne', 'sw', 'se')

    def __init__(self, canvas):
        self.canvas = canvas
        self.previews = OrderedDict()
        self.padding = 20
        self.indicators = None
        self._sel_id = None
        self._sel_widget = None
        self.toplevel_previews = []
        self.resource_paths = []

        self._moving = False
        self._last_event = None
        self._objects_moving = None
        canvas.bind('<Button-1>', self.click_handler)
        canvas.bind('<ButtonRelease-1>', self.release_handler)
        canvas.bind('<Motion>', self.motion_handler)
        canvas.bind('<4>', lambda event: canvas.yview('scroll', -1, 'units'))
        canvas.bind('<5>', lambda event: canvas.yview('scroll', 1, 'units'))
        self._create_indicators()
        
    def add_resource_path(self, path):
        self._resource_paths.append(path)

    def motion_handler(self, event):
        if not self._moving:
            c = event.widget
            x = c.canvasx(event.x)
            y = c.canvasy(event.y)
            if self._over_resizer(x, y):
                c.configure(cursor='fleur')
            else:
                c.configure(cursor='')
        else:
            dx = event.x - self._last_event.x
            dy = event.y - self._last_event.y
            self._last_event = event
            if dx or dy:
                self.resize_preview(dx, dy)

    def click_handler(self, event):
        c = event.widget
        x = c.canvasx(event.x)
        y = c.canvasy(event.y)

        if self._over_resizer(x, y):
            ids = c.find_overlapping(x, y, x, y)
            if ids:
                self._moving = True
                self._objects_moving = ids
                c.configure(cursor='fleur')
                self._last_event = event

    def release_handler(self, event):
        self._objects_moving = None
        self._moving = False

    def _over_resizer(self, x, y):
        "Returns True if mouse is over a resizer"

        over_resizer = False
        c = self.canvas
        ids = c.find_overlapping(x, y, x, y)
        if ids:
            o = ids[0]
            tags = c.gettags(o)
            if 'resizer' in tags:
                over_resizer = True
        return over_resizer

    def resize_preview(self, dw, dh):
        "Resizes preview that is currently dragged"

        # identify preview
        if self._objects_moving:
            id_ = self._objects_moving[0]
            tags = self.canvas.gettags(id_)
            for tag in tags:
                if tag.startswith('preview_'):
                    _, ident = tag.split('preview_')
                    preview = self.previews[ident]
                    preview.resize_by(dw, dh)
                    self.move_previews()
                    break
        self._update_cregion()

    def _update_cregion(self):
        # update canvas scrollregion
        bbox = self.canvas.bbox(tk.ALL)
        padd = 20
        if bbox is not None:
            region = (0, 0, bbox[2] + padd, bbox[3] + padd)
            self.canvas.configure(scrollregion=region)

    def move_previews(self):
        "Move previews after a resize event"

        # calculate new positions
        min_y = self._calc_preview_ypos()
        for idx, (key, p) in enumerate(self.previews.items()):
            new_dy = min_y[idx] - p.y
            self.previews[key].move_by(0, new_dy)
        self._update_cregion()
        self.show_selected(self._sel_id, self._sel_widget)

    def _calc_preview_ypos(self):
        "Calculates the previews positions on canvas"

        y = 10
        min_y = [y]
        for k, p in self.previews.items():
            y += p.height() + self.padding
            min_y.append(y)
        return min_y

    def _get_slot(self):
        "Returns the next coordinates for a preview"

        x = y = 10
        for k, p in self.previews.items():
            y += p.height() + self.padding
        return x, y

    def draw(self, identifier, widget_id, xmlnode, wclass):
        preview_class = Preview
        if wclass == 'tk.Menu':
            preview_class = MenuPreview
        elif wclass == 'tk.Toplevel':
            preview_class = ToplevelPreview
        elif wclass == 'pygubu.builder.widgets.dialog':
            preview_class = DialogPreview
        if identifier not in self.previews:
            x, y = self._get_slot()
            self.previews[identifier] = preview \
                = preview_class(identifier, self.canvas, x, y,
                                self.resource_paths)
        else:
            preview = self.previews[identifier]
        preview.update(widget_id, xmlnode)
        self.reset_selected(identifier)
        self.move_previews()

    def _create_indicators(self):
        # selected indicators
        self.indicators = []
        anchors = {'nw': tk.SE, 'ne': tk.SW, 'sw': tk.NE, 'se': tk.NW}
        for sufix in self.indicators_tag:
            label = tk.Label(self.canvas,
                             image=StockImage.get('indicator_' + sufix))
            self.indicators.append(label)
            self.canvas.create_window(-10, -10, anchor=anchors[sufix],
                                      window=label, tags=sufix)

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
        x, y = self.canvas.canvasx(x), self.canvas.canvasy(y)
        return (x, y)

    def show_selected(self, identifier, selected_id=None):
        canvas = self.canvas
        if selected_id is None:
            for indicator in self.indicators_tag:
                canvas.itemconfigure(indicator, state=tk.HIDDEN)
        elif identifier in self.previews:
            for indicator in self.indicators_tag:
                canvas.itemconfigure(indicator, state=tk.NORMAL)
            preview = self.previews[identifier]
            canvas.update_idletasks()
            widget = preview.get_widget_by_id(selected_id)
            for indicatorw in self.indicators:
                try:
                    indicatorw.lift(widget)
                except tk.TclError:
                    pass
            for tag in self.indicators_tag:
                x, y = self._calculate_indicator_coords(tag, widget)
                ox, oy = canvas.coords(tag)
                canvas.move(tag, x - ox, y - oy)
        self._sel_id = identifier
        self._sel_widget = selected_id

    def delete(self, identifier):
        if identifier in self.previews:
            preview = self.previews[identifier]
            preview.erase()
            del self.previews[identifier]
            self.reset_selected(identifier)
            self.move_previews()

    def reset_selected(self, identifier):
        if identifier == self._sel_id:
            self._sel_id = None
            self._sel_widget = None

    def remove_all(self):
        for identifier in list(self.previews):
            self.delete(identifier)
        self.resource_paths = []

    def preview_in_toplevel(self, identifier, widget_id, xmlnode):
        preview = self.previews[identifier]
        top = preview.create_toplevel(widget_id, xmlnode)
        self.toplevel_previews.append(top)

    def close_toplevel_previews(self):
        for top in self.toplevel_previews:
            top.destroy()
        self.toplevel_previews = []
