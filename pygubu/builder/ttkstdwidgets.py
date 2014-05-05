from __future__ import unicode_literals
import types
from collections import OrderedDict

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

from .builderobject import *


#
# ttk widgets
#

class TTKFrame(BuilderObject):
    class_ = ttk.Frame
    container = True
    properties = ['class_', 'cursor', 'height', 'padding',
            'relief', 'style', 'takefocus', 'width']
    ro_properties = ('class_',)

register_widget('ttk.Frame', TTKFrame, 'Frame', ('Containers', 'ttk'))


class TTKLabel(BuilderObject):
    class_ = ttk.Label
    container = False
    properties = ['anchor', 'background', 'borderwidth',
            'class_', 'compound', 'cursor', 'font', 'foreground',
            'image', 'justify', 'padding', 'relief',
            'style', 'takefocus', 'text', 'textvariable', 'underline',
            'width', 'wraplength']
    ro_properties = ('class_',)

register_widget('ttk.Label', TTKLabel, 'Label', ('Control & Display', 'ttk'))


class TTKButton(BuilderObject):
    class_= ttk.Button
    container= False
    properties = ['class_', 'command', 'compound', 'cursor',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline']
    ro_properties = ('class_',)
    command_properties = ('command',)

register_widget('ttk.Button', TTKButton, 'Button', ('Control & Display', 'ttk'))


class TTKCheckbutton(BuilderObject):
    class_ = ttk.Checkbutton
    container = False
    properties = ['class_', 'command', 'compound', 'cursor',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'variable', 'offvalue', 'onvalue', 'width']
    ro_properties = ('class_',)
    command_properties = ('command',)

register_widget('ttk.Checkbutton', TTKCheckbutton,
        'Checkbutton', ('Control & Display', 'ttk'))


class TTKRadiobutton(BuilderObject):
    class_ = ttk.Radiobutton
    container = False
    properties = ['class_', 'command', 'compound', 'cursor',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'value', 'variable', 'width']
    ro_properties = ('class_',)
    command_properties = ('command',)

register_widget('ttk.Radiobutton', TTKRadiobutton,
        'Radiobutton', ('Control & Display', 'ttk'))


class TTKCombobox(BuilderObject):
    class_ = ttk.Combobox
    container = False
    properties = ['class_', 'cursor', 'exportselection',
            'height', 'justify', 'postcommand', 'style', 'takefocus',
            'textvariable', 'validate', 'validatecommand', 'invalidcommand',
            'values', 'width', 'xscrollcommand', 'state',
            'validatecommand_args',
            'invalidcommand_args']
    ro_properties = ('class_',)
    command_properties = ('postcommand', 'validatecommand',
        'invalidcommand', 'xscrollcommand')

    def _set_property(self, target_widget, pname, value):
        if pname in ('validatecommand_args', 'invalidcommand_args'):
            pass
        else:
            super(TTKCombobox, self)._set_property(target_widget, pname, value)

    def _create_callback(self, cpname, command):
        callback = command
        if cpname in ('validatecommand', 'invalidcommand'):
            args = self.properties.get(cpname + '_args', '')
            if args:
                args = args.split(' ')
                callback = (self.widget.register(command),) + tuple(args)
            else:
                callback = self.widget.register(command)
        return callback

register_widget('ttk.Combobox', TTKCombobox,
        'Combobox', ('Control & Display', 'ttk'))


class TTKScrollbar(BuilderObject):
    class_ = ttk.Scrollbar
    container = False
    properties = ['class_', 'command', 'cursor', 'orient',
        'style', 'takefocus']
    ro_properties = ('class_',)
    command_properties = ('command',)

register_widget('ttk.Scrollbar', TTKScrollbar,
     'Scrollbar', ('Control & Display', 'ttk'))


class TTKSizegrip(BuilderObject):
    class_ = ttk.Sizegrip
    container = False
    properties = ['class_', 'style']
    ro_properties = ('class_',)

register_widget('ttk.Sizegrip', TTKSizegrip,
        'Sizegrip', ('Control & Display', 'ttk'))


class TTKEntry(EntryBaseBO):
    class_ = ttk.Entry
    container = False
    properties = ['class_', 'cursor', 'exportselection', 'font',
            'invalidcommand', 'justify', 'show', 'state', 'style', 'takefocus',
            'textvariable', 'validate', 'validatecommand',
            #'values',  << Commented, only useful on Combobox widget ?
            'width', 'xscrollcommand',
            'text', # < text is a custom property
            'validatecommand_args',
            'invalidcommand_args']
    ro_properties = ('class_',)
    command_properties = ('validatecommand', 'invalidcommand',
        'xscrollcommand')


register_widget('ttk.Entry', TTKEntry, 'Entry', ('Control & Display', 'ttk'))


class TTKProgressbar(BuilderObject):
    class_ = ttk.Progressbar
    container = False
    properties = ['class_', 'cursor', 'length', 'maximum', 'mode',
            'orient', 'style', 'takefocus', 'variable']
    ro_properties = ('class_',)

register_widget('ttk.Progressbar', TTKProgressbar,
        'Progressbar', ('Control & Display', 'ttk'))


class TTKScale(BuilderObject):
    class_ = ttk.Scale
    container = False
    properties = ['class_', 'command', 'cursor', 'from_', 'length',
            'orient', 'style', 'takefocus', 'to', 'variable', 'value']
    ro_properties = ('class_',)
    command_properties = ('command',)

register_widget('ttk.Scale', TTKScale, 'Scale', ('Control & Display',  'ttk'))


class TTKSeparator(BuilderObject):
    class_ = ttk.Separator
    container = False
    properties = ['class_', 'orient', 'style']
    ro_properties = ('class_',)

register_widget('ttk.Separator', TTKSeparator,
    'Separator', ('Control & Display',  'ttk'))


class TTKLabelframe(BuilderObject):
    class_ = ttk.Labelframe
    container = True
    properties = ['borderwidth', 'class_', 'cursor', 'height',
            'labelanchor', 'labelwidget', 'padding',
            'relief', 'style', 'takefocus', 'text', 'underline', 'width']
    ro_properties = ('class_',)

#TODO: Add helper so the labelwidget can be configured on GUI
register_widget('ttk.Labelframe', TTKLabelframe,
        'Labelframe', ('Containers', 'ttk'))


class TTKPanedwindow(PanedWindow):
    class_ = ttk.Panedwindow
    allowed_children = ('ttk.Panedwindow.Pane',)
    properties = ['class_', 'cursor', 'height', 'orient',
            'style', 'takefocus', 'width']
    ro_properties = ('class_','orient')

register_widget('ttk.Panedwindow', TTKPanedwindow,
        'Panedwindow', ('Containers', 'ttk'))


class TTKNotebook(BuilderObject):
    class_ = ttk.Notebook
    container = True
    allow_container_layout = False
    allowed_children = ('ttk.Notebook.Tab',)
    properties = ['class_', 'cursor', 'height',
            'padding', 'style', 'takefocus', 'width']
    ro_properties = ('class_',)

register_widget('ttk.Notebook', TTKNotebook,
        'Notebook', ('Containers', 'ttk'))


class TTKMenubuttonBO(BuilderObject):
    class_ = ttk.Menubutton
    container = False
    properties = ['class_', 'compound', 'cursor', 'direction',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'width']
    allowed_children = ('tk.Menu',)
    maxchildren = 1
    ro_properties = ('class_',)

    def add_child(self, bobject):
        self.widget.configure(menu=bobject.widget)

register_widget('ttk.Menubutton', TTKMenubuttonBO,
        'Menubutton', ('Control & Display', 'ttk',))


class TTKTreeviewBO(BuilderObject):
    class_ = ttk.Treeview
    container = False
    allowed_children = ('ttk.Treeview.Column',)
    properties = ['class_', 'cursor', 'height', 'padding', 'selectmode',
        'show', 'style', 'takefocus']
    ro_properties = ('class_',)

    def __init__(self, builder, wdescr):
        super(TTKTreeviewBO, self).__init__(builder, wdescr)
        self._columns = None
        self._headings = None
        self._dcolumns = None

    def configure(self):
        super(TTKTreeviewBO,self).configure()
        self.__configure_columns()

    def __configure_columns(self):
        if self._columns:
            columns = list(self._columns.keys())
            if '#0' in columns:
                columns.remove('#0')
            displaycolumns = self._dcolumns
            self.widget.configure(columns=columns,
                                    displaycolumns=displaycolumns)
            for col in self._columns:
                self.widget.column(col, **self._columns[col])
        if self._headings:
            for col in self._headings:
                self.widget.heading(col, **self._headings[col])

    def set_column(self, col_id, attrs, visible=True):
        if self._columns is None:
            self._columns = OrderedDict()
            self._dcolumns = list()
        self._columns[col_id] = attrs
        if visible and col_id != '#0':
            self._dcolumns.append(col_id)

    def set_heading(self, col_id, attrs):
        if self._headings is None:
            self._headings = OrderedDict()
        self._headings[col_id] = attrs


register_widget('ttk.Treeview', TTKTreeviewBO,
        'Treeview', ('Control & Display', 'ttk'))


#
# Helpers for Standard ttk widgets
#

class TTKPanedwindowPane(PanedWindowPane):
    class_ = None
    container = True
    allowed_parents = ('ttk.Panedwindow',)
    maxchildren = 1
    properties = ['weight']

register_widget('ttk.Panedwindow.Pane', TTKPanedwindowPane,
        'Panedwindow.Pane', ('Pygubu Helpers', 'ttk'))


class TTKNotebookTab(BuilderObject):
    class_ = None
    container = True
    layout_required = False
    allow_bindings = False
    allowed_parents = ('ttk.Notebook',)
    maxchildren = 1
    properties = ['compound', 'padding', 'sticky',
        'image', 'text', 'underline']

    def realize(self, parent):
        self.widget = parent.widget
        return self.widget

    def configure(self):
        pass

    def layout(self):
        pass

    def add_child(self, bobject):
        self.widget.add(bobject.widget, **self.properties)

register_widget('ttk.Notebook.Tab', TTKNotebookTab,
        'Notebook.Tab', ('Pygubu Helpers', 'ttk'))


class TTKTreeviewColBO(BuilderObject):
    class_ = None
    container = False
    layout_required = False
    allow_bindings = False
    allowed_parents = ('ttk.Treeview',)
    properties = [
        'tree_column', 'visible', 'text', 'image', 'command', 'heading_anchor',
        'column_anchor', 'minwidth', 'stretch', 'width' ]
    command_properties = ('command',)


    def realize(self, parent):
        self.widget = master = parent.widget

        col_props = dict(self.properties) #copy properties

        tree_column = col_props.pop('tree_column', 'False')
        tree_column = True if tree_column == 'True' else False
        column_id = '#0' if tree_column else self.objectid
        is_visible = True if col_props.pop('visible') == 'True' else False

        #configure heading properties
        command= col_props.pop('command', '')
        hprops = {
            'anchor': col_props.pop('heading_anchor', tk.W),
            'image': col_props.pop('image', ''),
            'text': col_props.pop('text', '')
        }
        parent.set_heading(column_id, hprops)

        #configure column properties
        cprops = {
            'anchor': col_props.pop('column_anchor', ''),
            'stretch': col_props.pop('stretch', '1'),
            'width': col_props.pop('width', '200'),
            'minwidth': col_props.pop('minwidth', '20')
        }
        parent.set_column(column_id, cprops, is_visible)
        return self.widget


    def configure(self):
        pass

    def layout(self):
        pass

    def _connect_command(self, cpname, callback):
        tree_column = self.properties.get('tree_column', 'False')
        tree_column = True if tree_column == 'True' else False
        column_id = '#0' if tree_column else self.objectid
        self.widget.heading(column_id, command=callback)


register_widget('ttk.Treeview.Column', TTKTreeviewColBO,
        'Treeview.Column', ('Pygubu Helpers', 'ttk'))


class TTKSpinboxBO(EntryBaseBO):
    class_ = None
    container = False
    properties = ['class_', 'cursor',
            'from_', 'to', 'increment',
            'values',  #<< Commented, only useful on Combobox widget ?
            'wrap', 'format', 'command',
            'exportselection', 'font',
            'invalidcommand', 'justify', 'show', 'state', 'style', 'takefocus',
            'textvariable', 'validate', 'validatecommand',
            'width', 'xscrollcommand',
            'text', # < text is a custom property
            'validatecommand_args', 'invalidcommand_args']
    ro_properties = ('class_',)
    command_properties = ('validatecommand', 'invalidcommand',
        'xscrollcommand', 'command')


if tk.TkVersion >= 8.6:
    if not hasattr(ttk, 'Spinbox'):
        from pygubu.widgets.ttkspinbox import Spinbox
        ttk.Spinbox = Spinbox

    TTKSpinboxBO.class_ = ttk.Spinbox
    
    register_widget('ttk.Spinbox', TTKSpinboxBO, 'Spinbox', ('Control & Display', 'ttk'))
