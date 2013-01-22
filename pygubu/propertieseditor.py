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

import re
from collections import defaultdict
import tkinter
from tkinter import ttk

from . import util
from . import builder
from . import properties
from .util.textentry import Textentry


CLASS_MAP = builder.CLASS_MAP

FLOAT_RE = re.compile(r'[+-]?(\d+(\.\d*)?)')

class PropertiesArray(util.ArrayVar):

    def __init__(self, master=None, value=None, name=None):
        super(util.ArrayVar, self).__init__(master, value, name)
        self._callback = None
        self._cbhandler = None

    def get_property_variable(self, group, name):
        if group not in properties.GROUPS:
            raise ValueError('Invalid group value')
        return self.__call__(group + name)

    def identify_property(self, element):
        result = (None, None)
        for groupname in properties.GROUPS:
            if element.startswith(groupname):
                result = (groupname, element.replace(groupname, ''))
                break
        return result

    def set_callback(self, callback):
        self._callback = callback
        self._cbhandler = None

    def enable_cb(self):
        if self._callback is not None:
            self._cbhandler = self.trace(mode="w", callback=self._callback)

    def disable_cb(self):
        if self._cbhandler is not None:
            self.trace_vdelete("w", self._cbhandler)


class WidgetPropertiesEditor:

    def __init__(self, app):
        self.app = app
        self.treeview = app.treeview
        self.propsframe = app.widget_props_frame
        self.packingframe = app.packing_props_frame
        self.arrayvar = PropertiesArray()
        self.prop_widget = {
            properties.GROUP_WIDGET: {},
            properties.GROUP_LAYOUT_GRID: {},
            properties.GROUP_LAYOUT_GRID_RC: {},
            properties.GROUP_CUSTOM: {},
            'internal': {}
        }
        #register validators
        tkwidget = self.treeview
        self.validators = {
            'number_integer': (tkwidget.register(self.validator_integer),
                '%d', '%P'),
            'number_float': (tkwidget.register(self.validator_float),
                '%d', '%P')
        }
        self.create_properties()
        self.create_grid_layout_editor()
        self.hide_all()
        self.arrayvar.set_callback(self.on_array_variable_changed)

        self.treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)


    def validator_integer(self, action, newvalue):
        valid = False
        if action == '1': #1: insert 0: delete
            valid = str(newvalue).isnumeric()
        else:
            valid = True
        return valid


    def validator_float(self, action, newvalue):
        valid = False
        if action == '1': #1: insert 0: delete
            match = FLOAT_RE.match(newvalue)
            if match is not None:
                valid = True
        else:
            valid = True
        return valid


    def create_properties(self):
        """Populate a frame with a list of all editable properties"""

        editor_frame = self.propsframe.innerframe
        prop_widget = self.prop_widget
        row=0
        col=0
        label_tpl = "{0}:"
        for name in properties.PropertiesMap[properties.GROUP_CUSTOM]:
            labeltext = label_tpl.format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_property_widget(editor_frame,
                properties.GROUP_CUSTOM, name)
            label.grid(row=row, column=col, sticky=tkinter.EW, pady=2)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW, pady=2)
            row += 1
            prop_widget[properties.GROUP_CUSTOM][name] = (label, widget)

        for name in properties.PropertiesMap[properties.GROUP_WIDGET]:
            labeltext = label_tpl.format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_property_widget(editor_frame,
                properties.GROUP_WIDGET, name)
            label.grid(row=row, column=col, sticky=tkinter.EW, pady=2)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW, pady=2)
            row += 1
            prop_widget[properties.GROUP_WIDGET][name] = (label, widget)


    def create_grid_layout_editor(self):
        master = self.packingframe.innerframe
        prop_widget = self.prop_widget
        frame = ttk.LabelFrame(master, text='Grid options:')
        label_tpl = "{0}:"
        row= col=0
        for name in properties.PropertiesMap[properties.GROUP_LAYOUT_GRID]:
            labeltext = label_tpl.format(name)
            label = ttk.Label(frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_property_widget(frame,
                properties.GROUP_LAYOUT_GRID, name)
            label.grid(row=row, column=col, sticky=tkinter.EW, pady=2)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW, pady=2)
            row += 1
            prop_widget[properties.GROUP_LAYOUT_GRID][name] = (label, widget)

        frame.grid(row=0, column=0)

        #labels
        group = properties.GROUP_LAYOUT_GRID_RC
        frame = ttk.LabelFrame(master, text='Grid row/column options:')
        row = col = 0
        icol = 1
        headers=[]
        for pname in properties.PropertiesMap[group]:
            label = ttk.Label(frame, text=pname)
            label.grid(row=row, column=icol)
            headers.append(label)
            icol += 1
        prop_widget['internal']['grid_rc_headers']= headers

        #
        name_format = '{}_{}_{}' #{row/column}_{number}_{name}
        max_rc = 50
        #rowconfig
        row += 1
        for index in range(0, max_rc):
            labeltext = 'Row {}:'.format(index)
            label = ttk.Label(frame, text=labeltext)
            label.grid(row=row, column=0)

            labeltext = 'Column {}:'.format(index)
            labelc = ttk.Label(frame, text=labeltext)
            labelc.grid(row=row+max_rc, column=0, sticky=tkinter.E, pady=2)

            icol = 1
            for pname in properties.PropertiesMap[group]:
                alias = name_format.format('row', index, pname)
                widget = self.create_grid_rc_widget(frame, pname, alias)
                widget.grid(row=row, column=icol, pady=2)
                prop_widget[group][alias]= (label, widget)

                alias = name_format.format('column', index, pname)
                widget = self.create_grid_rc_widget(frame, pname, alias)
                widget.grid(row=row+max_rc, column=icol, pady=2)
                prop_widget[group][alias]= (labelc, widget)

                icol += 1
            row +=1

        frame.grid(row=1, column=0, sticky=tkinter.NSEW)


    def create_grid_rc_widget(self, master, name, alias):
        group = properties.GROUP_LAYOUT_GRID_RC
        widgetvar = self.arrayvar.get_property_variable(group, alias);
        wdata = {}
        widget = None
        if name in properties.PropertiesMap[group]:
            wdata = properties.PropertiesMap[group][name]
            wtype = wdata['input_method']

        widget = self.__create_widget(master, wdata, widgetvar)
        widget.configure(width=4)
        return widget


    def create_property_widget(self, master, group, propertyname):
        """Creates a ui widget to edit the property"""

        widgetvar = self.arrayvar.get_property_variable(group, propertyname);
        wdata = {}

        widget = None
        if propertyname in properties.PropertiesMap[group]:
            wdata = properties.PropertiesMap[group][propertyname]
            wtype = wdata['input_method']

        widget = self.__create_widget(master, wdata, widgetvar)
        return widget


    def __create_widget(self, master, wdata, widgetvar):
        widget = None
        wtype = wdata.get('input_method', None)
        default = wdata.get('default', '')

        #I don't have class name at this moment
        #so setup class specific values on update_property_widget
        if wtype == 'entry':
            readonly = wdata.get('readonly', False)
            state = tkinter.DISABLED if readonly else tkinter.NORMAL
            widget = ttk.Entry(master, textvariable=widgetvar, state=state)
        elif wtype == 'textentry':
            widget = Textentry(master, textvariable=widgetvar,
                width=20, height=3)
        elif wtype == 'colorentry':
            frame, _, _ = util.make_color_selector(master, widgetvar)
            widget = frame
        elif wtype == 'choice':
            widget = ttk.Combobox(master, textvariable=widgetvar,
                state='readonly')
            values = wdata.get('values', None)
            if values is not None:
                widget.configure(values=values)
        elif wtype == 'spinbox':
            widget = tkinter.Spinbox(master, textvariable=widgetvar)
            vmin = wdata.get('min', 0)
            vmax = wdata.get('max', 99)
            increment = wdata.get('increment', 1)
            default = vmin if (vmin > 0 and default == '') else default
            widget.configure(from_=vmin, to=vmax, increment=increment)
            #validator
            validator = wdata.get('validator', None)
            if validator is not None:
                widget.configure(validate='key',
                    validatecommand=self.validators[validator])
        else:
            widget = ttk.Entry(master, textvariable=widgetvar)
        widgetvar.set(default)

        return widget


    def hide_all(self):
        """Hide all properties from property editor."""

        for group in self.prop_widget:
            for pname in self.prop_widget[group]:
                for widget in self.prop_widget[group][pname]:
                    widget.grid_remove()


    def update_property_widget(self, group, widget, variable,
        propertyname, classname, data):
        """Update widget property value with values from data."""

        wdata = {}
        if propertyname in properties.PropertiesMap[group]:
            wdata = properties.PropertiesMap[group][propertyname]

        wtype = wdata.get('input_method', '')

        #merge description for specific class
        if classname in wdata:
            wdata = dict(wdata, **wdata[classname])

        default = wdata.get('default', '')
        if wtype == 'spinbox':
            vmin = wdata.get('min', 0)
            vmax = wdata.get('max', 99)
            default = vmin if (int(vmin) > 0 and default == '') else default
        if wtype == 'choice':
            values = wdata.get('values', None)
            if values is not None:
                widget.configure(values=values)

        #variable = self.arrayvar.get_property_variable(group, propertyname)

        if propertyname in data:
            value = data[propertyname]
            if not value:
                value = default
            variable.set(value)
        else:
            variable.set('')


    def edit(self, item):
        """Copies properties values from data to the
           properties editor so they can be edited."""

        #first disable callback
        self.arrayvar.disable_cb()

        data = self.app.tree_editor.treedata[item]
        wclass = data['class']
        class_props = tuple(CLASS_MAP[wclass].properties)

        group = properties.GROUP_CUSTOM
        for key in properties.PropertiesMap[group]:
            if (key in properties.OBJECT_DEFAULT_ATTRS or key in class_props):
                label, widget = self.prop_widget[group][key]
                variable = self.arrayvar.get_property_variable(group, key)
                self.update_property_widget(group, widget, variable,
                    key, wclass, data)
                label.grid()
                widget.grid()
            else:
                #hide property widget
                label, widget = self.prop_widget[group][key]
                label.grid_remove()
                widget.grid_remove()

        group = properties.GROUP_WIDGET
        for key in properties.PropertiesMap[group]:
            if key in class_props:
                label, widget = self.prop_widget[group][key]
                variable = self.arrayvar.get_property_variable(group, key)
                self.update_property_widget(group, widget, variable,
                    key, wclass, data)
                label.grid()
                widget.grid()
            else:
                #hide property widget
                label, widget = self.prop_widget[group][key]
                label.grid_remove()
                widget.grid_remove()

        #grid layout properties
        group = properties.GROUP_LAYOUT_GRID
        for gkey in properties.PropertiesMap[group]:
            label, widget = self.prop_widget[group][gkey]
            gdata = data.get('packing', {})
            variable = self.arrayvar.get_property_variable(group, gkey)
            self.update_property_widget(group, widget, variable, gkey,
                    wclass, gdata)
            label.grid()
            widget.grid()

        group = properties.GROUP_LAYOUT_GRID_RC
        max_row, max_col = self.get_max_row_col(item)
        show_headers = False
        is_container = CLASS_MAP[wclass].container
        for key in self.prop_widget[group]:
            rowcol, number, name = self.identify_gridrc_property(key)
            number_str = str(number)
            number = int(number)
            if is_container and rowcol == 'row' and number <= max_row:
                label, widget = self.prop_widget[group][key]
                gdata = data.get('packing', {})
                rcdata = gdata.get('rows',{}).get(number_str, {})
                variable = self.arrayvar.get_property_variable(group, key)
                self.update_property_widget(group, widget, variable, name,
                    wclass, rcdata)
                label.grid(); widget.grid()
                show_headers = True
            elif is_container and rowcol == 'column' and number <= max_col:
                label, widget = self.prop_widget[group][key]
                gdata = data.get('packing', {})
                rcdata = gdata.get('columns',{}).get(number_str, {})
                variable = self.arrayvar.get_property_variable(group, key)
                self.update_property_widget(group, widget, variable, name,
                    wclass, rcdata)
                label.grid(); widget.grid()
                show_headers = True
            else:
                label, widget = self.prop_widget[group][key]
                label.grid_remove(); widget.grid_remove()

        for widget in self.prop_widget['internal']['grid_rc_headers']:
            if show_headers:
                widget.grid()
            else:
                widget.grid_remove()
        #
        self.propsframe.reposition()
        self.packingframe.reposition()

        #re-enable callback
        self.arrayvar.enable_cb()


    def on_array_variable_changed(self, varname, elementname, mode):
        '''Updates treeview values from property editor.'''

        new_value = self.arrayvar[elementname]
        pgroup, pname = self.arrayvar.identify_property(elementname)
        tv = self.treeview
        treedata = self.app.tree_editor.treedata
        sel = tv.selection()
        if sel:
            item = sel[0]
            if (pgroup in (properties.GROUP_WIDGET, properties.GROUP_CUSTOM)):
                treedata[item][pname] = new_value
                widget_id = treedata[item]['id']
                wclass = treedata[item]['class']
                treenode_label = '{0} - {1}'.format(widget_id,wclass)
                tv.item(item, text=treenode_label)
            elif (pgroup == properties.GROUP_LAYOUT_GRID and pname in
                    properties.PropertiesMap[properties.GROUP_LAYOUT_GRID]):
                treedata[item]['packing'][pname] = new_value
            elif (pgroup == properties.GROUP_LAYOUT_GRID_RC):
                layoutdata = treedata[item]['packing']
                row_col, number, name = self.identify_gridrc_property(pname)
                number = str(number)
                if row_col == 'row':
                    layoutdata['rows'][number][name] = new_value
                elif row_col == 'column':
                    layoutdata['columns'][number][name] = new_value
            self.app.tree_editor.draw_widget(item)


    def on_treeview_select(self, event):
        """Get the selected treeitem and display properties in
            property editor."""

        tv = self.treeview
        sel = tv.selection()
        if sel:
            item = sel[0]
            #rootitem = self.get_toplevel_parent(item)
            #if rootitem not in self.previewer.tabs:
            #    self.draw_widget(rootitem)
            self.edit(item)
        else:
            #No selection hide all
            self.hide_all()


    def get_max_row_col(self, item):
        tree = self.treeview
        max_row = 0
        max_col = 0
        children = tree.get_children(item)
        for child in children:
            data = self.app.tree_editor.treedata[child].get('packing', {})
            row = int(data.get('row', 0))
            col = int(data.get('column', 0))
            if row > max_row:
                max_row = row
            if col > max_col:
                max_col = col
        return (max_row, max_col)


    def identify_gridrc_property(self, alias):
        return alias.split('_')

