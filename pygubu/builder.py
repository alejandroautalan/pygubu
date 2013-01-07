#
# Copyright 2012 Alejandro Autalán
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

import logging
import xml.etree.ElementTree as ET
import tkinter
from tkinter import ttk

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('pygubu.builder')

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

_sticky_prop = {
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

TK_WIDGET_PROPS = {
    'activestyle': {
        'input_method': 'choice',
        'values': ('', 'underline', 'dotbox', 'none')
        },
    'activebackground': _default_entry_prop, #FIXME color property
    'activeborderwidth': _default_spinbox_prop,
    'activeforeground': _default_entry_prop, #FIXME color property
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
            'ttk.Label': ('', 'bottom', 'image', 'left', 'none',
                'right', 'text', 'top'),
            'ttk.Button': ('', tkinter.constants.TOP, tkinter.constants.BOTTOM,
                tkinter.constants.LEFT, tkinter.constants.RIGHT),
            'ttk.Checkbutton':
                ('', tkinter.constants.TOP, tkinter.constants.BOTTOM,
                tkinter.constants.LEFT, tkinter.constants.RIGHT),
            'ttk.Notebook.Tab':
                ('', tkinter.constants.TOP, tkinter.constants.BOTTOM,
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
    'direction': {
        'input_method': 'choice',
        'values': ('', 'above', 'below', 'flush', 'left', 'right')
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
    'image': _default_entry_prop, #FIXME image property
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
    'sticky': _sticky_prop,
    'style': _default_entry_prop,
    'tearoff': _default_entry_prop,
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
    'sticky': _sticky_prop
}

TK_GRID_RC_PROPS = {
#grid row and column properties (can be applied to each row or column)
    'minsize': _default_spinbox_prop,
    'pad': _default_spinbox_prop,
    'weight': _default_spinbox_prop
}


CLASS_MAP = {}


def register(classname, classobj):
    CLASS_MAP[classname] = classobj

#
# Base class
#
class BuilderObject:
    @classmethod
    def factory(cls, master, properties=None, layout_properties=None):
        clsobj = cls(master, properties, layout_properties)
        return clsobj

    def __init__(self, master, properties=None, layout_prop=None):
        self.widget = self.class_(master)
        self.properties = properties
        self.layout_properties = layout_prop

    def configure(self):
        for pname, value in self.properties.items():
            self.widget[pname] = value

    def layout(self):
        #use grid layout for all
        properties = self.layout_properties
        grid_rows = properties.pop('grid_rows', {})
        grid_cols = properties.pop('grid_columns', {})

        self.widget.grid(**properties)

        #get grid row and col properties:
        for row in grid_rows:
            self.widget.rowconfigure(row, **grid_rows[row])
        for col in grid_cols:
            self.widget.columnconfigure(col, **grid_cols[col])

    def add_child(self, cwidget):
        pass


#
# tkinter widgets
#
class TKListbox(BuilderObject):
    class_ =  tkinter.Listbox
    container = False
    properties = ['activestyle', 'background', 'borderwidth', 'cursor',
            'disabledforeground', 'exportselection', 'font',
            'foreground', 'height', 'highlightbackground', 'highlightcolor',
            'highlightthickness', 'listvariable', 'relief',
            'selectbackground', 'selectborderwidth', 'selectforeground',
            'selectmode', 'state', 'takefocus', 'width', 'xscrollcommand',
            'yscrollcommand']

register('Listbox', TKListbox)


class TKText(BuilderObject):
    class_ = tkinter.Text
    container = False
    properties = ['autoseparators', 'background', 'borderwidth', 'cursor',
            'exportselection', 'font',
            'foreground', 'height', 'highlightbackground', 'highlightcolor',
            'highlightthickness', 'insertbackground', 'insertborderwidth',
            'insertofftime', 'insertontime', 'insertwidth',
            'maxundo', 'padx', 'pady', 'relief', 'selectbackground',
            'selectborderwidth', 'selectforeground', 'spacing1',
            'spacing2', 'spacing3', 'state', 'tabs', 'takefocus',
            'undo', 'width', 'wrap', 'xscrollcommand', 'yscrollcommand',
            ]

register('Text', TKText)

#
# ttk widgets
#

class TTKFrame(BuilderObject):
    class_ = ttk.Frame
    container = True
    properties = ['class_', 'cursor', 'height', 'padding',
            'relief', 'style', 'takefocus', 'width']

register('ttk.Frame', TTKFrame)


class TTKLabel(BuilderObject):
    class_ = ttk.Label
    container = False
    properties = ['anchor', 'background', 'borderwidth',
            'class_', 'compound', 'cursor', 'font', 'foreground',
            'image', 'justify', 'padding', 'relief',
            'style', 'takefocus', 'text', 'textvariable', 'underline',
            'width', 'wraphlength']

register('ttk.Label', TTKLabel)


class TTKButton(BuilderObject):
    class_= ttk.Button
    container= False
    properties = ['class_', 'command', 'compound', 'cursor',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline']

register('ttk.Button', TTKButton)


class TTKCheckbutton(BuilderObject):
    class_ = ttk.Checkbutton
    container = False
    properties = ['class_', 'command', 'compound', 'cursor',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'variable', 'offvalue', 'onvalue', 'width']

register('ttk.Checkbutton', TTKCheckbutton)


class TTKRadiobutton(BuilderObject):
    class_ = ttk.Radiobutton
    container = False
    properties = ['class_', 'command', 'compound', 'cursor',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'value', 'variable', 'width']

register('ttk.Radiobutton', TTKRadiobutton)


class TTKCombobox(BuilderObject):
    class_ = ttk.Combobox
    container = False
    properties = ['class_', 'cursor', 'exportselection',
            'height', 'justify', 'postcommand', 'style', 'takefocus',
            'textvariable', 'validate', 'validatecommand', 'values',
            'width', 'xscrollcommand', 'state']

register('ttk.Combobox', TTKCombobox)


class TTKScrollbar(BuilderObject):
    class_ = ttk.Scrollbar
    container = False
    properties = ['class_', 'command', 'cursor', 'orient',
        'style', 'takefocus']

register('ttk.Scrollbar', TTKScrollbar)


class TTKSizegrip(BuilderObject):
    class_ = ttk.Sizegrip
    container = False
    properties = ['class_', 'style']

register('ttk.Sizegrip', TTKSizegrip)


class TTKEntry(BuilderObject):
    class_ = ttk.Entry
    container = False
    properties = ['class_', 'cursor', 'exportselection', 'font',
            'invalidcommand', 'justify', 'show', 'style', 'takefocus',
            'textvariable', 'validate', 'validatecommand', 'values',
            'width', 'xscrollcommand']

register('ttk.Entry', TTKEntry)


class TTKProgressbar(BuilderObject):
    class_ = ttk.Progressbar
    container = False
    properties = ['class_', 'cursor', 'length', 'maximum', 'mode',
            'orient', 'style', 'takefocus', 'variable']

register('ttk.Progressbar', TTKProgressbar)


class TTKScale(BuilderObject):
    class_ = ttk.Scale
    container = False
    properties = ['class_', 'command', 'cursor', 'from_', 'length',
            'orient', 'style', 'takefocus', 'to', 'variable', 'value',
            'variable']

register('ttk.Scale', TTKScale)


class TKSpinbox(BuilderObject):
    class_ = tkinter.Spinbox
    container = False
    properties = ['activebackground', 'background', 'borderwidth',
            'buttoncursor', 'buttondownrelief', 'buttonup', 'command',
            'cursor', 'disabledbackground', 'disabledforeground',
            'exportselection', 'font', 'foreground', 'format',
            'from_', 'highlightbackground', 'highlightcolor',
            'highlightthickness', 'increment', 'insertbackground',
            'insertborderwidth', 'insertofftime', 'insertontime',
            'insertwidth', 'justify', 'readonlybackground', 'relief',
            'repeatdelay', 'repeatinterval', 'selectbackground',
            'selectborderwidth', 'selectforeground', 'state', 'takefocus',
            'textvariable', 'to', 'values', 'width', 'wrap', 'xscrollcommand']

register('Spinbox', TKSpinbox)


class TTKSeparator(BuilderObject):
    class_ = ttk.Separator
    container = False
    properties = ['class_', 'orient', 'style']

register('ttk.Separator', TTKSeparator)


class TTKLabelframe:
    class_ = ttk.Labelframe
    container = True
    properties = ['borderwidth', 'class_', 'cursor', 'height',
            'labelanchor', 'labelwidget', 'padding',
            'relief', 'style', 'takefocus', 'text', 'underline', 'width']

register('ttk.Labelframe', TTKLabelframe)


class TTKPanedwindow(BuilderObject):
    class_ = ttk.Panedwindow
    container = False
    properties = ['class_', 'cursor', 'height', 'orient',
            'style', 'takefocus', 'width']

    def __init__(self, master, properties, layout_prop):
        orient = properties.pop('orient', 'vertical')
        self.widget = self.class_(master, orient=orient)
        self.properties = properties
        self.layout_properties = layout_prop

register('ttk.Panedwindow', TTKPanedwindow)


class TTKPanedwindowPane(BuilderObject):
    class_ = None
    container = True
    properties = ['weight']

    def __init__(self, master, properties, layout_prop):
        self.widget = master
        self.properties= properties
        self.layout_properties = layout_prop

    def configure(self):
        pass

    def layout(self):
        pass

    def add_child(self, cwidget):
        self.widget.add(cwidget, **self.properties)

register('ttk.Panedwindow.Pane', TTKPanedwindowPane)


class TTKNotebook(BuilderObject):
    class_ = ttk.Notebook
    container = True
    properties = ['class_', 'cursor', 'height',
            'padding', 'style', 'takefocus', 'width']

register('ttk.Notebook', TTKNotebook)


class TTKNotebookTab(BuilderObject):
    class_ = None
    container = True
    properties = ['compound', 'padding', 'sticky',
        'image', 'text', 'underline']

    def __init__(self, master, properties, layout_prop):
        self.widget = master
        self.properties= properties
        self.layout_properties = layout_prop

    def configure(self):
        pass

    def layout(self):
        pass

    def add_child(self, cwidget):
        self.widget.add(cwidget, **self.properties)

register('ttk.Notebook.Tab', TTKNotebookTab)


class TTKMenubutton(BuilderObject):
    class_ = ttk.Menubutton
    container = False
    properties = ['class_', 'compound', 'cursor', 'direction',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'width']

    def add_child(self, cwidget):
        self.widget['menu'] = cwidget

register('ttk.Menubutton', TTKMenubutton)


class TKMenu(BuilderObject):
    class_ = tkinter.Menu
    container = True
    properties = ['activebackground', 'activeborderwidth', 'activeforeground',
        'background', 'borderwidth', 'cursor', 'disabledforeground',
        'font', 'foreground', 'postcommand', 'relief', 'selectcolor',
        'tearoff', 'tearoffcommand', 'title']

    def layout(self):
        pass

register('tk.Menu', TKMenu)


class TKMenuitem(BuilderObject):
    class_ = None
    container = False
    itemtype = None
    #FIXME Move properties that are for specific items to the corresponding
    #  subclass, eg: onvalue, offvalue to checkbutton
    #FIXME Howto setup radio buttons variables ?
    properties = ['accelerator', 'activebackground', 'activeforeground',
        'background', 'bitmap', 'columnbreak', 'command', 'compound',
        'font', 'foreground', 'hidemargin', 'image', 'label',
        'offvalue', 'onvalue', 'selectcolor', 'selectimage', 'state',
        'underline', 'value', 'variable']

    def __init__(self, master, properties, layout_prop):
        self.widget = master
        master.add(self.itemtype, **properties)
        self.properties= properties
        self.layout_properties = layout_prop

    def configure(self):
        pass

    def layout(self):
        pass


class TKMenuitemSubmenu(TKMenu):
    properties = list(set(TKMenu.properties + TKMenuitem.properties))

    def __init__(self, master, properties, layout_prop):
        menu_properties = dict((k, v) for k, v in properties.items()
            if k in TKMenu.properties)

        item_properties = dict((k, v) for k, v in properties.items()
            if k in TKMenuitem.properties)

        self.widget = submenu = TKMenu.class_(master, **menu_properties)
        item_properties['menu'] = submenu
        master.add(tkinter.constants.CASCADE, **item_properties)
        self.properties = properties
        self.layout_properties = layout_prop

    def configure(self):
        pass

    def layout(self):
        pass

register('tk.Menuitem.Submenu', TKMenuitemSubmenu)


class TKMenuitemCommand(TKMenuitem):
    itemtype = tkinter.constants.COMMAND

register('tk.Menuitem.Command', TKMenuitemCommand)


class TKMenuitemCheckbutton(TKMenuitem):
    itemtype = tkinter.constants.CHECKBUTTON

register('tk.Menuitem.Checkbutton', TKMenuitemCheckbutton)


class TKMenuitemRadiobutton(TKMenuitem):
    itemtype = tkinter.constants.RADIOBUTTON

register('tk.Menuitem.Radiobutton', TKMenuitemRadiobutton)


class TKMenuitemSeparator(TKMenuitem):
    itemtype = tkinter.constants.SEPARATOR
    properties = []

register('tk.Menuitem.Separator', TKMenuitemSeparator)


class TTKTreeview(BuilderObject):
    class_ = ttk.Treeview
    container = False
    properties = ['class_', 'cursor', 'height', 'padding', 'selectmode',
        'show', 'style', 'takefocus']
    #FIXME add support to properties: 'columns', 'displaycolumns'
    # and columns properties

register('ttk.Treeview', TTKTreeview)


class TKCanvas(BuilderObject):
    class_ = tkinter.Canvas
    container = False
    properties = ['borderwidth', 'background', 'closeenough', 'confine',
        'cursor', 'height', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'relief', 'scrollregion', 'selectbackground',
        'selectborderwidth', 'selectforeground', 'takefocus', 'width',
        'xscrollincrement', 'xscrollcommand', 'yscrollincrement',
        'yscrollcommand']

register('tk.Canvas', TKCanvas)

#TODO: add a ScrollHelper class that adds and configures scrollbars to
# specific widgets such as Canvas, Text, Entry, etc.


#
# Builder class
#

class Tkbuilder:
    #TODO: Add a method 'bind' or similar to map commands to a function
    # something like: builder.bind(self)
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


    def get_object(self, name, master=None):
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
            properties = self.get_properties(element)
            layout = self.get_layout_properties(element)
            builderobj = CLASS_MAP[cname].factory(master, properties, layout)
            builderobj.configure()
            builderobj.layout()
            pwidget = builderobj.widget

            self.widgets[uniqueid] = pwidget

            xpath = "./child"
            children = element.findall(xpath)
            for child in children:
                child_object = child.find('./object')
                cwidget = self.realize(pwidget, child_object)
                builderobj.add_child(cwidget)

            return pwidget
        else:
            raise Exception('Class "{0}" not mapped'.format(cname))


    def get_layout_properties(self, element):
        #use grid layout for all
        #get packing properties
        layout_properties = {}
        packing_elem = element.find('./packing')
        if packing_elem is not None:
            layout_properties = self.get_properties(packing_elem)

            #get grid row and col properties:
            rows_dict = {}
            erows = packing_elem.find('./rows')
            if erows is not None:
                rows = erows.findall('./row')
                for row in rows:
                    row_id = row.get('id')
                    row_properties = self.get_properties(row)
                    rows_dict[row_id] = row_properties
            layout_properties['grid_rows'] = rows_dict

            columns_dict = {}
            ecolums = packing_elem.find('./columns')
            if ecolums is not None:
                columns = ecolums.findall('./column')
                for column in columns:
                    column_id = column.get('id')
                    column_properties = self.get_properties(column)
                    columns_dict[column_id] = column_properties
            layout_properties['grid_columns'] = columns_dict
        else:
            cname = element.get('class')
            uniqueid = element.get('id')
            logger.warning('No packing information for: (%s, %s).',
                cname, uniqueid)
        return layout_properties


    def get_properties(self, element):
        properties = element.findall('./property')
        pdict= {}
        for p in properties:
            pdict[p.get('name')] = p.text
        return pdict


