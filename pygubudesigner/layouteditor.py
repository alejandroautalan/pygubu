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

from __future__ import unicode_literals, print_function

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
from pygubudesigner.propertieseditor import PropertiesEditor

CLASS_MAP = builder.CLASS_MAP


class LayoutEditor(PropertiesEditor):

    def _create_properties(self):
        """Populate a frame with a list of all editable properties"""
        self._rcbag = {}  # bag for row/column prop editors
        self._fgrid = f = ttk.Labelframe(self._sframe.innerframe,
                                         text=_('Grid options:'), padding=5)
        f.grid(sticky='nswe')
        #  hack to resize correctly when properties are hidden
        label = ttk.Label(f)
        label.grid()

        label_tpl = "{0}:"
        row = 0
        col = 0

        groups = (
            ('00', properties.GRID_PROPERTIES, properties.LAYOUT_OPTIONS),
        )

        for gcode, plist, propdescr in groups:
            for name in plist:
                kwdata = propdescr[name]
                labeltext = label_tpl.format(name)
                label = ttk.Label(self._fgrid, text=labeltext, anchor=tk.W)
                label.grid(row=row, column=col, sticky=tk.EW, pady=2)
                widget = self._create_editor(self._fgrid, name, kwdata)
                widget.grid(row=row, column=col+1, sticky=tk.EW, pady=2)
                row += 1
                self._propbag[gcode+name] = (label, widget)

        # Grid row/col properties
        #labels
        gcode = '01'
        self._fgrc = fgrc = ttk.LabelFrame(self._sframe.innerframe,
                                           text=_('Grid row/column options:'),
                                           padding=5)
        fgrc.grid(row=1, column=0, sticky=tk.NSEW, pady='10 0')

        #hack to resize correctly when properties are hidden
        label = ttk.Label(fgrc)
        label.grid()

        row = col = 0
        icol = 1
        headers = []
        for pname in properties.GRID_RC_PROPERTIES:
            label = ttk.Label(fgrc, text=pname)
            label.grid(row=row, column=icol)
            headers.append(label)
            icol += 1
        self._internal = {'grc_headers': headers}

        #
        name_format = '{}_{}_{}'  # {row/column}_{number}_{name}
        MAX_RC = 50
        #rowconfig
        row += 1
        trow_label = _('Row {0}:')
        tcol_label = _('Column {0}:')
        for index in range(0, MAX_RC):
            labeltext = trow_label.format(index)
            label = ttk.Label(fgrc, text=labeltext)
            label.grid(row=row, column=0)

            labeltext = tcol_label.format(index)
            labelc = ttk.Label(fgrc, text=labeltext)
            labelc.grid(row=row + MAX_RC, column=0, sticky=tk.E, pady=2)

            icol = 1
            for pname in properties.GRID_RC_PROPERTIES:
                kwdata = properties.LAYOUT_OPTIONS[pname]

                alias = name_format.format('row', index, pname)
                widget = self._create_editor(fgrc, alias, kwdata)
                widget.grid(row=row, column=icol, pady=2, sticky='ew')
                self._rcbag[alias] = (label, widget)

                alias = name_format.format('column', index, pname)
                widget = self._create_editor(fgrc, alias, kwdata)
                widget.grid(row=row + MAX_RC, column=icol, pady=2, sticky='ew')
                self._rcbag[alias] = (labelc, widget)

                icol += 1
            row += 1

    def edit(self, wdescr):
        self._current = wdescr
        max_row = wdescr.max_row
        max_col = wdescr.max_col
        wclass = wdescr.get_class()
        class_descr = CLASS_MAP[wclass].builder
        max_children = CLASS_MAP[wclass].builder.maxchildren
        max_children = 0 if max_children is None else max_children
        is_container = CLASS_MAP[wclass].builder.container
        layout_required = CLASS_MAP[wclass].builder.layout_required
        allow_container_layout = CLASS_MAP[wclass].builder.allow_container_layout
        show_layout = layout_required

        #grid layout properties
        groups = (
            ('00', properties.GRID_PROPERTIES, properties.LAYOUT_OPTIONS),
        )

        for gcode, proplist, gproperties in groups:
            for name in proplist:
                propdescr = gproperties[name]
                label, widget = self._propbag[gcode + name]
                if show_layout:
                    self.update_editor(widget, wdescr, name, propdescr)
                    label.grid()
                    widget.grid()
                else:
                    label.grid_remove()
                    widget.grid_remove()

        show_layout = (is_container
                       and layout_required
                       and allow_container_layout
                       and max_children != 1)
        show_headers = False

        for key in self._rcbag:
            rowcol, number, name = self.identify_gridrc_property(key)
            number_str = str(number)
            number = int(number)
            propdescr = properties.LAYOUT_OPTIONS[name]
            if show_layout and rowcol == 'row' and number <= max_row:
                label, widget = self._rcbag[key]
                self.update_rc_editor(rowcol, number, widget,
                                      wdescr, name, propdescr)
                label.grid()
                widget.grid()
                show_headers = True
            elif show_layout and rowcol == 'column' and number <= max_col:
                label, widget = self._rcbag[key]
                self.update_rc_editor(rowcol, number, widget,
                                      wdescr, name, propdescr)
                label.grid()
                widget.grid()
                show_headers = True
            else:
                label, widget = self._rcbag[key]
                label.grid_remove()
                widget.grid_remove()

        for widget in self._internal['grc_headers']:
            if show_headers:
                widget.grid()
            else:
                widget.grid_remove()

        self._sframe.reposition()

    def _on_property_changed(self, name, editor):
        value = editor.value
        if name in properties.GRID_PROPERTIES:
            self._current.set_layout_property(name, value)
        else:
            # asume that is a grid row/col property
            rowcol, number, pname = self.identify_gridrc_property(name)
            if rowcol == 'row':
                self._current.set_grid_row_property(number, pname, value)
            else:
                self._current.set_grid_col_property(number, pname, value)

    def identify_gridrc_property(self, alias):
        return alias.split('_')

    def update_editor(self, editor, wdescr, pname, propdescr):
        pdescr = propdescr.copy()
        classname = wdescr.get_class()

        if classname in pdescr:
            pdescr = dict(pdescr, **pdescr[classname])

        params = pdescr.get('params', {})
        editor.parameters(**params)
        default = pdescr.get('default', '')

        value = wdescr.get_layout_property(pname)
        if not value and default:
            value = default
        editor.edit(value)

    def update_rc_editor(self, type_, index, editor, wdescr, pname, propdescr):
        pdescr = propdescr.copy()
        classname = wdescr.get_class()

        if classname in pdescr:
            pdescr = dict(pdescr, **pdescr[classname])

        params = pdescr.get('params', {})
        editor.parameters(**params)
        default = pdescr.get('default', '')

        value = ''
        if type_ == 'row':
            value = wdescr.get_grid_row_property(str(index), pname)
        else:
            value = wdescr.get_grid_col_property(str(index), pname)
        if not value and default:
            value = default
        editor.edit(value)

    def hide_all(self):
        super(LayoutEditor, self).hide_all()

        for _v, (label, widget) in self._rcbag.items():
            label.grid_remove()
            widget.grid_remove()
        
        for h in self._internal['grc_headers']:
            h.grid_remove()

