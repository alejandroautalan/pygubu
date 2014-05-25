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
from __future__ import unicode_literals, print_function
from collections import defaultdict

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

import os, sys
tpath = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
sys.path.insert(0, tpath)

import itertools

from pygubu import builder
from pygubudesigner.widgets import *
from pygubudesigner import properties
from pygubudesigner.i18n import translator as _

CLASS_MAP = builder.CLASS_MAP


class PropertiesEditor(object):
    def __init__(self, frame):
        self._current = None
        self._frame = frame
        self._propbag = {}
        self._create_properties()
        self.hide_all()

    def _create_properties(self):
        """Populate a frame with a list of all editable properties"""
        label_tpl = "{0}:"
        row = 0
        col = 0

        groups = (
            (_('Required'), properties.WIDGET_REQUIRED_OPTIONS),
            (_('Standard'), properties.WIDGET_STANDARD_OPTIONS),
            (_('Specific'), properties.WIDGET_SPECIFIC_OPTIONS),
            (_('Custom'), properties.WIDGET_CUSTOM_OPTIONS)
        )

        for gname, group in groups:
            padding = '0 0 0 5' if row == 0 else '0 5 0 5'
            label = ttk.Label(self._frame, text=gname,
                              font='TkDefaultFont 10 bold', padding=padding,
                              foreground='#000059')
            label.grid(row=row, column=0, sticky='we', columnspan=2)
            row += 1
            for name, kwdata in group:
                labeltext = label_tpl.format(name)
                label = ttk.Label(self._frame, text=labeltext, anchor=tk.W)
                label.grid(row=row, column=col, sticky=tk.EW, pady=2)
                widget = self._create_editor(self._frame, name, kwdata)
                widget.grid(row=row, column=col+1, sticky=tk.EW, pady=2)
                row += 1
                self._propbag[name] = (label, widget)

    def _create_editor(self, master, pname, wdata):
        editor = None
        wtype = wdata.get('editor', None)

        #I don't have class name at this moment
        #so setup class specific values on update_property_widget
        if wtype == 'entry':
            editor = EntryPropertyEditor(master)
        elif wtype == 'text':
            editor = TextPropertyEditor(master)
        elif wtype == 'choice':
            editor = ChoicePropertyEditor(master)
        elif wtype == 'spinbox':
            editor = SpinboxPropertyEditor(master)
        elif wtype == 'tkvarentry':
            editor = TkVarPropertyEditor(master)
        else:
            editor = EntryPropertyEditor(master)

        def make_on_change_cb(pname, editor):
            def on_change_cb(event):
                self._on_property_changed(pname, editor)
            return on_change_cb

        editor.bind('<<PropertyChanged>>', make_on_change_cb(pname, editor))
        return editor

    def _on_property_changed(self, name, editor):
        print(editor.value)

    def update_editor(self, editor, wdescr, pname, propdescr):
        pdescr = propdescr.copy()
        classname = wdescr.get_class()

        if classname in pdescr:
            pdescr = dict(pdescr, **pdescr[classname])
            
        params = pdescr.get('params', {})
        # print('pname:?', pname, ' Params:?', params)
        # print('pname:?', pname, ' editor:?', repr(editor))
        editor.parameters(**params)
        default = pdescr.get('default', '')

        value = wdescr.get_property(pname)
        if not value and default:
            value = default
        editor.edit(value)

    def edit(self, wdescr):
        wclass = wdescr.get_class()
        class_props = CLASS_MAP[wclass].classobj.properties
        allprops = itertools.chain(properties.WIDGET_REQUIRED_OPTIONS,
                                   properties.WIDGET_STANDARD_OPTIONS,
                                   properties.WIDGET_SPECIFIC_OPTIONS)
        for name, propdescr in allprops:
            label, widget = self._propbag[name]
            if name in properties.WIDGET_REQUIRED_PROPERTIES \
               or name in class_props:
                self.update_editor(widget, wdescr, name, propdescr)
                label.grid()
                widget.grid()
            else:
                #hide property widget
                label.grid_remove()
                widget.grid_remove()

    def hide_all(self):
        """Hide all properties from property editor."""
        self.current = None

        for _, (label, widget) in self._propbag.items():
            label.grid_remove()
            widget.grid_remove()


class LayoutEditor(object):
    def __init__(self, frame):
        w = ttk.Label(frame, text='Layout')
        w.grid()


class BindingsEditor(object):
    def __init__(self, treeview):
        pass


class WidgetEditor(object):

    def __init__(self, propsframe, layoutframe, bindingstree):
        self.properities_editor = PropertiesEditor(propsframe)
        self.layout_editor = LayoutEditor(layoutframe)
        self.bindings_editor = BindingsEditor(bindingstree)

    def edit(self, wdescr):
        self.properities_editor.edit(wdescr)

    def hide_all(self):
        self.properities_editor.hide_all()


if __name__ == '__main__':
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    pframe = ttk.LabelFrame(root, text='Properties')
    pframe.grid(row=0, column=0)
    lframe = ttk.LabelFrame(root, text='Layout')
    lframe.grid(row=0, column=1)
    bframe = ttk.LabelFrame(root, text='Bindings')
    bframe.grid(row=0, column=2)
    editor = WidgetEditor(pframe, lframe, bframe)

    root.mainloop()
