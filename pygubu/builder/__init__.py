# encoding: utf8
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

import os
import importlib
import logging
import xml.etree.ElementTree as ET
try:
    import tkinter
except:
    import Tkinter as tkinter
from collections import defaultdict

from pygubu.builder.builderobject import *
from pygubu.stockimage import *
import pygubu.builder.tkstdwidgets

logger = logging.getLogger(__name__)
logging.basicConfig()  # line added according to python documentation, to load standard Handlers of logging module

def data_xmlnode_to_dict(element, translator=None):
    data = {}

    data['class'] = element.get('class')
    data['id'] = element.get('id')

    # properties
    properties = element.findall('./property')
    pdict = {}
    for p in properties:
        pvalue = p.text
        if translator is not None and p.get('translatable'):
            pvalue = translator(pvalue)
        pdict[p.get('name')] = pvalue

    data['properties'] = pdict

    # Bindings
    bindings = []
    bind_elements = element.findall('./bind')
    for e in bind_elements:
        bindings.append({
            'sequence': e.get('sequence'),
            'handler': e.get('handler'),
            'add': e.get('add')
            })
    data['bindings'] = bindings

    # get layout properties
    # use grid layout for all
    layout_properties = {}
    layout_elem = element.find('./layout')
    if layout_elem is not None:
        props = layout_elem.findall('./property')
        for p in props:
            layout_properties[p.get('name')] = p.text

        # get grid row and col properties:
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


def data_dict_to_xmlnode(data, translatable_props=None):
    node = ET.Element('object')

    for prop in ('id', 'class'):
        node.set(prop, data[prop])

    wclass_props = sorted(CLASS_MAP[data['class']].builder.properties)
    for prop in wclass_props:
        pv = data['properties'].get(prop, None)
        if pv:
            pnode = ET.Element('property')
            pnode.set('name', prop)
            pnode.text = pv
            if translatable_props is not None and prop in translatable_props:
                pnode.set('translatable', 'yes')
            node.append(pnode)

    # bindings:
    bindings = sorted(data['bindings'], key=lambda b: b['sequence'])
    for v in bindings:
        bind = ET.Element('bind')
        for attr, value in v.items():
            bind.set(attr, value)
        node.append(bind)

    # layout:
    layout_required = CLASS_MAP[data['class']].builder.layout_required
    if layout_required:
        # create layout node
        layout = data['layout']
        layout_node = ET.Element('layout')
        has_layout = False
        sorted_keys = sorted(layout)
        for prop in sorted_keys:
            pv = layout[prop]
            if pv and prop != 'rows' and prop != 'columns':
                has_layout = True
                pnode = ET.Element('property')
                pnode.set('name', prop)
                pnode.text = pv
                layout_node.append(pnode)
        keys = {'rows': 'row', 'columns': 'column'}
        for key in keys:
            if key in layout:
                erows = ET.Element(key)
                include_key = False
                sorted_keys = sorted(layout[key])
                for rowid in sorted_keys:
                    erow = ET.Element(keys[key])
                    erow.set('id', rowid)
                    inlcude_rc = False
                    sorted_props = sorted(layout[key][rowid])
                    for pname in sorted_props:
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

class Builder(object):
    """Allows to build a tk interface from xml definition."""

    def __init__(self, translator=None):
        self.tree = None
        self.root = None
        self.objects = {}
        self.tkvariables = {}
        self._resource_paths = []
        self.translator = translator

    def add_resource_path(self, path):
        """Add additional path to the resources paths."""
        self._resource_paths.append(path)

    def get_image(self, path):
        """Return tk image corresponding to name which is taken form path."""
        image = ''
        name = os.path.basename(path)
        if not StockImage.is_registered(name):
            ipath = self.__find_image(path)
            if ipath is not None:
                StockImage.register(name, ipath)
            else:
                msg = "Image '{0}' not found in resource paths.".format(name)
                logger.warning(msg)
        try:
            image = StockImage.get(name)
        except StockImageException:
            # TODO: notify something here.
            pass
        return image

    def __find_image(self, relpath):
        image_path = None
        for rp in self._resource_paths:
            for root, dirs, files in os.walk(rp):
                if relpath in files:
                    image_path = os.path.join(root, relpath)
                    break
            if image_path is not None:
                break
        return image_path

    def get_variable(self, varname):
        """Return a tk variable created with 'create_variable' method."""
        return self.tkvariables[varname]
        
    def import_variables(self, container, varnames=None):
        """Helper method to avoid call get_variable for every variable."""
        if varnames is None:
            for keyword in self.tkvariables:
                setattr(container, keyword, self.tkvariables[keyword])
        else:
            for keyword in varnames:
                if keyword in self.tkvariables:
                    setattr(container, keyword, self.tkvariables[keyword])

    def create_variable(self, varname, vtype=None):
        """Create a tk variable.
        If the variable was created previously return that instance.
        """

        var_types = ('string', 'int', 'boolean', 'double')
        vname = varname
        var = None
        type_from_name = 'string'  # default type
        if ':' in varname:
            type_from_name, vname = varname.split(':')
            #  Fix incorrect order bug #33
            if type_from_name not in (var_types):
                #  Swap order
                type_from_name, vname = vname, type_from_name
                if type_from_name not in (var_types):
                    raise Exception('Undefined variable type in "{0}"'.format(varname))

        if vname in self.tkvariables:
            var = self.tkvariables[vname]
        else:
            if vtype is None:
                # get type from name
                if type_from_name == 'int':
                    var = tkinter.IntVar()
                elif type_from_name == 'boolean':
                    var = tkinter.BooleanVar()
                elif type_from_name == 'double':
                    var = tkinter.DoubleVar()
                else:
                    var = tkinter.StringVar()
            else:
                var = vtype()

            self.tkvariables[vname] = var
        return var

    def add_from_file(self, fpath):
        """Load ui definition from file."""
        if self.tree is None:
            base, name = os.path.split(fpath)
            self.add_resource_path(base)
            self.tree = tree = ET.parse(fpath)
            self.root = tree.getroot()
            self.objects = {}
        else:
            # TODO: append to current tree
            pass

    def add_from_string(self, strdata):
        """Load ui definition from string."""
        if self.tree is None:
            self.tree = tree = ET.ElementTree(ET.fromstring(strdata))
            self.root = tree.getroot()
            self.objects = {}
        else:
            # TODO: append to current tree
            pass

    def add_from_xmlnode(self, element):
        """Load ui definition from xml.etree.Element node."""
        if self.tree is None:
            root = ET.Element('interface')
            root.append(element)
            self.tree = tree = ET.ElementTree(root)
            self.root = tree.getroot()
            self.objects = {}
            # ET.dump(tree)
        else:
            # TODO: append to current tree
            pass

    def get_object(self, name, master=None):
        """Find and create the widget named name.
        Use master as parent. If widget was already created, return
        that instance."""
        widget = None
        if name in self.objects:
            widget = self.objects[name].widget
        else:
            xpath = ".//object[@id='{0}']".format(name)
            node = self.tree.find(xpath)
            if node is not None:
                root = BuilderObject(self, dict())
                root.widget = master
                bobject = self._realize(root, node)
                widget = bobject.widget
        if widget is None:
            raise Exception('Widget not defined.')
        return widget

    def _import_class(self, modulename):
        if modulename.startswith('ttk.'):
            importlib.import_module('pygubu.builder.ttkstdwidgets')
        else:
            # Import module as full path
            try:
                importlib.import_module(modulename)
            except ImportError as e:
                # A single module can contain various widgets
                # try to import the first part of the path
                if '.' in modulename:
                    first, last = modulename.rsplit('.', 1)
                    try:
                        importlib.import_module(first)
                    except ImportError as e:
                        importlib.import_module(last)
                else:
                    raise e

    def _realize(self, master, element):
        """Builds a widget from xml element using master as parent."""

        data = data_xmlnode_to_dict(element, self.translator)
        cname = data['class']
        uniqueid = data['id']

        if cname not in CLASS_MAP:
            self._import_class(cname)

        if cname in CLASS_MAP:
            self._pre_process_data(data)
            parent = CLASS_MAP[cname].builder.factory(self, data)
            widget = parent.realize(master)

            self.objects[uniqueid] = parent

            xpath = "./child"
            children = element.findall(xpath)
            for child in children:
                child_xml = child.find('./object')
                child = self._realize(parent, child_xml)
                parent.add_child(child)

            parent.configure()
            parent.layout()
            return parent
        else:
            raise Exception('Class "{0}" not mapped'.format(cname))

    def _pre_process_data(self, data):
        cname = data['class']
        uniqueid = data['id']
        layout = data['layout']
        layout_required = CLASS_MAP[cname].builder.layout_required
        if layout_required and not layout:
            logger.warning('No layout information for: (%s, %s).',
                           cname, uniqueid)

    def connect_callbacks(self, callbacks_bag):
        """Connect callbacks specified in callbacks_bag with callbacks
        defined in the ui definition.
        Return a list with the name of the callbacks not connected.
        """
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
