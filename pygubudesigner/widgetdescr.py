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
from collections import defaultdict

from pygubu.builder import data_dict_to_xmlnode, data_xmlnode_to_dict
from .util.observable import Observable
from .properties import TRANSLATABLE_PROPERTIES


class WidgetDescr(dict, Observable):

    def __init__(self, _class, _id):
        super(dict, self).__init__()
        #properties
        self['class'] = _class
        self['id'] = _id
        self['properties'] = {}
        self['layout'] = {}
        self['layout']['rows'] = defaultdict(dict)
        self['layout']['columns'] = defaultdict(dict)
        self['bindings'] = []


    def get_class(self):
        return self['class']


    def get_id(self):
        return self['id']

    def set_id(self, newid):
        self['id'] = newid


    def set_property(self, name, value):
        if name in ('id', 'class'):
            self[name] = value
        else:
            self['properties'][name] = value


    def get_property(self, name):
        if name in ('id', 'class'):
            return self[name]
        else:
            return self['properties'].get(name, '')


    def set_layout_property(self, name, value):
        self['layout'][name] = value


    def get_layout_property(self, name):
        default = ''
        if name in ('row', 'column'):
            default = '0'
        return self['layout'].get(name, default)


    def set_grid_row_property(self, row, name, value):
        self['layout']['rows'][row][name] = value


    def get_grid_row_property(self, row, name):
        return self['layout']['rows'][row].get(name, '0')


    def set_grid_col_property(self, col, name, value):
        self['layout']['columns'][col][name] = value


    def get_grid_col_property(self, col, name):
        return self['layout']['columns'][col].get(name, '0')


    def to_xml_node(self):
        return data_dict_to_xmlnode(self, TRANSLATABLE_PROPERTIES)


    def from_xml_node(self, node):
        data = data_xmlnode_to_dict(node)
        self.update(data)

    def get_bindings(self):
        blist = []
        for v in self['bindings']:
            blist.append((v['sequence'], v['handler'], v['add']))
        return blist

    def clear_bindings(self):
        self['bindings'] = []

    def add_binding(self, seq, handler, add):
        self['bindings'].append({
            'sequence': seq,
            'handler': handler,
            'add': add
            })
