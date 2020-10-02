# encoding: utf8
from __future__ import unicode_literals
import logging

try:
    import tkinter as tk
except:
    import Tkinter as tk

from .builderobject import BuilderObject, register_widget, EntryBaseBO
from .builderobject import PanedWindowBO, PanedWindowPaneBO

logger = logging.getLogger(__name__)

#
# tkinter widgets
#


class TKToplevel(BuilderObject):
    class_ = tk.Toplevel
    container = True
    layout_required = False
    allowed_parents = ('root',)
    maxchildren = 1
    OPTIONS_STANDARD = ('borderwidth', 'cursor', 'highlightbackground',
                        'highlightcolor', 'highlightthickness',
                        'padx', 'pady', 'relief', 'takefocus')
    OPTIONS_SPECIFIC = ('background',  'class_', 'container',
                        'height', 'width')
    OPTIONS_CUSTOM = ('title', 'geometry', 'overrideredirect', 'minsize',
                      'maxsize', 'resizable', 'iconbitmap', 'iconphoto')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
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
    
    def layout(self, target=None):
        # we marked this widget as not allowed to edit layout, and
        # by default the toplevel is configured to expand bot sides.
        if target is None:
            target = self.widget
        #self._grid_rc_layout(target)
        target.columnconfigure(0, weight=1)
        target.rowconfigure(0, weight=1)

    def _set_property(self, target_widget, pname, value):
        method_props = ('geometry', 'overrideredirect', 'title')
        if pname in method_props:
            method = getattr(target_widget, pname)
            method(value)
        elif pname == 'resizable' and value:
            target_widget.resizable(*self.RESIZABLE[value])
        elif pname == 'maxsize':
            if '|' in value:
                w, h = value.split('|')
                target_widget.maxsize(w, h)
        elif pname == 'minsize':
            if '|' in value:
                w, h = value.split('|')
                target_widget.minsize(w, h)
        elif pname == 'iconphoto':
            icon = self.builder.get_image(value)
            target_widget.iconphoto(True, icon)
        elif pname == 'iconbitmap':
            icon = self.builder.get_iconbitmap(value)
            target_widget.iconbitmap(icon)
        else:
            super(TKToplevel, self)._set_property(target_widget, pname, value)
    
    #
    # Code generation methods
    #
    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname in ('geometry', 'overrideredirect', 'title'):
            line = "{0}.{1}('{2}')".format(targetid, pname, value)
            code_bag[pname] = (line, )
        elif pname == 'resizable':
            p1, p2 = self.RESIZABLE[value]
            line = '{0}.resizable({1}, {2})'.format(targetid, p1, p2)
            code_bag[pname] = (line, )
        elif pname in ('maxsize', 'minsize'):
            if '|' in value:
                w, h = value.split('|')
                line = '{0}.{1}({2}, {3})'.format(targetid, pname, w, h)
                code_bag[pname] = (line, )
        elif pname == 'iconbitmap':
            bitmap = self.builder.code_create_iconbitmap(value)
            line = "{0}.iconbitmap('{1}')".format(targetid, bitmap)
            code_bag[pname] = (line, )
        elif pname == 'iconphoto':
            image = self.builder.code_create_image(value)
            line = "{0}.iconphoto(True, {1})".format(targetid, image)
            code_bag[pname] = (line, )            
        else:
            super(TKToplevel, self)._code_set_property(targetid, pname,
                                                   value, code_bag)

register_widget('tk.Toplevel', TKToplevel,
                'Toplevel', ('Containers', 'tk', 'ttk'))


class TKFrame(BuilderObject):
    OPTIONS_STANDARD = ('borderwidth', 'cursor', 'highlightbackground',
                        'highlightcolor', 'highlightthickness',
                        'padx', 'pady', 'relief', 'takefocus')
    OPTIONS_SPECIFIC = ('background',  'class_', 'container',
                        'height', 'width')
    class_ = tk.Frame
    container = True
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    ro_properties = ('class_',)

register_widget('tk.Frame', TKFrame, 'Frame', ('Containers', 'tk'))


class TKLabel(BuilderObject):
    OPTIONS_STANDARD = (
        'activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'compound',
        'cursor', 'disabledforeground', 'font', 'foreground', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'image', 'justify', 'padx', 'pady', 'relief',
        'takefocus', 'text', 'textvariable', 'underline',
        'wraplength')
    OPTIONS_SPECIFIC = ('height', 'state', 'width')
    class_ = tk.Label
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC

register_widget('tk.Label', TKLabel, 'Label', ('Control & Display', 'tk'))


class TKLabelFrame(BuilderObject):
    class_ = tk.LabelFrame
    container = True
    OPTIONS_STANDARD = (
        'borderwidth', 'cursor', 'font', 'foreground',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'padx', 'pady', 'relief', 'takefocus', 'text')
    OPTIONS_SPECIFIC = ('background', 'class_', 'height',
                        'labelanchor', 'width')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    ro_properties = ('class_',)

register_widget('tk.LabelFrame', TKLabelFrame,
                'LabelFrame', ('Containers', 'tk'))


class TKEntry(EntryBaseBO):
    OPTIONS_STANDARD = (
        'background', 'borderwidth', 'cursor', 'exportselection',
        'font', 'foreground', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'insertbackground', 'insertborderwidth',
        'insertofftime', 'insertontime', 'insertwidth', 'justify',
        'relief', 'selectbackground', 'selectborderwidth',
        'selectforeground', 'takefocus', 'textvariable', 'xscrollcommand')
    OPTIONS_SPECIFIC = (
        'disabledbackground', 'disabledforeground', 'invalidcommand',
        'readonlybackground', 'show', 'state',
        'validate', 'validatecommand', 'width')
    OPTIONS_CUSTOM = ('text', 'validatecommand_args', 'invalidcommand_args')
    class_ = tk.Entry
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = ('validatecommand', 'invalidcommand',
                          'xscrollcommand')

register_widget('tk.Entry', TKEntry, 'Entry', ('Control & Display', 'tk'))


class TKButton(BuilderObject):
    class_ = tk.Button
    container = False
    OPTIONS_STANDARD = (
        'activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'compound', 'cursor',
        'disabledforeground', 'font', 'foreground',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'image', 'justify',  'padx', 'pady', 'relief',
        'repeatdelay', 'repeatinterval',  'takefocus', 'text',
        'textvariable', 'underline',  'wraplength')
    OPTIONS_SPECIFIC = (
        'command', 'default', 'height', 'overrelief',
        'state', 'width')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('command',)

register_widget('tk.Button', TKButton, 'Button', ('Control & Display', 'tk'))


class TKCheckbutton(BuilderObject):
    class_ = tk.Checkbutton
    container = False
    OPTIONS_STANDARD = (
        'activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'compound', 'cursor',
        'disabledforeground', 'font', 'foreground',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'image', 'justify',  'padx', 'pady', 'relief',
        'takefocus', 'text', 'textvariable', 'underline',  'wraplength')
    OPTIONS_SPECIFIC = (
        'command', 'height', 'indicatoron', 'overrelief', 'offrelief',
        'offvalue', 'onvalue', 'overrelief', 'selectcolor', 'selectimage',
        'state', 'tristateimage', 'tristatevalue', 'variable', 'width')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('command',)

register_widget('tk.Checkbutton', TKCheckbutton,
                'Checkbutton', ('Control & Display', 'tk'))


class TKListbox(BuilderObject):
    class_ = tk.Listbox
    container = False
    OPTIONS_STANDARD = (
        'background', 'borderwidth', 'cursor',
        'disabledforeground', 'exportselection', 'font',
        'foreground',  'highlightbackground', 'highlightcolor',
        'highlightthickness',  'relief',
        'selectbackground', 'selectborderwidth', 'selectforeground',
        'setgrid', 'takefocus',  'xscrollcommand', 'yscrollcommand')
    OPTIONS_SPECIFIC = ('activestyle', 'height', 'listvariable',
                        'selectmode', 'state', 'width')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('xscrollcommand', 'yscrollcommand')

register_widget('tk.Listbox', TKListbox,
                'Listbox', ('Control & Display', 'tk'))


class TKText(BuilderObject):
    class_ = tk.Text
    container = False
    OPTIONS_STANDARD = (
        'background', 'borderwidth', 'cursor', 'exportselection', 'font',
        'foreground', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'insertbackground', 'insertborderwidth',
        'insertofftime', 'insertontime', 'insertwidth',
        'padx', 'pady', 'relief', 'selectbackground',
        'selectborderwidth', 'selectforeground', 'setgrid', 'takefocus',
        'xscrollcommand', 'yscrollcommand',)
    OPTIONS_SPECIFIC = (
        'autoseparators', 'blockcursor', 'endline', 'height',
        'inactiveselectbackgroud', 'insertunfocussed', 'maxundo',
        'spacing1', 'spacing2', 'spacing3', 'startline',
        'state', 'tabs', 'tabstyle', 'undo', 'width', 'wrap')
    OPTIONS_CUSTOM = ('text',)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = ('xscrollcommand', 'yscrollcommand')

    def _set_property(self, target_widget, pname, value):
        if pname == 'text':
            state = target_widget.cget('state')
            if state == tk.DISABLED:
                target_widget.configure(state=tk.NORMAL)
                target_widget.insert('0.0', value)
                target_widget.configure(state=tk.DISABLED)
            else:
                target_widget.insert('0.0', value)
        else:
            super(TKText, self)._set_property(target_widget, pname, value)
    
    #
    # Code generation methods
    #
    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == 'text':
            state_value = ''
            if 'state' in self.wmeta.properties:
                state_value = self.wmeta.properties['state']
            lines = []
            line = "_text_ = '''{0}'''".format(value)
            lines.append(line)
            if state_value == tk.DISABLED:
                line = "{0}.configure(state='normal')".format(targetid)
                lines.append(line)
                line = "{0}.insert('0.0', _text_)".format(targetid)
                lines.append(line)
                line = "{0}.configure(state='disabled')".format(targetid)
                lines.append(line)
            else:
                line = "{0}.insert('0.0', _text_)".format(targetid)
                lines.append(line)
            code_bag[pname] = lines
        else:
            super(TKText, self)._code_set_property(targetid, pname,
                                                   value, code_bag)


register_widget('tk.Text', TKText, 'Text', ('Control & Display', 'tk', 'ttk'))


class TKPanedWindow(PanedWindowBO):
    class_ = tk.PanedWindow
    allowed_children = ('tk.PanedWindow.Pane',)
    OPTIONS_STANDARD = (
        'background', 'borderwidth', 'cursor', 'orient', 'relief',)
    OPTIONS_SPECIFIC = (
        'handlepad', 'handlesize', 'height', 'opaqueresize',
        'sashcursor', 'sashpad', 'sashrelief', 'sashwidth', 'showhandle',
        'width')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC

register_widget('tk.PanedWindow', TKPanedWindow,
                'PanedWindow', ('Containers', 'tk'))


class TKMenubutton(BuilderObject):
    class_ = tk.Menubutton
    container = False
    OPTIONS_STANDARD = (
        'activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'compound', 'cursor',
        'disabledforeground', 'font', 'foreground',
        'highlightbackground', 'highlightcolor',
        'highlightthickness', 'image', 'justify', 'padx', 'pady',
        'relief', 'takefocus', 'text', 'textvariable',
        'underline',  'wraplength')
    OPTIONS_SPECIFIC = (
        'direction', 'height', 'indicatoron', 'state', 'width')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    allowed_children = ('tk.Menu',)
    maxchildren = 1

    def add_child(self, bobject):
        self.widget.configure(menu=bobject.widget)

register_widget('tk.Menubutton', TKMenubutton,
                'Menubutton', ('Menu', 'Control & Display', 'tk',))


class TKMessage(BuilderObject):
    class_ = tk.Message
    container = False
    OPTIONS_STANDARD = (
        'anchor', 'background', 'borderwidth', 'cursor',
        'font', 'foreground', 'highlightbackground', 'highlightcolor',
        'highlightthickness',  'padx', 'pady', 'relief',
        'takefocus', 'text', 'textvariable')
    OPTIONS_SPECIFIC = ('aspect', 'justify', 'width')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC

register_widget('tk.Message', TKMessage,
                'Message', ('Control & Display', 'tk', 'ttk'))


class TKRadiobutton(BuilderObject):
    class_ = tk.Radiobutton
    container = False
    OPTIONS_STANDARD = (
        'activebackground', 'activeforeground', 'anchor',
        'background', 'bitmap', 'borderwidth', 'compound', 'cursor',
        'disabledforeground', 'font', 'foreground',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'image', 'justify',  'padx', 'pady', 'relief',
        'takefocus', 'text', 'textvariable', 'underline',  'wraplength')
    OPTIONS_SPECIFIC = (
        'command', 'height', 'indicatoron', 'overrelief', 'offrelief',
        'overrelief', 'selectcolor', 'selectimage',
        'state', 'tristateimage', 'tristatevalue', 'value',
        'variable', 'width')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('command',)

register_widget('tk.Radiobutton', TKRadiobutton,
                'Radiobutton', ('Control & Display', 'tk'))


class TKScale(BuilderObject):
    class_ = tk.Scale
    container = False
    OPTIONS_STANDARD = (
        'activebackground', 'background', 'borderwidth',
        'cursor',  'font', 'foreground',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'orient', 'relief', 'repeatdelay', 'repeatinterval',
        'takefocus',  'troughcolor')
    OPTIONS_SPECIFIC = (
        'bigincrement', 'command', 'digits', 'from_', 'label', 'length',
        'resolution', 'showvalue', 'sliderlength', 'sliderrelief',
        'state', 'tickinterval', 'to', 'variable', 'width')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('command',)

register_widget('tk.Scale', TKScale, 'Scale', ('Control & Display', 'tk'))


class TKScrollbar(BuilderObject):
    class_ = tk.Scrollbar
    container = False
    OPTIONS_STANDARD = (
        'activebackground',  'background', 'borderwidth', 'cursor',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'jump', 'orient', 'relief', 'repeatdelay', 'repeatinterval',
        'takefocus', 'troughcolor')
    OPTIONS_SPECIFIC = (
        'activerelief', 'command', 'elementborderwidth', 'width')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('command',)

register_widget('tk.Scrollbar', TKScrollbar,
                'Scrollbar', ('Control & Display', 'tk'))


class TKSpinbox(BuilderObject):
    class_ = tk.Spinbox
    container = False
    OPTIONS_STANDARD = (
        'activebackground', 'background', 'borderwidth',
        'cursor', 'exportselection', 'font', 'foreground',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'insertbackground', 'insertborderwidth',
        'insertofftime', 'insertontime', 'insertwidth', 'justify',
        'relief', 'repeatdelay', 'repeatinterval',
        'selectbackground', 'selectborderwidth', 'selectforeground',
        'takefocus', 'textvariable', 'xscrollcommand')
    OPTIONS_SPECIFIC = (
        'buttonbackground', 'buttoncursor', 'buttondownrelief',
        'buttonuprelief', 'command', 'disabledbackground',
        'disabledforeground', 'format', 'from_', 'invalidcommand',
        'increment', 'readonlybackground', 'state', 'to',
        'validate', 'validatecommand', 'values', 'width', 'wrap',)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('command', 'invalidcommand', 'validatecommand',
                          'xscrollcommand')

    def configure(self):
        # hack to configure 'from_' and 'to' and avoid exception
        if 'from_' in self.wmeta.properties:
            from_ = float(self.wmeta.properties['from_'])
            to = float(self.wmeta.properties.get('to', 0))
            if from_ > to:
                to = from_ + 1
                self.wmeta.properties['to'] = str(to)
        super(TKSpinbox, self).configure()

register_widget('tk.Spinbox', TKSpinbox,
                'Spinbox', ('Control & Display', 'tk'))


class TKCanvas(BuilderObject):
    class_ = tk.Canvas
    container = False
    OPTIONS_STANDARD = (
        'background', 'borderwidth', 'cursor', 'highlightbackground',
        'highlightcolor', 'highlightthickness',
        'insertbackground', 'insertborderwidth', 'insertofftime',
        'insertontime', 'insertwidth', 'relief',  'selectbackground',
        'selectborderwidth', 'selectforeground', 'takefocus',
        'xscrollcommand', 'yscrollcommand')
    OPTIONS_SPECIFIC = (
        'closeenough', 'confine', 'height', 'scrollregion', 'state',
        'width', 'xscrollincrement', 'yscrollincrement')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('xscrollcommand', 'yscrollcommand')

register_widget('tk.Canvas', TKCanvas,
                'Canvas', ('Control & Display', 'tk', 'ttk'))


class TKMenu(BuilderObject):
    layout_required = False
    allowed_parents = ('root', 'tk.Menubutton', 'ttk.Menubutton')
    allowed_children = (
        'tk.Menuitem.Submenu', 'tk.Menuitem.Checkbutton',
        'tk.Menuitem.Command', 'tk.Menuitem.Radiobutton',
        'tk.Menuitem.Separator')
    class_ = tk.Menu
    container = True
    OPTIONS_STANDARD = ('activebackground', 'activeborderwidth',
                        'activeforeground',  'background', 'borderwidth',
                        'cursor', 'disabledforeground', 'font', 'foreground',
                        'relief', 'takefocus')
    OPTIONS_SPECIFIC = ('postcommand',  'tearoff', 'tearoffcommand', 'title')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ('postcommand', 'tearoffcommand')
    allow_bindings = False

    def layout(self):
        pass

register_widget('tk.Menu', TKMenu, 'Menu', ('Menu', 'Containers', 'tk', 'ttk'))

#
# Helpers for Standard tk widgets
#


class TKMenuitem(BuilderObject):
    class_ = None
    container = False
    itemtype = None
    layout_required = False
    OPTIONS_STANDARD = ('activebackground', 'activeforeground', 'background',
                        'bitmap', 'compound', 'foreground',  'state')
    OPTIONS_SPECIFIC = ('accelerator', 'columnbreak', 'command',
                        'font', 'hidemargin', 'image', 'label', 'underline')
    OPTIONS_CUSTOM = ('command_id_arg',)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = ('command',)
    allow_bindings = False

    def realize(self, parent):
        self.widget = master = parent.get_child_master()
        itemproperties = dict(self.wmeta.properties)
        self._setup_item_properties(itemproperties)
        master.add(self.itemtype, **itemproperties)
        index = master.index(tk.END)
        # TODO: index of items is shifted if tearoff is changed
        # for now check tearoff config and recalculate index.
        has_tearoff = True if master.type(0) == 'tearoff' else False
        tearoff_conf = parent.wmeta.properties.get('tearoff', '1')
        offset = 0
        if has_tearoff and tearoff_conf in ('0', 'false'):
            offset = 1
        self.__index = index - offset
        return self.widget

    def _setup_item_properties(self, itemprops):
        pname = 'command_id_arg'
        if pname in itemprops:
            itemprops.pop(pname)
        for pname in itemprops:
            if pname == 'variable':
                varname = itemprops[pname]
                itemprops[pname] = self.builder.create_variable(varname)
            if pname in ('image', 'selectimage'):
                name = itemprops[pname]
                itemprops[pname] = self.builder.get_image(name)

    def configure(self):
        pass

    def layout(self):
        pass

    def _create_callback(self, cpname, callback):
        command = callback
        include_id = self.wmeta.properties.get('command_id_arg', 'false')
        include_id = include_id.lower()
        if include_id != 'false':
            def item_callback(item_id=self.wmeta.identifier):
                callback(item_id)
            command = item_callback
        return command

    def _connect_command(self, cpname, callback):
        self.widget.entryconfigure(self.__index, command=callback)
    
    #
    # code generation functions
    #
    def code_realize(self, boparent, code_identifier=None):
        self._code_identifier = boparent.code_child_master()
        masterid = self._code_identifier
        code_bag, kwproperties, complex_properties = \
            self._code_process_properties(self.wmeta.properties,
                                          self._code_identifier)
        lines = []
        pbag = []
        for pname in kwproperties:
            line = "{0}={1}".format(pname, code_bag[pname])
            pbag.append(line)
        props = ''
        if pbag:
            props = ', ' + ', '.join(pbag)
        itemtype = self.itemtype
        line = "{0}.add('{1}'{2})".format(masterid, itemtype, props)
        lines.append(line)
        for pname in complex_properties:
            lines.extend(code_bag[pname])
        return lines
    
    def code_configure(self, targetid=None):
        return tuple()
    
    def _code_process_properties(self, properties, targetid):
        code_bag = {}
        for pname, value in properties.items():
            if (pname not in self.ro_properties):
                self._code_set_property(targetid, pname, value, code_bag)
        
        # properties
        # determine kw properties or complex properties
        kwproperties = []
        complex_properties = []
        for pname, value in code_bag.items():
            if isinstance(value, str):
                kwproperties.append(pname)
            else:
                complex_properties.append(pname)
        
        return (code_bag, kwproperties, complex_properties)
    
    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == 'command_id_arg':
            if value:
                line = "#TODO: setup command_id_arg '{0}' for menuitem."
                line = line.format(value)
                code_bag[pname] = (line, )
        else:
            super(TKMenuitem, self)._code_set_property(targetid, pname, value,
                                                       code_bag)
    
    def code_connect_commands(self):
        return tuple()


class TKMenuitemSubmenu(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    allowed_children = (
        'tk.Menuitem.Submenu', 'tk.Menuitem.Checkbutton',
        'tk.Menuitem.Command', 'tk.Menuitem.Radiobutton',
        'tk.Menuitem.Separator')
    OPTIONS_STANDARD = ('activebackground', 'activeborderwidth',
                        'activeforeground',  'background', 'borderwidth',
                        'bitmap', 'compound',
                        'cursor', 'disabledforeground', 'font', 'foreground',
                        'relief', 'takefocus', 'state')
    OPTIONS_SPECIFIC = ('accelerator', 'columnbreak',
                        'hidemargin', 'image', 'label',
                        'tearoff', 'tearoffcommand',
                        'underline')
    OPTIONS_CUSTOM = tuple()
    properties = tuple(set(OPTIONS_STANDARD + OPTIONS_SPECIFIC +
                           OPTIONS_CUSTOM))

    def realize(self, parent):
        master = parent.get_child_master()
        menu_properties = dict(
            (k, v) for k, v in self.wmeta.properties.items()
            if k in TKMenu.properties)
        self._setup_item_properties(menu_properties)

        item_properties = dict(
            (k, v) for k, v in self.wmeta.properties.items()
            if k in TKMenuitem.properties)
        self._setup_item_properties(item_properties)

        self.widget = submenu = TKMenu.class_(master, **menu_properties)
        item_properties['menu'] = submenu
        master.add(tk.CASCADE, **item_properties)
        return self.widget

    def configure(self):
        pass

    def layout(self):
        pass
    
    #
    # code generation functions
    #
    def code_realize(self, boparent, code_identifier=None):
        if self._code_identifier is None:
            self._code_identifier = self.wmeta.identifier
        
        masterid = boparent.code_child_master()
        lines = []
        # menu properties
        menuprop = {}
        for pname, value in self.wmeta.properties.items():
            if pname in TKMenu.properties:
                menuprop[pname] = value
        
        code_bag, kw_properties, complex_properties = \
            self._code_process_properties(menuprop,
                                          self.code_identifier())
        for pname in complex_properties:
            lines.extend(code_bag[pname])
            
        mpbag = []
        for pname in kw_properties:
            line = "{0}={1}".format(pname, code_bag[pname])
            mpbag.append(line)
        mprops = ''
        if mpbag:
            mprops = ', ' + ', '.join(mpbag)
        
        # item properties
        itemprop = {}
        for pname, value in self.wmeta.properties.items():
            if pname in TKMenuitem.properties:
                itemprop[pname] = value
        
        code_bag, kw_properties, complex_properties = \
            self._code_process_properties(itemprop, self.code_identifier())
        for pname in complex_properties:
            lines.extend(code_bag[pname])

        pbag = []
        prop = 'menu={0}'.format(self.code_identifier())
        pbag.append(prop)
        for pname in kw_properties:
            line = "{0}={1}".format(pname, code_bag[pname])
            pbag.append(line)
        props = ''
        if pbag:
            props = ', {0}'.format(', '.join(pbag))
        
        # creation
        line = "{0} = tk.Menu({1}{2})".format(self.code_identifier(),
                                              masterid, mprops)
        lines.append(line)
        line = "{0}.add(tk.CASCADE{1})".format(masterid, props)
        lines.append(line)
        
        return lines
    
    def code_configure(self, targetid=None):
        return tuple()


register_widget('tk.Menuitem.Submenu', TKMenuitemSubmenu,
                'Menuitem.Submenu', ('Menu', 'tk', 'ttk'))


class TKMenuitemCommand(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    itemtype = tk.COMMAND

register_widget('tk.Menuitem.Command', TKMenuitemCommand,
                'Menuitem.Command', ('Menu', 'tk', 'ttk'))


class TKMenuitemCheckbutton(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    itemtype = tk.CHECKBUTTON
    OPTIONS_STANDARD = TKMenuitem.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = \
        TKMenuitem.OPTIONS_SPECIFIC + \
        ('indicatoron', 'selectcolor', 'selectimage', 'variable')
    OPTIONS_CUSTOM = TKMenuitem.OPTIONS_CUSTOM
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM

register_widget('tk.Menuitem.Checkbutton', TKMenuitemCheckbutton,
                'Menuitem.Checkbutton', ('Menu', 'tk', 'ttk'))


class TKMenuitemRadiobutton(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    itemtype = tk.RADIOBUTTON
    OPTIONS_STANDARD = TKMenuitem.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = \
        TKMenuitem.OPTIONS_SPECIFIC + \
        ('onvalue', 'offvalue', 'value', 'variable')
    OPTIONS_CUSTOM = TKMenuitem.OPTIONS_CUSTOM
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM

register_widget('tk.Menuitem.Radiobutton', TKMenuitemRadiobutton,
                'Menuitem.Radiobutton', ('Menu', 'tk', 'ttk'))


class TKMenuitemSeparator(TKMenuitem):
    allowed_parents = ('tk.Menu', 'tk.Menuitem.Submenu')
    itemtype = tk.SEPARATOR
    OPTIONS_STANDARD = tuple()
    OPTIONS_SPECIFIC = tuple()
    OPTIONS_CUSTOM = tuple()
    properties = tuple()
    command_properties = tuple()

register_widget('tk.Menuitem.Separator', TKMenuitemSeparator,
                'Menuitem.Separator', ('Menu', 'tk', 'ttk'))


class TKPanedWindowPane(PanedWindowPaneBO):
    class_ = None
    container = True
    allowed_parents = ('tk.PanedWindow',)
    maxchildren = 1
    OPTIONS_SPECIFIC = ('height', 'hide', 'minsize',
                        'padx', 'pady', 'sticky', 'stretch', 'width')
    properties = OPTIONS_SPECIFIC

register_widget('tk.PanedWindow.Pane', TKPanedWindowPane,
                'PanedWindow.Pane', ('Pygubu Helpers', 'tk'))


class TKLabelwidgetBO(BuilderObject):
    class_ = None
    container = True
    allowed_parents = ('tk.LabelFrame', 'ttk.Labelframe')
    maxchildren = 1
    layout_required = False
    allow_bindings = False

    def realize(self, parent):
        self.widget = parent.get_child_master()
        return self.widget

    def add_child(self, bobject):
        self.widget.configure(labelwidget=bobject.widget)
    
    def layout(self, target=None, configure_gridrc=True):
        pass
    
    #
    # code generation functions
    #
    def code_realize(self, boparent, code_identifier=None):
        self._code_identifier = boparent.code_child_master()
        return tuple()
    
    def code_configure(self, targetid=None):
        return tuple()
    
    def code_layout(self, targetid=None):
        return tuple()
    
    def code_child_add(self, childid):
        line = '{0}.configure(labelwidget={1})'
        line = line.format(self.code_child_master(), childid)
        return (line,)


register_widget('pygubu.builder.widgets.Labelwidget', TKLabelwidgetBO,
                'Labelwidget', ('Pygubu Helpers', 'tk', 'ttk'))
