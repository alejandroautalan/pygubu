import types
import tkinter as ttk
from tkinter import ttk

from .builderobject import *

#
# tkinter widgets
#
class TKFrame(BuilderObject):
    class_ = tk.Frame
    container = True
    properties = ['background', 'borderwidth', 'cursor', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'padx', 'pady', 'relief', 'takefocus', 'width']

register_widget('tk.Frame', TKFrame, 'Frame', ('Containers', 'tk'))


class TKLabel(BuilderObject):
    class_ = tk.Label
    container = False
    properties = ['activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'compound',
        'cursor', 'disabledforeground', 'font', 'foreground', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'image', 'justify', 'padx', 'pady', 'relief', 'state',
        'takefocus', 'text', 'textvariable', 'underline',
        'width', 'wraplength']

register_widget('tk.Label', TKLabel, 'Label', ('Control & Display', 'tk'))


class TKLabelFrame(BuilderObject):
    class_ = tk.LabelFrame
    container = True
    properties = ['background', 'borderwidth', 'cursor', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'labelanchor', 'labelwidget', 'padx', 'pady', 'relief',
        'text', 'takefocus', 'width']
#TODO: Add helper so the labelwidget can be configured on GUI

register_widget('tk.LabelFrame', TKLabelFrame, 'LabelFrame', ('Containers', 'tk'))


class EntryBaseBO(BuilderObject):
    def set_property(self, pname, value):
        if pname == 'text':
            self.widget.delete('0', tk.END)
            self.widget.insert('0', value)
        elif pname in ('validatecommand_args', 'invalidcommand_args'):
            pass
        else:
            super(EntryBaseBO, self).set_property(pname, value)

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


class TKEntry(EntryBaseBO):
    class_ = tk.Entry
    container = False
    properties = ['background', 'borderwidth', 'cursor',
        'disabledbackground', 'disabledforeground', 'exportselection',
        'foreground', 'font', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'insertbackground', 'insertborderwidth',
        'insertofftime', 'insertontime', 'insertwidth', 'justify',
        'readonlybackground', 'relief', 'selectbackground',
        'selectborderwidth', 'selectforeground', 'show', 'state',
        'takefocus', 'textvariable', 'validate', 'validatecommand',
        'invalidcommand', 'width', 'wraplength', 'xscrollcommand',
        'text', # < text is a custom property
        'validatecommand_args',
        'invalidcommand_args']
    command_properties = ('validatecommand', 'invalidcommand',
         'xscrollcommand')

register_widget('tk.Entry', TKEntry, 'Entry', ('Control & Display', 'tk'))


class TKButton(BuilderObject):
    class_ = tk.Button
    container = False
    properties = ['activebackground', 'activeforeground', 'anchor',
        'borderwidth', 'background', 'bitmap', 'command', 'cursor',
        'default', 'disabledforeground', 'foreground', 'font', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'image', 'justify', 'overrelief', 'padx', 'pady', 'relief',
        'repeatdelay', 'repeatinterval', 'state', 'takefocus', 'text',
        'textvariable', 'underline', 'width', 'wraplength']
    command_properties = ('command',)

register_widget('tk.Button', TKButton, 'Button', ('Control & Display', 'tk'))


class TKCheckbutton(BuilderObject):
    class_ = tk.Checkbutton
    container = False
    properties = ['activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'command', 'compound',
        'cursor', 'disabledforeground', 'font', 'foreground', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'image', 'indicatoron', 'justify', 'offrelief', 'offvalue',
        'onvalue', 'overrelief', 'padx', 'pady', 'relief', 'selectcolor',
        'selectimage', 'state', 'takefocus', 'text', 'textvariable',
        'underline', 'variable', 'width', 'wraplength']
    command_properties = ('command',)

register_widget('tk.Checkbutton', TKCheckbutton,
    'Checkbutton', ('Control & Display', 'tk'))


class TKListbox(BuilderObject):
    class_ =  tk.Listbox
    container = False
    properties = ['activestyle', 'background', 'borderwidth', 'cursor',
            'disabledforeground', 'exportselection', 'font',
            'foreground', 'height', 'highlightbackground', 'highlightcolor',
            'highlightthickness', 'listvariable', 'relief',
            'selectbackground', 'selectborderwidth', 'selectforeground',
            'selectmode', 'state', 'takefocus', 'width', 'xscrollcommand',
            'yscrollcommand']
    command_properties = ('xscrollcommand', 'yscrollcommand')

register_widget('tk.Listbox', TKListbox, 'Listbox', ('Control & Display', 'tk'))


class TKText(BuilderObject):
    class_ = tk.Text
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
            'text'] #<- text is a custom property.
    command_properties = ('xscrollcommand', 'yscrollcommand')

    def set_property(self, pname, value):
        if pname == 'text':
            self.widget.insert('0.0', value)
        else:
            super(TKText, self).set_property(pname, value)


register_widget('tk.Text', TKText, 'Text', ('Control & Display', 'tk', 'ttk'))


class PanedWindow(BuilderObject):
    class_ = None
    container = True
    properties = []
    ro_properties = ('orient', )

    def realize(self, master):
        args = self._get_init_args()
        if 'orient' not in args:
            args['orient'] = 'vertical'
        self.widget = self.class_(master, **args)
        return self.widget


class PanedWindowPane(BuilderObject):
    class_ = None
    container = True
    properties = []
    layout_required = False

    def realize(self, master):
        self.widget = master
        return self.widget

    def configure(self):
        pass

    def layout(self):
        pass

    def add_child(self, cwidget):
        self.widget.add(cwidget, **self.properties)


class TKPanedWindow(PanedWindow):
    class_ = tk.PanedWindow
    allowed_children = ('tk.PanedWindow.Pane',)
    properties = ['background', 'borderwidth', 'cursor', 'handlepad',
        'handlesize', 'height', 'opaqueresize', 'orient', 'relief',
        'sashpad', 'sashrelief', 'sashwidth', 'showhandle', 'width']

register_widget('tk.PanedWindow', TKPanedWindow,
        'PanedWindow', ('Containers', 'tk'))


class TKPanedWindowPane(PanedWindowPane):
    class_ = None
    container = True
    allowed_parents = ('tk.PanedWindow',)
    maxchildren = 1
    properties = ['height', 'minsize', 'padx', 'pady', 'sticky']

register_widget('tk.PanedWindow.Pane', TKPanedWindowPane,
    'PanedWindow.Pane', ('Control & Display', 'tk'))


class TKMenubutton(BuilderObject):
    class_ = tk.Menubutton
    container = True
    properties = ['activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'compound', 'cursor',
        'direction', 'disabledforeground', 'foreground', 'font',
        'height', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'image', 'justify', 'padx',
        'pady', 'relief', 'state', 'takefocus', 'text', 'textvariable',
        'underline', 'width', 'wraplength']
    allowed_children = ('tk.Menu',)
    maxchildren = 1

    def add_child(self, cwidget):
        self.set_property('menu', cwidget)

register_widget('tk.Menubutton', TKMenubutton, 'Menubutton', ('Control & Display', 'tk',))


class TKMessage(BuilderObject):
    class_ = tk.Message
    container = False
    properties = ['aspect', 'background', 'borderwidth', 'cursor',
        'font', 'foreground', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'justify', 'padx', 'pady', 'relief',
        'takefocus', 'text', 'textvariable', 'width']

register_widget('tk.Message', TKMessage,
        'Message', ('Control & Display', 'tk'))


class TKRadiobutton(BuilderObject):
    class_ = tk.Radiobutton
    container = False
    properties = ['activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'command', 'compound',
        'cursor', 'disabledforeground', 'font', 'foreground', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'image', 'indicatoron', 'justify', 'offrelief', 'overrelief',
        'padx', 'pady', 'relief', 'selectcolor', 'selectimage', 'state',
        'takefocus', 'text', 'textvariable',
        'underline', 'variable', 'width', 'wraplength']
    command_properties = ('command',)

register_widget('tk.Radiobutton', TKRadiobutton,
        'Radiobutton', ('Control & Display', 'tk'))


class TKScale(BuilderObject):
    class_ = tk.Scale
    container = False
    properties = ['activebackground', 'background', 'borderwidth', 'command',
        'cursor', 'digits', 'font', 'foreground', 'from_',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'label', 'length', 'orient', 'relief', 'repeatdelay', 'repeatinterval',
        'resolution', 'showvalue', 'sliderlength', 'sliderrelief', 'state',
        'takefocus', 'tickinterval', 'to', 'troughcolor', 'variable', 'width']
    command_properties = ('command',)

register_widget('tk.Scale', TKScale, 'Scale', ('Control & Display', 'tk'))


class TKScrollbar(BuilderObject):
    class_ = tk.Scrollbar
    container = False
    properties = ['activebackground', 'activerelief', 'background',
        'borderwidth', 'command', 'cursor', 'elementborderwidth',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'jump', 'orient', 'relief', 'repeatdelay', 'repeatinterval',
        'takefocus', 'troughcolor', 'width']
    command_properties = ('command',)

register_widget('tk.Scrollbar', TKScrollbar,
        'Scrollbar', ('Control & Display', 'tk'))


class TKSpinbox(BuilderObject):
    class_ = tk.Spinbox
    container = False
    properties = ['activebackground', 'background', 'borderwidth',
        'buttonbackground', 'buttoncursor', 'buttondownrelief', 'buttonup',
        'command', 'cursor', 'disabledbackground', 'disabledforeground',
        'exportselection', 'font', 'foreground', 'format', 'from_',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'increment', 'insertbackground', 'insertborderwidth',
        'insertofftime', 'insertontime', 'insertwidth', 'justify',
        'readonlybackground', 'relief', 'repeatdelay', 'repeatinterval',
        'selectbackground', 'selectborderwidth', 'selectforeground', 'state',
        'takefocus', 'textvariable', 'to', 'values', 'width', 'wrap',
        'xscrollcommand']
    command_properties = ('command', 'xscrollcommand')

    def configure(self):
        #hack to configure 'from_' and 'to' and avoid exception
        if 'from_' in self.properties:
            from_ = float(self.properties['from_'])
            to = float(self.properties.get('to', 0))
            if from_ > to:
                to = from_ + 1
                self.properties['to'] = str(to)
        super(TKSpinbox, self).configure()

register_widget('tk.Spinbox', TKSpinbox, 'Spinbox', ('Control & Display', 'tk'))


class TKMenu(BuilderObject):
    layout_required = False
    allowed_parents = ('root', 'tk.Menubutton', 'ttk.Menubutton')
    allowed_children = ('tk.Menuitem.Submenu', 'tk.Menuitem.Checkbutton',
        'tk.Menuitem.Command', 'tk.Menuitem.Radiobutton',
        'tk.Menuitem.Separator')
    class_ = tk.Menu
    container = True
    properties = ['activebackground', 'activeborderwidth', 'activeforeground',
        'background', 'borderwidth', 'cursor', 'disabledforeground',
        'font', 'foreground', 'postcommand', 'relief', 'selectcolor',
        'tearoff', 'tearoffcommand', 'title']
    command_properties = ('postcommand', 'tearoffcommand')

    def layout(self):
        pass

register_widget('tk.Menu', TKMenu, 'Menu', ('Containers', 'tk', 'ttk'))


class TKMenuitem(BuilderObject):
    class_ = None
    container = False
    itemtype = None
    layout_required = False
    #FIXME Move properties that are for specific items to the corresponding
    #  subclass, eg: onvalue, offvalue to checkbutton
    #FIXME Howto setup radio buttons variables ?
    properties = ['accelerator', 'activebackground', 'activeforeground',
        'background', 'bitmap', 'columnbreak', 'command', 'compound',
        'font', 'foreground', 'hidemargin', 'image', 'label',
        'offvalue', 'onvalue', 'selectcolor', 'selectimage', 'state',
        'underline', 'value', 'variable',
        'command_id_arg', #<< custom property !!
        ]
    command_properties = ('command',)

    def realize(self, master):
        self.widget = master
        itemproperties = self.properties
        if 'command_id_arg' in itemproperties:
            itemproperties = dict(itemproperties)
            itemproperties.pop('command_id_arg')
        master.add(self.itemtype, **itemproperties)
        self.__index = master.index(tk.END)
        return self.widget

    def configure(self):
        pass

    def layout(self):
        pass


    def _create_callback(self, cpname, callback):
        command = callback
        include_id = self.properties.get('command_id_arg', 'False')
        if include_id != 'False':
            def item_callback(item_id=self.objectid):
                callback(item_id)
            command = item_callback
        return command

    def _connect_command(self, cpname, callback):
        self.widget.entryconfigure(self.__index, command=callback)


class TKMenuitemSubmenu(TKMenu):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    allowed_children = ('tk.Menuitem.Submenu', 'tk.Menuitem.Checkbutton',
        'tk.Menuitem.Command', 'tk.Menuitem.Radiobutton',
        'tk.Menuitem.Separator')
    properties = list(set(TKMenu.properties + TKMenuitem.properties))

    def realize(self, master):
        menu_properties = dict((k, v) for k, v in self.properties.items()
            if k in TKMenu.properties)

        item_properties = dict((k, v) for k, v in self.properties.items()
            if k in TKMenuitem.properties and k != 'command_id_arg')

        self.widget = submenu = TKMenu.class_(master, **menu_properties)
        item_properties['menu'] = submenu
        master.add(tk.constants.CASCADE, **item_properties)
        return self.widget


    def configure(self):
        pass

    def layout(self):
        pass

register_widget('tk.Menuitem.Submenu', TKMenuitemSubmenu,
        'Menuitem.Submenu', ('Control & Display', 'tk', 'ttk'))


class TKMenuitemCommand(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    itemtype = tk.constants.COMMAND

register_widget('tk.Menuitem.Command', TKMenuitemCommand,
    'Menuitem.Command', ('Control & Display', 'tk', 'ttk'))


class TKMenuitemCheckbutton(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    itemtype = tk.constants.CHECKBUTTON

register_widget('tk.Menuitem.Checkbutton', TKMenuitemCheckbutton,
    'Menuitem.Checkbutton', ('Control & Display', 'tk', 'ttk'))


class TKMenuitemRadiobutton(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    itemtype = tk.constants.RADIOBUTTON

register_widget('tk.Menuitem.Radiobutton', TKMenuitemRadiobutton,
    'Menuitem.Radiobutton', ('Control & Display', 'tk', 'ttk'))


class TKMenuitemSeparator(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    itemtype = tk.constants.SEPARATOR
    properties = []
    command_properties = tuple()

register_widget('tk.Menuitem.Separator', TKMenuitemSeparator,
        'Menuitem.Separator', ('Control & Display','tk', 'ttk'))


class TKCanvas(BuilderObject):
    class_ = tk.Canvas
    container = False
    properties = ['borderwidth', 'background', 'closeenough', 'confine',
        'cursor', 'height', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'relief', 'scrollregion', 'selectbackground',
        'selectborderwidth', 'selectforeground', 'takefocus', 'width',
        'xscrollincrement', 'xscrollcommand', 'yscrollincrement',
        'yscrollcommand']
    command_properties = ('xscrollcommand', 'yscrollcommand')

register_widget('tk.Canvas', TKCanvas,
        'Canvas', ('Control & Display', 'tk', 'ttk'))


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

    def set_property(self, pname, value):
        if pname in ('validatecommand_args', 'invalidcommand_args'):
            pass
        else:
            super(TTKCombobox, self).set_property(pname, value)

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
            'invalidcommand', 'justify', 'show', 'style', 'takefocus',
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
        'LabelFrame', ('Containers', 'ttk'))


class TTKPanedwindow(PanedWindow):
    class_ = ttk.Panedwindow
    allowed_children = ('ttk.Panedwindow.Pane',)
    properties = ['class_', 'cursor', 'height', 'orient',
            'style', 'takefocus', 'width']
    ro_properties = ('class_','orient')

register_widget('ttk.Panedwindow', TTKPanedwindow,
        'Panedwindow', ('Containers', 'ttk'))


class TTKPanedwindowPane(PanedWindowPane):
    class_ = None
    container = True
    allowed_parents = ('ttk.Panedwindow',)
    maxchildren = 1
    properties = ['weight']

register_widget('ttk.Panedwindow.Pane', TTKPanedwindowPane,
        'Panedwindow.Pane', ('Control & Display', 'ttk'))


class TTKNotebook(BuilderObject):
    class_ = ttk.Notebook
    container = True
    allowed_children = ('ttk.Notebook.Tab',)
    properties = ['class_', 'cursor', 'height',
            'padding', 'style', 'takefocus', 'width']
    ro_properties = ('class_',)

register_widget('ttk.Notebook', TTKNotebook,
        'Notebook', ('Containers', 'ttk'))


class TTKNotebookTab(BuilderObject):
    class_ = None
    container = True
    layout_required = False
    allowed_parents = ('ttk.Notebook',)
    maxchildren = 1
    properties = ['compound', 'padding', 'sticky',
        'image', 'text', 'underline']

    def realize(self, master):
        self.widget = master
        return self.widget

    def configure(self):
        pass

    def layout(self):
        pass

    def add_child(self, cwidget):
        self.widget.add(cwidget, **self.properties)

register_widget('ttk.Notebook.Tab', TTKNotebookTab,
        'Notebook.Tab', ('Control & Display', 'ttk'))


class TTKMenubutton(BuilderObject):
    class_ = ttk.Menubutton
    container = True
    properties = ['class_', 'compound', 'cursor', 'direction',
            'image', 'style', 'takefocus', 'text', 'textvariable',
            'underline', 'width']
    allowed_children = ('tk.Menu',)
    maxchildren = 1
    ro_properties = ('class_',)

    def add_child(self, cwidget):
        self.set_property('menu', cwidget)

register_widget('ttk.Menubutton', TTKMenubutton,
        'Menubutton', ('Control & Display', 'ttk',))


class TTKTreeview(BuilderObject):
    class_ = ttk.Treeview
    container = False
    properties = ['class_', 'cursor', 'height', 'padding', 'selectmode',
        'show', 'style', 'takefocus']
    ro_properties = ('class_',)
    #FIXME add support to properties: 'columns', 'displaycolumns'
    # and columns properties

register_widget('ttk.Treeview', TTKTreeview,
        'Treeview', ('Control & Display', 'ttk'))


