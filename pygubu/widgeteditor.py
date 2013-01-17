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

import xml.dom.minidom
import xml.etree.ElementTree as ET
from collections import Counter

from . import builder
from . import util
from . import properties


class WidgetsTreeEditor:
    def __init__(self, app):
        self.app = app
        self.treeview = app.treeview
        self.previewer = app.previewer
        self.treedata = {}
        self.counter = Counter()
        self.config_treeview()


    def config_treeview(self):
        """Sets treeview columns and other params"""
        tree = self.treeview
        columns = tuple()
        dcols = tuple()
        hcols = ('Widget Tree',) + columns
        util.configure_treeview(tree, columns, displaycolumns=dcols,
            headings=hcols, show_tree=True)
        tree.bind('<KeyPress-Delete>', self.on_treeview_delete_item)
        tree.bind('<Double-1>', self.on_treeview_double_click)


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
            item = self.get_toplevel_parent(item)
            widget_id = self.treedata[item]['id']
            xmlnode = self.tree_node_to_xml('', item)
            self.previewer.draw(item, widget_id, xmlnode)


    def on_treeview_double_click(self, event):
        tv = self.treeview
        sel = tv.selection()
        toplevel_items = tv.get_children()
        if sel:
            item = sel[0]
            self.draw_widget(item)


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
                self.previewer.delete(item)
            del self.treedata[item]
            tv.delete(item)
            self.draw_widget(parent)


    def tree_to_xml(self):
        """Traverses treeview and generates a ElementTree object"""

        tree = self.treeview
        root = ET.Element('interface')
        items = tree.get_children()
        for item in items:
            node = self.tree_node_to_xml('', item)
            root.append(node)

        return ET.ElementTree(root)


    def tree_node_to_xml(self, parent, item):
        """Converts a treeview item and children to xml nodes"""

        tree = self.treeview
        values = self.treedata[item]
        node = ET.Element('object')

        for prop in properties.OBJECT_DEFAULT_ATTRS:
            node.set(prop, values[prop])

        wclass_props = builder.CLASS_MAP[values['class']].properties
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
        for prop in properties.PropertiesMap[properties.GROUP_LAYOUT_GRID]:
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
            if builder.CLASS_MAP[sclass].container == True:
                #selected item is a container, set as root.
                root = selected_item
            else:
                #the item parent should be the container
                root = tree.parent(selected_item)

        #if insertion is at top level,
        #check that item to insert is a container.
        if not root:
            if builder.CLASS_MAP[wclass].container == False:
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
        for pname in builder.CLASS_MAP[wclass].properties:
            data[pname] = ''
            #default text for widgets with text prop:
            if pname == 'text':
                data[pname] = widget_id

        #default grid properties
        group = 'packing'
        data[group] = {}
        for prop_name in properties.PropertiesMap[properties.GROUP_LAYOUT_GRID]:
            data[group][prop_name] = ''

        rownum = str(len(tree.get_children(root)) - 1)
        data[group]['row'] = rownum
        data[group]['column'] = '0'

        self.treedata[item] = data

        #select and show the item created
        tree.selection_set(item)
        tree.see(item)
        #Do redraw
        self.draw_widget(item)


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

        if cname in builder.CLASS_MAP:
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

