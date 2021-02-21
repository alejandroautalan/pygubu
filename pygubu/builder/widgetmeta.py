# encoding: UTF-8
from __future__ import unicode_literals, print_function
import xml.etree.ElementTree as ET
from collections import namedtuple

__all__ = ['WidgetMeta', 'BindingMeta']

BindingMeta = namedtuple('BindingMeta',
                         ['sequence', 'handler', 'add'])

GridRCLine = namedtuple('GridRCLine', ['rctype', 'rcid', 'pname', 'pvalue'])


class WidgetMeta(object):
    def __init__(self, cname, identifier, manager=None,
                 properties_defaults=None,
                 layout_defaults=None):
        super(WidgetMeta, self).__init__()
        self.classname = cname
        self.identifier = identifier
        self.properties = {}
        self.bindings = []
        self._manager = manager if manager is not None else 'grid'
        self.layout_required = True
        self.layout_properties = {}
        self.gridrc_properties = []
        self.properties_defaults = properties_defaults if properties_defaults \
            is not None else {}
        self.layout_defaults = layout_defaults if layout_defaults \
            is not None else {}
        
        # init defaults
        self.apply_properties_defaults()
        self.apply_layout_defaults()
    
    @property
    def manager(self):
        return self._manager
    
    @manager.setter
    def manager(self, value):
        self._manager = value
        
    def apply_properties_defaults(self):
        for name, value in self.properties_defaults.items():
            self.properties[name] = value
    
    def apply_layout_defaults(self):
        layout_defaults_by_manager = self.layout_defaults
        if self.manager in self.layout_defaults:
            layout_defaults_by_manager = self.layout_defaults[self.manager]
        for name, value in layout_defaults_by_manager.items():
            self.layout_properties[name] = value
    
    def has_layout_defined(self):
        return (len(self.layout_properties) > 0)
    
    def clear_layout(self):
        self.layout_properties = {}
        self.gridrc_properties = []
        self.apply_layout_defaults()
    
    def get_gridrc_value(self, rctype, rcid, pname):
        value = None
        for line in self.gridrc_properties:
            if (line.rctype == rctype and line.rcid == rcid
                and line.pname == pname):
                value = line.pvalue
                break
        return value
    
    def set_gridrc_value(self, rctype, rcid, pname, value):
        index = None
        for i, r in enumerate(self.gridrc_properties):
            if r.rctype == rctype and r.rcid == rcid and r.pname == pname:
                index = i
                break
        if index is None:
            line = GridRCLine(rctype, rcid, pname, value)
            self.gridrc_properties.append(line)
        else:
            line = GridRCLine(rctype, rcid, pname, value)
            self.gridrc_properties[index] = line
    
    def __repr__(self):
        tpl = '''<WidgetMeta classname: {0} identifier: {1}>'''
        return tpl.format(self.classname, self.identifier)
    
    def copy_gridrc(self, from_, rctype):
        '''Copy gridrc lines of type rctype from from_'''
        rc = [ line for line in self.gridrc_properties 
               if line.rctype != rctype ]
        for line in from_.gridrc_properties:
            if line.rctype == rctype:
                rc.append(line)
        self.gridrc_properties = rc
    
    def copy_properties(self, wfrom):
        self.properties = wfrom.properties.copy()


if __name__ == '__main__':
    w = WidgetMeta('mywidget', 'w1')
    w.manager = 'pack'
    w.properties = {
        'key1': 'value1',
        'key2': 'value2'
    }
    w.bindings = [
        BindingMeta('<<event_1>>', 'callback_1', ''),
        BindingMeta('<<event_2>>', 'callback_2', '+')
    ]
    w.layout_properties = {
        'prop1': 'value1',
        'prop2': 'value2'
    }
    
    print('To xml')
    node = w.to_xmlnode()
    node = ET.tostring(node)
    print(node, end='\n\n')
    
    print('From xml:')
    strdata = '''<?xml version='1.0' encoding='utf-8'?>
<object class="ttk.Label" id="Label_1">
        <property name="text" translatable="yes">Label_1</property>
        <property name="background">yellow</property>
        <layout manager="grid">
          <property name="propagate">True</property>
          <property type="row" id="0" name="pad">20</property>
          <property type="col" id="0" name="pad">10</property>
          <property type="row" id="0" name="weight">1</property>
        </layout>
      </object>
    '''
    node = ET.fromstring(strdata)
    meta = WidgetMeta.from_xmlnode(node)
    print(meta)