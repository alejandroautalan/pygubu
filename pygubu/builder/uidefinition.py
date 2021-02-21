# encoding: UTF-8
from __future__ import unicode_literals, print_function
import sys
import json
import operator
import xml.etree.ElementTree as ET
from pygubu.builder.builderobject import CLASS_MAP
from pygubu.builder.widgetmeta import WidgetMeta, BindingMeta, GridRCLine


# in-place prettyprint formatter
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:  # Python 2
    JSONDecodeError = ValueError


class UIDefinition(object):
    TRANSLATABLE_PROPERTIES = ['label', 'text', 'title']
    TK_COMMAND_PROPERTIES =(
        'command', 'validatecommand', 'invalidcommand', 'postcommand',
        'xscrollcommand', 'yscrollcommand', 'tearoffcommand',
    )
    
    def __init__(self, wmetaclass=None, translator=None):
        super(UIDefinition, self).__init__()
        self.tree = None
        self.root = None
        self._latest_version = '1.1'
        self.version = self._latest_version
        self.author = ''
        self._ignore_properties = (
            'command_id_arg', 'idtocommand',
            'validatecommand_args', 'invalidcommand_args',
        )
        self.wmetaclass = wmetaclass
        if wmetaclass is None:
            self.wmetaclass = WidgetMeta
        self.translator = translator
        self.__create()
    
    def _prop_from_xml(self, pnode, element):
        pname = pnode.get('name')
        pvalue = pnode.text
        
        if pname in self._ignore_properties:
            return (None, None)
        
        if self.translator is not None and pnode.get('translatable'):
            pvalue = self.translator(pvalue)
        
        # if node has a type property, send value as a json string
        jvalue = {}
        if pnode.get('type'):
            for attr, attrval in pnode.items():
                jvalue[attr] = attrval
            jvalue['value'] = pnode.text
            pvalue = json.dumps(jvalue)
        # Process old ui versions
        if self.version < '1.1':
            if pname in self.TK_COMMAND_PROPERTIES:
                cmd = {
                    'type': 'command',
                    'value': pnode.text,
                    'cbtype': 'simple',
                    'args': '',
                }
                # get old format value
                xpath = "./property[@name='{0}']"
                for oldp in ('command_id_arg', 'idtocommand'):
                    dpath = xpath.format(oldp)
                    node = element.find(dpath)
                    if node is not None:
                        nvalue = node.text.lower()
                        if nvalue == 'true':
                            cmd['cbtype'] = 'with_wid'
                
                if pname in ('validatecommand', 'invalidcommand'):
                    cmd['cbtype'] = 'entry_validate'
                    # get old format args
                    pargs = '{0}_args'.format(pname)
                    dpath = xpath.format(pargs)
                    node = element.find(dpath)
                    if node is not None:
                        cmd['args'] = node.text
                pvalue = json.dumps(cmd)
        return (pname, pvalue)
    
    def xmlnode_to_widget(self, element):
        elemid = element.get('id')
        meta = self.wmetaclass(element.get('class'), elemid)
    
        # properties
        properties = element.findall('./property')
        pdict = {}
        for p in properties:
            pname, pvalue = self._prop_from_xml(p, element)
            if pname is not None:
                pdict[pname] = pvalue
        
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
        if self.version == '':
            # try to load old version grid rc info
            # Gridrc info was in the parent, or
            # in the widget itself if has no parent.
            xpath = ".//*[@id='{0}']/../..".format(elemid)
            parent = self.root.find(xpath)
            if parent is None:
                if layout_elem is not None:
                    self.__load_old_gridrc_layout(layout_elem, meta)
            else:
                layout_elem = parent.find('./layout')
                if layout_elem is not None:
                    self.__load_old_gridrc_layout(layout_elem, meta)
        
        return meta
    
    def __load_old_gridrc_layout(self, element, meta):
        '''Load old grid rc information.'''
        
        rows = element.findall('./rows/row')
        for row in rows:
            rid = row.get('id')
            props = row.findall('./property')
            for p in props:
                rpname = p.get('name')
                rpvalue = p.text
                line = GridRCLine('row', rid, rpname, rpvalue)
                meta.gridrc_properties.append(line)
        columns = element.findall('./columns/column')
        for col in columns:
            cid = col.get('id')
            props = col.findall('./property')
            for p in props:
                cpname = p.get('name')
                cpvalue = p.text
                line = GridRCLine('col', cid, cpname, cpvalue)
                meta.gridrc_properties.append(line)
        
    def _prop_to_xml(self, pname, pvalue):
        pnode = ET.Element('property')
        pnode.set('name', pname)
        pnode.text = pvalue
        if pname in self.TRANSLATABLE_PROPERTIES:
            pnode.set('translatable', 'yes')
        # if pvalue is a json do special
        try:
            dv = json.loads(pvalue)
            if isinstance(dv, dict):
                if 'value' not in dv:
                    raise Exception('Invalid json value for property')
                for k, attrval in dv.items():
                    if k != 'value':
                        pnode.set(k, str(attrval))
                pnode.text = dv['value']
        except JSONDecodeError:
            pass
        
        return pnode
    
    def widget_to_xmlnode(self, wmeta):
        '''Returns xml representation of widget'''
        
        node = ET.Element('object')
    
        node.set('class', wmeta.classname)
        node.set('id', wmeta.identifier)
    
        pkeys = sorted(wmeta.properties.keys())
        for pkey in pkeys:
            pnode = self._prop_to_xml(pkey, wmeta.properties[pkey])
            node.append(pnode)
    
        # bindings:
        bindings = sorted(wmeta.bindings, key=operator.itemgetter(0, 1))
        for b in bindings:
            bind = ET.Element('bind')
            for key in b._fields:
                bind.set(key, getattr(b, key))
            node.append(bind)
    
        # layout:
        #if self.layout_required:
        if CLASS_MAP[wmeta.classname].builder.layout_required:
            # create layout node
            layout_node = ET.Element('layout')
            layout_node.set('manager', wmeta.manager)
            
            keys = sorted(wmeta.layout_properties)
            for prop in keys:
                pnode = ET.Element('property')
                pnode.set('name', prop)
                pnode.text = wmeta.layout_properties[prop]
                layout_node.append(pnode)
            
            lines = sorted(wmeta.gridrc_properties,
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
        
    def __create(self):
        # Version 1.0: start of schema versioning, implements multiple layout managers
        # Version 1.1: remove idtocommand and command_id_arg properties
        self.root = root = ET.Element('interface')
        root.set('version', self._latest_version)
        if self.author:
            root.set('author', self.author)
        self.tree = ET.ElementTree(root)
    
    def _tree_load(self, tree, default_version=None):
        if default_version is None:
            default_version = ''
        self.tree = tree
        self.root = tree.getroot()
        self.version = self.root.get('version', default_version)
        self.author = self.root.get('author', '')
    
    def load_file(self, file_or_filename):
        etree = None
        # python2 issues
        try:
            etree = ET.parse(file_or_filename)
        except ET.ParseError:
            parser = ET.XMLParser(encoding='UTF-8')
            etree = ET.parse(file_or_filename, parser)
        self._tree_load(etree)
    
    def load_from_string(self, source, version=None):
        tree = ET.ElementTree(ET.fromstring(source))
        self._tree_load(tree, version)
    
    def get_xmlnode(self, identifier):
        xpath = ".//object[@id='{0}']".format(identifier)
        node = self.tree.find(xpath)
        return node
        
    def add_xmlnode(self, node, parent=None):
        if parent is None:
            self.root.append(node)
        else:
            parent.append(node)
        return node
    
    def add_xmlchild(self, parent, node):
        child = ET.Element('child')
        child.append(node)
        parent.append(child)
        
    def __str__(self):
        encoding='unicode'
        if sys.version_info < (3,0):
            encoding='utf-8'
        return ET.tostring(self.root, encoding=encoding)
    
    def __repr__(self):
        return '<UIFile xml="{0}">'.format(self.__str__())
        
    def save(self, file_or_filename):
        indent(self.root)
        self.tree.write(file_or_filename,
                        xml_declaration=True, encoding='utf-8')
    
    def get_widget(self, identifier):
        wmeta = None
        xpath = ".//object[@id='{0}']".format(identifier)
        node = self.tree.find(xpath)
        if node is not None:
            wmeta = self.xmlnode_to_widget(node)
        return wmeta
    
    def widgets(self):
        xpath = "./object"
        children = self.root.findall(xpath)
        for child in children:
            wmeta = self.xmlnode_to_widget(child)
            yield wmeta
    
    def widget_children(self, identifier):
        xpath = ".//object[@id='{0}']".format(identifier)
        node = self.tree.find(xpath)
        if node is not None:
            xpath = "./child/object"
            children = node.findall(xpath)
            for child in children:
                wmeta = self.xmlnode_to_widget(child)
                yield wmeta
    
    def replace_widget(self, identifier, rootmeta):
        xpath = ".//object[@id='{0}']".format(identifier)
        parent = self.root.find(xpath + '/..')
        target = parent.find(xpath)
        
        if parent is not None:
            # found something
            parent.remove(target)
            replacement = self.widget_to_xmlnode(rootmeta)
            xpath = "./child/object"
            children = target.findall(xpath)
            for child in children:
                self.add_xmlchild(replacement, child)
            if parent.tag == 'interface':
                parent.append(replacement)
            else:
                self.add_xmlchild(parent, replacement)
        


if __name__ == '__main__':
    ui = UIDefinition()
    ui.author = 'Module test'
    print(ui)
    
    xml='''<?xml version='1.0' encoding='utf-8'?>
<interface author="anonymous">
</interface>
'''
    ui.load_from_string(xml)
    print(ui, ui.author, ui.version)
    
    print('Iterating file:')
    fname = 'managers.ui'
    ui.load_file(fname)
    
    def print_widgets(w):
        print(w)
        for cw in ui.widget_children(w.identifier):
            print_widgets(cw)
    
    for w in ui.widgets():
        print_widgets(w)
