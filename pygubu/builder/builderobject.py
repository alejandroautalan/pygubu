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
    # allow_container_layout, True if widget can setup grid row/col options
    allow_container_layout = True
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
        return clsobj

    def __init__(self, builder, wdescr):
        self.widget = None
        self.builder = builder
        self.objectid = wdescr.get('id', None)
        self.descr = wdescr
        self.properties = wdescr.get('properties', {})
        self.layout_properties = wdescr.get('layout', {})
        self.bindings = wdescr.get('bindings', [])

    def realize(self, parent):
        args = self._get_init_args()
        master = parent.get_child_master()
        self.widget = self.class_(master, **args)
        return self.widget

    def _get_init_args(self):
        """Creates dict with properties marked as readonly"""

        args = {}
        for rop in self.ro_properties:
            if rop in self.properties:
                args[rop] = self.properties[rop]
        return args

    def configure(self, target=None):
        if target is None:
            target = self.widget
        for pname, value in self.properties.items():
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
                if 'text' in self.properties and pname == 'textvariable':
                    propvalue.set(self.properties['text'])
                elif 'value' in self.properties and pname == 'variable':
                    propvalue.set(self.properties['value'])
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

    def layout(self, target=None):
        if not self.layout_required:
            return
        if target is None:
            target = self.widget

        #use grid layout for all
        self._grid_layout(target)

    def _grid_layout(self, target, configure_rc=True):
        properties = dict(self.layout_properties)
        grid_propagate = properties.pop('propagate', 'True')
        rowsprop = properties.pop('rows', None)
        colsprop = properties.pop('columns', None)

        target.grid(**properties)
        if grid_propagate != 'True':
            target.grid_propagate(0)
        if configure_rc:
            self._grid_rc_layout(target, rowsprop, colsprop)

    def _grid_rc_layout(self, target, rowsprop=None, colsprop=None):
        if rowsprop is None:
            properties = dict(self.layout_properties)
            rowsprop = properties.pop('rows', {})
            colsprop = properties.pop('columns', {})
        # configure grid row/col properties:
        for row in rowsprop:
            target.rowconfigure(row, **rowsprop[row])
        for col in colsprop:
            target.columnconfigure(col, **colsprop[col])

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
                cmd_name = self.properties.get(cmd, None)
                if cmd_name is not None:
                    if cmd_name in cmd_bag:
                        callback = self._create_callback(cmd,
                                                         cmd_bag[cmd_name])
                        self._connect_command(cmd, callback)
                    else:
                        notconnected.append(cmd_name)
        else:
            for cmd in self.command_properties:
                cmd_name = self.properties.get(cmd, None)
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
            for bind in self.bindings:
                cb_name = bind.get('handler', None)
                if cb_name is not None:
                    if cb_name in cb_bag:
                        callback = cb_bag[cb_name]
                        cb_seq = bind.get('sequence')
                        cb_add = bind.get('add', None)
                        self.widget.bind(cb_seq, callback, add=cb_add)
                    else:
                        notconnected.append(cb_name)
        else:
            for bind in self.bindings:
                cb_name = bind.get('handler', None)
                if cb_name is not None:
                    if hasattr(cb_bag, cb_name):
                        callback = getattr(cb_bag, cb_name)
                        cb_seq = bind.get('sequence')
                        cb_add = bind.get('add', None)
                        self.widget.bind(cb_seq, callback, add=cb_add)
                    else:
                        notconnected.append(cb_name)
        if notconnected:
            return notconnected
        else:
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
            args = self.properties.get(cpname + '_args', '')
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
        master = parent.widget
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
        self.widget = parent.widget
        return self.widget

    def configure(self):
        pass

    def layout(self):
        pass

    def add_child(self, bobject):
        self.widget.add(bobject.widget, **self.properties)
