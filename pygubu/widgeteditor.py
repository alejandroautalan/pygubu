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
from collections import Counter, defaultdict

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
        keys = {'rows':'row', 'columns':'column'}
        for key in keys:
            if key in pvalues:
                erows = ET.Element(key)
                for rowid in pvalues[key]:
                    erow = ET.Element(keys[key])
                    erow.set('id', rowid)
                    for pname in pvalues[key][rowid]:
                        eprop = ET.Element('property')
                        eprop.set('name', pname)
                        eprop.text = pvalues[key][rowid][pname]
                        erow.append(eprop)
                    erows.append(erow)
                packing_node.append(erows)

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
            selected_is_container = builder.CLASS_MAP[sclass].container
            if selected_is_container:
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
        if root:
            rootclass = self.treedata[root]['class']
            children_count = len(self.treeview.get_children(root))
            maxchildren = builder.CLASS_MAP[rootclass].maxchildren
            print('childrencount {}, maxchildren {}'.format(children_count, maxchildren))
            if maxchildren is not None and children_count >= maxchildren:
                print('Only {} children allowed'.format(maxchildren))
                return
            allowed_children = builder.CLASS_MAP[rootclass].allowed_children
            print('class {} allowed {}'.format(rootclass, allowed_children))
            if allowed_children is not None and wclass not in allowed_children:
                print('Child class {} not allowed'.format(wclass))
                return
            allowed_parents = builder.CLASS_MAP[wclass].allowed_parents
            print('class {} allowed parents {}'.format(rootclass, allowed_parents))
            if allowed_parents is not None and rootclass not in allowed_parents:
                print('Parent class {} not allowed for {}'.format(rootclass, wclass))
                return
        else:
            ##Validate if it can be added at root level
            allowed_parents = builder.CLASS_MAP[wclass].allowed_parents
            if allowed_parents is not None and 'root' not in allowed_parents:
                print('Class {} not allowed at root level'.format(wclass))
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
            pdescription = {}
            pgroup = properties.GROUP_WIDGET
            if pname in properties.PropertiesMap[pgroup]:
                pdescription = properties.PropertiesMap[pgroup][pname]
            else:
                pgroup = properties.GROUP_CUSTOM
                pdescription = properties.PropertiesMap[pgroup][pname]
            if wclass in pdescription:
                pdescription = dict(pdescription, **pdescription[wclass])
            data[pname] = str(pdescription.get('default', ''))
            #default text for widgets with text prop:
            if pname in ('text', 'label'):
                data[pname] = widget_id

        #default grid properties
        is_container = builder.CLASS_MAP[wclass].container
        group = 'packing'
        data[group] = {}
        for prop_name in properties.PropertiesMap[properties.GROUP_LAYOUT_GRID]:
            data[group][prop_name] = ''

        rownum = str(len(tree.get_children(root)) - 1)
        data[group]['row'] = rownum
        data[group]['column'] = '0'

        if is_container:
            data[group]['rows'] = defaultdict(dict)
            data[group]['columns'] = defaultdict(dict)

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
                #get grid row and col properties:
                rows_dict = defaultdict(dict)
                erows = packing_elem.find('./rows')
                if erows is not None:
                    rows = erows.findall('./row')
                    for row in rows:
                        row_id = row.get('id')
                        row_properties = self.get_properties(row)
                        rows_dict[row_id] = row_properties
                data['packing']['rows'] = rows_dict

                columns_dict = defaultdict(dict)
                ecolums = packing_elem.find('./columns')
                if ecolums is not None:
                    columns = ecolums.findall('./column')
                    for column in columns:
                        column_id = column.get('id')
                        column_properties = self.get_properties(column)
                        columns_dict[column_id] = column_properties
                data['packing']['columns'] = columns_dict

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

