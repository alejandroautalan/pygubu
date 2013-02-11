from collections import defaultdict

import pygubu.builder
from .util.observable import Observable


class WidgetDescr(dict, Observable):

    def __init__(self, _class, _id):
        super(dict, self).__init__()
        #properties
        self['class'] = _class
        self['id'] = _id
        self['properties'] = {}
        self['layout'] = {}


    def get_class(self):
        return self['class']


    def get_id(self):
        return self['id']


    def set_property(self, name, value):
        if name == 'id':
            self[name] = value
        else:
            self['properties'][name] = value


    def get_property(self, name):
        return self['properties'].get(name, None)


    def set_layout_propery(self, name, value):
        self['layout'][name] = value


    def get_layout_propery(self, name):
        return self['layout'].get(name, None)


    def set_grid_row_property(self, row, name, value):
        if 'rows' not in self['layout']:
            self['layout']['rows'] = defaultdict(dict)
        self['layout']['rows'][row][name] = value


    def get_grid_row_property(self, row, name):
        return self['layout']['rows'][row].get(name, None)


    def set_grid_col_property(self, col, name, value):
        if 'rows' not in self['layout']:
            self['layout']['columns'] = defaultdict(dict)
        self['layout']['columns'][col][name] = value


    def get_grid_col_property(self, col, name):
        return self['layout']['columns'][col].get(name, None)


    def to_xml_node(self):
        return pygubu.builder.data_dict_to_xmlnode(self)


    def from_xml_node(self, node):
        data = pygubu.builder.data_xmlnode_to_dict(node)
        self.update(data)



