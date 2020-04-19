from __future__ import unicode_literals, print_function
import xml.etree.ElementTree as ET
import operator
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
    
    @classmethod
    def from_xmlnode(cls, element, translator=None):
        meta = cls(element.get('class'), element.get('id'))
    
        # properties
        properties = element.findall('./property')
        pdict = {}
        for p in properties:
            pvalue = p.text
            if translator is not None and p.get('translatable'):
                pvalue = translator(pvalue)
            pdict[p.get('name')] = pvalue
    
        meta.properties = pdict
    
        # Bindings
        bindings = []
        bind_elements = element.findall('./bind')
        for e in bind_elements:
            binding = BindingMeta(
                e.get('sequence'), e.get('handler'), e.get('add')
            )
            bindings.append(binding)
        meta.bindings = bindings
    
        # layout properties
        # use grid layout by default
        manager = 'grid'
        layout_elem = element.find('./layout')
        if layout_elem is not None:
            manager = layout_elem.get('manager', 'grid')
            meta.manager = manager
            props = layout_elem.findall('./property')
            if manager == 'grid':
                for p in props:
                    ptype = p.get('type', None)
                    if ptype is None:
                        meta.layout_properties[p.get('name')] = p.text
                    else:
                        rcid = p.get('id')
                        rcname = p.get('name')
                        rcvalue = p.text
                        line = GridRCLine(ptype, rcid, rcname, rcvalue)
                        meta.gridrc_properties.append(line)
            else:
                for p in props:
                    meta.layout_properties[p.get('name')] = p.text
        return meta
    
    def to_xmlnode(self, translatable_props=None):
        node = ET.Element('object')
    
        node.set('class', self.classname)
        node.set('id', self.identifier)
    
        pkeys = sorted(self.properties.keys())
        for pkey in pkeys:
            pnode = ET.Element('property')
            pnode.set('name', pkey)
            pnode.text = self.properties[pkey]
            if (translatable_props is not None 
                and pkey in translatable_props):
                pnode.set('translatable', 'yes')
            node.append(pnode)
    
        # bindings:
        bindings = sorted(self.bindings, key=operator.itemgetter(0, 1))
        for b in bindings:
            bind = ET.Element('bind')
            for key in b._fields:
                bind.set(key, getattr(b, key))
            node.append(bind)
    
        # layout:
        if self.layout_required:
            # create layout node
            layout_node = ET.Element('layout')
            layout_node.set('manager', self.manager)
            
            keys = sorted(self.layout_properties)
            for prop in keys:
                pnode = ET.Element('property')
                pnode.set('name', prop)
                pnode.text = self.layout_properties[prop]
                layout_node.append(pnode)
            
            lines = sorted(self.gridrc_properties,
                           key=operator.itemgetter(0,1,2))
            for line in lines:
                p = ET.Element('property')
                p.set('type', line.rctype)
                p.set('id', line.rcid)
                p.set('name', line.pname)
                p.text = line.pvalue
                layout_node.append(p)
            # Append node layout
            node.append(layout_node)
        return node


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