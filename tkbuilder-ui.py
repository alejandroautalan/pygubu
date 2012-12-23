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
    'column', 'columnspan', 'in_', 'ipadx', 'ipady', 'padx', 'pady',
    'row', 'rowspan', 'sticky'
)

ITEM_PROPS = WIDGET_ATTRS + WIDGET_PROPS + WIDGET_GRID_PROPS


class TkBuilderUI(Application):
    
    def _create_ui(self):
        class WidgetContainer(object):
            pass
        
        self.counter = Counter()
        self.widgets = widgets = WidgetContainer()
        
        widgets.project_lbl = w = ttk.Label(self, text='Project:')
        w.grid(row=0, column=0, sticky='nw')
        
        widgets.project_name = w = ttk.Label(self, text='NewProject1')
        w.grid(row=0, column=1, sticky='nw')
        
        #menu
        widgets.menu_btn = w = tkinter.Menubutton(self, text='◉')
        w.grid(row=0, column=2)
        
        widgets.mainmenu = w = tkinter.Menu(widgets.menu_btn)
        w.add_command(label='Open …', command=self.on_menuitem_open_clicked)
        w.add_command(label='Save …', command=self.on_menuitem_save_clicked)
        w.add_separator()
        w.add_command(label='Quit …', command=self.quit)
        
        widgets.menu_btn.configure(menu=widgets.mainmenu)
        
        #Main paned window
        widgets.mainpane = mp = ttk.Panedwindow(self, orient='horizontal')
        mp.grid(row=1, column=0, columnspan=3, sticky='nsew')
        
        #treeview pane
        widgets.treeview = w = create_scrollable(mp, ttk.Treeview)
        mp.add(w.frame, weight=1)
        self.config_treeview()
        
        #Properties pane
        widgets.propframe = f = ttk.Frame(mp)
        mp.add(f, weight=1)
        
        values = list(CLASS_MAP.keys())
        values.sort()
        widgets.class_cbox_var = v = tkinter.StringVar()
        widgets.class_cbox = w = ttk.Combobox(f,
            state='readonly', textvariable=v, values=values)
        w.grid(row=0, column=0)
        v.set('Frame')
        
        widgets.add_btn = w = ttk.Button(f, text='Add',
            command=self.on_add_btn_clicked)
        w.grid(row=0, column=1, padx=(5,0))
        
        #canvas viewer
        widgets.canvas = w = create_scrollable(mp, tkinter.Canvas,
            background='white')
        mp.add(w.frame, weight=3)
        self.config_canvas()
        
        
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        

        #app config
        self.set_title('SQLA Explorer')
        self.set_size('800x600')
        self.pack_configure(padx=5, pady=5)


    def config_canvas(self):
        self.widgets.canvas.configure(scrollregion=(0, 0, "50i", "50i"))
        self.widgets.canvaswindow = self.widgets.canvas.create_window(1, 1,
            anchor='nw')

    
    def config_treeview(self):
        """Sets treeview columns and other params"""
        
        tv = self.widgets.treeview
        columns = ITEM_PROPS
        #dcols = WIDGET_ATTRS + WIDGET_GRID_PROPS
        dcols = tuple()
        #hcols = ('widget',) + columns
        hcols = None
        configure_treeview(tv, columns, displaycolumns=dcols, headings=hcols,
            show_tree=True)
        tv.bind('<<TreeviewSelect>>', self.on_treeview_select)
    
    
    def on_treeview_select(self, event):
        tv = self.widgets.treeview
        sel = tv.selection()
        if sel:
            item = sel[0]
            rootitems = tv.get_children()
            if item in rootitems:
                self.draw_widget(item)
                
    
    def draw_widget(self, item):
        tv = self.widgets.treeview
        canvas = self.widgets.canvas
        values = tv.set(item)
        uniqueid = values['id']
        xmlnode = self.tree_node_to_xml(tv, '', item)
        builder = tkbuilder.Tkbuilder()
        builder.add_from_xmlnode(xmlnode)
        widget = builder.get_object(canvas, uniqueid)
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


    def populate_tree(self, master, parent, element):
        """Reads xml nodes and populates tree item"""
        
        cname = element.get('class')
        uniqueid = element.get('id')
        
        #print('on serialize for ', cname)
        
        if cname in CLASS_MAP:
            #update counter
            self.counter[cname] += 1
            pwidget = self.widgets.treeview.insert(master, 'end', text=uniqueid)
            self.widgets.treeview.set(pwidget, 'class', cname)
            self.widgets.treeview.set(pwidget, 'id', uniqueid)
            
            xpath = './packing'
            packing_elem = parent.find(xpath)
            if packing_elem is not None:
                properties = self.get_properties(packing_elem)
                print(properties)
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
            
            values = tree.set(child)
            packing_node = ET.Element('packing')
            has_packing = False
            for prop in WIDGET_GRID_PROPS:
                pv = values.get(prop, None)
                if pv:
                    has_packing = True
                    pnode = ET.Element('property')
                    pnode.set('name', prop)
                    pnode.text = pv
                    packing_node.append(pnode)
            if has_packing:
                cnode.append(packing_node)
            
            node.append(cnode)
        
        return node
            
        

if __name__ == '__main__':
    app = TkBuilderUI(tkinter.Tk())
    app.run()
