from __future__ import unicode_literals, print_function
import sys
import xml.etree.ElementTree as ET
from pygubu.builder.widgetmeta import WidgetMeta


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


class UIDefinition(object):
    def __init__(self, author=None, wmetaclass=None, translator=None):
        super(UIDefinition, self).__init__()
        self.tree = None
        self.root = None
        self.version = 0
        self.author = author if author is not None else ''
        self.wmetaclass = wmetaclass
        if wmetaclass is None:
            self.wmetaclass = WidgetMeta
        self.translator = translator
        self.__create()
        
    def __create(self):
        self.root = root = ET.Element('interface')
        root.set('version', '1.0')
        if self.author:
            root.set('author', self.author)
        self.tree = ET.ElementTree(root)
    
    def _tree_load(self, tree):
        self.tree = tree
        self.root = tree.getroot()
        self.version = self.root.get('version', '')
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
    
    def load_from_string(self, source):
        self._tree_load(ET.ElementTree(ET.fromstring(source)))
        
    def add_xmlnode(self, node, parent=None):
        if parent is None:
            self.root.append(node)
        else:
            parent.append(node)
        return node
    
    def add_xmlchild(self, parent, node):
        xpath = "./child"
        child = parent.find(xpath)
        if child is None:
            child = ET.Element('child')
            parent.append(child)
        child.append(node)
        
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
            wmeta = self.wmetaclass.from_xmlnode(node, self.translator)
        return wmeta
    
    def widgets(self):
        xpath = "./object"
        children = self.root.findall(xpath)
        for child in children:
            wmeta = self.wmetaclass.from_xmlnode(child, self.translator)
            yield wmeta
    
    def widget_children(self, identifier):
        xpath = ".//object[@id='{0}']".format(identifier)
        node = self.tree.find(xpath)
        if node is not None:
            xpath = "./child"
            children = node.findall(xpath)
            for child in children:
                oxml = child.find('./object')
                wmeta = self.wmetaclass.from_xmlnode(oxml, self.translator)
                yield wmeta
        


if __name__ == '__main__':
    ui = UIDefinition('Module test')
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
