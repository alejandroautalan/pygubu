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
        self['layout']['rows'] = defaultdict(dict)
        self['layout']['columns'] = defaultdict(dict)


    def get_class(self):
        return self['class']


    def get_id(self):
        return self['id']


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


    def set_layout_propery(self, name, value):
        self['layout'][name] = value


    def get_layout_propery(self, name):
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
        return pygubu.builder.data_dict_to_xmlnode(self)


    def from_xml_node(self, node):
        data = pygubu.builder.data_xmlnode_to_dict(node)
        self.update(data)



