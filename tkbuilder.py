import xml.etree.ElementTree as ET
import tkinter
from tkinter import ttk


CLASS_MAP = {
    'Frame': {
        'class': ttk.Frame,
        'container': True,
        'properties': ['class_', 'cursor', 'height', 'padding',
            'relief', 'style', 'takefocus', 'width',
            ],
        },
    'Label': {
        'class': ttk.Label,
        'container': False,
        'properties': ['anchor', 'background', 'borderwidth',
            'class_', 'compound', 'cursor', 'font', 'foreground',
            'image', 'justify', 'padding', 'relief',
            'style', 'takefocus', 'text', 'textvariable', 'underline',
            'width', 'wraphlength',
            ],
        },
    'Button': {
        'class': ttk.Button,
        'container': False,
        'properties': ['class_', 'command', 'compound', 'cursor',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline',
            ],
        },
    'Entry': {
        'class': ttk.Entry,
        'container': False,
        'properties': ['class_', 'cursor', 'exportselection', 'font',
            'invalidcommand', 'justify', 'show', 'style', 'takefocus',
            'textvariable', 'validate', 'validatecommand', 'values',
            'width', 'xscrollcommand',
            ],
        },
    'Checkbutton': {
        'class': ttk.Checkbutton,
        'container': False,
        'properties': ['class_', 'command', 'compound', 'cursor',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'variable', 'offvalue', 'onvalue', 'width',
            ],
        },
    'Radiobutton': {
        'class': ttk.Radiobutton,
        'container': False,
            'properties': ['class_', 'command', 'compound', 'cursor',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'variable', 'width',
            ],
        },
    'Combobox': {
        'class': ttk.Combobox,
        'container': False,
        'properties': ['class_', 'cursor', 'exportselection',
            'height', 'justify', 'postcommand', 'style', 'takefocus',
            'textvariable', 'validate', 'validatecommand', 'values',
            'width', 'xscrollcommand'
            ],
        },
    'Listbox': {
        'class': tkinter.Listbox,
        'container': False,
        'properties': ['activestyle', 'background', 'borderwidth', 'cursor',
            'disabledforeground', 'exportselection', 'font',
            'foreground', 'height', 'highlightbackground', 'highlightcolor',
            'highlightthickness', 'listvariable', 'relief',
            'selectbackground', 'selectborderwidth', 'selectforeground',
            'selectmode', 'state', 'takefocus', 'width', 'xscrollcommand',
            'yscrollcommand',
            ],
        },
    'Scrollbar': {
        'class': ttk.Scrollbar,
        'container': False,
        'properties': ['class_', 'command', 'cursor',
            'orient', 'style', 'takefocus',
            ],
        },
    'Sizegrip': {
        'class': ttk.Sizegrip,
        'container': False,
        'properties': ['class_', 'style', ],
        },
    'Text': {
        'class': tkinter.Text,
        'container': False,
        'properties': ['autoseparators', 'background', 'borderwidth', 'cursor',
            'exportselection', 'font',
            'foreground', 'height', 'highlightbackground', 'highlightcolor',
            'highlightthickness', 'insertbackground', 'insertborderwidth',
            'insertofftime', 'insertontime', 'insertwidth',
            'maxundo', 'padx', 'pady', 'relief', 'selectbackground',
            'selectborderwidth', 'selectforeground', 'spacing1',
            'spacing2', 'spacing3', 'state', 'tabs', 'takefocus',
            'undo', 'width', 'wrap', 'xscrollcommand', 'yscrollcommand',
            ],
        },
    'Progressbar': {
        'class': ttk.Progressbar,
        'container': False,
        'properties': ['class_', 'cursor', 'length', 'maximum', 'mode',
            'orient', 'style', 'takefocus', 'variable',
            ],
        },
    'Scale': {
        'class': ttk.Scale,
        'container': False,
        'properties': ['class_', 'command', 'cursor', 'from_', 'length',
            'orient', 'style', 'takefocus', 'to', 'variable', 'value',
            'variable',
            ],
        },
    'Spinbox': {
        'class': tkinter.Spinbox,
        'container': False,
        'properties': ['activebackground', 'background', 'borderwidth',
            'buttoncursor', 'buttondownrelief', 'buttonup', 'command',
            'cursor', 'disabledbackground', 'disabledforeground',
            'exportselection', 'font', 'foreground', 'format',
            'from_', 'highlightbackground', 'highlightcolor',
            'highlightthickness', 'increment', 'insertbackground',
            'insertborderwidth', 'insertofftime', 'insertontime',
            'insertwidth', 'justify', 'readonlybackground', 'relief',
            'repeatdelay', 'repeatinterval', 'selectbackground',
            'selectborderwidth', 'selectforeground', 'state', 'takefocus',
            'textvariable', 'to', 'values', 'width', 'wrap', 'xscrollcommand',
            ],
        },
    'Separator': {
        'class': ttk.Separator,
        'container': False,
        'properties': ['class_', 'orient', 'style', ],
        },
    'Labelframe': {
        'class': ttk.Labelframe,
        'container': True,
        'properties': ['borderwidth', 'class_', 'cursor', 'height',
            'labelanchor', 'labelwidget', 'padding',
            'relief', 'style', 'takefocus', 'text', 'underline',
            'width',
            ],
        },
    'Panedwindow': {
        'class': ttk.Panedwindow,
        'container': False,
        'properties': ['class_', 'cursor', 'height', 'orient',
            'style', 'takefocus', 'width',
            ],
        },
    'Notebook': {
        'class': ttk.Notebook,
        'container': False,
        'properties': ['class_', 'cursor', 'height',
            'padding', 'style', 'takefocus', 'width',
            ],
        },
    'Menubutton': {
        'class': ttk.Menubutton,
        'container': False,
        'properties': ['class_', 'compound', 'cursor', 'direction',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'width',
            ],
        },
}


class Tkbuilder:
    def __init__(self):
        self.tree = None
        self.root = None
        self.widgets = {}
        
    def add_from_file(self, fpath):
        if self.tree is None:
            self.tree = tree = ET.parse(fpath)
            self.root = tree.getroot()
            self.widgets = {}
        else:
            #TODO: append to current tree
            pass


    def add_from_xmlnode(self, element):
        if self.tree is None:
            root = ET.Element('interface')
            root.append(element)
            self.tree = tree = ET.ElementTree(root)
            self.root = tree.getroot()
            self.widgets = {}
            ET.dump(tree)
        else:
            #TODO: append to current tree
            pass

    
    def get_object(self, master, name):
        widget = None
        if name in self.widgets:
            widget = self.widgets[name]
        else:
            xpath = ".//object[@id='{0}']".format(name)
            node = self.tree.find(xpath)
            if node is not None:
                widget = self.realize(master, node)
        if widget is None:
            raise Exception('Widget not defined.')
        return widget


    def realize(self, master, element):
        cname = element.get('class')
        uniqueid = element.get('id')
        
        #print('on serialize for ', cname)
        
        if cname in CLASS_MAP:
            pwidget = CLASS_MAP[cname]['class'](master)
            
            self.widgets[uniqueid] = pwidget
            
            xpath = "./child"
            children = element.findall(xpath)
            for child in children:
                child_object = child.find('./object')
                cwidget = self.realize(pwidget, child_object)
                self.configure_layout(element, child, pwidget, cwidget)
            
            self.configure_widget(pwidget, cname, element)
            return pwidget
        else:
            raise Exception('Class "{0}" not mapped'.format(cname))


    def configure_layout(self, parent_element, child_element, pwidget, cwidget):
        #use grid layout for all
        parent_class = parent_element.get('class')
        child_class = child_element.find('./object').get('id')
        msg = 'configuring  layout for {0} {1}'.format(parent_class,
            child_class)
        print(msg)
        
        #get packing properties
        packing_elem = child_element.find('./packing')
        #print('child: ', ET.tostring(child_element))
        layout_properties = self.get_properties(packing_elem)
        print(layout_properties)
        
        row = layout_properties.get('row', 0)
        column = layout_properties.get('column', 0)
        #print('row:{0}, column:{1}'.format(row, column))
        
        cwidget.grid(row=row, column=column)
            
    
    def configure_widget(self, widget, cname, element):
        properties = self.get_properties(element)
        attrib = {}
        
        for pname, value in properties.items():
            print('Setting: ', cname, pname, value)
            widget[pname] = value
        
#        for pname, value in properties.items():
#            prop_dict = CLASS_MAP[cname]['properties']['direct']
#            if pname in prop_dict:
#                attrib[prop_dict[pname]] = value
#        if attrib:
#            widget.configure(**attrib)
#            
#        for pname, value in properties.items():
#            prop_dict = CLASS_MAP[cname]['properties']['bymethod']
#            if pname in prop_dict:
#                set_prop_method = prop_dict[pname]
#                set_prop_method(widget, value)


    def get_properties(self, element):
        properties = element.findall('./property')
        pdict= {}
        for p in properties:
            pdict[p.get('name')] = p.text
        return pdict


