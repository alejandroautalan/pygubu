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
from pygubu import util
from pygubu import builder
from pygubu import tkproperties


CLASS_MAP = builder.CLASS_MAP

WIDGET_ATTRS = (
    'class', 'id',
)

WIDGET_ATTRS_DESCR = {
    'class': {
        'input_method': 'entry',
        'readonly': True
    },
    'id': {'input_method': 'entry'}
}

wprops = set()
for c in CLASS_MAP:
    wprops.update(CLASS_MAP[c].properties)

WIDGET_PROPS = list(wprops)
WIDGET_PROPS.sort()
WIDGET_PROPS = tuple(WIDGET_PROPS)

WIDGET_GRID_PROPS = (
    #packing
    'row', 'column', 'rowspan', 'columnspan', 'padx', 'pady',
    'ipadx', 'ipady', 'sticky'  #removed property: 'in_'
)

WIDGET_ATTRS_PLUS_WIDGET_PROPS = tuple(set(WIDGET_ATTRS + WIDGET_PROPS))


class PropertiesArray(util.ArrayVar):
    WIDGET_PROP = 'VWP'
    PACKING_PROP = 'VPP'

    def __init__(self, master=None, value=None, name=None):
        super(util.ArrayVar, self).__init__(master, value, name)
        self._callback = None
        self._cbhandler = None

    def get_widget_prop(self, name):
        return self.__call__(self.WIDGET_PROP + name)

    def get_packing_prop(self, name):
        return self.__call__(self.PACKING_PROP + name)

    def identify_property(self, element):
        result = (None, None)
        if element.startswith(self.WIDGET_PROP):
            result = (self.WIDGET_PROP, element.replace(self.WIDGET_PROP, ''))
        elif element.startswith(self.PACKING_PROP):
            result = (self.PACKING_PROP, element.replace(self.PACKING_PROP, ''))
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
    WIDGET_GROUP = 'widget'
    PACKING_GROUP = 'packing'

    def __init__(self, app):
        self.app = app
        self.treeview = app.treeview
        self.propsframe = app.widget_props_frame
        self.packingframe = app.packing_props_frame
        self.arrayvar = PropertiesArray()
        self.prop_widget = {
            self.WIDGET_GROUP: {},
            self.PACKING_GROUP: {}
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
        for name in WIDGET_ATTRS:
            labeltext = label_tpl.format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_widget_property_widget(editor_frame, name)
            label.grid(row=row, column=col, sticky=tkinter.EW)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW)
            row += 1
            prop_widget[self.WIDGET_GROUP][name] = (label, widget)

        for name in WIDGET_PROPS:
            labeltext = label_tpl.format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_widget_property_widget(editor_frame, name)
            label.grid(row=row, column=col, sticky=tkinter.EW)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW)
            row += 1
            prop_widget[self.WIDGET_GROUP][name] = (label, widget)

        editor_frame = self.packingframe

        for name in WIDGET_GRID_PROPS:
            labeltext = label_tpl.format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_packing_property_widget(editor_frame, name)
            label.grid(row=row, column=col, sticky=tkinter.EW)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW)
            row += 1
            prop_widget[self.PACKING_GROUP][name] = (label, widget)

        self.hide_all()


    def create_widget_property_widget(self, master, propertyname):
        """Creates a ui widget to edit the property"""

        widgetvar = self.arrayvar.get_widget_prop(propertyname);
        wdata = {}

        widget = None
        if propertyname in WIDGET_ATTRS:
            wdata = WIDGET_ATTRS_DESCR[propertyname]
            wtype = wdata['input_method']
        if propertyname in tkproperties.TK_WIDGET_PROPS:
            wdata = tkproperties.TK_WIDGET_PROPS[propertyname]
            wtype = wdata['input_method']

        widget = self.__create_widget(master, wdata, widgetvar)
        return widget


    def create_packing_property_widget(self, master, propertyname):
        widgetvar = self.arrayvar.get_packing_prop(propertyname);
        wdata = {}
        if propertyname in tkproperties.TK_GRID_PROPS:
            wdata = tkproperties.TK_GRID_PROPS[propertyname]

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
        if group == self.WIDGET_GROUP:
            if propertyname in tkproperties.TK_WIDGET_PROPS:
                wdata = tkproperties.TK_WIDGET_PROPS[propertyname]
            elif propertyname in WIDGET_ATTRS_DESCR:
                wdata = WIDGET_ATTRS_DESCR[propertyname]
        elif group == self.PACKING_GROUP:
            if propertyname in tkproperties.TK_GRID_PROPS:
                wdata = tkproperties.TK_GRID_PROPS[propertyname]
            elif propertyname in tkproperties.TK_GRID_RC_PROPS:
                wdata = tkproperties.TK_GRID_RC_PROPS[propertyname]

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

        variable = None
        if group == self.WIDGET_GROUP:
            variable = self.arrayvar.get_widget_prop(propertyname)
        else:
            variable = self.arrayvar.get_packing_prop(propertyname)
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
        wprops = WIDGET_ATTRS + tuple(CLASS_MAP[wclass].properties)

        #for key in data.keys():
        for key in WIDGET_ATTRS_PLUS_WIDGET_PROPS:
            if key in wprops:
                label, widget = self.prop_widget[self.WIDGET_GROUP][key]
                self.update_property_widget(self.WIDGET_GROUP, widget, key,
                    wclass, data)
                label.grid()
                widget.grid()
            else:
                #hide property widget
                label, widget = self.prop_widget[self.WIDGET_GROUP][key]
                label.grid_remove()
                widget.grid_remove()

        #packing properties
        for gkey in WIDGET_GRID_PROPS:
            label, widget = self.prop_widget[self.PACKING_GROUP][gkey]
            gdata = data.get('packing', {})
            self.update_property_widget(self.PACKING_GROUP, widget, gkey,
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
            if (pgroup == PropertiesArray.WIDGET_PROP
                and pname in WIDGET_ATTRS_PLUS_WIDGET_PROPS):
                treedata[item][pname] = new_value
                widget_id = treedata[item]['id']
                wclass = treedata[item]['class']
                treenode_label = '{0} - {1}'.format(widget_id,wclass)
                tv.item(item, text=treenode_label)
            elif (pgroup == PropertiesArray.PACKING_PROP
                and pname in WIDGET_GRID_PROPS):
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


