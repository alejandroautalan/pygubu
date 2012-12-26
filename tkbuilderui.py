# This file is part of Foobar.

# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>

import xml.dom.minidom
import xml.etree.ElementTree as ET
from collections import Counter
from myttk import *
from tkinter import filedialog
import tkbuilder


CLASS_MAP = tkbuilder.CLASS_MAP

WIDGET_ATTRS = (
    'class', 'id',
)

wprops = set()
for c in CLASS_MAP:
    wprops.update(CLASS_MAP[c]['properties'])

WIDGET_PROPS = list(wprops)
WIDGET_PROPS.sort()
WIDGET_PROPS = tuple(WIDGET_PROPS)

WIDGET_GRID_PROPS = (
    #packing
    'row', 'column', 'rowspan', 'columnspan', 'padx', 'pady',
    'ipadx', 'ipady', 'sticky', 'in_'
)

ITEM_PROPS = WIDGET_ATTRS + WIDGET_PROPS + WIDGET_GRID_PROPS


class TkBuilderUI(Application):
    """Main gui class"""

    def _create_ui(self):
        """Creates all gui widgets"""

        class WidgetContainer(object):
            """Dummy container class"""
            pass

        self.counter = Counter()
        self.widgets = widgets = WidgetContainer()
        self.prop_vars = ArrayVar()
        self.cb_prop_vars = None

        widgets.frame1 = f1 = ttk.Frame(self)
        f1.grid(row=0, column=0, sticky='nswe')
        f1.columnconfigure(1, weight=1)

        widgets.project_lbl = w = ttk.Label(f1, text='Project:')
        w.grid(row=0, column=0, sticky='nw')

        widgets.project_name = w = ttk.Label(f1, text='NewProject1',
            anchor=tkinter.W)
        w.grid(row=0, column=1, sticky='nw')

        #menu
        widgets.menu_btn = w = tkinter.Menubutton(f1, text='◉')
        w.grid(row=0, column=2)

        widgets.mainmenu = w = tkinter.Menu(widgets.menu_btn)
        w.add_command(label='Open …', command=self.on_menuitem_open_clicked)
        w.add_command(label='Save …', command=self.on_menuitem_save_clicked)
        w.add_separator()
        w.add_command(label='Quit …', command=self.quit)

        widgets.menu_btn.configure(menu=widgets.mainmenu)

        #Main paned window
        widgets.mainpane = mp = ttk.Panedwindow(self, orient='horizontal')
        mp.grid(row=1, column=0, sticky='nsew')

        #subpane1
        widgets.pane1 = pane1 = ttk.PanedWindow(self, orient='vertical')
        mp.add(pane1)

        #Treeview on pane1
        widgets.treeview = w = create_scrollable(pane1, ttk.Treeview)
        pane1.add(w.frame)
        self.config_treeview()

        #Properties frame
        widgets.propframe = f = ttk.Frame(pane1)
        f.columnconfigure(1, weight=1)
        pane1.add(f)

        values = list(CLASS_MAP.keys())
        values.sort()
        widgets.class_cbox_var = v = tkinter.StringVar()
        widgets.class_cbox = w = ttk.Combobox(f,
            state='readonly', textvariable=v, values=values)
        w.grid(row=0, column=0)
        v.set('Frame')

        #add widget button
        widgets.add_btn = w = ttk.Button(f, text='Add',
            command=self.on_add_btn_clicked)
        w.grid(row=0, column=1, padx=(5, 0))

        #properties frame
        widgets.notebook = nb = ttk.Notebook(f)
        nb.grid(row=1, column=0, columnspan=2, sticky=tkinter.NSEW)
        self.create_properties_editor(nb)

        #canvas viewer
        widgets.preview = f2 = ttk.Labelframe(mp, text='Preview')
        f2.rowconfigure(0, weight=1)
        f2.columnconfigure(0, weight=1)
        mp.add(f2)

        widgets.canvas = w = create_scrollable(f2, tkinter.Canvas,
            background='white')
        w.frame.grid(sticky=tkinter.NSEW)

        self.config_canvas()

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        #app config
        self.set_title('A tkinter GUI builder')
        self.set_size('800x600')
        self.pack_configure(padx=5, pady=5)


    def config_canvas(self):
        """Configures the canvas"""

        self.widgets.canvas.configure(scrollregion=(0, 0, "50i", "50i"))
        self.widgets.canvaswindow = self.widgets.canvas.create_window(1, 1,
            anchor='nw')


    def config_treeview(self):
        """Sets treeview columns and other params"""

        tv = self.widgets.treeview
        columns = ITEM_PROPS
        #dcols = WIDGET_ATTRS + WIDGET_GRID_PROPS
        dcols = tuple()
        hcols = ('Widgets',) + columns
        configure_treeview(tv, columns, displaycolumns=dcols, headings=hcols,
            show_tree=True)
        tv.bind('<<TreeviewSelect>>', self.on_treeview_select)
        tv.bind('<KeyPress-Delete>', self.on_treeview_delete_item)


    def create_property_widget(self, master, propertyname):
        """Creates a ui widget to edit the property"""

        widget = None
        widgetvar = self.prop_vars(propertyname)

        wtype = ''
        if propertyname in tkbuilder.TK_WIDGET_PROPS:
            wdata = tkbuilder.TK_WIDGET_PROPS[propertyname]
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


    def update_property_widget(self, widget, treeitem,
            propertyname, classname):
        wtype = ''
        if propertyname in tkbuilder.TK_WIDGET_PROPS:
            wdata = tkbuilder.TK_WIDGET_PROPS[propertyname]
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

        treevalues = self.widgets.treeview.set(treeitem)
        variable = self.prop_vars(propertyname)
        if propertyname in treevalues:
            variable.set(treevalues[propertyname])


    def create_properties_editor(self, notebook):
        """Create a frame with a list of all editable properties"""

        editor_frame = ttk.Frame(notebook)
        editor_frame.columnconfigure(1, weight=1)
        notebook.add(editor_frame, text='General', sticky=tkinter.NSEW)

        self.widgets.prop_editor = prop_editor = {}

        row=0
        col=0
        for name in WIDGET_ATTRS:
            labeltext = "{0}:".format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_property_widget(editor_frame, name)
            label.grid(row=row, column=col, sticky=tkinter.EW)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW)
            row += 1
            prop_editor[name] = (label, widget)
            #initialy hide all
            label.grid_remove()
            widget.grid_remove()

        for name in WIDGET_PROPS:
            labeltext = "{0}:".format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_property_widget(editor_frame, name)
            label.grid(row=row, column=col, sticky=tkinter.EW)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW)
            row += 1
            prop_editor[name] = (label, widget)
            #initialy hide all
            label.grid_remove()
            widget.grid_remove()

        editor_frame = ttk.Frame(notebook)
        editor_frame.columnconfigure(1, weight=1)
        notebook.add(editor_frame, text='Packing', sticky=tkinter.NSEW)

        for name in WIDGET_GRID_PROPS:
            labeltext = "{0}:".format(name)
            label = ttk.Label(editor_frame, text=labeltext, anchor=tkinter.W)
            widget = self.create_property_widget(editor_frame, name)
            label.grid(row=row, column=col, sticky=tkinter.EW)
            widget.grid(row=row, column=col+1, sticky=tkinter.EW)
            row += 1
            prop_editor[name] = (label, widget)
            #initialy hide all
            label.grid_remove()
            widget.grid_remove()

        #connect callback
        self.cb_prop_vars = self.prop_vars.trace(mode="w",
            callback=self.on_property_variable_changed)

        return editor_frame


    def hide_all_properties(self):
        """Hide all properties from property editor."""

        for pname in ITEM_PROPS:
            label, widget = self.widgets.prop_editor[pname]
            label.grid_remove()
            widget.grid_remove()


    def edit_item_properties(self, item):
        """Copies properties values from the treeview to the
           properties editor so they can be edited."""

        #first disable callback for better performance ??
        self.prop_vars.trace_vdelete("w", self.cb_prop_vars)

        tv = self.widgets.treeview
        values = tv.set(item)
        wclass = values['class']
        wprops = WIDGET_ATTRS + tuple(CLASS_MAP[wclass]['properties']) \
            + WIDGET_GRID_PROPS

        for key in values.keys():
            if key in wprops:
                label, widget = self.widgets.prop_editor[key]
                self.update_property_widget(widget, item, key, wclass)
                label.grid()
                widget.grid()
            else:
                label, widget = self.widgets.prop_editor[key]
                label.grid_remove()
                widget.grid_remove()

        #re-enable callback
        #connect callback
        self.cb_prop_vars = self.prop_vars.trace(mode="w",
            callback=self.on_property_variable_changed)


    def on_property_variable_changed(self, varname, elementname, mode):
        '''Updates treeview values from property editor'''

        new_value = self.prop_vars[elementname]
        tv = self.widgets.treeview
        sel = tv.selection()
        if sel:
            item = sel[0]
            tv.set(item, elementname, new_value)
            if elementname in WIDGET_ATTRS:
                widget_id = tv.set(item, 'id')
                wclass = tv.set(item, 'class')
                treenode_label = '{0} - {1}'.format(widget_id,wclass)
                tv.item(item, text=treenode_label)
            self.draw_widget(self.get_toplevel_parent(item))


    def get_toplevel_parent(self, treeitem):
        tv = self.widgets.treeview
        toplevel_items = tv.get_children()
        toplevel_parent = None

        item = treeitem
        while not (item in toplevel_items):
            item = tv.parent(item)

        return item


    def on_treeview_select(self, event):
        """Get the selected treeitem and display properties in
            property editor."""

        tv = self.widgets.treeview
        sel = tv.selection()
        if sel:
            item = sel[0]
            rootitems = tv.get_children()
            if item in rootitems:
                self.draw_widget(item)
            self.edit_item_properties(item)


    def on_treeview_delete_item(self, event):
        """Removes item from treeview"""

        tv = self.widgets.treeview
        sel = tv.selection()
        toplevel_items = tv.get_children()
        if sel:
            item = sel[0]
            parent = ''
            if item not in toplevel_items:
                parent = self.get_toplevel_parent(item)
            else:
                self.hide_all_properties()
            tv.delete(item)
            self.draw_widget(parent)


    def draw_widget(self, item):
        """Create a preview of the selected treeview item"""

        #TODO: Fix this draw method, currently it consumes a lot of memory.
        # Maybe maintain a reference to the widget y update using that
        # reference.   To text xml genration, put a button that sais
        # "render in toplevel" or something.
        tv = self.widgets.treeview
        canvas = self.widgets.canvas

        widget = ''
        if item:
            values = tv.set(item)
            uniqueid = values['id']
            xmlnode = self.tree_node_to_xml(tv, '', item)
            builder = tkbuilder.Tkbuilder()
            builder.add_from_xmlnode(xmlnode)
            widget = builder.get_object(canvas, uniqueid)

        canvas.delete(self.widgets.canvaswindow)
        self.widgets.canvaswindow = canvas.create_window(1, 1, anchor='nw')
        canvas.itemconfigure(self.widgets.canvaswindow, window=widget)


    def on_add_btn_clicked(self):
        """Adds selected widget class to treeview"""

        tree = self.widgets.treeview
        #get widget class name to insert
        wclass = self.widgets.class_cbox_var.get()
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
            sclass = svalues['class']
            if CLASS_MAP[sclass]['container'] == True:
                #selected item is a container, set as root.
                root = selected_item
            else:
                #the item parent should be the container
                root = tree.parent(selected_item)

        #if insertion is at top level,
        #check that item to insert is a container.
        if not root:
            if CLASS_MAP[wclass]['container'] == False:
                print('Warning: Widget to insert is not a container.')
                return

        #root item should be set at this point

        #increment class counter
        self.counter[wclass] += 1

        #setup properties
        widget_id = '{0}_{1}'.format(wclass, self.counter[wclass])
        wvalues = [wclass, widget_id]

        treenode_label = '{0} - {1}'.format(widget_id,wclass)
        item = tree.insert(root, 'end', text=treenode_label)
        tree.set(item, 'class', wclass)
        tree.set(item, 'id', widget_id)
        #default text for widgets with text prop:
        prop_name = 'text'
        if prop_name in CLASS_MAP[wclass]['properties']:
            tree.set(item, prop_name, widget_id)
        #default grid properties
        for prop_name in WIDGET_GRID_PROPS:
            tree.set(item, prop_name, '')
        rownum = str(len(tree.get_children(root)) - 1)
        tree.set(item, 'row', rownum)
        tree.set(item, 'column', '0')

        #select and show the item created
        tree.selection_set(item)
        tree.see(item)


    def on_menuitem_open_clicked(self):
        """Opens xml file and load to treeview"""

        fname = filedialog.askopenfilename()
        if fname:
            self.load_file(fname)


    def on_menuitem_save_clicked(self):
        """Save treeview to xml file"""

        fname = filedialog.asksaveasfilename()
        if fname:
            xml_tree = self.tree_to_xml()
            #xml_tree.write(fname, encoding='utf-8', xml_declaration=True)

            xmlvar = xml.dom.minidom.parseString(
                ET.tostring(xml_tree.getroot()))
            pretty_xml_as_string = xmlvar.toprettyxml(indent=' '*4)
            with open(fname, 'w') as f:
                f.write(pretty_xml_as_string)
            #print(pretty_xml_as_string)


    def load_file(self, filename):
        """Load xml into treeview"""

        self.counter.clear()
        etree = ET.parse(filename)
        eroot = etree.getroot()

        for element in eroot:
            self.populate_tree('', eroot, element)
        self.widgets.project_name.configure(text=filename)


    def populate_tree(self, master, parent, element):
        """Reads xml nodes and populates tree item"""

        cname = element.get('class')
        uniqueid = element.get('id')

        if cname in CLASS_MAP:
            #update counter
            self.counter[cname] += 1
            treenode_label = '{0} - {1}'.format(uniqueid, cname)
            pwidget = self.widgets.treeview.insert(master, 'end',
                text=treenode_label)
            self.widgets.treeview.set(pwidget, 'class', cname)
            self.widgets.treeview.set(pwidget, 'id', uniqueid)

            #packing element must be present
            xpath = './packing'
            packing_elem = element.find(xpath)
            properties = self.get_properties(packing_elem)
            for k, v in properties.items():
                self.widgets.treeview.set(pwidget, k, v)

            xpath = "./child"
            children = element.findall(xpath)
            for child in children:
                child_object = child.find('./object')
                cwidget = self.populate_tree(pwidget, child, child_object)
                #self.configure_layout(element, child, pwidget, cwidget)

            self.config_tree_widget(pwidget, cname, element)
            return pwidget
        else:
            raise Exception('Class "{0}" not mapped'.format(cname))


    def config_tree_widget(self, widget, cname, element):
        """Reads xml property nodes and populates tree item"""

        properties = self.get_properties(element)

        for pname, value in properties.items():
            self.widgets.treeview.set(widget, pname, value)


    def get_properties(self, element):
        """Gets name, value from property nodes in element"""

        properties = element.findall('./property')
        pdict= {}
        for p in properties:
            pdict[p.get('name')] = p.text
        return pdict


    def tree_to_xml(self):
        """Traverses treeview and generates a ElementTree object"""

        tree = self.widgets.treeview
        root = ET.Element('interface')
        items = tree.get_children()
        for item in items:
            node = self.tree_node_to_xml(tree, '', item)
            root.append(node)

        return ET.ElementTree(root)


    def tree_node_to_xml(self, tree, parent, item):
        """Converts a treeview item and children to xml nodes"""

        values = tree.set(item)
        node = ET.Element('object')

        for prop in WIDGET_ATTRS:
            node.set(prop, values[prop])

        wclass_props = CLASS_MAP[values['class']]['properties']
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
            cwidget = self.tree_node_to_xml(tree, item, child)
            cnode.append(cwidget)
            node.append(cnode)

        #create packing node
        packing_node = ET.Element('packing')
        has_packing = False
        for prop in WIDGET_GRID_PROPS:
            pv = values.get(prop, None)
            print('packing:', prop, pv)
            if pv:
                has_packing = True
                pnode = ET.Element('property')
                pnode.set('name', prop)
                pnode.text = pv
                packing_node.append(pnode)
        if has_packing:
            node.append(packing_node)

        return node


if __name__ == '__main__':
    app = TkBuilderUI(tkinter.Tk())
    app.run()
