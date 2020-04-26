# encoding: utf8
from __future__ import unicode_literals
import logging
from collections import namedtuple
try:
    import tkinter as tk
except:
    import Tkinter as tk

__all__ = [
    'BuilderObject', 'EntryBaseBO', 'PanedWindowBO', 'PanedWindowPaneBO',
    'WidgetDescription', 'CLASS_MAP', 'CUSTOM_PROPERTIES',
    'register_widget', 'register_property']

logger = logging.getLogger(__name__)


WidgetDescription = namedtuple('WidgetDescription',
                              ['classname', 'builder', 'label', 'tags'])

CLASS_MAP = {}


def register_widget(classname, builder, label=None, tags=None):
    if label is None:
        label = classname
    if tags is None:
        tags = tuple()

    CLASS_MAP[classname] = WidgetDescription(classname, builder, label, tags)


CUSTOM_PROPERTIES = {}


def register_property(name, description):
    if name in CUSTOM_PROPERTIES:
        CUSTOM_PROPERTIES[name].update(description)
        logger.debug('Updating registered property {0}'.format(name))
    else:
        CUSTOM_PROPERTIES[name] = description
        logger.debug('Registered property {0}'.format(name))


#
# Base class
#
class BuilderObject(object):
    """Base class for Widgets created with Builder"""

    OPTIONS_STANDARD = tuple()
    OPTIONS_SPECIFIC = tuple()
    OPTIONS_CUSTOM = tuple()
    class_ = None
    container = False
    allowed_parents = None
    allowed_children = None
    maxchildren = None
    properties = tuple()
    ro_properties = tuple()
    layout_required = True
    command_properties = tuple()
    allow_bindings = True
    tkvar_properties = ('listvariable', 'textvariable', 'variable')
    tkimage_properties = ('image', 'selectimage')
    tkfont_properties = ('font',)

    @classmethod
    def factory(cls, builder, wdata):
        clsobj = cls(builder, wdata)
        wdata.layout_required = clsobj.layout_required
        return clsobj

    def __init__(self, builder, wmeta):
        super(BuilderObject, self).__init__()
        self.widget = None
        self.builder = builder
        self.wmeta = wmeta

    def realize(self, parent):
        args = self._get_init_args()
        master = parent.get_child_master()
        self.widget = self.class_(master, **args)
        return self.widget

    def _get_init_args(self):
        """Creates dict with properties marked as readonly"""

        args = {}
        for rop in self.ro_properties:
            if rop in self.wmeta.properties:
                args[rop] = self.wmeta.properties[rop]
        return args

    def configure(self, target=None):
        if target is None:
            target = self.widget
        for pname, value in self.wmeta.properties.items():
            if (pname not in self.ro_properties and
                pname not in self.command_properties):
                self._set_property(target, pname, value)

    def _set_property(self, target_widget, pname, value):
        if pname not in self.__class__.properties:
            msg = "Attempt to set an unknown property '{0}' on class '{1}'"
            msg = msg.format(pname, repr(self.class_))
            logger.warning(msg)
        else:
            propvalue = value
            if pname in self.tkvar_properties:
                propvalue = self.builder.create_variable(value)
                if 'text' in self.wmeta.properties and pname == 'textvariable':
                    propvalue.set(self.wmeta.properties['text'])
                elif 'value' in self.wmeta.properties and pname == 'variable':
                    propvalue.set(self.wmeta.properties['value'])
            elif pname in self.tkimage_properties:
                propvalue = self.builder.get_image(value)
            elif pname == 'takefocus':
                if value:
                    propvalue = tk.getboolean(value)

            try:
                target_widget[pname] = propvalue
            except tk.TclError as e:
                msg = "Failed to set property '{0}' on class '{1}'. TclError: {2}"
                msg = msg.format(pname, repr(self.class_), str(e))
                logger.error(msg)

    def layout(self, target=None, configure_gridrc=True):
        if self.layout_required:
            if target is None:
                target = self.widget
    
            # Check manager
            manager = self.wmeta.manager
            if manager == 'grid':
                self._grid_layout(target)
            elif manager == 'pack':
                self._pack_layout(target)
            elif manager == 'place':
                self._place_layout(target)
            else:
                msg = 'Invalid layout manager: {0}'.format(manager)
                raise Exception(msg)
        if configure_gridrc:
            parent = target.nametowidget(target.winfo_parent())
            self._gridrc_config(parent)

    def _pack_layout(self, target):
        properties = dict(self.wmeta.layout_properties)
        propagate = properties.pop('propagate', 'true')
        # Do pack
        target.pack(**properties)
        if propagate.lower() != 'true':
            target.pack_propagate(0)
    
    def _place_layout(self, target):
        # Do place
        target.place(**self.wmeta.layout_properties)
    
    def _grid_layout(self, target):
        properties = dict(self.wmeta.layout_properties)
        propagate = properties.pop('propagate', 'true')
        target.grid(**properties)
        if propagate.lower != 'true':
            target.grid_propagate(0)

    def _gridrc_config(self, target):
        # configure grid row/col properties:
        for type_, num, pname, value in self.wmeta.gridrc_properties:
            if type_ == 'row':
                target.rowconfigure(num, **{pname: value})
            else:
                target.columnconfigure(num, **{pname: value})

    def get_child_master(self):
        return self.widget

    def add_child(self, bobject):
        pass

    def _create_callback(self, cpname, command):
        return command

    def _connect_command(self, cpname, callback):
        prop = {cpname: callback}
        self.widget.configure(**prop)

    def connect_commands(self, cmd_bag):
        notconnected = []

        if isinstance(cmd_bag, dict):
            for cmd in self.command_properties:
                cmd_name = self.wmeta.properties.get(cmd, None)
                if cmd_name is not None:
                    if cmd_name in cmd_bag:
                        callback = self._create_callback(cmd,
                                                         cmd_bag[cmd_name])
                        self._connect_command(cmd, callback)
                    else:
                        notconnected.append(cmd_name)
        else:
            for cmd in self.command_properties:
                cmd_name = self.wmeta.properties.get(cmd, None)
                if cmd_name is not None:
                    if hasattr(cmd_bag, cmd_name):
                        callback = self._create_callback(cmd,
                            getattr(cmd_bag, cmd_name))
                        self._connect_command(cmd, callback)
                    else:
                        notconnected.append(cmd_name)
        if notconnected:
            return notconnected
        else:
            return None

    def connect_bindings(self, cb_bag):
        notconnected = []

        if isinstance(cb_bag, dict):
            for bind in self.wmeta.bindings:
                cb_name = bind.handler
                if cb_name in cb_bag:
                    callback = cb_bag[cb_name]
                    self.widget.bind(bind.sequence, callback, add=bind.add)
                else:
                    notconnected.append(cb_name)
        else:
            for bind in self.wmeta.bindings:
                cb_name = bind.handler
                if hasattr(cb_bag, cb_name):
                    callback = getattr(cb_bag, cb_name)
                    self.widget.bind(bind.sequence, callback, add=bind.add)
                else:
                    notconnected.append(cb_name)
        if notconnected:
            return notconnected
        else:
            return None

    def code_generator(self, masterid):
        '''Return a CodeGeneratorBase instance for this builder'''
        return None


#
# Base clases for some widgets
#
class EntryBaseBO(BuilderObject):
    """Base class for tk.Entry and ttk.Entry builder objects"""
    def _set_property(self, target_widget, pname, value):
        if pname == 'text':
            target_widget.delete('0', tk.END)
            target_widget.insert('0', value)
        elif pname in ('validatecommand_args', 'invalidcommand_args'):
            pass
        else:
            super(EntryBaseBO, self)._set_property(target_widget, pname, value)

    def _create_callback(self, cpname, command):
        callback = command
        if cpname in ('validatecommand', 'invalidcommand'):
            args = self.wmeta.properties.get(cpname + '_args', '')
            if args:
                args = args.split(' ')
                callback = (self.widget.register(command),) + tuple(args)
            else:
                callback = self.widget.register(command)
        return callback


class PanedWindowBO(BuilderObject):
    """Base class for tk.PanedWindow and ttk.Panedwindow builder objects"""
    class_ = None
    container = True
    allow_container_layout = False
    properties = []
    ro_properties = ('orient', )

    def realize(self, parent):
        master = parent.get_child_master()
        args = self._get_init_args()
        if 'orient' not in args:
            args['orient'] = 'vertical'
        self.widget = self.class_(master, **args)
        return self.widget


#
# Base clases for some widget Helpers
#
class PanedWindowPaneBO(BuilderObject):
    class_ = None
    container = True
    allow_container_layout = False
    properties = []
    layout_required = False
    allow_bindings = False

    def realize(self, parent):
        self.widget = parent.get_child_master()
        return self.widget

    def configure(self):
        pass

    def layout(self):
        pass

    def add_child(self, bobject):
        self.widget.add(bobject.widget, **self.wmeta.properties)



class CodeGeneratorBase(object):
    
    def __init__(self, builder, masterid):
        super(CodeGeneratorBase, self).__init__()
        self.builder = builder
        self.masterid = masterid
        self.identifier = builder.wmeta.identifier
    
    def create(self):
        pass
    
    def configure(self):
        pass
    
    def layout(self):
        pass

    def add_child(self, childid, childmeta):
        pass
    
    def child_master(self):
        return self.identifier