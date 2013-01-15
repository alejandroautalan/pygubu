# This file is part of pygubu.

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

import os
import xml.dom.minidom
import xml.etree.ElementTree as ET
from collections import Counter

import tkinter
from tkinter import ttk
from tkinter import filedialog

import pygubu
from pygubu import util
from pygubu import builder
from pygubu import tkproperties


CLASS_MAP = builder.CLASS_MAP

WIDGET_ATTRS = (
    'class', 'id',
)

wprops = set()
for c in CLASS_MAP:
    wprops.update(CLASS_MAP[c].properties)

WIDGET_PROPS = list(wprops)
WIDGET_PROPS.sort()
WIDGET_PROPS = tuple(WIDGET_PROPS)

WIDGET_GRID_PROPS = (
    #packing
    'row', 'column', 'rowspan', 'columnspan', 'padx', 'pady',
    'ipadx', 'ipady', 'sticky', 'in_'
)

ITEM_PROPS = tuple(set(WIDGET_ATTRS + WIDGET_PROPS))


class PreviewHelper:
    def __init__(self, notebook):
        self.notebook = notebook
        self.builders = {}
        self.canvases = {}
        self.tabs = {}
        self.windows = {}
        self.preview_tag = 'previewwindow'

    def draw(self, identifier, widget_id, xmlnode):
        uibuilder = pygubu.Builder()
        canvas = None
        if identifier not in self.builders:
            canvas = util.create_scrollable(self.notebook, tkinter.Canvas,
                background='white', scrollregion="0 0 80i 80i")
            self.canvases[identifier] = canvas
            self.notebook.add(canvas.frame, text=widget_id,
                sticky=tkinter.NSEW)
            self.tabs[identifier] = canvas.frame
        else:
            del self.builders[identifier]
            canvas = self.canvases[identifier]
            canvas.itemconfigure(self.preview_tag, window='')
            window = self.windows[identifier]
            window.destroy()

        uibuilder.add_from_xmlnode(xmlnode)
        self.builders[identifier] = uibuilder

        preview_widget = uibuilder.get_object(widget_id, canvas)
        self.windows[identifier] = preview_widget
        canvas.itemconfigure(self.preview_tag, window=preview_widget)

    def delete(self, identifier):
        self.notebook.forget(self.tabs[identifier])
        del self.tabs[identifier]


class ArrayVarHelper(util.ArrayVar):
    def __init__(self, master=None, value=None, name=None):
        super(util.ArrayVar, self).__init__(master, value, name)
        self._callback = None
        self._cbhandler = None

    def set_callback(self, callback):
        self._callback = callback
        self._cbhandler = None

    def enable_cb(self):
        if self._callback is not None:
            self._cbhandler = self.trace(mode="w", callback=self._callback)

    def disable_cb(self):
        if self._cbhandler is not None:
            self.trace_vdelete("w", self._cbhandler)


class WidgetPropertiesHelper:
    def __init__(self, arrayvar, propsframe, packingframe):
        self.propsframe = propsframe
        self.packingframe = packingframe
        self.arrayvar = arrayvar
        self.prop_widget = {}
        self.create_properties()


    def create_properties(self):
        """Populate a frame with a list of all editable properties"""

        editor_frame = self.propsframe
        prop_widget = self.prop_widget
        prop_widget['property'] = {}
        prop_widget['packing'] = {}
        row=0
        col=0
        for name in WIDGET_ATTRS:
            labeltext = "{0}:".format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_property_widget(editor_frame, name)
            label.grid(row=row, column=col, sticky=tkinter.EW)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW)
            row += 1
            prop_widget['property'][name] = (label, widget)

        for name in WIDGET_PROPS:
            labeltext = "{0}:".format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_property_widget(editor_frame, name)
            label.grid(row=row, column=col, sticky=tkinter.EW)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW)
            row += 1
            prop_widget['property'][name] = (label, widget)

        editor_frame = self.packingframe

        for name in WIDGET_GRID_PROPS:
            labeltext = "{0}:".format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_property_widget(editor_frame, name)
            label.grid(row=row, column=col, sticky=tkinter.EW)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW)
            row += 1
            prop_widget['packing'][name] = (label, widget)

        self.hide_all()


    def create_property_widget(self, master, propertyname):
        """Creates a ui widget to edit the property"""

        widget = None
        widgetvar = self.arrayvar(propertyname)

        wtype = ''
        if propertyname in tkproperties.TK_WIDGET_PROPS:
            wdata = tkproperties.TK_WIDGET_PROPS[propertyname]
            wtype = wdata['input_method']
        elif propertyname in tkproperties.TK_GRID_PROPS:
            wdata = tkproperties.TK_GRID_PROPS[propertyname]
            wtype = wdata['input_method']

        if wtype == 'entry':
            widget = ttk.Entry(master, textvariable=widgetvar)
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
            widget.configure(from_=vmin, to=vmax)
        else:
            widget = ttk.Entry(master, textvariable=widgetvar)

        return widget


    def hide_all(self):
        """Hide all properties from property editor."""

        for group in self.prop_widget:
            for pname in self.prop_widget[group]:
                label, widget = self.prop_widget[group][pname]
                label.grid_remove()
                widget.grid_remove()


    def update_property_widget(self, widget, propertyname, classname, data):
        """Update widget property value with values from data."""

        wtype = ''
        if propertyname in tkproperties.TK_WIDGET_PROPS:
            wdata = tkproperties.TK_WIDGET_PROPS[propertyname]
            wtype = wdata['input_method']
        elif propertyname in tkproperties.TK_GRID_PROPS:
            wdata = tkproperties.TK_GRID_PROPS[propertyname]
            wtype = wdata['input_method']
        elif propertyname in tkproperties.TK_GRID_RC_PROPS:
            wdata = tkproperties.TK_GRID_RC_PROPS[propertyname]
            wtype = wdata['input_method']

        if wtype == 'choice':
            values = wdata.get('values', None)
            if values is not None:
                if isinstance(values, dict):
                    pass
                    values = values.get(classname, None)
                    if values:
                        widget.configure(values=values)
                else:
                    widget.configure(values=values)

        variable = self.arrayvar(propertyname)
        if propertyname in data:
            variable.set(data[propertyname])


    def edit(self, data):
        """Copies properties values from data to the
           properties editor so they can be edited."""

        #first disable callback for better performance ??
        self.arrayvar.disable_cb()

        wclass = data['class']
        wprops = WIDGET_ATTRS + tuple(CLASS_MAP[wclass].properties)

        #self.hide_all()

        #for key in data.keys():
        for key in ITEM_PROPS:
            if key in wprops:
                label, widget = self.prop_widget['property'][key]
                self.update_property_widget(widget, key, wclass, data)
                label.grid()
                widget.grid()
            else:
                label, widget = self.prop_widget['property'][key]
                label.grid_remove()
                widget.grid_remove()

        #pagking properties
        for gkey in WIDGET_GRID_PROPS:
            label, widget = self.prop_widget['packing'][gkey]
            gdata = data.get('packing', {})
            self.update_property_widget(widget, gkey, wclass, gdata)
            label.grid()
            widget.grid()

        #re-enable callback
        self.arrayvar.enable_cb()


class WidgetsTreeHelper:
    def __init__(self, treeview, props_editor, previewer, arrayvar):
        self.treeview = treeview
        self.previewer = previewer
        self.props_editor = props_editor
        self.arrayvar = arrayvar
        self.treedata = {}
        self.counter = Counter()

        self.config_treeview()
        self.arrayvar.set_callback(self.on_property_variable_changed)
        self.arrayvar.enable_cb()

    def config_treeview(self):
        """Sets treeview columns and other params"""
        tree = self.treeview
        columns = tuple()
        dcols = tuple()
        hcols = ('Widget Tree',) + columns
        util.configure_treeview(tree, columns, displaycolumns=dcols,
            headings=hcols, show_tree=True)
        tree.bind('<<TreeviewSelect>>', self.on_treeview_select)
        tree.bind('<KeyPress-Delete>', self.on_treeview_delete_item)


    def get_toplevel_parent(self, treeitem):
        """Returns the top level parent for treeitem."""
        tv = self.treeview
        toplevel_items = tv.get_children()

        item = treeitem
        while not (item in toplevel_items):
            item = tv.parent(item)

        return item

    def draw_widget(self, item):
        """Create a preview of the selected treeview item"""
        tv = self.treeview

        if item:
            widget_id = self.treedata[item]['id']
            xmlnode = self.tree_node_to_xml('', item)
            self.previewer.draw(item, widget_id, xmlnode)


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
            self.props_editor.edit(self.treedata[item])


    def on_treeview_delete_item(self, event):
        """Removes item from treeview"""

        tv = self.treeview
        sel = tv.selection()
        toplevel_items = tv.get_children()
        if sel:
            item = sel[0]
            parent = ''
            if item not in toplevel_items:
                parent = self.get_toplevel_parent(item)
            else:
                self.props_editor.hide_all()
                self.previewer.delete(item)
            del self.treedata[item]
            tv.delete(item)
            self.draw_widget(parent)


    def tree_to_xml(self):
        """Traverses treeview and generates a ElementTree object"""

        tree = self.widgets.treeview
        root = ET.Element('interface')
        items = tree.get_children()
        for item in items:
            node = self.tree_node_to_xml(tree, '', item)
            root.append(node)

        return ET.ElementTree(root)


    def tree_node_to_xml(self, parent, item):
        """Converts a treeview item and children to xml nodes"""

        tree = self.treeview
        values = self.treedata[item]
        node = ET.Element('object')

        for prop in WIDGET_ATTRS:
            node.set(prop, values[prop])

        wclass_props = CLASS_MAP[values['class']].properties
        for prop in wclass_props:
            pv = values.get(prop, None)
            if pv:
                pnode = ET.Element('property')
                pnode.set('name', prop)
                pnode.text = pv
                node.append(pnode)

        children = tree.get_children(item)
        for child in children:
            cnode = ET.Element('child')
            cwidget = self.tree_node_to_xml(item, child)
            cnode.append(cwidget)
            node.append(cnode)

        #create packing node
        pvalues = values['packing']
        packing_node = ET.Element('packing')
        has_packing = False
        for prop in WIDGET_GRID_PROPS:
            pv = pvalues.get(prop, None)
            if pv:
                has_packing = True
                pnode = ET.Element('property')
                pnode.set('name', prop)
                pnode.text = pv
                packing_node.append(pnode)
        if has_packing:
            node.append(packing_node)

        return node


    def add_widget(self, wclass):
        """Adds a new item to the treeview."""

        tree = self.treeview
        #get the selected item:
        selected_item = ''
        tsel = tree.selection()
        if tsel:
            selected_item = tsel[0]

        #by default insert at top level
        root = ''

        #check if selected item is a container
        if selected_item:
            svalues = tree.set(selected_item)
            sclass = self.treedata[selected_item]['class']
            if CLASS_MAP[sclass].container == True:
                #selected item is a container, set as root.
                root = selected_item
            else:
                #the item parent should be the container
                root = tree.parent(selected_item)

        #if insertion is at top level,
        #check that item to insert is a container.
        if not root:
            if CLASS_MAP[wclass].container == False:
                print('Warning: Widget to insert is not a container.')
                return

        #root item should be set at this point

        #increment class counter
        self.counter[wclass] += 1

        #setup properties
        widget_id = '{0}_{1}'.format(wclass, self.counter[wclass])

        treenode_label = '{0} - {1}'.format(widget_id,wclass)
        item = tree.insert(root, 'end', text=treenode_label)

        data = {}
        data['class'] = wclass
        data['id'] = widget_id

        #setup properties
        for pname in CLASS_MAP[wclass].properties:
            data[pname] = ''
            #default text for widgets with text prop:
            if pname == 'text':
                data[pname] = widget_id

        #default grid properties
        group = 'packing'
        data[group] = {}
        for prop_name in WIDGET_GRID_PROPS:
            data[group][prop_name] = ''

        rownum = str(len(tree.get_children(root)) - 1)
        data[group]['row'] = rownum
        data[group]['column'] = '0'

        self.treedata[item] = data

        #select and show the item created
        tree.selection_set(item)
        tree.see(item)
        #Do redraw
        self.draw_widget(self.get_toplevel_parent(item))


    def on_property_variable_changed(self, varname, elementname, mode):
        '''Updates treeview values from property editor.'''

        new_value = self.arrayvar[elementname]
        tv = self.treeview
        sel = tv.selection()
        if sel:
            item = sel[0]
            self.treedata[item][elementname] = new_value
            if elementname in WIDGET_ATTRS:
                widget_id = self.treedata[item]['id']
                wclass = self.treedata[item]['class']
                treenode_label = '{0} - {1}'.format(widget_id,wclass)
                tv.item(item, text=treenode_label)
            self.draw_widget(self.get_toplevel_parent(item))


    def load_file(self, filename):
        """Load file into treeview"""

        self.counter.clear()
        etree = ET.parse(filename)
        eroot = etree.getroot()

        for element in eroot:
            self.populate_tree('', eroot, element)


    def populate_tree(self, master, parent, element):
        """Reads xml nodes and populates tree item"""

        cname = element.get('class')
        uniqueid = element.get('id')
        data = {}

        if cname in CLASS_MAP:
            #update counter
            self.counter[cname] += 1
            treenode_label = '{0} - {1}'.format(uniqueid, cname)
            pwidget = self.treeview.insert(master, 'end',
                text=treenode_label)
            data['class'] = cname
            data['id'] = uniqueid

            #properties
            properties = self.get_properties(element)
            for pname, value in properties.items():
                data[pname] = value

            #packing element
            data['packing'] = {}
            xpath = './packing'
            packing_elem = element.find(xpath)
            if packing_elem is not None:
                properties = self.get_properties(packing_elem)
                for key, value in properties.items():
                    data['packing'][key] = value

            self.treedata[pwidget] = data

            xpath = "./child"
            children = element.findall(xpath)
            for child in children:
                child_object = child.find('./object')
                cwidget = self.populate_tree(pwidget, child, child_object)

            return pwidget
        else:
            raise Exception('Class "{0}" not mapped'.format(cname))


    def get_properties(self, element):
        """Gets name, value from property nodes in element"""

        properties = element.findall('./property')
        pdict= {}
        for p in properties:
            pdict[p.get('name')] = p.text
        return pdict



class PygubuUI(util.Application):
    """Main gui class"""

    def _create_ui(self):
        """Creates all gui widgets"""

        self.preview = None
        self.arrayvar = ArrayVarHelper()
        self.builder = builder = pygubu.Builder()

        uifile = os.path.join(os.path.dirname(__file__),"../ui/pygubu-ui.ui")
        builder.add_from_file(uifile)

        #build main ui
        builder.get_object('mainwindow', self)
        toplevel = self.winfo_toplevel()
        menu = builder.get_object('mainmenu', toplevel)
        toplevel['menu'] = menu

        #menu
        menu = builder.get_object('filemenu')
        #fileopen
        menu.entryconfigure(1, command=self.on_menuitem_open_clicked)
        #filesave
        menu.entryconfigure(2, command=self.on_menuitem_save_clicked)
        #filequit
        menu.entryconfigure(4, command=self.quit)

        #Class selector values
        self.configure_widget_list()

        #widget tree
        self.treeview = tree = builder.get_object('treeview1')

        #properties frame
        propframe = builder.get_object('propertiesframe')
        packingframe = builder.get_object('packingframe')
        self.propshelper = WidgetPropertiesHelper(self.arrayvar,
            propframe, packingframe)

        nbpreview = builder.get_object('notebookpreview')
        self.preview = PreviewHelper(nbpreview)
        self.treehelper = WidgetsTreeHelper(self.treeview,
            self.propshelper, self.preview, self.arrayvar)

        self.grid(row=0, column=0, sticky='nswe')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.set_resizable()

        #app config
        self.set_title('Pygubu a GUI builder for tkinter')
        self.set_size('800x600')


    def configure_widget_list(self):
        self.widgetlist = tv = self.builder.get_object("widgetlist")
        tv.heading('#0', text='Widget List')
        tv.bind('<Double-1>', lambda e: self.on_add_widget_event())
        values = list(CLASS_MAP.keys())
        values.sort()
        for value in values:
            tv.insert('', tkinter.END, text=value)


    def on_add_widget_event(self):
        wlist = self.widgetlist
        #get widget class name to insert
        selection = wlist.selection()
        if selection:
            item = selection[0]
            wclass = wlist.item(item, 'text')
            self.treehelper.add_widget(wclass)


    def on_add_btn_clicked(self):
        """Adds selected widget class to treeview"""

        tree = self.treeview
        #get widget class name to insert
        wclass = self.class_cbox_var.get()

        self.treehelper.add_widget(wclass)


    def on_menuitem_open_clicked(self):
        """Opens xml file and load to treeview"""

        fname = filedialog.askopenfilename()
        if fname:
            self.load_file(fname)


    def on_menuitem_save_clicked(self):
        """Save treeview to xml file"""

        fname = filedialog.asksaveasfilename()
        if fname:
            self.save_file(fname)


    def save_file(self, filename):
        xml_tree = self.treehelper.tree_to_xml()
        xmlvar = xml.dom.minidom.parseString(
            ET.tostring(xml_tree.getroot()))
        pretty_xml_as_string = xmlvar.toprettyxml(indent=' '*4)
        with open(filename, 'w') as f:
            f.write(pretty_xml_as_string)


    def load_file(self, filename):
        """Load xml into treeview"""

        self.treehelper.load_file(filename)
        self.project_name.configure(text=filename)


def start_pygubu():
    app = PygubuUI(tkinter.Tk())
    app.run()


if __name__ == '__main__':
    start_pygubu()

