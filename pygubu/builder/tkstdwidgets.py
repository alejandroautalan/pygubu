from __future__ import unicode_literals
import types

try:
    import tkinter as tk
except:
    import Tkinter as tk

from .builderobject import *

#
# tkinter widgets
#
class TKToplevel(BuilderObject):
    class_ = tk.Toplevel
    container = True
    allow_container_layout = False
    layout_required = False
    allowed_parents = ('root',)
#    allowed_children = ('tk.Frame', 'ttk.Frame')
#    maxchildren = 1
    properties = ('background', 'borderwidth', 'class_', 'cursor', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness', 'padx',
        'pady', 'relief', 'takefocus', 'width',
        #Extra properties as methods
        'title', 'geometry', 'overrideredirect', 'minsize', 'maxsize',
        'resizable')
    RESIZABLE = {
        'both': (True, True),
        'horizontally': (True, False),
        'vertically': (False, True),
        'none': (False, False)
        }
        
    def realize(self, parent):
        args = self._get_init_args()
        master = parent.get_child_master()
        if master is None and tk._default_root is None:
            self.widget = tk.Tk()
        else:
            self.widget = self.class_(master, **args)
        return self.widget
        
    def _set_property(self, target_widget, pname, value):
        method_props = ('geometry', 'overrideredirect', 'title')
        if pname in method_props:
            method = getattr(target_widget, pname)
            method(value)
        elif pname == 'resizable' and value:
            target_widget.resizable(*self.RESIZABLE[value])
            if value in ('both', 'horizontally'):
                target_widget.columnconfigure(0, weight=1)
            if value in ('both', 'vertically'):
                target_widget.rowconfigure(0, weight=1)
        elif pname == 'maxsize':
            if '|' in value:
                w, h = value.split('|')
                target_widget.maxsize(w, h)
        elif pname == 'minsize':
            if '|' in value:
                w, h = value.split('|')
                target_widget.minsize(w, h)
        else:
            super(TKToplevel, self)._set_property(target_widget, pname, value)

register_widget('tk.Toplevel', TKToplevel, 'Toplevel', ('Containers', 'tk', 'ttk'))


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

    def _set_property(self, target_widget, pname, value):
        if pname == 'text':
            target_widget.insert('0.0', value)
        else:
            super(TKText, self)._set_property(target_widget,pname, value)


register_widget('tk.Text', TKText, 'Text', ('Control & Display', 'tk', 'ttk'))



class TKPanedWindow(PanedWindow):
    class_ = tk.PanedWindow
    allowed_children = ('tk.PanedWindow.Pane',)
    properties = ['background', 'borderwidth', 'cursor', 'handlepad',
        'handlesize', 'height', 'opaqueresize', 'orient', 'relief',
        'sashpad', 'sashrelief', 'sashwidth', 'showhandle', 'width']

register_widget('tk.PanedWindow', TKPanedWindow,
        'PanedWindow', ('Containers', 'tk'))


class TKMenubutton(BuilderObject):
    class_ = tk.Menubutton
    container = False
    properties = ['activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'compound', 'cursor',
        'direction', 'disabledforeground', 'foreground', 'font',
        'height', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'image', 'justify', 'padx',
        'pady', 'relief', 'state', 'takefocus', 'text', 'textvariable',
        'underline', 'width', 'wraplength']
    allowed_children = ('tk.Menu',)
    maxchildren = 1

    def add_child(self, bobject):
        self.widget.configure(menu=bobject.widget)

register_widget('tk.Menubutton', TKMenubutton, 'Menubutton', ('Control & Display', 'tk',))


class TKMessage(BuilderObject):
    class_ = tk.Message
    container = False
    properties = ['aspect', 'background', 'borderwidth', 'cursor',
        'font', 'foreground', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'justify', 'padx', 'pady', 'relief',
        'takefocus', 'text', 'textvariable', 'width']

register_widget('tk.Message', TKMessage,
        'Message', ('Control & Display', 'tk', 'ttk'))


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
    allow_container_layout = False
    properties = ['activebackground', 'activeborderwidth', 'activeforeground',
        'background', 'borderwidth', 'cursor', 'disabledforeground',
        'font', 'foreground', 'postcommand', 'relief', 'selectcolor',
        'tearoff', 'tearoffcommand', 'title']
    command_properties = ('postcommand', 'tearoffcommand')
    allow_bindings = False

    def layout(self):
        pass

register_widget('tk.Menu', TKMenu, 'Menu', ('Containers', 'tk', 'ttk'))


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
# Helpers for Standard tk widgets
#

class TKMenuitem(BuilderObject):
    class_ = None
    container = False
    itemtype = None
    layout_required = False
    properties = ['accelerator', 'activebackground', 'activeforeground',
        'background', 'bitmap', 'columnbreak', 'command', 'compound',
        'font', 'foreground', 'hidemargin', 'image', 'label', 'state',
        'underline',
        'command_id_arg', #<< custom property !!
        ]
    command_properties = ('command',)
    allow_bindings = False

    def realize(self, parent):
        self.widget = master = parent.widget
        itemproperties = dict(self.properties)
        pname = 'command_id_arg'
        if pname in itemproperties:
            itemproperties.pop(pname)
        pname = 'variable'
        if pname in itemproperties:
            varname = itemproperties[pname]
            itemproperties[pname] = self.builder.create_variable(pname)
        for imageprop in ('image', 'selectimage'):
            if imageprop in itemproperties:
                name = itemproperties[imageprop]
                itemproperties[imageprop] = self.builder.get_image(name)
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

    def realize(self, parent):
        master = parent.widget
        menu_properties = dict((k, v) for k, v in self.properties.items()
            if k in TKMenu.properties)

        item_properties = dict((k, v) for k, v in self.properties.items()
            if k in TKMenuitem.properties and k != 'command_id_arg')

        self.widget = submenu = TKMenu.class_(master, **menu_properties)
        item_properties['menu'] = submenu
        master.add(tk.CASCADE, **item_properties)
        return self.widget


    def configure(self):
        pass

    def layout(self):
        pass

register_widget('tk.Menuitem.Submenu', TKMenuitemSubmenu,
        'Menuitem.Submenu', ('Pygubu Helpers', 'tk', 'ttk'))


class TKMenuitemCommand(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    itemtype = tk.COMMAND

register_widget('tk.Menuitem.Command', TKMenuitemCommand,
    'Menuitem.Command', ('Pygubu Helpers', 'tk', 'ttk'))


class TKMenuitemCheckbutton(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    itemtype = tk.CHECKBUTTON
    properties = TKMenuitem.properties + \
            ['indicatoron', 'selectcolor', 'selectimage', 'variable']

register_widget('tk.Menuitem.Checkbutton', TKMenuitemCheckbutton,
    'Menuitem.Checkbutton', ('Pygubu Helpers', 'tk', 'ttk'))


class TKMenuitemRadiobutton(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    itemtype = tk.RADIOBUTTON
    properties = TKMenuitemCheckbutton.properties + \
            ['onvalue', 'offvalue', 'value']

register_widget('tk.Menuitem.Radiobutton', TKMenuitemRadiobutton,
    'Menuitem.Radiobutton', ('Pygubu Helpers', 'tk', 'ttk'))


class TKMenuitemSeparator(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    itemtype = tk.SEPARATOR
    properties = []
    command_properties = tuple()

register_widget('tk.Menuitem.Separator', TKMenuitemSeparator,
        'Menuitem.Separator', ('Pygubu Helpers','tk', 'ttk'))


class TKPanedWindowPane(PanedWindowPane):
    class_ = None
    container = True
    allowed_parents = ('tk.PanedWindow',)
    maxchildren = 1
    properties = ['height', 'minsize', 'padx', 'pady', 'sticky']

register_widget('tk.PanedWindow.Pane', TKPanedWindowPane,
    'PanedWindow.Pane', ('Pygubu Helpers', 'tk'))
