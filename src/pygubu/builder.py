# encoding: utf-8
import importlib
import logging
import tkinter
from pathlib import Path

from .component.builderobject import CLASS_MAP, BuilderObject
from .component.widgetmeta import WidgetMeta
from .stockimage import StockImage, StockImageException
from .component.uidefinition import UIDefinition
from .component.plugin_manager import PluginManager

logger = logging.getLogger(__name__)


#
# Builder class
#


class Builder(object):
    """Allows to build a tk interface from xml definition.

    Parameters
    ----------
    translator: callable
        function used to process translatable strings.
    """

    TK_VARIABLE_TYPES = ("string", "int", "boolean", "double")

    def __init__(self, translator=None):
        super(Builder, self).__init__()
        self.uidefinition = UIDefinition(translator=translator)
        self.root = None
        self.objects = {}
        self.tkvariables = {}
        self.translator = translator

    def add_resource_path(self, path):
        """Add additional path to the resources paths."""
        StockImage.add_resource_path(path)

    def add_resource_package(self, pkg: str):
        StockImage.add_resource_package(pkg)

    def get_image(self, path):
        """Return tk image corresponding to name which is taken form path."""
        image = ""
        name = Path(path).name
        if not StockImage.is_registered(name):
            StockImage.find_and_register(name)
        try:
            image = StockImage.get(name)
        except StockImageException:
            # TODO: notify something here.
            pass
        return image

    def get_iconbitmap(self, path):
        """Return path to use as iconbitmap property."""
        image = None
        name = Path(path).name
        if not StockImage.is_registered(name):
            StockImage.find_and_register(name)
        try:
            image = StockImage.as_iconbitmap(name)
        except StockImageException:
            # TODO: notify something here.
            pass
        return image

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
        vtype = "string"  # default type if not defined
        if ":" in name_or_desc:
            vtype, vname = name_or_desc.split(":")
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
                if type_from_name == "int":
                    var = tkinter.IntVar()
                elif type_from_name == "boolean":
                    var = tkinter.BooleanVar()
                elif type_from_name == "double":
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

    def get_object(self, name, master=None, extra_init_args: dict = None):
        """Find and create the widget named name.
        Use master as parent. If widget was already created, return
        that instance."""
        widget = None
        if name in self.objects:
            widget = self.objects[name].widget
        else:
            wmeta = self.uidefinition.get_widget(name)
            if wmeta is not None:
                rmeta = WidgetMeta("root", "root")
                root = BuilderObject(self, rmeta)
                root.widget = master
                bobject = self._realize(root, wmeta, extra_init_args)
                widget = bobject.widget
        if widget is None:
            msg = 'Widget "{0}" not defined.'.format(name)
            raise Exception(msg)
        return widget

    def _import_class(self, builder_id):
        plugin_managed = False
        for loader in PluginManager.builder_plugins():
            if loader.can_load(builder_id):
                _module = loader.get_module_for(builder_id)
                try:
                    importlib.import_module(_module)
                    plugin_managed = True
                    logger.debug("Module %s loaded.", _module)
                except (ModuleNotFoundError, ImportError) as e:
                    msg = "Failed to import module as fullname: %s"
                    logger.debug(msg, _module)
                    raise e

        # If no plugin, Try loading as old custom widget method.
        if not plugin_managed:
            _module = builder_id
            try:
                # Import module as full path
                importlib.import_module(_module)
                logger.debug("Module %s loaded.", _module)
            except (ModuleNotFoundError, ImportError) as e:
                # A single module can contain various widgets
                # try to import the first part of the path
                if "." in _module:
                    first, last = _module.rsplit(".", 1)
                    try:
                        importlib.import_module(first)
                        logger.debug("Module %s loaded.", first)
                    except (ModuleNotFoundError, ImportError):
                        importlib.import_module(last)
                        logger.debug("Module %s loaded.", last)
                else:
                    msg = "Failed to import module: %s"
                    logger.debug(msg, _module)
                    raise e

    def is_mapped(self, builder_uid):
        return builder_uid in CLASS_MAP

    def _get_builder_for(self, builder_uid):
        return CLASS_MAP[builder_uid].builder

    def _realize(self, master, wmeta, extra_init_args: dict = None):
        """Builds a widget from widget metadata using master as parent."""

        if not self.is_mapped(wmeta.classname):
            self._import_class(wmeta.classname)

        if self.is_mapped(wmeta.classname):
            bclass = self._get_builder_for(wmeta.classname)
            parent = bclass.factory(self, wmeta)
            self._pre_realize(parent)
            parent.realize(master, extra_init_args)
            parent.configure()

            self.objects[wmeta.identifier] = parent

            for childmeta in self.uidefinition.widget_children(
                wmeta.identifier
            ):
                child = self._realize(parent, childmeta)
                parent.add_child(child)
            parent.configure_children()
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
        has_layout = len(wmeta.layout_properties) > 1
        if wmeta.layout_required and not has_layout:
            logger.debug(
                "No layout information for: (%s, %s).",
                cname,
                wmeta.identifier,
            )

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
            msg = "Missing callbacks for commands: %s"
            logger.warning(msg, notconnected)
            return notconnected
        else:
            return None

    def forget_unnamed(self):
        """Removes unnamed object from the objects attribute.

        User should calls this method at the end of the build process,
        after calling "connect_callbacks".
        """
        for key in list(self.objects.keys()):
            if not self.objects[key].wmeta.is_named:
                del self.objects[key]

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

    def code_translate_str(self, value: str) -> str:
        raise NotImplementedError()


# Load plugins on module init
PluginManager.load_plugins()
