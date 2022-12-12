# encoding: utf-8
import tkinter as tk
import tkinter.ttk as ttk
from collections import OrderedDict

from pygubu.i18n import _
from pygubu.api.v1 import BuilderObject, register_widget
from pygubu.component.builderobject import (
    EntryBaseBO,
    PanedWindowBO,
    PanedWindowPaneBO,
    OptionMenuBaseMixin,
)


#
# ttk widgets
#
class TTKWidgetBO(BuilderObject):
    OPTIONS_LABEL = (
        "text",
        "textvariable",
        "underline",
        "image",
        "compound",
        "width",
    )
    OPTIONS_COMPATIBILITY = ("state",)
    OPTIONS_STANDARD = ("class_", "cursor", "takefocus", "style")
    OPTIONS_SPECIFIC = tuple()
    OPTIONS_CUSTOM = tuple()
    ro_properties = ("class_",)


class TTKFrame(TTKWidgetBO):
    OPTIONS_SPECIFIC = ("borderwidth", "relief", "padding", "height", "width")
    class_ = ttk.Frame
    container = True
    container_layout = True
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC


register_widget("ttk.Frame", TTKFrame, "Frame", (_("Containers"), "ttk"))


class TTKLabel(TTKWidgetBO):
    OPTIONS_STANDARD = (
        TTKWidgetBO.OPTIONS_STANDARD
        + TTKWidgetBO.OPTIONS_LABEL
        + ("borderwidth",)
    )
    OPTIONS_SPECIFIC = (
        "anchor",
        "background",
        "font",
        "foreground",
        "justify",
        "padding",
        "relief",
        "state",
        "wraplength",
    )
    class_ = ttk.Label
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC


register_widget("ttk.Label", TTKLabel, "Label", (_("Control & Display"), "ttk"))


class TTKButton(TTKWidgetBO):
    OPTIONS_STANDARD = (
        TTKWidgetBO.OPTIONS_STANDARD
        + TTKWidgetBO.OPTIONS_LABEL
        + TTKWidgetBO.OPTIONS_COMPATIBILITY
    )
    OPTIONS_SPECIFIC = ("command", "default")
    class_ = ttk.Button
    container = False
    properties = (
        OPTIONS_STANDARD + OPTIONS_SPECIFIC + TTKWidgetBO.OPTIONS_CUSTOM
    )
    command_properties = ("command",)


register_widget(
    "ttk.Button", TTKButton, "Button", (_("Control & Display"), "ttk")
)


class TTKCheckbutton(TTKWidgetBO):
    OPTIONS_STANDARD = (
        TTKWidgetBO.OPTIONS_STANDARD
        + TTKWidgetBO.OPTIONS_LABEL
        + TTKWidgetBO.OPTIONS_COMPATIBILITY
    )
    OPTIONS_SPECIFIC = ("command", "offvalue", "onvalue", "variable")
    class_ = ttk.Checkbutton
    container = False
    properties = (
        OPTIONS_STANDARD + OPTIONS_SPECIFIC + TTKWidgetBO.OPTIONS_CUSTOM
    )
    command_properties = ("command",)


register_widget(
    "ttk.Checkbutton",
    TTKCheckbutton,
    "Checkbutton",
    (_("Control & Display"), "ttk"),
)


class TTKRadiobutton(TTKWidgetBO):
    OPTIONS_STANDARD = (
        TTKWidgetBO.OPTIONS_STANDARD
        + TTKWidgetBO.OPTIONS_LABEL
        + TTKWidgetBO.OPTIONS_COMPATIBILITY
    )
    OPTIONS_SPECIFIC = ("command", "value", "variable")
    class_ = ttk.Radiobutton
    container = False
    properties = (
        OPTIONS_STANDARD + OPTIONS_SPECIFIC + TTKWidgetBO.OPTIONS_CUSTOM
    )
    ro_properties = ("class_",)
    command_properties = ("command",)


register_widget(
    "ttk.Radiobutton",
    TTKRadiobutton,
    "Radiobutton",
    (_("Control & Display"), "ttk"),
)


class TTKCombobox(TTKWidgetBO):
    OPTIONS_SPECIFIC = (
        "exportselection",
        "justify",
        "height",
        "postcommand",
        "state",
        "textvariable",
        "values",
        "width",
        "validate",
        "validatecommand",
        "invalidcommand",
        "xscrollcommand",
    )
    class_ = ttk.Combobox
    container = False
    properties = (
        TTKWidgetBO.OPTIONS_STANDARD
        + OPTIONS_SPECIFIC
        + TTKWidgetBO.OPTIONS_CUSTOM
    )
    command_properties = (
        "postcommand",
        "validatecommand",
        "invalidcommand",
        "xscrollcommand",
    )
    virtual_events = ("<<ComboboxSelected>>",)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname == "values":
            return self.code_escape_str(value)
        return super()._code_process_property_value(targetid, pname, value)


register_widget(
    "ttk.Combobox", TTKCombobox, "Combobox", (_("Control & Display"), "ttk")
)


class TTKScrollbar(TTKWidgetBO):
    OPTIONS_SPECIFIC = ("command", "orient")
    class_ = ttk.Scrollbar
    container = False
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ("command",)


register_widget(
    "ttk.Scrollbar", TTKScrollbar, "Scrollbar", (_("Control & Display"), "ttk")
)


class TTKSizegrip(TTKWidgetBO):
    class_ = ttk.Sizegrip
    container = False
    properties = TTKWidgetBO.OPTIONS_STANDARD + TTKWidgetBO.OPTIONS_SPECIFIC


register_widget(
    "ttk.Sizegrip", TTKSizegrip, "Sizegrip", (_("Control & Display"), "ttk")
)


class TTKEntry(TTKWidgetBO, EntryBaseBO):
    OPTIONS_STANDARD = TTKWidgetBO.OPTIONS_STANDARD + ("xscrollcommand",)
    OPTIONS_SPECIFIC = (
        "exportselection",
        "font",
        "invalidcommand",
        "justify",
        "show",
        "state",
        "textvariable",
        "validate",
        "validatecommand",
        "width",
    )
    OPTIONS_CUSTOM = ("text",)
    class_ = ttk.Entry
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = ("validatecommand", "invalidcommand", "xscrollcommand")


register_widget("ttk.Entry", TTKEntry, "Entry", (_("Control & Display"), "ttk"))


class TTKProgressbar(TTKWidgetBO):
    OPTIONS_SPECIFIC = (
        "orient",
        "length",
        "mode",
        "maximum",
        "value",
        "variable",
    )  # 'phase' is read-only
    class_ = ttk.Progressbar
    container = False
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC


register_widget(
    "ttk.Progressbar",
    TTKProgressbar,
    "Progressbar",
    (_("Control & Display"), "ttk"),
)


class TTKScale(TTKWidgetBO):
    OPTIONS_SPECIFIC = (
        "command",
        "from_",
        "length",
        "orient",
        "state",
        "to",
        "value",
        "variable",
    )
    class_ = ttk.Scale
    container = False
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC
    command_properties = ("command",)


register_widget("ttk.Scale", TTKScale, "Scale", (_("Control & Display"), "ttk"))


class TTKSeparator(TTKWidgetBO):
    OPTIONS_SPECIFIC = ("orient",)
    class_ = ttk.Separator
    container = False
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC


register_widget(
    "ttk.Separator", TTKSeparator, "Separator", (_("Control & Display"), "ttk")
)


class TTKLabelframe(TTKWidgetBO):
    OPTIONS_STANDARD = TTKFrame.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = TTKFrame.OPTIONS_SPECIFIC + (
        "labelanchor",
        "text",
        "underline",
    )
    class_ = ttk.Labelframe
    container = True
    container_layout = True
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC


register_widget(
    "ttk.Labelframe", TTKLabelframe, "Labelframe", (_("Containers"), "ttk")
)


class TTKPanedwindow(TTKWidgetBO, PanedWindowBO):
    OPTIONS_SPECIFIC = ("orient", "height", "width")
    class_ = ttk.Panedwindow
    allowed_children = ("ttk.Panedwindow.Pane",)
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC
    ro_properties = ("class_", "orient")
    virtual_events = ("<<EnteredChild>>",)


register_widget(
    "ttk.Panedwindow", TTKPanedwindow, "Panedwindow", (_("Containers"), "ttk")
)


class TTKNotebook(TTKWidgetBO):
    OPTIONS_SPECIFIC = ("height", "padding", "width")
    class_ = ttk.Notebook
    container = True
    allowed_children = ("ttk.Notebook.Tab",)
    properties = TTKWidgetBO.OPTIONS_STANDARD + OPTIONS_SPECIFIC
    virtual_events = ("<<NotebookTabChanged>>",)


register_widget(
    "ttk.Notebook", TTKNotebook, "Notebook", (_("Containers"), "ttk")
)


class TTKMenubuttonBO(TTKWidgetBO):
    OPTIONS_STANDARD = (
        TTKWidgetBO.OPTIONS_STANDARD
        + TTKWidgetBO.OPTIONS_LABEL
        + TTKWidgetBO.OPTIONS_COMPATIBILITY
    )
    OPTIONS_SPECIFIC = ("direction",)  # 'menu'
    class_ = ttk.Menubutton
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    allowed_children = ("tk.Menu",)
    maxchildren = 1

    def add_child(self, bobject):
        self.widget.configure(menu=bobject.widget)

    def code_child_add(self, childid):
        lines = [f"{self.code_identifier()}.configure(menu={childid})"]
        return lines


register_widget(
    "ttk.Menubutton",
    TTKMenubuttonBO,
    "Menubutton",
    (
        _("Menu"),
        _("Control & Display"),
        "ttk",
    ),
)


class TTKTreeviewBO(TTKWidgetBO):
    OPTIONS_STANDARD = TTKWidgetBO.OPTIONS_STANDARD + (
        "xscrollcommand",
        "yscrollcommand",
    )
    OPTIONS_SPECIFIC = ("height", "padding", "selectmode", "show")
    class_ = ttk.Treeview
    container = False
    allowed_children = ("ttk.Treeview.Column",)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC
    virtual_events = (
        "<<TreeviewSelect>>",
        "<<TreeviewOpen>>",
        "<<TreeviewClose>>",
    )

    def __init__(self, builder, wdescr):
        super(TTKTreeviewBO, self).__init__(builder, wdescr)
        self._columns = None
        self._headings = None
        self._dcolumns = None

    def configure_children(self):
        self.__configure_columns()

    def __configure_columns(self):
        if self._columns:
            columns = list(self._columns.keys())
            if "#0" in columns:
                columns.remove("#0")
            displaycolumns = self._dcolumns
            self.widget.configure(
                columns=columns, displaycolumns=displaycolumns
            )
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
        if visible and col_id != "#0":
            self._dcolumns.append(col_id)

    def set_heading(self, col_id, attrs):
        if self._headings is None:
            self._headings = OrderedDict()
        self._headings[col_id] = attrs

    #
    # Code generation methods
    #
    def code_configure_children(self, targetid=None):
        if targetid is None:
            targetid = self.code_identifier()
        lines = []
        if self._columns:
            columns = list(self._columns.keys())
            if "#0" in columns:
                columns.remove("#0")
            displaycolumns = self._dcolumns
            line = f"{targetid}_cols = {repr(columns)}"
            lines.append(line)
            line = f"{targetid}_dcols = {repr(displaycolumns)}"
            lines.append(line)
            line = "{0}.configure(columns={0}_cols, displaycolumns={0}_dcols)"
            line = line.format(targetid)
            lines.append(line)
            for col in self._columns:
                code_bag, kwp, _ = self._code_process_properties(
                    self._columns[col], targetid
                )
                bag = []
                for pname in kwp:
                    s = f"{pname}={code_bag[pname]}"
                    bag.append(s)
                kwargs = ",".join(bag)
                line = f'{targetid}.column("{col}", {kwargs})'
                lines.append(line)
        if self._headings:
            for col in self._headings:
                code_bag, kwp, _ = self._code_process_properties(
                    self._headings[col], targetid
                )
                bag = []
                for pname in kwp:
                    s = f"{pname}={code_bag[pname]}"
                    bag.append(s)
                kwargs = ",".join(bag)
                line = f'{targetid}.heading("{col}", {kwargs})'
                lines.append(line)

        return lines


register_widget(
    "ttk.Treeview", TTKTreeviewBO, "Treeview", (_("Control & Display"), "ttk")
)


#
# Helpers for Standard ttk widgets
#


class TTKPanedwindowPane(TTKWidgetBO, PanedWindowPaneBO):
    OPTIONS_STANDARD = tuple()
    OPTIONS_SPECIFIC = ("weight",)
    class_ = None
    container = True
    allowed_parents = ("ttk.Panedwindow",)
    maxchildren = 1
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC


register_widget(
    "ttk.Panedwindow.Pane",
    TTKPanedwindowPane,
    "Panedwindow.Pane",
    (_("Pygubu Helpers"), "ttk"),
)


class TTKNotebookTab(TTKWidgetBO):
    OPTIONS_STANDARD = tuple()
    OPTIONS_SPECIFIC = (
        "state",
        "sticky",
        "padding",
        "text",
        "image",
        "compound",
        "underline",
    )
    class_ = None
    container = True
    layout_required = False
    allow_bindings = False
    allowed_parents = ("ttk.Notebook",)
    maxchildren = 1
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC

    def realize(self, parent, extra_init_args: dict = None):
        self.widget = parent.get_child_master()
        return self.widget

    def configure(self, target=None):
        pass

    def layout(self, target=None):
        pass

    def add_child(self, bobject):
        self.widget.add(bobject.widget, **self.wmeta.properties)

    #
    # Code generation methods
    #
    def code_realize(self, boparent, code_identifier=None):
        self._code_identifier = boparent.code_child_master()
        return tuple()

    def code_configure(self, targetid=None):
        return tuple()

    def code_child_add(self, childid):
        targetid = self.code_identifier()
        code_bag, kw, _ = self._code_process_properties(
            self.wmeta.properties, targetid
        )
        kwbag = []
        for pname in kw:
            arg = f"{pname}={code_bag[pname]}"
            kwbag.append(arg)
        kwargs = ""
        if kwbag:
            kwargs = f", {', '.join(kwbag)}"
        line = f"{targetid}.add({childid}{kwargs})"
        return [line]


register_widget(
    "ttk.Notebook.Tab",
    TTKNotebookTab,
    "Notebook.Tab",
    (_("Pygubu Helpers"), "ttk"),
)


class TTKTreeviewColumnBO(TTKWidgetBO):
    OPTIONS_STANDARD = tuple()
    OPTIONS_SPECIFIC = (
        "text",
        "image",
        "command",
        "heading_anchor",
        "column_anchor",
        "minwidth",
        "stretch",
        "width",
    )
    OPTIONS_CUSTOM = (
        "tree_column",
        "visible",
    )
    class_ = None
    container = False
    layout_required = False
    allow_bindings = False
    allowed_parents = ("ttk.Treeview",)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = ("command",)

    def realize(self, parent, extra_init_args: dict = None):
        self.widget = parent.get_child_master()
        col_props = dict(self.wmeta.properties)  # copy properties
        self._setup_column(parent, col_props)
        return self.widget

    def _get_heading_properties(self, props):
        text = props.pop("text", None)
        if text is None:
            text = self.wmeta.identifier
        hprops = {"anchor": props.pop("heading_anchor", tk.W), "text": text}
        # Only add image if has value. Fix code generation
        imgvalue = props.pop("image", None)
        if imgvalue:
            hprops["image"] = self._process_property_value("image", imgvalue)
        return hprops

    def _get_column_properties(self, props):
        cprops = {
            "anchor": props.pop("column_anchor", ""),
            "stretch": props.pop("stretch", "1"),
            "width": props.pop("width", "200"),
            "minwidth": props.pop("minwidth", "20"),
        }
        return cprops

    def _setup_column(self, parent, col_props):
        tree_column = col_props.pop("tree_column", "false")
        tree_column = tree_column.lower()
        tree_column = True if tree_column == "true" else False
        column_id = "#0" if tree_column else self.wmeta.identifier
        visible = col_props.pop("visible", "true")
        visible = visible.lower()
        is_visible = True if visible == "true" else False

        # configure heading properties
        col_props.pop("command", "")
        hprops = self._get_heading_properties(col_props)
        parent.set_heading(column_id, hprops)

        # configure column properties
        cprops = self._get_column_properties(col_props)
        parent.set_column(column_id, cprops, is_visible)

    def configure(self, target=None):
        pass

    def layout(self, target=None):
        pass

    def _connect_command(self, cpname, callback):
        tree_column = self.wmeta.properties.get("tree_column", "false")
        tree_column = tree_column.lower()
        tree_column = True if tree_column == "true" else False
        column_id = "#0" if tree_column else self.wmeta.identifier
        self.widget.heading(column_id, command=callback)

    #
    # Code generation methods
    #
    def code_realize(self, boparent, code_identifier=None):
        self._code_identifier = boparent.code_child_master()
        col_props = dict(self.wmeta.properties)  # copy properties
        self._setup_column(boparent, col_props)
        return tuple()

    def code_configure(self, targetid=None):
        return tuple()


register_widget(
    "ttk.Treeview.Column",
    TTKTreeviewColumnBO,
    "Treeview.Column",
    (_("Pygubu Helpers"), "ttk"),
)


class TTKSpinboxBO(TTKWidgetBO, EntryBaseBO):
    OPTIONS_STANDARD = TTKEntry.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = TTKEntry.OPTIONS_SPECIFIC + (
        "from_",
        "to",
        "increment",
        "values",
        "wrap",
        "format",
        "command",
    )
    OPTIONS_CUSTOM = TTKEntry.OPTIONS_CUSTOM
    class_ = None
    container = False
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = (
        "validatecommand",
        "invalidcommand",
        "xscrollcommand",
        "command",
    )
    virtual_events = ("<<Increment>>", "<<Decrement>>")


if tk.TkVersion >= 8.6:
    if not hasattr(ttk, "Spinbox"):
        from pygubu.widgets.ttkspinbox import Spinbox

        ttk.Spinbox = Spinbox

    TTKSpinboxBO.class_ = ttk.Spinbox

    register_widget(
        "ttk.Spinbox", TTKSpinboxBO, "Spinbox", (_("Control & Display"), "ttk")
    )


class OptionMenuBO(OptionMenuBaseMixin, BuilderObject):
    class_ = ttk.OptionMenu
    properties = (
        "style",
        "direction",
        "command",
        "variable",
        "value",
        "values",
    )
    command_properties = ("command",)
    ro_properties = ("variable", "value", "values")

    def _create_option_menu(self, master, variable, value, values, command):
        return self.class_(master, variable, value, *values, command=command)

    def _code_create_optionmenu(
        self,
        identifier,
        classname,
        master,
        value_arg,
        variable_arg,
        command_arg,
    ):
        return f"{identifier} = {classname}({master}, {variable_arg}, {value_arg}, *__values, command={command_arg})"


register_widget(
    "ttk.OptionMenu",
    OptionMenuBO,
    "OptionMenu",
    (_("Control & Display"), "ttk"),
)


class LabeledScaleBO(BuilderObject):
    class_ = ttk.LabeledScale
    properties = (
        "compound",
        "variable",
        "from_",
        "to",
    )
    ro_properties = ("compound", "from_", "to", "variable")
    virtual_events = ("<<RangeChanged>>",)

    def _connect_binding(self, sequence: str, callback, add):
        self.widget.scale.bind(sequence, callback, add)

    def _code_connect_binding(
        self, target: str, sequence: str, callback: str, add_arg: str
    ):
        scale = f"{target}.scale"
        return super()._code_connect_binding(scale, sequence, callback, "+")


register_widget(
    "ttk.LabeledScale",
    LabeledScaleBO,
    "LabeledScale",
    (_("Control & Display"), "ttk"),
)
