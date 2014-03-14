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
import re
from collections import defaultdict
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from pygubu import builder
from . import util
from . import properties
from .widgets import ColorEntry, Textentry, TkVarEntry, ImageEntry
from .widgets import SizeEntry
from .bindingseditor import BindingsEditor
from .i18n import translator as _


CLASS_MAP = builder.CLASS_MAP

FLOAT_RE = re.compile(r'[+-]?(\d+(\.\d*)?)')


class PropertiesArray(util.ArrayVar):

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


class WidgetPropertiesEditor:

    def __init__(self, app):
        self.current = None #data to edit
        #self.app = app
        #self.treeview = app.treeview
        self.properties_sf = app.builder.get_object('properties_sf')
        self.propsframe = app.widget_props_frame
        self.layoutframe_sf = app.builder.get_object('layoutframe_sf')
        self.layoutframe = app.layout_props_frame
        self.bindingsframe = app.bindings_frame
        self.arrayvar = PropertiesArray()
        self.prop_widget = {
            properties.GROUP_WIDGET: {},
            properties.GROUP_LAYOUT_GRID: {},
            properties.GROUP_LAYOUT_GRID_RC: {},
            properties.GROUP_CUSTOM: {},
            'internal': {}
        }
        self._editor_ready = False
        self._var_prev_value = {}
        #register validators
        tkwidget = self.propsframe
        self.validators = {
            'number_integer': (tkwidget.register(self.validator_integer),
                '%d', '%P'),
            'number_float': (tkwidget.register(self.validator_float),
                '%d', '%P'),
            'alphanumeric': (tkwidget.register(self.validator_alphanumeric),
                '%d', '%P'),
            'tkpadding': (tkwidget.register(self.validator_tkpadding4),
                '%d', '%P'),
            'tkpadding2': (tkwidget.register(self.validator_tkpadding2),
                '%d', '%P'),
            'entry_validate_args': (tkwidget.register(
                self.validator_entry_validate_args), '%d', '%P'),
        }
        self.create_properties()
        self.create_grid_layout_editor()

        self.bindings_editor = BindingsEditor(app.bindings_tree)

        self.hide_all()


    def validator_tkpadding4(self, action, newvalue):
        return self.validator_tkpadding(action, newvalue, 4)

    def validator_tkpadding2(self, action, newvalue):
        return self.validator_tkpadding(action, newvalue, 2)


    def validator_tkpadding(self, action, newvalue, maxitems):
        valid = True
        if action == '1': #1: insert 0: delete
            nums = newvalue.split()
            if len(nums) <= maxitems:
                for num in nums:
                    if not num.isdigit():
                        valid = False
                        break;
            else:
                valid = False
        else:
            valid = True
        return valid


    def validator_alphanumeric(self, action, newvalue):
        valid = False
        if action == '1': #1: insert 0: delete
            valid = str(newvalue).isalnum()
        else:
            valid = True
        return valid


    def validator_integer(self, action, newvalue):
        valid = False
        if action == '1': #1: insert 0: delete
            valid = str(newvalue).isalnum()
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


    def validator_entry_validate_args(self, action, newvalue):
        valid = True
        valid_args = ('%', '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        if action == '1': #1: insert 0: delete
            args = newvalue.split()
            for arg in args:
                if arg not in valid_args:
                    valid = False
                    break
        else:
            valid = True
        return valid


    def connect_focusout_cb(self, widget, pname):
        def focusout_handler(event, self=self, pname=pname):
            self.on_property_changed(pname)
        widget.bind('<FocusOut>', focusout_handler, add='+')


    def connect_on_enterkey_cb(self, widget, pname):
        def enterkey_handler(event, self=self, pname=pname):
            self.on_property_changed(pname)
        widget.bind('<KeyPress-Return>', enterkey_handler, add='+')
        widget.bind('<KeyPress-KP_Enter>', enterkey_handler, add='+')


    def connect_command_cb(self, widget, pname):
        def command_handler(self=self, pname=pname):
            self.on_property_changed(pname)
        widget.configure(command=command_handler)


    def connect_virtualevent_cb(self, eventname, widget, pname):
        def virtualevent_handler(event, self=self, pname=pname):
            self.on_property_changed(pname)
        widget.bind(eventname, virtualevent_handler, add='+')


    def connect_variable_cb(self, variable, pname):
        def var_handler(varname, elementname, mode, self=self, pname=pname):
            self.on_property_changed(pname)
        variable.trace('w', callback=var_handler)


    def on_property_changed(self, pname):
        '''Updates treeview values from property editor.'''

        #Do not redraw if editor is not ready. See edit method.
        if not self._editor_ready:
            return

        new_value = self.arrayvar[pname]
        old_value = self._var_prev_value.get(pname, '')

        #Do not redraw if same values
        #print('new ', new_value, ' old ', old_value)
        if new_value == old_value:
            return
        self._var_prev_value[pname] = new_value

        pgroup, pname = self.arrayvar.identify_property(pname)
        if self.current is not None:
            data = self.current
            widget_id = data.get_id()
            wclass = data.get_class()

            if (pgroup in (properties.GROUP_WIDGET, properties.GROUP_CUSTOM)):

                if new_value:
                    data.set_property(pname, new_value)
                else:
                    data.set_property(pname, '')

            elif (pgroup == properties.GROUP_LAYOUT_GRID and pname in
                    properties.PropertiesMap[properties.GROUP_LAYOUT_GRID]):

                if new_value:
                    data.set_layout_property(pname, new_value)
                else:
                    data.set_layout_property(pname, '')

            elif (pgroup == properties.GROUP_LAYOUT_GRID_RC):
                row_col, number, name = self.identify_gridrc_property(pname)
                number = str(number)
                if row_col == 'row':
                    if new_value:
                        data.set_grid_row_property(number, name, new_value)
                    else:
                        data.set_grid_row_property(number, name, '')
                elif row_col == 'column':
                    if new_value:
                        data.set_grid_col_property(number, name, new_value)
                    else:
                        data.set_grid_col_property(number, name, '')

            data.notify(self)


    def create_properties(self):
        """Populate a frame with a list of all editable properties"""

        editor_frame = self.propsframe
        prop_widget = self.prop_widget

        #hack to resize correctly when properties are hidden
        label = ttk.Label(editor_frame)
        label.grid()

        row=0
        col=0
        label_tpl = "{0}:"
        group = properties.GROUP_CUSTOM
        for name in properties.PropertiesMap[group]:
            labeltext = label_tpl.format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tk.W)
            togrid, widget = self.create_property_widget(editor_frame,
                group, name)
            label.grid(row=row, column=col, sticky=tk.EW, pady=2)
            togrid.grid(row=row, column=col+1, sticky=tk.EW, pady=2)
            row += 1
            prop_widget[group][name] = (label, togrid)

        group = properties.GROUP_WIDGET
        for name in properties.PropertiesMap[group]:
            labeltext = label_tpl.format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tk.W)
            togrid, widget = self.create_property_widget(editor_frame,
                group, name)
            label.grid(row=row, column=col, sticky=tk.EW, pady=2)
            togrid.grid(row=row, column=col+1, sticky=tk.EW, pady=2)
            row += 1
            prop_widget[group][name] = (label, togrid)


    def create_grid_layout_editor(self):
        master = self.layoutframe
        prop_widget = self.prop_widget
        frame = ttk.LabelFrame(master, text=_('Grid options:'), padding=5)

        #hack to resize correctly when properties are hidden
        label = ttk.Label(frame)
        label.grid()

        label_tpl = "{0}:"
        row= col=0
        group = properties.GROUP_LAYOUT_GRID
        for name in properties.PropertiesMap[group]:
            labeltext = label_tpl.format(name)
            label = ttk.Label(frame, text=labeltext, anchor=tk.W)
            togrid, widget = self.create_property_widget(frame, group, name)
            label.grid(row=row, column=col, sticky=tk.EW, pady=2)
            togrid.grid(row=row, column=col+1, sticky=tk.EW, pady=2)
            row += 1
            prop_widget[group][name] = (label, togrid)

        frame.grid(row=0, column=0, sticky=tk.NSEW)

        #labels
        group = properties.GROUP_LAYOUT_GRID_RC
        frame = ttk.LabelFrame(master, text=_('Grid row/column options:'),
            padding=5)

        #hack to resize correctly when properties are hidden
        label = ttk.Label(frame)
        label.grid()

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
        trow_label = _('Row {0}:')
        tcol_label = _('Column {0}:')
        for index in range(0, max_rc):
            labeltext = trow_label.format(index)
            label = ttk.Label(frame, text=labeltext)
            label.grid(row=row, column=0)

            labeltext = tcol_label.format(index)
            labelc = ttk.Label(frame, text=labeltext)
            labelc.grid(row=row+max_rc, column=0, sticky=tk.E, pady=2)

            icol = 1
            for pname in properties.PropertiesMap[group]:
                alias = name_format.format('row', index, pname)
                togrid, widget = self.create_grid_rc_widget(frame, pname, alias)
                togrid.grid(row=row, column=icol, pady=2)
                prop_widget[group][alias]= (label, togrid)

                alias = name_format.format('column', index, pname)
                togrid, widget = self.create_grid_rc_widget(frame, pname, alias)
                togrid.grid(row=row+max_rc, column=icol, pady=2)
                prop_widget[group][alias]= (labelc, togrid)

                icol += 1
            row +=1

        frame.grid(row=1, column=0, sticky=tk.NSEW, pady='10 0')


    def create_grid_rc_widget(self, master, name, alias):
        group = properties.GROUP_LAYOUT_GRID_RC
        widgetvar = self.arrayvar.get_property_variable(group, alias);
        wdata = {}
        widget = None
        if name in properties.PropertiesMap[group]:
            wdata = properties.PropertiesMap[group][name]
            wtype = wdata['input_method']

        togrid, widget = self.__create_widget(master, wdata, group+alias,
            widgetvar)
        widget.configure(width=4)
        return (togrid, widget)


    def create_property_widget(self, master, group, propertyname):
        """Creates a ui widget to edit the property"""

        widgetvar = self.arrayvar.get_property_variable(group, propertyname);
        wdata = {}

        widget = None
        if propertyname in properties.PropertiesMap[group]:
            wdata = properties.PropertiesMap[group][propertyname]

        togrid, widget = self.__create_widget(master, wdata,
            group+propertyname, widgetvar)
        return (togrid, widget)


    def __create_widget(self, master, wdata, propalias, widgetvar):
        widget = None
        togrid = None
        wtype = wdata.get('input_method', None)
        default = wdata.get('default', '')

        #I don't have class name at this moment
        #so setup class specific values on update_property_widget
        if wtype == 'entry':
            readonly = wdata.get('readonly', False)
            state = tk.DISABLED if readonly else tk.NORMAL
            widget = ttk.Entry(master, textvariable=widgetvar, state=state)
            togrid = widget
            #validator
            validator = wdata.get('validator', None)
            if validator is not None:
                widget.configure(validate='key',
                    validatecommand=self.validators[validator])
            self.connect_focusout_cb(widget, propalias)
            self.connect_on_enterkey_cb(widget, propalias)
        elif wtype == 'textentry':
            widget = Textentry(master, textvariable=widgetvar)
            widget.text.configure(width=20, height=3)
            togrid = widget
            self.connect_virtualevent_cb('<<TextentryChanged>>', widget, propalias)
        elif wtype == 'colorentry':
            widget = ColorEntry(master, textvariable=widgetvar)
            togrid = widget
            self.connect_virtualevent_cb('<<ColorEntryChanged>>', widget, propalias)
        elif wtype == 'imageentry':
            widget= ImageEntry(master, textvariable=widgetvar)
            togrid = widget
            self.connect_virtualevent_cb('<<ImageEntryChanged>>', widget, propalias)
        elif wtype == 'choice':
            readonly = wdata.get('readonly', False)
            status = 'readonly' if readonly else tk.NORMAL
            widget = ttk.Combobox(master, textvariable=widgetvar,
                state=status)
            togrid = widget
            values = wdata.get('values', None)
            if values is not None:
                widget.configure(values=values)
            self.connect_variable_cb(widgetvar, propalias)
        elif wtype == 'tkvarentry':
            widget = TkVarEntry(master, textvariable=widgetvar,
                        width=20, height=3)
            togrid = widget
            self.connect_virtualevent_cb('<<TkVarEntryChanged>>', widget, propalias)
        elif wtype == 'spinbox':
            status= tk.NORMAL
            readonly = wdata.get('readonly', False)
            if readonly:
                status = 'readonly'
            widget = tk.Spinbox(master, textvariable=widgetvar,
                        state=status, readonlybackground='white')
            togrid = widget
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
            self.connect_focusout_cb(widget, propalias)
            self.connect_command_cb(widget, propalias)
            self.connect_on_enterkey_cb(widget, propalias)
        elif wtype == 'sizeentry':
            widget = togrid = SizeEntry(master, textvariable=widgetvar)
            self.connect_virtualevent_cb('<<SizeEntryChanged>>',
                widget, propalias)
        else:
            widget = ttk.Entry(master, textvariable=widgetvar)
            togrid = widget
            self.connect_focusout_cb(widget, propalias)
            self.connect_on_enterkey_cb(widget, propalias)
        widgetvar.set(default)

        return (togrid, widget)


    def hide_all(self):
        """Hide all properties from property editor."""
        self.current = None
        for group in self.prop_widget:
            for pname in self.prop_widget[group]:
                for widget in self.prop_widget[group][pname]:
                    widget.grid_remove()
        self.properties_sf.reposition()
        self.layoutframe_sf.reposition()

        self.bindingsframe.grid_remove()
        self.bindings_editor.clear()


    def update_property_widget(self, group, widget, variable,
        propertyname, classname, data, roc=None, rc_id=None):
        """Update widget property value with values from data."""

        wdata = {}
        if propertyname in properties.PropertiesMap[group]:
            wdata = properties.PropertiesMap[group][propertyname]

        wtype = wdata.get('input_method', '')

        #merge description for specific class
        if classname in wdata:
            wdata = dict(wdata, **wdata[classname])

        default = wdata.get('default', '')
        if wtype == 'entry':
            #switch validator mode for entry
            validator = wdata.get('validator', None)
            if validator is not None:
                widget.configure(validate='key',
                    validatecommand=self.validators[validator])
        if wtype == 'spinbox':
            vmin = wdata.get('min', 0)
            vmax = wdata.get('max', 99)
            default = vmin if (int(vmin) > 0 and default == '') else default
        if wtype == 'choice':
            readonly = wdata.get('readonly', False)
            status = 'readonly' if readonly else tk.NORMAL
            values = wdata.get('values', None)
            if values is not None:
                widget.configure(values=values, state=status)
        if wtype == 'sizeentry':
            mode = wdata.get('mode', '')
            widget.set_mode(mode)

        value = ''
        if group in (properties.GROUP_CUSTOM, properties.GROUP_WIDGET):
            value = data.get_property(propertyname)
        elif group == properties.GROUP_LAYOUT_GRID:
            value = data.get_layout_property(propertyname)
        elif group == properties.GROUP_LAYOUT_GRID_RC:
            if roc == 'row':
                value = data.get_grid_row_property(rc_id, propertyname)
            else:
                value = data.get_grid_col_property(rc_id, propertyname)

        if not value and default:
            value = default

        variable.set(value)
        self._var_prev_value[group+propertyname] = value


    def edit(self, data, max_row=1, max_col=1):
        """Copies properties values from data to the
           properties editor so they can be edited."""

        self._var_prev_value.clear()
        #
        self._editor_ready = False
        self.current = data

        wclass = data.get_class()
        class_props = tuple(CLASS_MAP[wclass].classobj.properties)

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

        max_children = CLASS_MAP[wclass].classobj.maxchildren
        max_children = 0 if max_children is None else max_children
        is_container = CLASS_MAP[wclass].classobj.container
        layout_required = CLASS_MAP[wclass].classobj.layout_required
        allow_container_layout = CLASS_MAP[wclass].classobj.allow_container_layout
        show_layout = layout_required
        #grid layout properties
        group = properties.GROUP_LAYOUT_GRID
        for gkey in properties.PropertiesMap[group]:
            label, widget = self.prop_widget[group][gkey]
            if show_layout:
                variable = self.arrayvar.get_property_variable(group, gkey)
                self.update_property_widget(group, widget, variable, gkey,
                        wclass, data)
                label.grid()
                widget.grid()
            else:
                label.grid_remove()
                widget.grid_remove()

        group = properties.GROUP_LAYOUT_GRID_RC
        #max_row, max_col = self.get_max_row_col(item)
        show_layout = (is_container
                        and layout_required
                        and allow_container_layout
                        and max_children != 1)
        show_headers = False
        for key in self.prop_widget[group]:
            rowcol, number, name = self.identify_gridrc_property(key)
            number_str = str(number)
            number = int(number)
            if show_layout and rowcol == 'row' and number <= max_row:
                label, widget = self.prop_widget[group][key]
                variable = self.arrayvar.get_property_variable(group, key)
                self.update_property_widget(group, widget, variable, name,
                    wclass, data, rowcol, number_str)
                label.grid(); widget.grid()
                show_headers = True
            elif show_layout and rowcol == 'column' and number <= max_col:
                label, widget = self.prop_widget[group][key]
                variable = self.arrayvar.get_property_variable(group, key)
                self.update_property_widget(group, widget, variable, name,
                    wclass, data, rowcol, number_str)
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
        self.properties_sf.reposition()
        self.layoutframe_sf.reposition()
        #
        allow_edit = CLASS_MAP[wclass].classobj.allow_bindings
        if allow_edit:
            self.bindingsframe.grid()
        else:
            self.bindingsframe.grid_remove()
        self.bindings_editor.allow_edit(allow_edit)
        self.bindings_editor.edit(data)

        self._editor_ready = True


    def identify_gridrc_property(self, alias):
        return alias.split('_')
