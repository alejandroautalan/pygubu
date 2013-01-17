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

from . import util
from . import builder
from . import properties


CLASS_MAP = builder.CLASS_MAP


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
            properties.GROUP_CUSTOM: {}
        }
        self.create_properties()
        self.arrayvar.set_callback(self.on_array_variable_changed)

        self.treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)


    def create_properties(self):
        """Populate a frame with a list of all editable properties"""

        editor_frame = self.propsframe
        prop_widget = self.prop_widget
        row=0
        col=0
        label_tpl = "{0}:"
        for name in properties.PropertiesMap[properties.GROUP_CUSTOM]:
            labeltext = label_tpl.format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_property_widget(editor_frame,
                properties.GROUP_CUSTOM, name)
            label.grid(row=row, column=col, sticky=tkinter.EW)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW)
            row += 1
            prop_widget[properties.GROUP_CUSTOM][name] = (label, widget)

        for name in properties.PropertiesMap[properties.GROUP_WIDGET]:
            labeltext = label_tpl.format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_property_widget(editor_frame,
                properties.GROUP_WIDGET, name)
            label.grid(row=row, column=col, sticky=tkinter.EW)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW)
            row += 1
            prop_widget[properties.GROUP_WIDGET][name] = (label, widget)

        editor_frame = self.packingframe

        for name in properties.PropertiesMap[properties.GROUP_LAYOUT_GRID]:
            labeltext = label_tpl.format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_property_widget(editor_frame,
                properties.GROUP_LAYOUT_GRID, name)
            label.grid(row=row, column=col, sticky=tkinter.EW)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW)
            row += 1
            prop_widget[properties.GROUP_LAYOUT_GRID][name] = (label, widget)

        self.hide_all()


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

        if wtype == 'entry':
            readonly = wdata.get('readonly', False)
            state = tkinter.DISABLED if readonly else tkinter.NORMAL
            widget = ttk.Entry(master, textvariable=widgetvar, state=state)
        elif wtype == 'choice':
            widget = ttk.Combobox(master, textvariable=widgetvar,
                state='readonly')
            values = wdata.get('values', None)
            if values is not None:
                if isinstance(values, dict):
                    #I don't have class name at this moment
                    #setup on update_property_widget
                    pass
                else:
                    widget.configure(values=values)
        elif wtype == 'spinbox':
            widget = tkinter.Spinbox(master, textvariable=widgetvar)
            vmin = wdata.get('min', 0)
            vmax = wdata.get('max', 99)
            default = vmin if (vmin > 0 and default == '') else default
            widget.configure(from_=vmin, to=vmax)
        else:
            widget = ttk.Entry(master, textvariable=widgetvar)
        widgetvar.set(default)

        return widget


    def hide_all(self):
        """Hide all properties from property editor."""

        for group in self.prop_widget:
            for pname in self.prop_widget[group]:
                label, widget = self.prop_widget[group][pname]
                label.grid_remove()
                widget.grid_remove()


    def update_property_widget(
        self, group, widget, propertyname, classname, data):
        """Update widget property value with values from data."""

        wdata = {}
        if propertyname in properties.PropertiesMap[group]:
            wdata = properties.PropertiesMap[group][propertyname]

        wtype = wdata.get('input_method', '')
        default = wdata.get('default', '')
        if wtype == 'spinbox':
            vmin = wdata.get('min', 0)
            vmax = wdata.get('max', 99)
            default = vmin if (int(vmin) > 0 and default == '') else default
        if wtype == 'choice':
            values = wdata.get('values', None)
            if values is not None:
                if isinstance(values, dict):
                    values = values.get(classname, None)
                    if values:
                        widget.configure(values=values)
                else:
                    widget.configure(values=values)

        variable = self.arrayvar.get_property_variable(group, propertyname)

        if propertyname in data:
            value = data[propertyname]
            if not value:
                value = default
            variable.set(value)


    def edit(self, data):
        """Copies properties values from data to the
           properties editor so they can be edited."""

        #first disable callback
        self.arrayvar.disable_cb()

        wclass = data['class']
        class_props = tuple(CLASS_MAP[wclass].properties)

        group = properties.GROUP_CUSTOM
        for key in properties.PropertiesMap[group]:
            if (key in properties.OBJECT_DEFAULT_ATTRS or key in class_props):
                label, widget = self.prop_widget[group][key]
                self.update_property_widget(group, widget,
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
                self.update_property_widget(group, widget,
                    key, wclass, data)
                label.grid()
                widget.grid()
            else:
                #hide property widget
                label, widget = self.prop_widget[group][key]
                label.grid_remove()
                widget.grid_remove()

        #packing properties
        group = properties.GROUP_LAYOUT_GRID
        for gkey in properties.PropertiesMap[group]:
            label, widget = self.prop_widget[group][gkey]
            gdata = data.get('packing', {})
            self.update_property_widget(group, widget, gkey,
                    wclass, gdata)
            label.grid()
            widget.grid()

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
            self.edit(self.app.tree_editor.treedata[item])
        else:
            #No selection hide all
            self.hide_all()


