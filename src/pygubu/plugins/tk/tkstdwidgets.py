# encoding: utf-8
import logging
import tkinter as tk

from pygubu.i18n import _
from pygubu.api.v1 import BuilderObject, register_widget
from pygubu.component.builderobject import (
    CB_TYPES,
    EntryBaseBO,
    PanedWindowBO,
    PanedWindowPaneBO,
    OptionMenuBaseMixin,
)

logger = logging.getLogger(__name__)

#
# tkinter widgets
#
_toplevel_87 = tuple()
if tk.TkVersion >= 8.7:
    _toplevel_87 = ("backgroundimage", "tile")


class TKToplevel(BuilderObject):
    class_ = tk.Toplevel
    container = True
    layout_required = False
    container_layout = True
    allowed_parents = ("root",)
    # maxchildren = 2  # A menu and a frame
    OPTIONS_STANDARD = (
        "borderwidth",
        "cursor",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "padx",
        "pady",
        "relief",
        "takefocus",
    )
    OPTIONS_SPECIFIC = (
        "background",
        "class_",
        "container",
        "height",
        "width",
    ) + _toplevel_87
    OPTIONS_CUSTOM = (
        "title",
        "geometry",
        "overrideredirect",
        "minsize",
        "maxsize",
        "resizable",
        "iconbitmap",
        "iconphoto",
    )
    ro_properties = ("container",)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    RESIZABLE = {
        "both": (True, True),
        "horizontally": (True, False),
        "vertically": (False, True),
        "none": (False, False),
    }

    def realize(self, parent, extra_init_args: dict = None):
        args = self._get_init_args(extra_init_args)
        master = parent.get_child_master()
        if master is None and tk._default_root is None:
            self.widget = tk.Tk()
        else:
            self.widget = self.class_(master, **args)
        return self.widget

    # def layout(self, target=None):
    # we marked this widget as not allowed to edit layoutu
    #    pass

    def _set_property(self, target_widget, pname, value):
        method_props = ("geometry", "overrideredirect", "title")
        if pname in method_props:
            method = getattr(target_widget, pname)
            method(value)
        elif pname == "resizable" and value:
            target_widget.resizable(*self.RESIZABLE[value])
        elif pname == "maxsize":
            if "|" in value:
                w, h = value.split("|")
                target_widget.maxsize(w, h)
        elif pname == "minsize":
            if "|" in value:
                w, h = value.split("|")
                target_widget.minsize(w, h)
        elif pname == "iconphoto":
            icon = self.builder.get_image(value)
            target_widget.iconphoto(True, icon)
        elif pname == "iconbitmap":
            icon = self.builder.get_iconbitmap(value)
            target_widget.iconbitmap(icon)
        else:
            super(TKToplevel, self)._set_property(target_widget, pname, value)

    #
    # Code generation methods
    #
    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname in ("geometry", "overrideredirect", "title"):
            line = f'{targetid}.{pname}("{value}")'
            code_bag[pname] = (line,)
        elif pname == "resizable":
            p1, p2 = self.RESIZABLE[value]
            line = "{0}.resizable({1}, {2})".format(targetid, p1, p2)
            code_bag[pname] = (line,)
        elif pname in ("maxsize", "minsize"):
            if "|" in value:
                w, h = value.split("|")
                line = "{0}.{1}({2}, {3})".format(targetid, pname, w, h)
                code_bag[pname] = (line,)
        elif pname == "iconbitmap":
            bitmap = self.builder.code_create_iconbitmap(value)
            line = f'{targetid}.iconbitmap("{bitmap}")'
            code_bag[pname] = (line,)
        elif pname == "iconphoto":
            image = self.builder.code_create_image(value)
            line = "{0}.iconphoto(True, {1})".format(targetid, image)
            code_bag[pname] = (line,)
        else:
            super(TKToplevel, self)._code_set_property(
                targetid, pname, value, code_bag
            )


register_widget(
    "tk.Toplevel", TKToplevel, "Toplevel", (_("Containers"), "tk", "ttk")
)


class TKFrame(BuilderObject):
    OPTIONS_STANDARD = (
        "borderwidth",
        "cursor",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "padx",
        "pady",
        "relief",
        "takefocus",
    )
    OPTIONS_SPECIFIC = (
        "background",
        "class_",
        "container",
        "height",
        "width",
    )
    class_ = tk.Frame
    container = True
    container_layout = True
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    ro_properties = ("class_", "container")


register_widget("tk.Frame", TKFrame, "Frame", (_("Containers"), "tk"))


class TKLabel(BuilderObject):
    OPTIONS_STANDARD = (
        "activebackground",
        "activeforeground",
        "anchor",
        "background",
        "bitmap",
        "borderwidth",
        "compound",
        "cursor",
        "disabledforeground",
        "font",
        "foreground",
        "height",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "image",
        "justify",
        "padx",
        "pady",
        "relief",
        "takefocus",
        "text",
        "textvariable",
        "underline",
        "wraplength",
    )
    OPTIONS_SPECIFIC = ("height", "state", "width")
    class_ = tk.Label
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC


register_widget("tk.Label", TKLabel, "Label", (_("Control & Display"), "tk"))


class TKLabelFrame(BuilderObject):
    class_ = tk.LabelFrame
    container = True
    container_layout = True
    OPTIONS_STANDARD = (
        "borderwidth",
        "cursor",
        "font",
        "foreground",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "padx",
        "pady",
        "relief",
        "takefocus",
        "text",
    )
    OPTIONS_SPECIFIC = (
        "background",
        "class_",
        "height",
        "labelanchor",
        "width",
    )
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    ro_properties = ("class_",)


register_widget(
    "tk.LabelFrame", TKLabelFrame, "LabelFrame", (_("Containers"), "tk")
)


class TKEntry(EntryBaseBO):
    OPTIONS_STANDARD = (
        "background",
        "borderwidth",
        "cursor",
        "exportselection",
        "font",
        "foreground",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "insertbackground",
        "insertborderwidth",
        "insertofftime",
        "insertontime",
        "insertwidth",
        "justify",
        "relief",
        "selectbackground",
        "selectborderwidth",
        "selectforeground",
        "takefocus",
        "textvariable",
        "xscrollcommand",
    )
    OPTIONS_SPECIFIC = (
        "disabledbackground",
        "disabledforeground",
        "invalidcommand",
        "readonlybackground",
        "show",
        "state",
        "validate",
        "validatecommand",
        "width",
    )
    OPTIONS_CUSTOM = ("text",)
    class_ = tk.Entry
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = (
        "validatecommand",
        "invalidcommand",
        "xscrollcommand",
    )


register_widget("tk.Entry", TKEntry, "Entry", (_("Control & Display"), "tk"))


class TKButton(BuilderObject):
    class_ = tk.Button
    container = False
    OPTIONS_STANDARD = (
        "activebackground",
        "activeforeground",
        "anchor",
        "background",
        "bitmap",
        "borderwidth",
        "compound",
        "cursor",
        "disabledforeground",
        "font",
        "foreground",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "image",
        "justify",
        "padx",
        "pady",
        "relief",
        "repeatdelay",
        "repeatinterval",
        "takefocus",
        "text",
        "textvariable",
        "underline",
        "wraplength",
    )
    OPTIONS_SPECIFIC = (
        "command",
        "default",
        "height",
        "overrelief",
        "state",
        "width",
    )
    properties = (
        OPTIONS_STANDARD + OPTIONS_SPECIFIC + BuilderObject.OPTIONS_CUSTOM
    )
    command_properties = ("command",)


register_widget("tk.Button", TKButton, "Button", (_("Control & Display"), "tk"))


class TKCheckbutton(BuilderObject):
    class_ = tk.Checkbutton
    container = False
    OPTIONS_STANDARD = (
        "activebackground",
        "activeforeground",
        "anchor",
        "background",
        "bitmap",
        "borderwidth",
        "compound",
        "cursor",
        "disabledforeground",
        "font",
        "foreground",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "image",
        "justify",
        "padx",
        "pady",
        "relief",
        "takefocus",
        "text",
        "textvariable",
        "underline",
        "wraplength",
    )
    OPTIONS_SPECIFIC = (
        "command",
        "height",
        "indicatoron",
        "overrelief",
        "offrelief",
        "offvalue",
        "onvalue",
        "overrelief",
        "selectcolor",
        "selectimage",
        "state",
        "tristateimage",
        "tristatevalue",
        "variable",
        "width",
    )
    properties = (
        OPTIONS_STANDARD + OPTIONS_SPECIFIC + BuilderObject.OPTIONS_CUSTOM
    )
    command_properties = ("command",)


register_widget(
    "tk.Checkbutton",
    TKCheckbutton,
    "Checkbutton",
    (_("Control & Display"), "tk"),
)


class TKRadiobutton(BuilderObject):
    class_ = tk.Radiobutton
    container = False
    OPTIONS_STANDARD = (
        "activebackground",
        "activeforeground",
        "anchor",
        "background",
        "bitmap",
        "borderwidth",
        "compound",
        "cursor",
        "disabledforeground",
        "font",
        "foreground",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "image",
        "justify",
        "padx",
        "pady",
        "relief",
        "takefocus",
        "text",
        "textvariable",
        "underline",
        "wraplength",
    )
    OPTIONS_SPECIFIC = (
        "command",
        "height",
        "indicatoron",
        "overrelief",
        "offrelief",
        "overrelief",
        "selectcolor",
        "selectimage",
        "state",
        "tristateimage",
        "tristatevalue",
        "value",
        "variable",
        "width",
    )
    properties = (
        OPTIONS_STANDARD + OPTIONS_SPECIFIC + BuilderObject.OPTIONS_CUSTOM
    )
    command_properties = ("command",)


register_widget(
    "tk.Radiobutton",
    TKRadiobutton,
    "Radiobutton",
    (_("Control & Display"), "tk"),
)


class TKListbox(BuilderObject):
    class_ = tk.Listbox
    container = False
    OPTIONS_STANDARD = (
        "background",
        "borderwidth",
        "cursor",
        "disabledforeground",
        "exportselection",
        "font",
        "foreground",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "justify",
        "relief",
        "selectbackground",
        "selectborderwidth",
        "selectforeground",
        "setgrid",
        "takefocus",
        "xscrollcommand",
        "yscrollcommand",
    )
    OPTIONS_SPECIFIC = (
        "activestyle",
        "height",
        "listvariable",
        "selectmode",
        "state",
        "width",
    )
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ("xscrollcommand", "yscrollcommand")


register_widget(
    "tk.Listbox", TKListbox, "Listbox", (_("Control & Display"), "tk")
)


class TKText(BuilderObject):
    class_ = tk.Text
    container = False
    OPTIONS_STANDARD = (
        "background",
        "borderwidth",
        "cursor",
        "exportselection",
        "font",
        "foreground",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "insertbackground",
        "insertborderwidth",
        "insertofftime",
        "insertontime",
        "insertwidth",
        "padx",
        "pady",
        "relief",
        "selectbackground",
        "selectborderwidth",
        "selectforeground",
        "setgrid",
        "takefocus",
        "xscrollcommand",
        "yscrollcommand",
    )
    OPTIONS_SPECIFIC = (
        "autoseparators",
        "blockcursor",
        "endline",
        "height",
        "inactiveselectbackground",
        "insertunfocussed",
        "maxundo",
        "spacing1",
        "spacing2",
        "spacing3",
        "startline",
        "state",
        "tabs",
        "tabstyle",
        "undo",
        "width",
        "wrap",
    )
    OPTIONS_CUSTOM = ("text",)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = ("xscrollcommand", "yscrollcommand")

    def _set_property(self, target_widget, pname, value):
        if pname == "text":
            state = target_widget.cget("state")
            if state == tk.DISABLED:
                target_widget.configure(state=tk.NORMAL)
                target_widget.insert("0.0", value)
                target_widget.configure(state=tk.DISABLED)
            else:
                target_widget.insert("0.0", value)
        else:
            super(TKText, self)._set_property(target_widget, pname, value)

    #
    # Code generation methods
    #
    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == "text":
            state_value = ""
            if "state" in self.wmeta.properties:
                state_value = self.wmeta.properties["state"]
            sval = self.builder.code_translate_str(value)
            lines = [
                f"_text_ = {sval}",
            ]
            if state_value == tk.DISABLED:
                lines.extend(
                    (
                        f'{targetid}.configure(state="normal")',
                        f'{targetid}.insert("0.0", _text_)',
                        f'{targetid}.configure(state="disabled")',
                    )
                )
            else:
                lines.append(f'{targetid}.insert("0.0", _text_)')
            code_bag[pname] = lines
        else:
            super(TKText, self)._code_set_property(
                targetid, pname, value, code_bag
            )


register_widget(
    "tk.Text", TKText, "Text", (_("Control & Display"), "tk", "ttk")
)


class TKPanedWindow(PanedWindowBO):
    class_ = tk.PanedWindow
    allowed_children = ("tk.PanedWindow.Pane",)
    OPTIONS_STANDARD = (
        "background",
        "borderwidth",
        "cursor",
        "orient",
        "relief",
    )
    OPTIONS_SPECIFIC = (
        "handlepad",
        "handlesize",
        "height",
        "opaqueresize",
        "proxybackground",
        "proxyborderwidth",
        "proxyrelief",
        "sashcursor",
        "sashpad",
        "sashrelief",
        "sashwidth",
        "showhandle",
        "width",
    )
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC


register_widget(
    "tk.PanedWindow", TKPanedWindow, "PanedWindow", (_("Containers"), "tk")
)


class TKMenubutton(BuilderObject):
    class_ = tk.Menubutton
    container = False
    OPTIONS_STANDARD = (
        "activebackground",
        "activeforeground",
        "anchor",
        "background",
        "bitmap",
        "borderwidth",
        "compound",
        "cursor",
        "disabledforeground",
        "font",
        "foreground",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "image",
        "justify",
        "padx",
        "pady",
        "relief",
        "takefocus",
        "text",
        "textvariable",
        "underline",
        "wraplength",
    )
    OPTIONS_SPECIFIC = (
        "direction",
        "height",
        "indicatoron",
        "state",
        "width",
    )
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    allowed_children = ("tk.Menu",)
    maxchildren = 1

    def add_child(self, bobject):
        self.widget.configure(menu=bobject.widget)

    def code_child_add(self, childid):
        lines = [f"{self.code_identifier()}.configure(menu={childid})"]
        return lines


register_widget(
    "tk.Menubutton",
    TKMenubutton,
    "Menubutton",
    (
        _("Menu"),
        _("Control & Display"),
        "tk",
    ),
)


class TKMessage(BuilderObject):
    class_ = tk.Message
    container = False
    OPTIONS_STANDARD = (
        "anchor",
        "background",
        "borderwidth",
        "cursor",
        "font",
        "foreground",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "padx",
        "pady",
        "relief",
        "takefocus",
        "text",
        "textvariable",
    )
    OPTIONS_SPECIFIC = ("aspect", "justify", "width")
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC


register_widget(
    "tk.Message", TKMessage, "Message", (_("Control & Display"), "tk", "ttk")
)


class TKScale(BuilderObject):
    class_ = tk.Scale
    container = False
    OPTIONS_STANDARD = (
        "activebackground",
        "background",
        "borderwidth",
        "cursor",
        "font",
        "foreground",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "orient",
        "relief",
        "repeatdelay",
        "repeatinterval",
        "takefocus",
        "troughcolor",
    )
    OPTIONS_SPECIFIC = (
        "bigincrement",
        "command",
        "digits",
        "from_",
        "label",
        "length",
        "resolution",
        "showvalue",
        "sliderlength",
        "sliderrelief",
        "state",
        "tickinterval",
        "to",
        "variable",
        "width",
    )
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ("command",)


register_widget("tk.Scale", TKScale, "Scale", (_("Control & Display"), "tk"))


class TKScrollbar(BuilderObject):
    class_ = tk.Scrollbar
    container = False
    OPTIONS_STANDARD = (
        "activebackground",
        "background",
        "borderwidth",
        "cursor",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "jump",
        "orient",
        "relief",
        "repeatdelay",
        "repeatinterval",
        "takefocus",
        "troughcolor",
    )
    OPTIONS_SPECIFIC = (
        "activerelief",
        "command",
        "elementborderwidth",
        "width",
    )
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ("command",)


register_widget(
    "tk.Scrollbar", TKScrollbar, "Scrollbar", (_("Control & Display"), "tk")
)


class TKSpinbox(BuilderObject):
    class_ = tk.Spinbox
    container = False
    OPTIONS_STANDARD = (
        "activebackground",
        "background",
        "borderwidth",
        "cursor",
        "exportselection",
        "font",
        "foreground",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "insertbackground",
        "insertborderwidth",
        "insertofftime",
        "insertontime",
        "insertwidth",
        "justify",
        "relief",
        "repeatdelay",
        "repeatinterval",
        "selectbackground",
        "selectborderwidth",
        "selectforeground",
        "takefocus",
        "textvariable",
        "xscrollcommand",
    )
    OPTIONS_SPECIFIC = (
        "buttonbackground",
        "buttoncursor",
        "buttondownrelief",
        "buttonuprelief",
        "command",
        "disabledbackground",
        "disabledforeground",
        "format",
        "from_",
        "invalidcommand",
        "increment",
        "readonlybackground",
        "state",
        "to",
        "validate",
        "validatecommand",
        "values",
        "width",
        "wrap",
    )
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = (
        "command",
        "invalidcommand",
        "validatecommand",
        "xscrollcommand",
    )

    def _set_property(self, target_widget, pname, value):
        # hack to configure 'from_' and 'to' and avoid exception
        if pname == "from_":
            from_ = float(value)
            to = float(self.wmeta.properties.get("to", 0))
            if from_ > to:
                to = from_ + 1
            target_widget.configure(from_=from_, to=to)
        else:
            super(TKSpinbox, self)._set_property(target_widget, pname, value)


register_widget(
    "tk.Spinbox", TKSpinbox, "Spinbox", (_("Control & Display"), "tk")
)


class TKCanvas(BuilderObject):
    class_ = tk.Canvas
    container = False
    OPTIONS_STANDARD = (
        "background",
        "borderwidth",
        "cursor",
        "highlightbackground",
        "highlightcolor",
        "highlightthickness",
        "insertbackground",
        "insertborderwidth",
        "insertofftime",
        "insertontime",
        "insertwidth",
        "relief",
        "selectbackground",
        "selectborderwidth",
        "selectforeground",
        "takefocus",
        "xscrollcommand",
        "yscrollcommand",
    )
    OPTIONS_SPECIFIC = (
        "closeenough",
        "confine",
        "height",
        "scrollregion",
        "state",
        "width",
        "xscrollincrement",
        "yscrollincrement",
    )
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ("xscrollcommand", "yscrollcommand")


register_widget(
    "tk.Canvas", TKCanvas, "Canvas", (_("Control & Display"), "tk", "ttk")
)


class TKMenu(BuilderObject):
    layout_required = False
    allowed_parents = (
        "root",
        "tk.Menubutton",
        "ttk.Menubutton",
        "pygubu.builder.widgets.toplevelmenu",
    )
    allowed_children = (
        "tk.Menuitem.Submenu",
        "tk.Menuitem.Checkbutton",
        "tk.Menuitem.Command",
        "tk.Menuitem.Radiobutton",
        "tk.Menuitem.Separator",
    )
    class_ = tk.Menu
    container = True
    OPTIONS_STANDARD = (
        "activebackground",
        "activeborderwidth",
        "activeforeground",
        "background",
        "borderwidth",
        "cursor",
        "disabledforeground",
        "font",
        "foreground",
        "relief",
        "takefocus",
    )
    OPTIONS_SPECIFIC = (
        "postcommand",
        "selectcolor",
        "tearoff",
        "tearoffcommand",
        "title",
    )
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ("postcommand", "tearoffcommand")
    allow_bindings = False

    def __init__(self, builder, wdescr):
        super().__init__(builder, wdescr)
        self._menuitems = None

    def layout(self, target=None):
        pass

    #
    # code generation functions
    #
    def add_menuitem(self, itemid, itemtype, properties):
        if self._menuitems is None:
            self._menuitems = []
        self._menuitems.append((itemtype, properties))

    def code_realize(self, boparent, code_identifier=None):
        start = -1
        tearoff_conf = self.wmeta.properties.get("tearoff", "true")
        if tearoff_conf in ("1", "true"):
            start = 0
        self.code_item_index = start
        return super(TKMenu, self).code_realize(boparent, code_identifier)

    def _code_define_callback_args(self, cmd_pname, cmd):
        args = None
        if cmd_pname == "tearoffcommand":
            args = ("menu", "tearoff")
        return args

    def code_configure_children(self, targetid=None):
        if self._menuitems is None:
            return tuple()

        if targetid is None:
            targetid = self.code_identifier()
        lines = []
        for itemtype, kwp in self._menuitems:
            bag = []
            for pname, value in kwp.items():
                s = f"{pname}={value}"
                bag.append(s)
            props = ""
            if bag:
                props = ", " + ", ".join(bag)
            line = f'{targetid}.add("{itemtype}"{props})'
            lines.append(line)
        return lines


register_widget("tk.Menu", TKMenu, "Menu", (_("Menu"), "tk", "ttk"))


#
# Helpers for Standard tk widgets
#


class TKMenuitem(BuilderObject):
    class_ = None
    container = False
    itemtype = None
    layout_required = False
    OPTIONS_STANDARD = (
        "activebackground",
        "activeforeground",
        "background",
        "bitmap",
        "compound",
        "foreground",
        "state",
    )
    OPTIONS_SPECIFIC = (
        "accelerator",
        "columnbreak",
        "command",
        "font",
        "hidemargin",
        "image",
        "label",
        "underline",
    )
    properties = (
        OPTIONS_STANDARD + OPTIONS_SPECIFIC + BuilderObject.OPTIONS_CUSTOM
    )
    command_properties = ("command",)
    allow_bindings = False

    def realize(self, parent, extra_init_args: dict = None):
        self.widget = master = parent.get_child_master()
        itemproperties = dict(self.wmeta.properties)
        self._setup_item_properties(itemproperties)
        master.add(self.itemtype, **itemproperties)
        self._setup_item_index(parent)
        return self.widget

    def _setup_item_index(self, parent):
        master = parent.get_child_master()
        index = master.index(tk.END) or 0
        # TODO: index of items is shifted if tearoff is changed
        # for now check tearoff config and recalculate index.
        has_tearoff = True if master.type(0) == "tearoff" else False
        tearoff_conf = parent.wmeta.properties.get("tearoff", "1")
        offset = 0
        if has_tearoff and tearoff_conf in ("0", "false"):
            offset = 1
        self.__index = index - offset

    def _setup_item_properties(self, itemprops):
        for pname in itemprops:
            if pname == "variable":
                varname = itemprops[pname]
                itemprops[pname] = self.builder.create_variable(varname)
            if pname in ("image", "selectimage"):
                name = itemprops[pname]
                itemprops[pname] = self.builder.get_image(name)

    def configure(self):
        pass

    def layout(self, target=None):
        pass

    def _connect_command(self, cpname, callback):
        self.widget.entryconfigure(self.__index, command=callback)

    #
    # code generation functions
    #
    def code_realize(self, boparent, code_identifier=None):
        self._code_identifier = boparent.code_child_master()
        (
            code_bag,
            kwproperties,
            complex_properties,
        ) = self._code_process_properties(
            self.wmeta.properties, self._code_identifier, skip_commands=False
        )

        properties = {}
        for pname in kwproperties:
            properties[pname] = code_bag[pname]
        boparent.add_menuitem(self.wmeta.identifier, self.itemtype, properties)

        lines = []
        for pname in complex_properties:
            lines.extend(code_bag[pname])
        return lines

    def code_configure(self, targetid=None):
        return tuple()

    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == "command_id_arg":
            # pass, property for command configuration
            pass
        else:
            super(TKMenuitem, self)._code_set_property(
                targetid, pname, value, code_bag
            )

    def _pass_widgetid_to_callback(self):
        include_id = self.wmeta.properties.get(
            "command_id_arg", "false"
        ).lower()
        return include_id == "true"

    def _code_define_callback_args(self, cmd_pname, cmd):
        cmdtype = cmd["cbtype"]
        args = None
        if cmdtype == CB_TYPES.WITH_WID or self._pass_widgetid_to_callback():
            args = ("itemid",)
        return args

    def _code_define_callback(self, cmd_pname, cmd):
        usercb = super()._code_define_callback(cmd_pname, cmd)
        self._realcb = usercb
        args = self._code_define_callback_args(cmd_pname, cmd)
        if args is not None and "itemid" in args:
            usercb = f"{self.wmeta.identifier}_cmd"
        return usercb

    def _code_connect_item_command(self, cmd_pname, cmd, cbname):
        lines = []
        if cbname != self._realcb:
            cbname = self._realcb
            newcb = f"{self.wmeta.identifier}_cmd"
            wid = self.wmeta.identifier
            line = f'def {newcb}(itemid="{wid}"): {cbname}(itemid)'
            lines.append(line)
        return lines

    def _code_connect_command(self, cmd_pname, cmd, cbname):
        if self.itemtype != "submenu":
            return self._code_connect_item_command(cmd_pname, cmd, cbname)
        else:
            return super(TKMenuitem, self)._code_connect_command(
                cmd_pname, cmd, cbname
            )


class TKMenuitemSubmenu(TKMenuitem):
    itemtype = "submenu"
    allowed_parents = ("tk.Menu", "tk.Menuitem.Submenu")
    allowed_children = (
        "tk.Menuitem.Submenu",
        "tk.Menuitem.Checkbutton",
        "tk.Menuitem.Command",
        "tk.Menuitem.Radiobutton",
        "tk.Menuitem.Separator",
    )
    OPTIONS_STANDARD = (
        "activebackground",
        "activeborderwidth",
        "activeforeground",
        "background",
        "borderwidth",
        "bitmap",
        "compound",
        "cursor",
        "disabledforeground",
        "font",
        "foreground",
        "relief",
        "takefocus",
        "state",
    )
    OPTIONS_SPECIFIC = (
        "accelerator",
        "columnbreak",
        "hidemargin",
        "image",
        "label",
        "selectcolor",
        "tearoff",
        "tearoffcommand",
        "underline",
        "postcommand",
    )
    OPTIONS_CUSTOM = ("specialmenu",)
    properties = tuple(
        set(OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM)
    )
    # ro_properties = ('specialmenu', )
    command_properties = ("postcommand", "tearoffcommand")

    def __init__(self, builder, wdescr):
        super().__init__(builder, wdescr)
        self._menuitems = None

    def realize(self, parent, extra_init_args: dict = None):
        master = parent.get_child_master()
        self._setup_item_index(parent)

        menu_properties = dict(
            (k, v)
            for k, v in self.wmeta.properties.items()
            if k in TKMenu.properties or k == "specialmenu"
        )
        self._setup_item_properties(menu_properties)

        item_properties = dict(
            (k, v)
            for k, v in self.wmeta.properties.items()
            if k in TKMenuitem.properties
        )
        self._setup_item_properties(item_properties)

        self.widget = submenu = TKMenu.class_(master, **menu_properties)
        item_properties["menu"] = submenu
        master.add(tk.CASCADE, **item_properties)
        return self.widget

    def _setup_item_properties(self, itemprops):
        super(TKMenuitemSubmenu, self)._setup_item_properties(itemprops)
        pname = "specialmenu"
        if pname in itemprops:
            specialmenu = itemprops.pop(pname)
            itemprops["name"] = specialmenu

    def configure(self):
        pass

    def layout(self, target=None):
        pass

    def _connect_command(self, cpname, callback):
        # suported commands: tearoffcommand, postcommand
        kwargs = {cpname: callback}
        self.widget.configure(**kwargs)

    #
    # code generation functions
    #
    def add_menuitem(self, itemid, itemtype, properties):
        if self._menuitems is None:
            self._menuitems = []
        self._menuitems.append((itemtype, properties))

    def code_realize(self, boparent, code_identifier=None):
        self._code_identifier = code_identifier
        masterid = boparent.code_child_master()
        lines = []
        # menu properties
        menuprop = {}
        for pname, value in self.wmeta.properties.items():
            if pname in TKMenu.properties:
                menuprop[pname] = value
            if pname == "specialmenu":
                menuprop["name"] = value

        (
            code_bag,
            kw_properties,
            complex_properties,
        ) = self._code_process_properties(menuprop, self.code_identifier())
        for pname in complex_properties:
            lines.extend(code_bag[pname])

        mpbag = []
        for pname in kw_properties:
            line = "{0}={1}".format(pname, code_bag[pname])
            mpbag.append(line)
        mprops = ""
        if mpbag:
            mprops = ", " + ", ".join(mpbag)

        # item properties
        itemprop = {}
        for pname, value in self.wmeta.properties.items():
            if pname in TKMenuitem.properties:
                itemprop[pname] = value

        (
            code_bag,
            kw_properties,
            complex_properties,
        ) = self._code_process_properties(itemprop, self.code_identifier())
        for pname in complex_properties:
            lines.extend(code_bag[pname])

        pbag = []
        prop = "menu={0}".format(self.code_identifier())
        pbag.append(prop)
        for pname in kw_properties:
            line = "{0}={1}".format(pname, code_bag[pname])
            pbag.append(line)
        props = ""
        if pbag:
            props = ", {0}".format(", ".join(pbag))

        # creation
        line = "{0} = tk.Menu({1}{2})".format(
            self.code_identifier(), masterid, mprops
        )
        lines.append(line)
        line = "{0}.add(tk.CASCADE{1})".format(masterid, props)
        lines.append(line)

        return lines

    def code_configure(self, targetid=None):
        return tuple()

    def code_configure_children(self, targetid=None):
        if self._menuitems is None:
            return tuple()

        if targetid is None:
            targetid = self.code_identifier()
        lines = []
        for itemtype, kwp in self._menuitems:
            bag = []
            for pname, value in kwp.items():
                s = f"{pname}={value}"
                bag.append(s)
            props = ""
            if bag:
                props = ", " + ", ".join(bag)
            line = f'{targetid}.add("{itemtype}"{props})'
            lines.append(line)
        return lines

    def _code_define_callback_args(self, cmd_pname, cmd):
        args = None
        if cmd_pname == "tearoffcommand":
            args = ("menu", "tearoff")
        return args


register_widget(
    "tk.Menuitem.Submenu",
    TKMenuitemSubmenu,
    "Menuitem.Submenu",
    (_("Menu"), "tk", "ttk"),
)


class TKMenuitemCommand(TKMenuitem):
    allowed_parents = ("tk.Menu", "tk.Menuitem.Submenu")
    itemtype = tk.COMMAND


register_widget(
    "tk.Menuitem.Command",
    TKMenuitemCommand,
    "Menuitem.Command",
    (_("Menu"), "tk", "ttk"),
)


class TKMenuitemCheckbutton(TKMenuitem):
    allowed_parents = ("tk.Menu", "tk.Menuitem.Submenu")
    itemtype = tk.CHECKBUTTON
    OPTIONS_STANDARD = TKMenuitem.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = TKMenuitem.OPTIONS_SPECIFIC + (
        "indicatoron",
        "onvalue",
        "offvalue",
        "selectcolor",
        "selectimage",
        "variable",
    )
    OPTIONS_CUSTOM = TKMenuitem.OPTIONS_CUSTOM
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM


register_widget(
    "tk.Menuitem.Checkbutton",
    TKMenuitemCheckbutton,
    "Menuitem.Checkbutton",
    (_("Menu"), "tk", "ttk"),
)


class TKMenuitemRadiobutton(TKMenuitem):
    allowed_parents = ("tk.Menu", "tk.Menuitem.Submenu")
    itemtype = tk.RADIOBUTTON
    OPTIONS_STANDARD = TKMenuitem.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = TKMenuitem.OPTIONS_SPECIFIC + (
        "indicatoron",
        "selectcolor",
        "selectimage",
        "value",
        "variable",
    )
    OPTIONS_CUSTOM = TKMenuitem.OPTIONS_CUSTOM
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM


register_widget(
    "tk.Menuitem.Radiobutton",
    TKMenuitemRadiobutton,
    "Menuitem.Radiobutton",
    (_("Menu"), "tk", "ttk"),
)


class TKMenuitemSeparator(TKMenuitem):
    allowed_parents = ("tk.Menu", "tk.Menuitem.Submenu")
    itemtype = tk.SEPARATOR
    OPTIONS_STANDARD = ("background",)
    OPTIONS_SPECIFIC = tuple()
    OPTIONS_CUSTOM = tuple()
    properties = tuple()
    command_properties = tuple()


register_widget(
    "tk.Menuitem.Separator",
    TKMenuitemSeparator,
    "Menuitem.Separator",
    (_("Menu"), "tk", "ttk"),
)


class TKPanedWindowPane(PanedWindowPaneBO):
    class_ = None
    container = True
    allowed_parents = ("tk.PanedWindow",)
    maxchildren = 1
    OPTIONS_SPECIFIC = (
        "height",
        "hide",
        "minsize",
        "padx",
        "pady",
        "sticky",
        "stretch",
        "width",
    )
    properties = OPTIONS_SPECIFIC


register_widget(
    "tk.PanedWindow.Pane",
    TKPanedWindowPane,
    "PanedWindow.Pane",
    (_("Pygubu Helpers"), "tk"),
)


class TKLabelwidgetBO(BuilderObject):
    class_ = None
    container = True
    allowed_parents = ("tk.LabelFrame", "ttk.Labelframe")
    maxchildren = 1
    layout_required = False
    allow_bindings = False

    def realize(self, parent, extra_init_args: dict = None):
        self.widget = parent.get_child_master()
        return self.widget

    def add_child(self, bobject):
        self.widget.configure(labelwidget=bobject.widget)

    def layout(self, target=None):
        pass

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
        line = "{0}.configure(labelwidget={1})"
        line = line.format(self.code_child_master(), childid)
        return (line,)


register_widget(
    "pygubu.builder.widgets.Labelwidget",
    TKLabelwidgetBO,
    "Labelwidget",
    (_("Pygubu Helpers"), "tk", "ttk"),
)


class ToplevelMenuHelperBO(BuilderObject):
    class_ = None
    container = True
    allowed_parents = ("tk.Toplevel",)
    maxchildren = 1
    layout_required = False
    allow_bindings = False

    def realize(self, parent, extra_init_args: dict = None):
        self.widget = parent.get_child_master()
        return self.widget

    def add_child(self, bobject):
        self.widget.configure(menu=bobject.widget)

    def layout(self, target=None):
        pass

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
        line = "{0}.configure(menu={1})"
        line = line.format(self.code_child_master(), childid)
        return (line,)


register_widget(
    "pygubu.builder.widgets.toplevelmenu",
    ToplevelMenuHelperBO,
    "ToplevelMenu",
    (_("Menu"), _("Pygubu Helpers"), "tk", "ttk"),
)


class TKOptionMenu(OptionMenuBaseMixin, BuilderObject):
    class_ = tk.OptionMenu
    properties = ("command", "variable", "value", "values")
    command_properties = ("command",)
    ro_properties = ("variable", "value", "values")


register_widget(
    "tk.OptionMenu",
    TKOptionMenu,
    "OptionMenu",
    (_("Control & Display"), "tk"),
)
