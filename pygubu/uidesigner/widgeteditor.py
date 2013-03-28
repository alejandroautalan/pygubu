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

import xml.dom.minidom
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
import logging

from pygubu import builder
from . import util
from . import properties
from .widgetdescr import WidgetDescr


logger = logging.getLogger('pygubu.designer')


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
        columns = ('class', 'row', 'col', 'space_trick')
        dcols = columns
        hcols = ('Widget Tree', ' '*10, ' '*2, ' '*2, ' ')
        util.configure_treeview(tree, columns, displaycolumns=dcols,
            headings=hcols, show_tree=True)
        tree.bind('<KeyPress-Delete>', self.on_treeview_delete_item)
        tree.bind('<Double-1>', self.on_treeview_double_click)
        tree.bind('<<TreeviewSelect>>', self.on_treeview_select, add='+')
        tree.bind('<Control-KeyPress-i>', self.on_item_move_up)
        tree.bind('<Control-KeyPress-k>', self.on_item_move_down)


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
            selected_id = self.treedata[item]['id']
            item = self.get_toplevel_parent(item)
            widget_id = self.treedata[item]['id']
            wclass = self.treedata[item]['class']
            xmlnode = self.tree_node_to_xml('', item)
            is_menu = True if wclass == 'tk.Menu' else False
            self.previewer.draw(item, widget_id, xmlnode, is_menu)
            self.previewer.show_selected(item, selected_id)


    def on_treeview_double_click(self, event):
        tv = self.treeview
        sel = tv.selection()
        toplevel_items = tv.get_children()
        if sel:
            item = sel[0]
            if tv.parent(item) == '':
                #only redraw if toplevel is double clicked
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
            self.app.set_changed()
            if parent:
                self.draw_widget(parent)
            else:
                self.app.properties_editor.hide_all()


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
        data = self.treedata[item]
        node = data.to_xml_node()

        children = tree.get_children(item)
        for child in children:
            cnode = ET.Element('child')
            cwidget = self.tree_node_to_xml(item, child)
            cnode.append(cwidget)
            node.append(cnode)

        return node


    def _insert_item(self, root, data):
        tree = self.treeview
        treelabel = data.get_id()
        row = col = ''
        if root != '' and 'layout' in data:
            #if 'row' in data['layout']:
            #    row = data['layout']['row']
            #    col = data['layout']['column']
            row = data.get_layout_propery('row')
            col = data.get_layout_propery('column')
        values = (data.get_class(), row, col)
        item = tree.insert(root, 'end', text=treelabel, values=values)
        data.attach(self)
        self.app.set_changed()

        return item


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
            sclass = self.treedata[selected_item].get_class()
            selected_is_container = builder.CLASS_MAP[sclass].classobj.container
            if selected_is_container:
                #selected item is a container, set as root.
                root = selected_item
            else:
                #the item parent should be the container
                root = tree.parent(selected_item)

        #if insertion is at top level,
        #check that item to insert is a container.
        if not root:
            if builder.CLASS_MAP[wclass].classobj.container == False:
                logger.warning('{0} is not a container.'.format(wclass))
                return
        if root:
            rootclass = self.treedata[root].get_class()
            children_count = len(self.treeview.get_children(root))
            maxchildren = builder.CLASS_MAP[rootclass].classobj.maxchildren
            #print('childrencount {}, maxchildren {}'.format(children_count, maxchildren))
            if maxchildren is not None and children_count >= maxchildren:
                logger.warning('Only {} children allowed'.format(maxchildren))
                return
            allowed_children = builder.CLASS_MAP[rootclass].classobj.allowed_children
            #print('class {} allowed {}'.format(rootclass, allowed_children))
            if allowed_children is not None and wclass not in allowed_children:
                msg = '{0} is not allowed as child of {1}'.format(wclass, rootclass)
                logger.warning(msg)
                return
            allowed_parents = builder.CLASS_MAP[wclass].classobj.allowed_parents
            #print('class {} allowed parents {}'.format(rootclass, allowed_parents))
            if allowed_parents is not None and rootclass not in allowed_parents:
                logger.warning('{0} is not allowed as parent of {1}'.format(rootclass, wclass))
                return
        else:
            ##Validate if it can be added at root level
            allowed_parents = builder.CLASS_MAP[wclass].classobj.allowed_parents
            if allowed_parents is not None and 'root' not in allowed_parents:
                logger.warning('{0} not allowed at root level'.format(wclass))
                return

        #root item should be set at this point
        #increment class counter
        self.counter[wclass] += 1

        #setup properties
        widget_id = '{0}_{1}'.format(wclass, self.counter[wclass])

        data = WidgetDescr(wclass, widget_id)

        #setup default values for properties
        for pname in builder.CLASS_MAP[wclass].classobj.properties:
            pdescription = {}
            pgroup = properties.GROUP_WIDGET
            if pname in properties.PropertiesMap[pgroup]:
                pdescription = properties.PropertiesMap[pgroup][pname]
            else:
                pgroup = properties.GROUP_CUSTOM
                pdescription = properties.PropertiesMap[pgroup][pname]
            if wclass in pdescription:
                pdescription = dict(pdescription, **pdescription[wclass])
            default_value = str(pdescription.get('default', ''))
            data.set_property(pname, default_value)
            #default text for widgets with text prop:
            if pname in ('text', 'label'):
                data.set_property(pname, widget_id)

        #default grid properties
        is_container = builder.CLASS_MAP[wclass].classobj.container
        pgroup = properties.GROUP_LAYOUT_GRID
        for prop_name in properties.PropertiesMap[pgroup]:
            pdescription = properties.PropertiesMap[pgroup][prop_name]
            if wclass in pdescription:
                pdescription = dict(pdescription, **pdescription[wclass])
            default_value = str(pdescription.get('default', ''))
            data.set_layout_propery(prop_name, default_value)

        rownum = '0'
        if root:
            rownum = str(self.get_max_row(root)+1)
        data.set_layout_propery('row', rownum)
        data.set_layout_propery('column', '0')

        #if is_container:
        #    data[group]['rows'] = defaultdict(dict)
        #    data[group]['columns'] = defaultdict(dict)

        item = self._insert_item(root, data)
        self.treedata[item] = data

        #select and show the item created
        tree.selection_set(item)
        tree.see(item)
        #Do redraw
        self.draw_widget(item)


    def remove_all(self):
        children = self.treeview.get_children()
        if children:
            self.treeview.delete(*children)


    def load_file(self, filename):
        """Load file into treeview"""

        self.counter.clear()
        etree = ET.parse(filename)
        eroot = etree.getroot()

        self.remove_all()

        for element in eroot:
            self.populate_tree('', eroot, element)


    def populate_tree(self, master, parent, element):
        """Reads xml nodes and populates tree item"""

        data = WidgetDescr(None, None)
        data.from_xml_node(element)
        cname = data.get_class()
        uniqueid = data.get_id()

        if cname in builder.CLASS_MAP:
            #update counter
            self.counter[cname] += 1

            pwidget = self._insert_item(master, data)
            self.treedata[pwidget] = data

            xpath = "./child"
            children = element.findall(xpath)
            for child in children:
                child_object = child.find('./object')
                cwidget = self.populate_tree(pwidget, child, child_object)

            return pwidget
        else:
            raise Exception('Class "{0}" not mapped'.format(cname))


    def get_max_row(self, item):
        tree = self.treeview
        max_row = -1
        children = tree.get_children(item)
        for child in children:
            data = self.treedata[child].get('layout', {})
            row = int(data.get('row', 0))
            if row > max_row:
                max_row = row
        return max_row


    def on_treeview_select(self, event):
        tree = self.treeview
        sel = tree.selection()
        if sel:
            item = sel[0]
            top = self.get_toplevel_parent(item)
            selected_id = self.treedata[item].get_id()
            self.previewer.show_selected(top, selected_id)
            max_rc = self.get_max_row_col(item)
            self.app.properties_editor.edit(self.treedata[item], *max_rc)
        else:
            #No selection hide all
            self.app.properties_editor.hide_all()


    def get_max_row_col(self, item):
        tree = self.treeview
        max_row = 0
        max_col = 0
        children = tree.get_children(item)
        for child in children:
            data = self.treedata[child]
            row = int(data.get_layout_propery('row'))
            col = int(data.get_layout_propery('column'))
            if row > max_row:
                max_row = row
            if col > max_col:
                max_col = col
        return (max_row, max_col)


    def update_event(self, obj):
        tree = self.treeview
        data = obj
        item = self.get_item_by_data(obj)
        if item:
            if data.get_id() != tree.item(item, 'text'):
                tree.item(item, text=data.get_id())
            #if tree.parent(item) != '' and 'layout' in data:
            if tree.parent(item) != '':
                row = data.get_layout_propery('row')
                col = data.get_layout_propery('column')
                values = tree.item(item, 'values')
                if (row != values[1] or col != values[2]):
                    values = (data.get_class(), row, col)
                tree.item(item, values=values)
            self.draw_widget(item)
            self.app.set_changed()


    def get_item_by_data(self, data):
        skey = None
        for key, value in self.treedata.items():
            if value == data:
                skey = key
                break
        return skey


    def on_item_move_up(self, event):
        tree = self.treeview
        sel = tree.selection()
        if sel:
            item = sel[0]
            parent = tree.parent(item)
            prev = tree.prev(item)
            if prev:
                prev_idx = tree.index(prev)
                tree.move(item, parent, prev_idx)


    def on_item_move_down(self, event):
        tree = self.treeview
        sel = tree.selection()
        if sel:
            item = sel[0]
            parent = tree.parent(item)
            next = tree.next(item)
            if next:
                next_idx = tree.index(next)
                tree.move(item, parent, next_idx)

