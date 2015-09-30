from __future__ import unicode_literals
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
class TTKWidgetBO(BuilderObject):
    OPTIONS_LABEL = ('text', 'textvariable', 'underline', 'image', 'compound',
                     'width')
    OPTIONS_COMPATIBILITY = ('state',)
    OPTIONS_STANDARD = ('class_', 'cursor', 'takefocus', 'style')
    OPTIONS_SPECIFIC = tuple()
    OPTIONS_CUSTOM = tuple()
    ro_properties = ('class_',)


class TTKFrame(TTKWidgetBO):
    OPTIONS_SPECIFIC = ('borderwidth', 'relief', 'padding', 'height', 'width')
    class_ = ttk.Frame
    container = True
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC

register_widget('ttk.Frame', TTKFrame, 'Frame', ('Containers', 'ttk'))


class TTKLabel(TTKWidgetBO):
    OPTIONS_STANDARD = \
        TTKWidgetBO.OPTIONS_STANDARD + \
        TTKWidgetBO.OPTIONS_LABEL + ('borderwidth',)
    OPTIONS_SPECIFIC = (
        'anchor', 'background', 'font', 'foreground', 'justify',
        'padding', 'relief', 'wraplength')
    class_ = ttk.Label
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC

register_widget('ttk.Label', TTKLabel, 'Label', ('Control & Display', 'ttk'))


class TTKButton(TTKWidgetBO):
    OPTIONS_STANDARD = (TTKWidgetBO.OPTIONS_STANDARD +
                        TTKWidgetBO.OPTIONS_LABEL +
                        TTKWidgetBO.OPTIONS_COMPATIBILITY)
    OPTIONS_SPECIFIC = ('command', 'default')
    class_ = ttk.Button
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('command',)

register_widget('ttk.Button', TTKButton,
                'Button', ('Control & Display', 'ttk'))


class TTKCheckbutton(TTKWidgetBO):
    OPTIONS_STANDARD = (TTKWidgetBO.OPTIONS_STANDARD +
                        TTKWidgetBO.OPTIONS_LABEL +
                        TTKWidgetBO.OPTIONS_COMPATIBILITY)
    OPTIONS_SPECIFIC = ('command', 'offvalue', 'onvalue', 'variable')
    class_ = ttk.Checkbutton
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('command',)

register_widget('ttk.Checkbutton', TTKCheckbutton,
                'Checkbutton', ('Control & Display', 'ttk'))


class TTKRadiobutton(TTKWidgetBO):
    OPTIONS_STANDARD = (TTKWidgetBO.OPTIONS_STANDARD +
                        TTKWidgetBO.OPTIONS_LABEL +
                        TTKWidgetBO.OPTIONS_COMPATIBILITY)
    OPTIONS_SPECIFIC = ('command', 'value', 'variable')
    class_ = ttk.Radiobutton
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    ro_properties = ('class_',)
    command_properties = ('command',)

register_widget('ttk.Radiobutton', TTKRadiobutton,
                'Radiobutton', ('Control & Display', 'ttk'))


class TTKCombobox(TTKWidgetBO):
    OPTIONS_SPECIFIC = ('exportselection', 'justify', 'height',
                        'postcommand', 'state', 'textvariable', 'values',
                        'width', 'validate', 'validatecommand',
                        'invalidcommand', 'xscrollcommand')
    OPTIONS_CUSTOM = ('validatecommand_args', 'invalidcommand_args')
    class_ = ttk.Combobox
    container = False
    properties = (TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC +
                  OPTIONS_CUSTOM)
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

register_widget('ttk.Combobox', TTKCombobox, 'Combobox',
                ('Control & Display', 'ttk'))


class TTKScrollbar(TTKWidgetBO):
    OPTIONS_SPECIFIC = ('command', 'orient')
    class_ = ttk.Scrollbar
    container = False
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('command',)

register_widget('ttk.Scrollbar', TTKScrollbar,
                'Scrollbar', ('Control & Display', 'ttk'))


class TTKSizegrip(TTKWidgetBO):
    class_ = ttk.Sizegrip
    container = False
    properties = (TTKWidgetBO.OPTIONS_STANDARD +
                  TTKWidgetBO.OPTIONS_SPECIFIC)

register_widget('ttk.Sizegrip', TTKSizegrip,
                'Sizegrip', ('Control & Display', 'ttk'))


class TTKEntry(TTKWidgetBO, EntryBaseBO):
    OPTIONS_STANDARD = TTKWidgetBO.OPTIONS_STANDARD + ('xscrollcommand',)
    OPTIONS_SPECIFIC = ('exportselection', 'font', 'invalidcommand',
                        'justify', 'show', 'state', 'textvariable',
                        'validate', 'validatecommand', 'width')
    OPTIONS_CUSTOM = ('text', 'validatecommand_args', 'invalidcommand_args')
    class_ = ttk.Entry
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = ('validatecommand', 'invalidcommand',
                          'xscrollcommand')


register_widget('ttk.Entry', TTKEntry, 'Entry', ('Control & Display', 'ttk'))


class TTKProgressbar(TTKWidgetBO):
    OPTIONS_SPECIFIC = ('orient', 'length', 'mode', 'maximum',
                        'value', 'variable')  # 'phase' is read-only
    class_ = ttk.Progressbar
    container = False
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC

register_widget('ttk.Progressbar', TTKProgressbar,
                'Progressbar', ('Control & Display', 'ttk'))


class TTKScale(TTKWidgetBO):
    OPTIONS_SPECIFIC = ('command', 'from_', 'length', 'orient',
                        'to', 'value', 'variable')
    class_ = ttk.Scale
    container = False
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('command',)

register_widget('ttk.Scale', TTKScale, 'Scale', ('Control & Display', 'ttk'))


class TTKSeparator(TTKWidgetBO):
    OPTIONS_SPECIFIC = ('orient',)
    class_ = ttk.Separator
    container = False
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC

register_widget('ttk.Separator', TTKSeparator,
                'Separator', ('Control & Display', 'ttk'))


class TTKLabelframe(TTKWidgetBO):
    OPTIONS_STANDARD = TTKFrame.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = (TTKFrame.OPTIONS_SPECIFIC +
                        ('labelanchor', 'text', 'underline'))
    class_ = ttk.Labelframe
    container = True
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC

register_widget('ttk.Labelframe', TTKLabelframe,
                'Labelframe', ('Containers', 'ttk'))


class TTKPanedwindow(TTKWidgetBO, PanedWindowBO):
    OPTIONS_SPECIFIC = ('orient', 'height', 'width')
    class_ = ttk.Panedwindow
    allowed_children = ('ttk.Panedwindow.Pane',)
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC
    ro_properties = ('class_', 'orient')

register_widget('ttk.Panedwindow', TTKPanedwindow,
                'Panedwindow', ('Containers', 'ttk'))


class TTKNotebook(TTKWidgetBO):
    OPTIONS_SPECIFIC = ('height', 'padding', 'width')
    class_ = ttk.Notebook
    container = True
    allow_container_layout = False
    allowed_children = ('ttk.Notebook.Tab',)
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC

register_widget('ttk.Notebook', TTKNotebook,
                'Notebook', ('Containers', 'ttk'))


class TTKMenubuttonBO(TTKWidgetBO):
    OPTIONS_STANDARD = (TTKWidgetBO.OPTIONS_STANDARD +
                        TTKWidgetBO.OPTIONS_LABEL +
                        TTKWidgetBO.OPTIONS_COMPATIBILITY)
    OPTIONS_SPECIFIC = ('direction',)  # 'menu'
    class_ = ttk.Menubutton
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    allowed_children = ('tk.Menu',)
    maxchildren = 1

    def add_child(self, bobject):
        self.widget.configure(menu=bobject.widget)

register_widget('ttk.Menubutton', TTKMenubuttonBO,
                'Menubutton', ('Control & Display', 'ttk',))


class TTKTreeviewBO(TTKWidgetBO):
    OPTIONS_STANDARD = (TTKWidgetBO.OPTIONS_STANDARD +
                        ('xscrollcommand', 'yscrollcommand'))
    OPTIONS_SPECIFIC = ('height', 'padding', 'selectmode', 'show')
    class_ = ttk.Treeview
    container = False
    allowed_children = ('ttk.Treeview.Column',)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC

    def __init__(self, builder, wdescr):
        super(TTKTreeviewBO, self).__init__(builder, wdescr)
        self._columns = None
        self._headings = None
        self._dcolumns = None

    def configure(self):
        super(TTKTreeviewBO, self).configure()
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

class TTKPanedwindowPane(TTKWidgetBO, PanedWindowPaneBO):
    OPTIONS_STANDARD = tuple()
    OPTIONS_SPECIFIC = ('weight',)
    class_ = None
    container = True
    allowed_parents = ('ttk.Panedwindow',)
    maxchildren = 1
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC

register_widget('ttk.Panedwindow.Pane', TTKPanedwindowPane,
                'Panedwindow.Pane', ('Pygubu Helpers', 'ttk'))


class TTKNotebookTab(TTKWidgetBO):
    OPTIONS_STANDARD = tuple()
    OPTIONS_SPECIFIC = ('state', 'sticky', 'padding', 'text',
                        'image', 'compound', 'underline')
    class_ = None
    container = True
    layout_required = False
    allow_bindings = False
    allowed_parents = ('ttk.Notebook',)
    maxchildren = 1
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC

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


class TTKTreeviewColBO(TTKWidgetBO):
    OPTIONS_STANDARD = tuple()
    OPTIONS_SPECIFIC = ('text', 'image', 'command', 'heading_anchor',
                        'column_anchor', 'minwidth', 'stretch', 'width')
    OPTIONS_CUSTOM = ('tree_column', 'visible',)
    class_ = None
    container = False
    layout_required = False
    allow_bindings = False
    allowed_parents = ('ttk.Treeview',)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = ('command',)

    def realize(self, parent):
        self.widget = parent.widget

        col_props = dict(self.properties)  # copy properties

        tree_column = col_props.pop('tree_column', 'false')
        tree_column = tree_column.lower()
        tree_column = True if tree_column == 'true' else False
        column_id = '#0' if tree_column else self.objectid
        visible = col_props.pop('visible', 'false')
        visible = visible.lower()
        is_visible = True if visible == 'true' else False

        #configure heading properties
        col_props.pop('command', '')
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
        tree_column = self.properties.get('tree_column', 'false')
        tree_column = tree_column.lower()
        tree_column = True if tree_column == 'true' else False
        column_id = '#0' if tree_column else self.objectid
        self.widget.heading(column_id, command=callback)

register_widget('ttk.Treeview.Column', TTKTreeviewColBO,
                'Treeview.Column', ('Pygubu Helpers', 'ttk'))


class TTKSpinboxBO(TTKWidgetBO, EntryBaseBO):
    OPTIONS_STANDARD = TTKEntry.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = (TTKEntry.OPTIONS_SPECIFIC +
                        ('from_', 'to', 'increment', 'values',
                         'wrap', 'format', 'command'))
    OPTIONS_CUSTOM = TTKEntry.OPTIONS_CUSTOM
    class_ = None
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = ('validatecommand', 'invalidcommand',
                          'xscrollcommand', 'command')


if tk.TkVersion >= 8.6:
    if not hasattr(ttk, 'Spinbox'):
        from pygubu.widgets.ttkspinbox import Spinbox
        ttk.Spinbox = Spinbox

    TTKSpinboxBO.class_ = ttk.Spinbox

    register_widget('ttk.Spinbox', TTKSpinboxBO,
                    'Spinbox', ('Control & Display', 'ttk')
                    )
