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

import os
import importlib
import logging
import xml.etree.ElementTree as ET
import tkinter
from tkinter import ttk
from collections import defaultdict

from pygubu.builder.builderobject import *
from pygubu.stockimage import *
import pygubu.builder.tkstdwidgets

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('pygubu.builder')

#
#
#
def data_xmlnode_to_dict(element):
    data = {}

    data['class'] = element.get('class')
    data['id'] = element.get('id')

    #properties
    properties = element.findall('./property')
    pdict= {}
    for p in properties:
        pdict[p.get('name')] = p.text

    data['properties'] = pdict

    #Bindings
    bindings = []
    bind_elements = element.findall('./bind')
    for e in bind_elements:
        bindings.append({
            'sequence': e.get('sequence'),
            'handler': e.get('handler'),
            'add': e.get('add')
            })
    data['bindings'] = bindings

    #get layout properties
    #use grid layout for all
    layout_properties = {}
    layout_elem = element.find('./layout')
    if layout_elem is not None:
        props = layout_elem.findall('./property')
        for p in props:
            layout_properties[p.get('name')] = p.text

        #get grid row and col properties:
        rows_dict = defaultdict(dict)
        erows = layout_elem.find('./rows')
        if erows is not None:
            rows = erows.findall('./row')
            for row in rows:
                row_id = row.get('id')
                row_properties = {}
                props = row.findall('./property')
                for p in props:
                    row_properties[p.get('name')] = p.text
                rows_dict[row_id] = row_properties
        layout_properties['rows'] = rows_dict

        columns_dict = defaultdict(dict)
        ecolums = layout_elem.find('./columns')
        if ecolums is not None:
            columns = ecolums.findall('./column')
            for column in columns:
                column_id = column.get('id')
                column_properties = {}
                props = column.findall('./property')
                for p in props:
                    column_properties[p.get('name')] = p.text
                columns_dict[column_id] = column_properties
        layout_properties['columns'] = columns_dict
    data['layout'] = layout_properties

    return data


def data_dict_to_xmlnode(data):
    node = ET.Element('object')

    for prop in ('id', 'class'):
        node.set(prop, data[prop])

    wclass_props = CLASS_MAP[data['class']].classobj.properties
    for prop in wclass_props:
        pv = data['properties'].get(prop, None)
        if pv:
            pnode = ET.Element('property')
            pnode.set('name', prop)
            pnode.text = pv
            node.append(pnode)

    #bindings:
    for v in data['bindings']:
        bind = ET.Element('bind')
        for attr, value in v.items():
            bind.set(attr, value)
        node.append(bind)

    #layout:
    layout_required = CLASS_MAP[data['class']].classobj.layout_required
    if layout_required:
        #create layout node
        layout = data['layout']
        layout_node = ET.Element('layout')
        has_layout = False
        for prop in layout:
            pv = layout[prop]
            if pv and prop != 'rows' and prop != 'columns':
                has_layout = True
                pnode = ET.Element('property')
                pnode.set('name', prop)
                pnode.text = pv
                layout_node.append(pnode)
        keys = {'rows':'row', 'columns':'column'}
        for key in keys:
            if key in layout:
                erows = ET.Element(key)
                include_key = False
                for rowid in layout[key]:
                    erow = ET.Element(keys[key])
                    erow.set('id', rowid)
                    inlcude_rc = False
                    for pname in layout[key][rowid]:
                        include_key = True
                        inlcude_rc = True
                        eprop = ET.Element('property')
                        eprop.set('name', pname)
                        eprop.text = layout[key][rowid][pname]
                        erow.append(eprop)
                    if inlcude_rc:
                        erows.append(erow)
                if include_key:
                    layout_node.append(erows)

        if has_layout:
            node.append(layout_node)

    return node


#
# Builder class
#

class Builder:
    """Allows to build a tk interface from xml definition."""

    def __init__(self):
        self.tree = None
        self.root = None
        self.objects = {}
        self.tkvariables = {}
        self._resource_paths = []


    def add_resource_path(self, path):
        self._resource_paths.append(path)


    def get_image(self, name):
        image = ''
        if not StockImage.is_registered(name):
            ipath = self.__find_image(name)
            if ipath is not None:
                StockImage.register(name, ipath)
        try:
            image = StockImage.get(name)
        except StockImageException as e:
            pass
        return image


    def __find_image(self, name):
        image_path = None
        for rp in self._resource_paths:
            path = os.path.join(rp, name)
            if os.path.exists(path):
                image_path = path
                break
        return image_path


    def get_variable(self, varname):
        """
        Returns a tk variable created previously.
        """
        return self.tkvariables[varname]


    def create_variable(self, varname, vtype=None):
        """
        Create a tk variable

        If the variable was created previously return that instance.
        """

        var = None
        if varname in self.tkvariables:
            var = self.tkvariables[varname]
        else:
            if vtype is None:
                #get type from name
                lvname = varname.lower()
                if lvname.startswith('int'):
                    var = tkinter.IntVar()
                elif lvname.startswith('bool'):
                    var = tkinter.BooleanVar()
                elif lvname.startswith('double'):
                    var = tkinter.DoubleVar()
                else:
                    var = tkinter.StringVar()
            else:
                var = vtype()

            self.tkvariables[varname] = var
        return var


    def add_from_file(self, fpath):
        if self.tree is None:
            base, name = os.path.split(fpath)
            self.add_resource_path(base)
            self.tree = tree = ET.parse(fpath)
            self.root = tree.getroot()
            self.objects = {}
        else:
            #TODO: append to current tree
            pass


    def add_from_string(self, strdata):
        if self.tree is None:
            self.tree = tree = ET.ElementTree(ET.fromstring(strdata))
            self.root = tree.getroot()
            self.objects = {}
        else:
            #TODO: append to current tree
            pass


    def add_from_xmlnode(self, element):
        if self.tree is None:
            root = ET.Element('interface')
            root.append(element)
            self.tree = tree = ET.ElementTree(root)
            self.root = tree.getroot()
            self.objects = {}
            #ET.dump(tree)
        else:
            #TODO: append to current tree
            pass


    def get_object(self, name, master=None):
        widget = None
        if name in self.objects:
            widget = self.objects[name].widget
        else:
            xpath = ".//object[@id='{0}']".format(name)
            node = self.tree.find(xpath)
            if node is not None:
                root = BuilderObject(self, dict())
                root.widget = master
                bobject = self.realize(root, node)
                widget = bobject.widget
        if widget is None:
            raise Exception('Widget not defined.')
        return widget


    def _import_class(self, modulename):
        if modulename.startswith('ttk.'):
            importlib.import_module('pygubu.builder.ttkstdwidgets')
        else:
            importlib.import_module(modulename)


    def realize(self, master, element):
        """Builds a widget from xml element using master as parent"""

        data = data_xmlnode_to_dict(element)
        cname = data['class']
        uniqueid = data['id']

        if cname not in CLASS_MAP:
            self._import_class(cname)

        if cname in CLASS_MAP:
            self._check_data(data)
            parent = CLASS_MAP[cname].classobj.factory(self, data)
            widget = parent.realize(master)

            self.objects[uniqueid] = parent

            xpath = "./child"
            children = element.findall(xpath)
            for child in children:
                child_xml = child.find('./object')
                child = self.realize(parent, child_xml)
                parent.add_child(child)

            parent.configure()
            parent.layout()
            return parent
        else:
            raise Exception('Class "{0}" not mapped'.format(cname))


    def _check_data(self, data):
        cname = data['class']
        uniqueid = data['id']
        layout = data['layout']
        layout_required = CLASS_MAP[cname].classobj.layout_required
        if layout_required and not layout:
            logger.warning('No layout information for: (%s, %s).',
                cname, uniqueid)


    def connect_callbacks(self, callbacks_bag):
        notconnected = []
        for wname, builderobj in self.objects.items():
            missing = builderobj.connect_commands(callbacks_bag)
            if missing is not None:
                notconnected.extend(missing)
            missing = builderobj.connect_bindings(callbacks_bag)
            if missing is not None:
                notconnected.extend(missing)
        if notconnected:
            notconnected = list(set(notconnected))
            msg = 'Missing callbacks for commands: {}'.format(notconnected)
            logger.warning(msg)
            return notconnected
        else:
            return None

