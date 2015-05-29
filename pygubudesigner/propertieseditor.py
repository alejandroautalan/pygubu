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
import logging

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubu import builder
from pygubudesigner.widgets.propertyeditor import create_editor
from pygubudesigner import properties
from pygubudesigner.i18n import translator as _

logger = logging.getLogger(__name__)
CLASS_MAP = builder.CLASS_MAP


class PropertiesEditor(object):
    def __init__(self, frame):
        self._current = None
        self._sframe = frame
        self._frame = None
        self._propbag = {}
        self._create_properties()
        self.hide_all()

    def _create_properties(self):
        """Populate a frame with a list of all editable properties"""
        self._frame = f = ttk.Labelframe(self._sframe.innerframe,
                                         text=_('Widget properties'))
        f.grid(sticky='nswe')

        label_tpl = "{0}:"
        row = 0
        col = 0

        groups = (
            ('00', _('Required'), properties.WIDGET_REQUIRED_OPTIONS,
             properties.REQUIRED_OPTIONS),
            ('01', _('Standard'), properties.WIDGET_STANDARD_OPTIONS,
             properties.TK_WIDGET_OPTIONS),
            ('02', _('Specific'), properties.WIDGET_SPECIFIC_OPTIONS,
             properties.TK_WIDGET_OPTIONS),
            ('03', _('Custom'), properties.WIDGET_CUSTOM_OPTIONS,
             properties.CUSTOM_OPTIONS),
        )

        for gcode, gname, plist, propdescr in groups:
            padding = '0 0 0 5' if row == 0 else '0 5 0 5'
            label = ttk.Label(self._frame, text=gname,
                              font='TkDefaultFont 10 bold', padding=padding,
                              foreground='#000059')
            label.grid(row=row, column=0, sticky='we', columnspan=2)
            row += 1
            for name in plist:
                kwdata = propdescr[name]
                labeltext = label_tpl.format(name)
                label = ttk.Label(self._frame, text=labeltext, anchor=tk.W)
                label.grid(row=row, column=col, sticky=tk.EW, pady=2)
                widget = self._create_editor(self._frame, name, kwdata)
                widget.grid(row=row, column=col+1, sticky=tk.EW, pady=2)
                row += 1
                self._propbag[gcode+name] = (label, widget)
                logger.debug('Created property: {0}-{1}'.format(gname,name))

    def _create_editor(self, master, pname, wdata):
        editor = None
        wtype = wdata.get('editor', None)

        #I don't have class name at this moment
        #so setup class specific values on update_property_widget
        editor = create_editor(wtype, master)

        def make_on_change_cb(pname, editor):
            def on_change_cb(event):
                self._on_property_changed(pname, editor)
            return on_change_cb

        editor.bind('<<PropertyChanged>>', make_on_change_cb(pname, editor))
        return editor

    def _on_property_changed(self, name, editor):
        self._current.set_property(name, editor.value)

    def update_editor(self, editor, wdescr, pname, propdescr):
        pdescr = propdescr.copy()
        classname = wdescr.get_class()

        if classname in pdescr:
            pdescr = dict(pdescr, **pdescr[classname])

        params = pdescr.get('params', {})
        editor.parameters(**params)
        default = pdescr.get('default', '')

        value = wdescr.get_property(pname)
        if not value and default:
            value = default
        editor.edit(value)

    def edit(self, wdescr):
        self._current = wdescr
        wclass = wdescr.get_class()
        class_descr = CLASS_MAP[wclass].builder
        
        # GroupCode, PropertyType, dict, tuple
        groups = (
            ('00', None, properties.WIDGET_REQUIRED_OPTIONS,
             properties.REQUIRED_OPTIONS),
            ('01', 'OPTIONS_STANDARD', properties.WIDGET_STANDARD_OPTIONS,
             properties.TK_WIDGET_OPTIONS),
            ('02', 'OPTIONS_SPECIFIC', properties.WIDGET_SPECIFIC_OPTIONS,
             properties.TK_WIDGET_OPTIONS),
            ('03', 'OPTIONS_CUSTOM', properties.WIDGET_CUSTOM_OPTIONS,
             properties.CUSTOM_OPTIONS)
        )
        for gcode, attrname, proplist, gproperties in groups:
            for name in proplist:
                propdescr = gproperties[name]
                label, widget = self._propbag[gcode + name]
                if gcode == '00' or name in getattr(class_descr, attrname):
                    self.update_editor(widget, wdescr, name, propdescr)
                    label.grid()
                    widget.grid()
                else:
                    #hide property widget
                    label.grid_remove()
                    widget.grid_remove()
        self._sframe.reposition()

    def hide_all(self):
        """Hide all properties from property editor."""
        self.current = None

        for _v, (label, widget) in self._propbag.items():
            label.grid_remove()
            widget.grid_remove()
