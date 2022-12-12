# encoding: utf-8
import json
import logging
import tkinter as tk
from collections import defaultdict, namedtuple

__all__ = [
    "BuilderObject",
    "EntryBaseBO",
    "PanedWindowBO",
    "PanedWindowPaneBO",
    "WidgetDescription",
    "CLASS_MAP",
    "CB_TYPES",
    "CUSTOM_PROPERTIES",
    "TRANSLATABLE_PROPERTIES",
]

logger = logging.getLogger(__name__)

#
# Utility functions
#


def isfloat(num: str) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False


#
# BuilderObject
#

WidgetDescription = namedtuple(
    "WidgetDescription", ["classname", "builder", "label", "tags", "group"]
)

CLASS_MAP = {}
CUSTOM_PROPERTIES = {}


class CB_TYPES:
    """Callback types"""

    SIMPLE = "simple"
    WITH_WID = "with_wid"
    ENTRY_VALIDATE = "entry_validate"
    SCROLL = "scroll"
    SCROLLSET = "scrollset"
    SCALE = "scale"
    BIND_EVENT = "bind_event"


TRANSLATABLE_PROPERTIES = ["label", "text", "title"]

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
    container_layout = False
    allowed_parents = None
    allowed_children = None
    maxchildren = None
    properties = tuple()
    ro_properties = tuple()
    layout_required = True
    command_properties = tuple()
    allow_bindings = True
    tkvar_properties = ("listvariable", "textvariable", "variable")
    tkimage_properties = (
        "image",
        "selectimage",
        "iconphoto",
        "backgroundimage",
    )
    tkfont_properties = ("font",)
    virtual_events = tuple()

    @classmethod
    def factory(cls, builder, wdata):
        clsobj = cls(builder, wdata)
        wdata.layout_required = clsobj.layout_required
        return clsobj

    @classmethod
    def add_allowed_parent(cls, builder_uid):
        if cls.allowed_parents is None:
            cls.allowed_parents = (builder_uid,)
        else:
            cls.allowed_parents = cls.allowed_parents + (builder_uid,)

    @classmethod
    def add_allowed_child(cls, builder_uid):
        if cls.allowed_children is None:
            cls.allowed_children = (builder_uid,)
        else:
            cls.allowed_children = cls.allowed_children + (builder_uid,)

    def __init__(self, builder, wmeta):
        super(BuilderObject, self).__init__()
        self.widget = None
        self.builder = builder
        self.wmeta = wmeta
        self._code_identifier = None

    def realize(self, parent, extra_init_args: dict = None):
        args = self._get_init_args(extra_init_args)
        master = parent.get_child_master()
        self.widget = self.class_(master, **args)
        return self.widget

    def _get_init_args(self, extra_init_args: dict = None):
        """Creates dict with properties marked as readonly"""

        args = {}
        for rop in self.ro_properties:
            if rop in self.wmeta.properties:
                pvalue = self._process_property_value(
                    rop, self.wmeta.properties[rop]
                )
                args[rop] = pvalue
        if extra_init_args is not None:
            for key, value in extra_init_args.items():
                args[key] = value
        return args

    def configure(self, target=None):
        if target is None:
            target = self.widget
        for pname, value in self.wmeta.properties.items():
            if (
                pname not in self.ro_properties
                and pname not in self.command_properties
            ):
                self._set_property(target, pname, value)

    def configure_children(self, target=None):
        "Aditional configurations after adding all children."
        pass

    def _process_property_value(self, pname, value):
        propvalue = value
        if pname in self.tkvar_properties:
            propvalue = self.builder.create_variable(value)
            if "text" in self.wmeta.properties and pname == "textvariable":
                propvalue.set(self.wmeta.properties["text"])
            elif "value" in self.wmeta.properties and pname == "variable":
                propvalue.set(self.wmeta.properties["value"])
        elif pname in self.tkimage_properties:
            propvalue = self.builder.get_image(value)
        elif pname == "takefocus":
            if value:
                propvalue = tk.getboolean(value)
        return propvalue

    def _set_property(self, target_widget, pname, value):
        if pname not in self.__class__.properties:
            msg = "Attempt to set an unknown property '%s' on class '%s'"
            logger.warning(msg, pname, repr(self.class_))
        else:
            try:
                logger.debug("processing property %s value", pname)
                propvalue = self._process_property_value(pname, value)
                logger.debug("setting property %s = %s", pname, propvalue)
                target_widget.configure(**{pname: propvalue})
            except Exception as e:
                msg = "Failed to set property '%s' on class '%s'. Error: %s"
                logger.error(msg, pname, repr(self.class_), str(e))
                # logger.exception(e)

    def layout(self, target=None):
        if target is None:
            target = self.widget
        if self.layout_required:
            # Check manager
            manager = self.wmeta.manager
            logger.debug(
                "Applying %s layout to %s", manager, self.wmeta.identifier
            )
            properties = self.wmeta.layout_properties
            if manager == "grid":
                target.grid(**properties)
            elif manager == "pack":
                target.pack(**properties)
            elif manager == "place":
                target.place(**self.wmeta.layout_properties)
            else:
                msg = f"Invalid layout manager: {manager}"
                raise Exception(msg)

        # container layout
        if self.container_layout:
            self._container_layout(
                target,
                self.wmeta.container_manager,
                self.wmeta.container_properties,
            )

    def _container_layout(self, target, container_manager, properties):
        # Do container layout
        propagate = properties.get("propagate", "true")
        propagate = tk.getboolean(propagate)
        anchor = properties.get("anchor", None)

        if container_manager == "grid":
            if anchor:
                target.grid_anchor(anchor)
            if not propagate:
                target.grid_propagate(0)
            self._gridrc_config(target)
        elif container_manager == "pack":
            if not propagate:
                target.pack_propagate(0)
        elif container_manager is None:
            raise Exception("Container Manager is none :(")

    def _gridrc_config(self, target):
        # configure grid row/col properties:
        for type_, num, pname, value in self.wmeta.gridrc_properties:
            if type_ == "row":
                target.rowconfigure(num, **{pname: value})
            else:
                target.columnconfigure(num, **{pname: value})

    def get_child_master(self):
        return self.widget

    def add_child(self, bobject):
        pass

    def _create_callback(self, cmd, command):
        callback = command
        cmd_type = cmd["cbtype"]
        if cmd_type == CB_TYPES.WITH_WID:

            def widget_callback(button_id=self.wmeta.identifier):
                command(button_id)

            callback = widget_callback
        if cmd_type == CB_TYPES.ENTRY_VALIDATE:
            args = cmd["args"]
            if args:
                args = args.split(" ")
                callback = (self.widget.register(command),) + tuple(args)
            else:
                callback = self.widget.register(command)
        return callback

    def _connect_command(self, cmd_pname, callback):
        prop = {cmd_pname: callback}
        self.widget.configure(**prop)

    def connect_commands(self, cmd_bag):
        notconnected = []
        commands = {}
        for cmd_pname in self.command_properties:
            cmd = self.wmeta.properties.get(cmd_pname, None)
            if cmd is not None:
                cmd = json.loads(cmd)
                cmd_name = (cmd["value"]).strip()
                if cmd_name:
                    commands[cmd_pname] = cmd
                else:
                    msg = "%s: invalid value for property '%s'."
                    logger.warning(msg, self.wmeta.identifier, cmd_pname)

        if isinstance(cmd_bag, dict):
            for cmd_pname, cmd in commands.items():
                cmd_name = cmd["value"]
                if cmd_name in cmd_bag:
                    callback = self._create_callback(cmd, cmd_bag[cmd_name])
                    self._connect_command(cmd_pname, callback)
                else:
                    notconnected.append(cmd_name)
        else:
            for cmd_pname, cmd in commands.items():
                cmd_name = cmd["value"]
                if hasattr(cmd_bag, cmd_name):
                    callback = self._create_callback(
                        cmd, getattr(cmd_bag, cmd_name)
                    )
                    self._connect_command(cmd_pname, callback)
                else:
                    notconnected.append(cmd_name)
        if notconnected:
            return notconnected
        else:
            return None

    def _connect_binding(self, sequence: str, callback, add):
        self.widget.bind(sequence, callback, add)

    def connect_bindings(self, cb_bag):
        notconnected = []

        if isinstance(cb_bag, dict):
            for bind in self.wmeta.bindings:
                cb_name = bind.handler
                if cb_name in cb_bag:
                    callback = cb_bag[cb_name]
                    self._connect_binding(bind.sequence, callback, add=bind.add)
                else:
                    notconnected.append(cb_name)
        else:
            for bind in self.wmeta.bindings:
                cb_name = bind.handler
                if hasattr(cb_bag, cb_name):
                    callback = getattr(cb_bag, cb_name)
                    self._connect_binding(bind.sequence, callback, add=bind.add)
                else:
                    notconnected.append(cb_name)
        if notconnected:
            return notconnected
        else:
            return None

    #
    # Code generation methods
    #
    @staticmethod
    def code_escape_str(value: str) -> str:
        return repr(value)

    def _code_get_init_args(self, code_identifier):
        """Creates dict with properties marked as readonly"""
        args = {}
        for rop in self.ro_properties:
            if rop in self.wmeta.properties:
                pvalue = self._code_process_property_value(
                    code_identifier, rop, self.wmeta.properties[rop]
                )
                args[rop] = pvalue
        return args

    def code_realize(self, boparent, code_identifier=None):
        if code_identifier is not None:
            self._code_identifier = code_identifier
        lines = []
        master = boparent.code_child_master()
        init_args = self._code_get_init_args(self.code_identifier())
        bag = []
        for pname, value in init_args.items():
            bag.append(f"{pname}={value}")
        kwargs = ""
        if bag:
            kwargs = f""", {", ".join(bag)}"""
        s = f"{self.code_identifier()} = {self._code_class_name()}({master}{kwargs})"
        lines.append(s)
        return lines

    def code_identifier(self):
        if self._code_identifier is None:
            return self.wmeta.identifier
        return self._code_identifier

    def code_child_master(self):
        return self.code_identifier()

    def code_child_add(self, childid):
        return []

    def code_configure(self, targetid=None):
        if targetid is None:
            targetid = self.code_identifier()
        (
            code_bag,
            kwproperties,
            complex_properties,
        ) = self._code_process_properties(self.wmeta.properties, targetid)
        lines = []
        args_bag = []
        for pname in sorted(kwproperties):
            arg_stmt = f"{pname}={code_bag[pname]}"
            args_bag.append(arg_stmt)
        if args_bag:
            args = ", ".join(args_bag)
            line = f"{targetid}.configure({args})"
            lines.append(line)
        for pname in complex_properties:
            lines.extend(code_bag[pname])

        return lines

    def code_configure_children(self, target=None):
        "Aditional configurations after adding all children."
        return tuple()

    def code_layout(self, targetid=None, parentid=None):
        if targetid is None:
            targetid = self.code_identifier()
        if parentid is None:
            parentid = targetid
        lines = []
        if self.layout_required:
            manager = self.wmeta.manager
            layout = self.wmeta.layout_properties
            args_bag = []
            for p, v in sorted(layout.items()):
                pvalue = self._code_process_layout_property(manager, p, v)
                arg_stmt = f"{p}={pvalue}"
                args_bag.append(arg_stmt)
            args = ", ".join(args_bag)

            line = f"{targetid}.{manager}({args})"
            lines.append(line)

        if self.container_layout:
            manager = self.wmeta.container_manager
            container_prop = self.wmeta.container_properties
            pvalue = str(container_prop.get("propagate", "")).lower()
            if "propagate" in container_prop and pvalue == "false":
                line = f"{targetid}.{manager}_propagate(0)"
                lines.append(line)
            if manager == "grid" and "anchor" in container_prop:
                value = container_prop.get("anchor")
                line = f'{targetid}.{manager}_anchor("{value}")'
                lines.append(line)

            rowbag = defaultdict(list)
            colbag = defaultdict(list)
            for type_, num, pname, value in self.wmeta.gridrc_properties:
                pvalue = self._code_process_layout_property(
                    "grid", pname, value
                )
                arg = f"{pname}={pvalue}"
                if type_ == "row":
                    rowbag[num].append(arg)
                else:
                    colbag[num].append(arg)
            for k, bag in rowbag.items():
                args = ", ".join(bag)
                rowid = f'"{k}"' if k == "all" else k
                line = f"{targetid}.rowconfigure({rowid}, {args})"
                lines.append(line)
            for k, bag in colbag.items():
                args = ", ".join(bag)
                colid = f'"{k}"' if k == "all" else k
                line = f"{targetid}.columnconfigure({colid}, {args})"
                lines.append(line)
        return lines

    def _code_class_name(self):
        cname = None
        # try here ?
        cname = self.builder.code_classname_for(self)
        if cname is None:
            if self.class_ is not None:
                prefix = self.class_.__module__
                name = self.class_.__name__
                cname = f"{prefix}.{name}"
            else:
                cname = "ClassNameNotDefined"
        return cname

    def _code_process_properties(
        self, properties, targetid, skip_ro=True, skip_commands=True
    ):
        code_bag = {}
        for pname, value in properties.items():
            if pname in self.ro_properties and skip_ro:
                continue
            if pname in self.command_properties and skip_commands:
                continue
            self._code_set_property(targetid, pname, value, code_bag)

        # properties
        # determine kw properties or complex properties
        kwproperties = []
        complex_properties = []
        for pname, value in code_bag.items():
            if (
                isinstance(value, str)
                or isinstance(value, bool)
                or isinstance(value, int)
                or isinstance(value, float)
            ):
                kwproperties.append(pname)
            else:
                complex_properties.append(pname)

        return (code_bag, kwproperties, complex_properties)

    def _code_process_property_value(self, targetid, pname, value: str):
        propvalue = None
        if pname in self.tkvar_properties:
            propvalue = self._code_set_tkvariable_property(pname, value)
        elif pname in self.command_properties:
            cmd = json.loads(value)
            propvalue = self._code_define_callback(pname, cmd)
        elif pname in self.tkimage_properties:
            propvalue = self.builder.code_create_image(value)
        elif pname == "takefocus":
            propvalue = str(tk.getboolean(value))
        elif pname in TRANSLATABLE_PROPERTIES:
            propvalue = self.builder.code_translate_str(value)
        # default processing
        if propvalue is None:
            pvalue_str = str(value)
            propvalue = (
                pvalue_str
                if pvalue_str.isnumeric() or isfloat(pvalue_str)
                else f'"{value}"'
            )
        return propvalue

    def _code_set_property(self, targetid, pname, value, code_bag):
        code_bag[pname] = self._code_process_property_value(
            targetid, pname, value
        )

    def _code_set_tkvariable_property(self, pname, value):
        """Create code for tk variable property.
        Can be used from subclases for custom tk variable properties."""
        varvalue = None
        if "text" in self.wmeta.properties and pname == "textvariable":
            varvalue = self.wmeta.properties["text"]
        elif "value" in self.wmeta.properties and pname == "variable":
            varvalue = self.wmeta.properties["value"]
        propvalue = self.builder.code_create_variable(value, varvalue)
        return propvalue

    def code_connect_commands(self):
        commands = {}
        for cmd_pname in self.command_properties:
            cmd = self.wmeta.properties.get(cmd_pname, None)
            if cmd is not None:
                cmd = json.loads(cmd)
                cmd_name = (cmd["value"]).strip()
                if cmd_name:
                    commands[cmd_pname] = cmd
                else:
                    msg = "%s: invalid callback name for property '%s'."
                    logger.warning(msg, self.wmeta.identifier, cmd_pname)
        lines = []
        for cmd_pname, cmd in commands.items():
            callback = self._code_define_callback(cmd_pname, cmd)
            cmd_code = self._code_connect_command(cmd_pname, cmd, callback)
            if cmd_code:
                lines.extend(cmd_code)
        return lines

    def _code_define_callback_args(self, cmd_pname, cmd):
        cmdtype = cmd["cbtype"]
        args = None
        if cmdtype == CB_TYPES.WITH_WID:
            args = ("widget_id",)
        if cmdtype == CB_TYPES.SCALE:
            args = ("scale_value",)
        if cmdtype == CB_TYPES.SCROLLSET:
            args = ("first", "last")
        if cmdtype == CB_TYPES.SCROLL:
            args = ("mode", "value", "units")
        if cmdtype == CB_TYPES.ENTRY_VALIDATE:
            cb_args = cmd["args"]
            if cb_args:
                name_map = {
                    "%d": "d_action",
                    "%i": "i_index",
                    "%P": "p_entry_value",
                    "%s": "s_prev_value",
                    "%S": "s_new_value",
                    "%v": "v_validate",
                    "%V": "v_condition",
                    "%W": "w_entry_name",
                }
                args = []
                for key in cb_args.split():
                    args.append(name_map[key])

        return args

    def _code_define_callback(self, cmd_pname, cmd):
        cmdname = cmd["value"]
        cmdtype = cmd["cbtype"]
        args = self._code_define_callback_args(cmd_pname, cmd)
        wid = self.code_identifier()
        return self.builder.code_create_callback(wid, cmdname, cmdtype, args)

    def _code_connect_command(self, cmd_pname, cmd, cbname):
        target = self.code_identifier()
        args = cmd.get("args", "")
        args = args.split() if args else None
        lines = []
        cmdtype = cmd["cbtype"]
        if args is not None:
            if cmdtype == CB_TYPES.WITH_WID:
                wid = self.wmeta.identifier
                fdef = f'_wcmd = lambda wid="{wid}": {cbname}(wid)'
                cbname = "_wcmd"
                lines.append(fdef)
            if cmdtype == CB_TYPES.ENTRY_VALIDATE:
                original_cb = cbname
                tk_args = [f'"{a}"' for a in args]
                tk_args = ",".join(tk_args)
                fdef = f"_validatecmd = ({target}.register({original_cb}), {tk_args})"
                cbname = "_validatecmd"
                lines.append(fdef)
        line = f"{target}.configure({cmd_pname}={cbname})"
        lines.append(line)
        return lines

    def _code_connect_binding(
        self, target: str, sequence: str, callback: str, add_arg: str
    ):
        return f'{target}.bind("{sequence}", {callback}, add="{add_arg}")'

    def code_connect_bindings(self):
        lines = []
        target = self.code_identifier()
        for bind in self.wmeta.bindings:
            cb_name = self.builder.code_create_callback(
                target, bind.handler, CB_TYPES.BIND_EVENT
            )
            add_arg = "+" if bind.add else ""
            line = self._code_connect_binding(
                target, bind.sequence, cb_name, add_arg
            )
            lines.append(line)
        return lines

    def _code_process_layout_property(
        self, manager: str, pname: str, pvalue: str
    ) -> str:
        pvalue_str = str(pvalue)
        fvalue = (
            pvalue_str
            if pvalue_str.isnumeric() or isfloat(pvalue_str)
            else f'"{pvalue}"'
        )
        return fvalue

    def code_imports(self):
        # will return an iterable of (module, classname/function) to import
        # or None
        return None


#
# Base clases for some widgets
#
class EntryBaseBO(BuilderObject):
    """Base class for tk.Entry and ttk.Entry builder objects"""

    def _set_property(self, target_widget, pname, value):
        if pname == "text":
            wstate = str(target_widget["state"])
            if wstate != "normal":
                # change state temporarily
                target_widget["state"] = "normal"
            target_widget.delete("0", tk.END)
            target_widget.insert("0", value)
            target_widget["state"] = wstate
        else:
            super(EntryBaseBO, self)._set_property(target_widget, pname, value)

    #
    # Code generation methods
    #
    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == "text":
            fval = self.builder.code_translate_str(value)
            lines = [
                f"_text_ = {fval}",
                f'{targetid}.delete("0", "end")',
                f'{targetid}.insert("0", _text_)',
            ]
            if "state" in self.wmeta.properties:
                state_value = self.wmeta.properties["state"]
                if state_value != "normal":
                    lines.insert(1, f'{targetid}["state"] = "normal"')
                    line = f'{targetid}["state"] = "{state_value}"'
                    lines.append(line)
            code_bag[pname] = lines
        else:
            super(EntryBaseBO, self)._code_set_property(
                targetid, pname, value, code_bag
            )


class PanedWindowBO(BuilderObject):
    """Base class for tk.PanedWindow and ttk.Panedwindow builder objects"""

    class_ = None
    container = True
    properties = []
    ro_properties = ("orient",)

    def realize(self, parent, extra_init_args: dict = None):
        master = parent.get_child_master()
        args = self._get_init_args(extra_init_args)
        if "orient" not in args:
            args["orient"] = "vertical"
        self.widget = self.class_(master, **args)
        return self.widget


#
# Base clases for some widget Helpers
#
class PanedWindowPaneBO(BuilderObject):
    class_ = None
    container = True
    properties = []
    layout_required = False
    allow_bindings = False

    def realize(self, parent, extra_init_args: dict = None):
        self.widget = parent.get_child_master()
        return self.widget

    def configure(self):
        pass

    def layout(self):
        pass

    def add_child(self, bobject):
        self.widget.add(bobject.widget, **self.wmeta.properties)

    #
    # code generation functions
    #
    def code_realize(self, boparent, code_identifier=None):
        self._code_identifier = boparent.code_child_master()
        return tuple()

    def code_configure(self, targetid=None):
        return tuple()

    def code_layout(self, targetid=None, parentid=None):
        return tuple()

    def code_child_add(self, childid):
        config = []
        masterid = self.code_child_master()
        for pname, val in self.wmeta.properties.items():
            line = f'{pname}="{val}"'
            config.append(line)
        kw = ""
        lines = []
        if config:
            kw = f""", {", ".join(config)}"""
        line = f"{masterid}.add({childid}{kw})"
        lines.append(line)
        return lines


#
# Base mixin for OptionMenu
#
class OptionMenuBaseMixin:
    def realize(self, parent, extra_init_args: dict = None):
        init_args = self._get_init_args(extra_init_args)
        master = parent.get_child_master()

        # prepare init args
        variable = init_args.pop("variable", None)
        value = init_args.pop("value", None)
        if variable is None:
            varname = "{0}__var".format(self.wmeta.identifier)
            variable = self.builder.create_variable(varname)
        if value is not None:
            variable.set(value)
        values = init_args.pop("values", "")
        if values is not None:
            values = values.split(",")

        class _cb_proxy(object):
            def __init__(self):
                super(_cb_proxy, self).__init__()
                self.callback = None

            def __call__(self, arg1):
                if self.callback is not None:
                    self.callback(arg1)

        cb_proxy = _cb_proxy()

        # tk.OptionMenu and ttk.OptionMenu differ on constructor
        # class so, move code to method than can be overriden

        self.widget = self._create_option_menu(
            master, variable, value, values, cb_proxy
        )
        self.widget._cb_proxy = cb_proxy
        return self.widget

    def _create_option_menu(self, master, variable, value, values, command):
        return self.class_(master, variable, *values, command=command)

    def _connect_command(self, cmd_pname, callback):
        if cmd_pname == "command":
            self.widget._cb_proxy.callback = callback
        else:
            super()._connect_command(cmd_pname, callback)

    #
    # Code generation methods
    #
    def code_realize(self, boparent, code_identifier=None):
        import json

        if code_identifier is not None:
            self._code_identifier = code_identifier
        lines = []
        master = boparent.code_child_master()
        init_args = self._code_get_init_args(self.code_identifier())
        command_arg = None
        variable_arg = None
        # value_arg = None

        # command property
        pname = "command"
        if pname in self.wmeta.properties:
            value = json.loads(self.wmeta.properties[pname])
            cmdname = value["value"]
            cmdtype = value["type"]
            args = ("option",)
            pvalue = self.builder.code_create_callback(
                self.code_identifier(), cmdname, cmdtype, args
            )
            command_arg = f"{pvalue}"

        # Value property
        #
        # Already setup in _code_get_init_args if set by user.
        # But if not:
        var_value = init_args.get("value", None)

        # Variable property
        pname = "variable"
        varname = "__tkvar"
        if pname in init_args:
            varname = init_args[pname]
        else:
            str_val = "" if var_value is None else var_value
            line = f"__tkvar = tk.StringVar(value={str_val})"
            lines.append(line)
        variable_arg = varname

        # values property
        pname = "values"
        om_values = []
        if pname in self.wmeta.properties:
            value = self.wmeta.properties["values"]
            om_values = value.split(",")
        line = f"__values = {om_values}"
        lines.append(line)
        s = self._code_create_optionmenu(
            self.code_identifier(),
            self._code_class_name(),
            master,
            var_value,
            variable_arg,
            command_arg,
        )
        lines.append(s)
        return lines

    def _code_create_optionmenu(
        self,
        identifier,
        classname,
        master,
        value_arg,
        variable_arg,
        command_arg,
    ):
        return f"{identifier} = {classname}({master}, {variable_arg}, *__values, command={command_arg})"

    def code_configure(self, targetid=None):
        return []

    def code_connect_commands(self):
        return []
