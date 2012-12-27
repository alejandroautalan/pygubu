import xml.etree.ElementTree as ET
import tkinter
from tkinter import ttk


_default_entry_prop = {
    'input_method': 'entry',
}

_default_spinbox_prop = {
    'input_method': 'spinbox',
    'min': 0,
    'max': 999,
}

_dimension_prop = {
    'input_method': 'spinbox',
    'min': 0,
    'max': 999,
}

TK_WIDGET_PROPS = {
    'activestyle': {
        'input_method': 'choice',
        'values': ('', 'underline', 'dotbox', 'none')
        },
    'anchor': {
        'input_method': 'choice',
        'values': ('', tkinter.W, tkinter.CENTER, tkinter.E),
        },
    'background': _default_entry_prop,
    'borderwidth': _dimension_prop,
    'class_': _default_entry_prop,
    'command': _default_entry_prop,
    'compound': {
        'input_method': 'choice',
        'values': {
            'Label': ('', 'bottom', 'image', 'left', 'none',
                'right', 'text', 'top'),
            'Button': ('', tkinter.constants.TOP, tkinter.constants.BOTTOM,
                tkinter.constants.LEFT, tkinter.constants.RIGHT),
            'Checkbutton':('', tkinter.constants.TOP, tkinter.constants.BOTTOM,
                tkinter.constants.LEFT, tkinter.constants.RIGHT)
            }
        },
    'cursor': {
        'input_method': 'choice',
        'values': ('', 'arrow', 'based_arrow_down', 'based_arrow_up', 'boat',
            'bogosity', 'bottom_left_corner', 'bottom_right_corner',
            'bottom_side', 'bottom_tee', 'box_spiral', 'center_ptr', 'circle',
            'clock', 'coffee_mug', 'cross', 'cross_reverse', 'crosshair',
            'diamond_cross', 'dot', 'dotbox', 'double_arrow',  'draft_large',
            'draft_small', 'draped_box', 'exchange', 'fleur', 'gobbler',
            'gumby', 'hand1', 'hand2', 'heart', 'icon', 'iron_cross',
            'left_ptr', 'left_side', 'left_tee', 'leftbutton', 'll_angle',
            'lr_angle', 'man', 'middlebutton', 'mouse', 'pencil', 'pirate',
            'plus', 'question_arrow', 'right_ptr', 'right_side', 'right_tee',
            'rightbutton', 'rtl_logo', 'sailboat', 'sb_down_arrow',
            'sb_h_double_arrow', 'sb_left_arrow', 'sb_right_arrow',
            'sb_up_arrow', 'sb_v_double_arrow', 'shuttle', 'sizing', 'spider',
            'spraycan', 'star', 'target', 'tcross', 'top_left_arrow',
            'top_left_corner', 'top_right_corner', 'top_side', 'top_tee',
            'trek', 'ul_angle', 'umbrella', 'ur_angle', 'watch', 'xterm',
            'X_cursor')
        },
    'disabledforeground': _default_entry_prop, #FIXME color prop
    'exportselection': {
        'input_method': 'choice',
        'values': ('', '0', '1')
        },
    'font': _default_entry_prop,
    'foreground': _default_entry_prop, #FIXME color prop
    'height': _dimension_prop, #FIXME this prop has diferent interpretations
    'highlightbackground': _default_entry_prop, #FIXME color prop
    'highlightcolor': _default_entry_prop, #FIXME color prop
    'highlightthickness': _default_entry_prop,
    'invalidcommand': _default_entry_prop,
    'image': _default_entry_prop,
    'justify': {
        'input_method': 'choice',
        'values': ('', tkinter.constants.LEFT, tkinter.constants.CENTER,
            tkinter.constants.RIGHT),
        },
    'listvariable': _default_entry_prop,
    'onvalue': _default_entry_prop,
    'orient': {
        'input_method': 'choice',
        'values': (tkinter.constants.VERTICAL, tkinter.constants.HORIZONTAL)
        },
    'padding': _dimension_prop,
    'postcommand': _default_entry_prop,
    'relief': {
        'input_method': 'choice',
        'values': ('', tkinter.constants.FLAT, 'raised', 'sunken', 'groove', 'ridge')
        },
    'selectbackground': _default_entry_prop, #FIXME color prop
    'selectborderwidth': _default_spinbox_prop,
    'selectforeground': _default_entry_prop, #FIXME color prop
    'selectmode': {
        'input_method': 'choice',
        'values': ('', tkinter.constants.BROWSE, tkinter.constants.SINGLE,
            tkinter.constants.MULTIPLE, tkinter.constants.EXTENDED)
        },
    'show': _default_entry_prop,
    'state': {
        'input_method': 'choice',
        'values': {
            'Entry': ('', tkinter.constants.NORMAL,
                tkinter.constants.DISABLED, 'disabled'),
            'Combobox': ('', 'readonly'),
            'Listbox': ('', tkinter.constants.NORMAL,
                tkinter.constants.DISABLED)
            }
        },
    'style': _default_entry_prop,
    'takefocus': {
        'input_method': 'choice',
        'values': ('', tkinter.constants.TRUE, tkinter.constants.FALSE),
        },
    'text': _default_entry_prop,
    'textvariable': _default_entry_prop,
    'underline': _default_spinbox_prop,
    'validate': _default_entry_prop,
    'validatecommand': _default_entry_prop,
    'value': _default_entry_prop,
    'values': _default_entry_prop, #FIXME This should be treated as a list?
    'width': _dimension_prop, #FIXME width is not a dimension for Entry
    'wraphlength':_dimension_prop,
    'xscrollcommand': _default_entry_prop,
    'yscrollcommand': _default_entry_prop,
}

TK_GRID_PROPS = {
#grid packing properties
    'column': _default_spinbox_prop,
    'columnspan': _default_spinbox_prop,
    'in_': _default_entry_prop,
    'ipadx': _default_spinbox_prop,
    'ipady': _default_spinbox_prop,
    'padx': _default_spinbox_prop,
    'pady': _default_spinbox_prop,
    'row': _default_spinbox_prop,
    'rowspan': _default_spinbox_prop,
    'sticky': {
        'input_method': 'choice',
        'values': ('', tkinter.constants.N, tkinter.constants.S,
            tkinter.constants.E, tkinter.constants.W,
            tkinter.constants.NE, tkinter.constants.NW,
            tkinter.constants.SE, tkinter.constants.SW,
            tkinter.constants.EW, tkinter.constants.NS,
            tkinter.constants.NS + tkinter.constants.W,
            tkinter.constants.NS + tkinter.constants.E,
            tkinter.constants.NSEW
            )
        }
}

TK_GRID_RC_PROPS = {
#grid row and column properties (can be applied to each row or column)
    'minsize': _default_spinbox_prop,
    'pad': _default_spinbox_prop,
    'weight': _default_spinbox_prop
}

TK_LAYOUT_PROPS = dict(TK_GRID_PROPS)
TK_LAYOUT_PROPS.update(TK_GRID_RC_PROPS)


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
            'underline', 'value', 'variable', 'width',
            ],
        },
    'Combobox': {
        'class': ttk.Combobox,
        'container': False,
        'properties': ['class_', 'cursor', 'exportselection',
            'height', 'justify', 'postcommand', 'style', 'takefocus',
            'textvariable', 'validate', 'validatecommand', 'values',
            'width', 'xscrollcommand', 'state'
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

        if cname in CLASS_MAP:
            pwidget = CLASS_MAP[cname]['class'](master)

            self.widgets[uniqueid] = pwidget

            xpath = "./child"
            children = element.findall(xpath)
            for child in children:
                child_object = child.find('./object')
                cwidget = self.realize(pwidget, child_object)

            self.configure_widget(pwidget, cname, element)
            self.configure_layout(element, pwidget)
            return pwidget
        else:
            raise Exception('Class "{0}" not mapped'.format(cname))


    def configure_layout(self, element, widget):
        #use grid layout for all
        #get packing properties
        packing_elem = element.find('./packing')
        layout_properties = self.get_properties(packing_elem)

        widget.grid(**layout_properties)

        #get grid row and col properties:
        erows = packing_elem.find('./rows')
        if erows is not None:
            rows = erows.findall('./row')
            for row in rows:
                row_id = row.get('id')
                row_properties = self.get_properties(row)
                widget.rowconfigure(row_id, **row_properties)

        ecolums = packing_elem.find('./columns')
        if ecolums is not None:
            columns = ecolums.findall('./column')
            for column in columns:
                column_id = column.get('id')
                column_properties = self.get_properties(column)
                widget.columnconfigure(column_id, **row_properties)


    def configure_widget(self, widget, cname, element):
        properties = self.get_properties(element)
        attrib = {}

        for pname, value in properties.items():
            widget[pname] = value


    def get_properties(self, element):
        properties = element.findall('./property')
        pdict= {}
        for p in properties:
            pdict[p.get('name')] = p.text
        return pdict


