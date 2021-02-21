# encoding: utf8
from __future__ import unicode_literals

import os
import importlib
import logging
import xml.etree.ElementTree as ET
try:
    import tkinter
except:
    import Tkinter as tkinter

from pygubu.builder.builderobject import BuilderObject, CLASS_MAP, CB_TYPES
from pygubu.builder.widgetmeta import WidgetMeta
from pygubu.stockimage import StockImage, StockImageException
from .uidefinition import UIDefinition

logger = logging.getLogger(__name__)


#
# Builder class
#

class Builder(object):
    """Allows to build a tk interface from xml definition."""
    TK_VARIABLE_TYPES = ('string', 'int', 'boolean', 'double')

    def __init__(self, translator=None):
        super(Builder, self).__init__()
        self.uidefinition = UIDefinition(translator=translator)
        self.root = None
        self.objects = {}
        self.tkvariables = {}
        self._resource_paths = []
        self.translator = translator

    def add_resource_path(self, path):
        """Add additional path to the resources paths."""
        self._resource_paths.append(path)

    def get_image(self, path):
        """Return tk image corresponding to name which is taken form path."""
        image = ''
        name = os.path.basename(path)
        self.__load_image(path)
        try:
            image = StockImage.get(name)
        except StockImageException:
            # TODO: notify something here.
            pass
        return image
    
    def get_iconbitmap(self, path):
        """Return path to use as iconbitmap property."""
        image = None
        name = os.path.basename(path)
        self.__load_image(path)
        try:
            image = StockImage.as_iconbitmap(name)
        except StockImageException:
            # TODO: notify something here.
            pass
        return image
    
    def __load_image(self, path):
        name = os.path.basename(path)
        if not StockImage.is_registered(name):
            ipath = self.__find_image(path)
            if ipath is not None:
                StockImage.register(name, ipath)
            else:
                msg = "Image '%s' not found in resource paths."
                logger.warning(msg, name)        

    def __find_image(self, relpath):
        image_path = None
        for rp in self._resource_paths:
            for root, dirs, files in os.walk(rp):
                if relpath in files:
                    image_path = os.path.join(root, relpath)
                    break
            if image_path is not None:
                break
        return image_path

    def get_variable(self, varname):
        """Return a tk variable created with 'create_variable' method."""
        return self.tkvariables[varname]
        
    def import_variables(self, container, varnames=None):
        """Helper method to avoid call get_variable for every variable."""
        if varnames is None:
            for keyword in self.tkvariables:
                setattr(container, keyword, self.tkvariables[keyword])
        else:
            for keyword in varnames:
                if keyword in self.tkvariables:
                    setattr(container, keyword, self.tkvariables[keyword])

    def _process_variable_description(self, name_or_desc):
        vname = name_or_desc
        vtype = 'string'  # default type if not defined
        if ':' in name_or_desc:
            vtype, vname = name_or_desc.split(':')
            #  Fix incorrect order bug #33
            if vtype not in self.TK_VARIABLE_TYPES:
                #  Swap order
                vtype, vname = vname, vtype
                if vtype not in self.TK_VARIABLE_TYPES:
                    msg = 'Undefined variable type in "{0}"'.format(vname)
                    raise Exception(msg)
        return (vname, vtype)

    def create_variable(self, varname, vtype=None):
        """Create a tk variable.
        If the variable was created previously return that instance.
        """
        vname, type_from_name = self._process_variable_description(varname)

        if vname in self.tkvariables:
            var = self.tkvariables[vname]
        else:
            if vtype is None:
                # get type from name
                if type_from_name == 'int':
                    var = tkinter.IntVar()
                elif type_from_name == 'boolean':
                    var = tkinter.BooleanVar()
                elif type_from_name == 'double':
                    var = tkinter.DoubleVar()
                else:
                    var = tkinter.StringVar()
            else:
                var = vtype()

            self.tkvariables[vname] = var
        return var

    def add_from_file(self, file_or_filename):
        """Load ui definition from file."""
        self.uidefinition.load_file(file_or_filename)

    def add_from_string(self, strdata):
        self.uidefinition.load_from_string(strdata)

    def add_from_xmlnode(self, element):
        """Load ui definition from xml.etree.Element node."""
        self.uidefinition.add_xmlnode(element)

    def get_object(self, name, master=None):
        """Find and create the widget named name.
        Use master as parent. If widget was already created, return
        that instance."""
        widget = None
        if name in self.objects:
            widget = self.objects[name].widget
        else:
            wmeta = self.uidefinition.get_widget(name)
            if wmeta is not None:
                rmeta = WidgetMeta('root', 'root')
                root = BuilderObject(self, rmeta)
                root.widget = master
                bobject = self._realize(root, wmeta)
                widget = bobject.widget
        if widget is None:
            msg = 'Widget "{0}" not defined.'.format(name)
            raise Exception(msg)
        return widget

    def _import_class(self, modulename):
        if modulename.startswith('tk.'):
            importlib.import_module('pygubu.builder.tkstdwidgets')
        elif modulename.startswith('ttk.'):
            importlib.import_module('pygubu.builder.ttkstdwidgets')
        else:
            # Import module as full path
            try:
                importlib.import_module(modulename)
            except ImportError as e:
                msg = 'Failed to import module as fullname: %s'
                logger.warning(msg, modulename)
                logger.exception(e)
                # A single module can contain various widgets
                # try to import the first part of the path
                if '.' in modulename:
                    first, last = modulename.rsplit('.', 1)
                    try:
                        importlib.import_module(first)
                    except ImportError as e:
                        importlib.import_module(last)
                else:
                    raise e

    def _realize(self, master, wmeta):
        """Builds a widget from widget metadata using master as parent."""
        
        if wmeta.classname not in CLASS_MAP:
            self._import_class(wmeta.classname)

        if wmeta.classname in CLASS_MAP:
            bclass = CLASS_MAP[wmeta.classname].builder
            parent = bclass.factory(self, wmeta)
            self._pre_realize(parent)
            parent.realize(master)

            self.objects[wmeta.identifier] = parent

            for childmeta in \
                self.uidefinition.widget_children(wmeta.identifier):
                child = self._realize(parent, childmeta)
                parent.add_child(child)
            parent.configure()
            parent.layout()
            
            self._post_realize(parent)
            
            return parent
        else:
            msg = 'Class "{0}" not mapped'.format(wmeta.classname)
            raise Exception(msg)

    def _pre_realize(self, bobject):
        wmeta = bobject.wmeta
        cname = wmeta.classname
        wmeta.layout_required = bobject.layout_required
        has_layout = (len(wmeta.layout_properties) > 1)
        if wmeta.layout_required and not has_layout:
            logger.debug('No layout information for: (%s, %s).',
                           cname, wmeta.identifier)
    
    def _post_realize(self, bobject):
        pass

    def connect_callbacks(self, callbacks_bag):
        """Connect callbacks specified in callbacks_bag with callbacks
        defined in the ui definition.
        Return a list with the name of the callbacks not connected.
        """
        notconnected = []
        for wname, builderobj in self.objects.items():
            missing = builderobj.connect_commands(callbacks_bag)
            if missing is not None:
                notconnected.extend(missing)
            missing = builderobj.connect_bindings(callbacks_bag)
            if missing is not None:
                notconnected.extend(missing)
        if notconnected:
            notconnected = list(set(notconnected))
            msg = 'Missing callbacks for commands: %s'
            logger.warning(msg, notconnected)
            return notconnected
        else:
            return None
    
    def code_create_variable(self, name_or_desc, value, vtype=None):
        raise NotImplementedError()
    
    def code_create_image(self, filename):
        raise NotImplementedError()
    
    def code_create_iconbitmap(self, filename):
        raise NotImplementedError()
    
    def code_classname_for(self, bobject):
        raise NotImplementedError()
    
    def code_create_callback(self, widgetid, cbname, cbtype, args=None):
        raise NotImplementedError()
