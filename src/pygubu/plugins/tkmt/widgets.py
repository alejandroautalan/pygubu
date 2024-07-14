import os
import json
import tkinter as tk
import TKinterModernThemes as tkmt
import TKinterModernThemes.WidgetFrame as tkmt_widgets

from pygubu.i18n import _
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.utils.datatrans import ListDTO
from ..tkmt import _designer_tab_label, _plugin_uid
from .base import (
    TkmtWidgetBO,
    WidgetAsMethodBO,
    CommandProxy,
    GROUP_ROOT,
    GROUP_CONTAINER,
    GROUP_DISPLAY,
    GROUP_INPUT,
)


running_in_designer = os.getenv("PYGUBU_DESIGNER_RUNNING")


class ThemedTKinterFrameBO(TkmtWidgetBO):
    allow_bindings = False
    layout_required = False
    allowed_parents = ("root",)
    class_ = tkmt.ThemedTKinterFrame
    container = True
    pos_args = ("title",)
    kw_args = ("theme", "mode", "usecommandlineargs", "useconfigfile")
    properties = pos_args + kw_args
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {"title": self.wmeta.identifier}


_builder_uid = f"{_plugin_uid}.ThemedTKinterFrame"
_themedtkinterframe = _builder_uid
register_widget(
    _builder_uid,
    ThemedTKinterFrameBO,
    "ThemedTKinterFrame",
    ("ttk", _designer_tab_label),
    GROUP_ROOT,
)


class FrameBO(WidgetAsMethodBO):
    container = True
    master_add_method = "addFrame"
    pos_args = ("name",)
    properties = pos_args + WidgetAsMethodBO.kw_args

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {"name": self.wmeta.identifier}


_builder_uid = f"{_plugin_uid}.Frame"
_frame = _builder_uid
register_widget(
    _builder_uid,
    FrameBO,
    "Frame",
    ("ttk", _designer_tab_label),
    GROUP_CONTAINER,
)

FrameBO.add_allowed_parent(_themedtkinterframe)
FrameBO.add_allowed_parent(_frame)


class LabelFrameBO(WidgetAsMethodBO):
    container = True
    master_add_method = "addLabelFrame"
    pos_args = ("text",)
    properties = pos_args + WidgetAsMethodBO.kw_args
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {"text": self.wmeta.identifier}


_builder_uid = f"{_plugin_uid}.LabelFrame"
_labelframe = _builder_uid
register_widget(
    _builder_uid,
    LabelFrameBO,
    "LabelFrame",
    ("ttk", _designer_tab_label),
    GROUP_CONTAINER,
)

FrameBO.add_allowed_parent(_themedtkinterframe)
FrameBO.add_allowed_parent(_frame)
FrameBO.add_allowed_parent(_labelframe)


class FrameNextColBO(BuilderObject):
    allow_bindings = False
    layout_required = False

    def realize(self, parent, extra_init_args: dict = None):
        self.widget = parent.widget
        master = parent.get_child_master()
        master.nextCol()
        return self.widget

    def code_realize(self, boparent, code_identifier=None):
        lines = []
        master = boparent.code_child_master()
        s = f"{master}.nextCol()"
        lines.append(s)
        return lines


_builder_uid = f"{_plugin_uid}.FrameNextCol"
register_widget(
    _builder_uid,
    FrameNextColBO,
    "Frame.NextCol",
    ("ttk", _designer_tab_label),
    GROUP_CONTAINER,
)

FrameNextColBO.add_allowed_parent(_themedtkinterframe)
FrameNextColBO.add_allowed_parent(_frame)
FrameNextColBO.add_allowed_parent(_labelframe)


class SeparatorBO(WidgetAsMethodBO):
    master_add_method = "Seperator"


_builder_uid = f"{_plugin_uid}.Separator"
register_widget(
    _builder_uid,
    SeparatorBO,
    "Separator",
    ("ttk", _designer_tab_label),
    GROUP_DISPLAY,
)


class ButtonBO(WidgetAsMethodBO):
    master_add_method = "Button"
    pos_args = ("text", "command")
    kw_args = ("args",) + WidgetAsMethodBO.kw_args
    properties = pos_args + kw_args
    ro_properties = properties
    command_properties = ("command",)

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "text": self.wmeta.identifier,
            "command": None,
        }


_builder_uid = f"{_plugin_uid}.Button"
register_widget(
    _builder_uid, ButtonBO, "Button", ("ttk", _designer_tab_label), GROUP_INPUT
)


class AccentButtonBO(ButtonBO):
    master_add_method = "AccentButton"


_builder_uid = f"{_plugin_uid}.AccentButton"
register_widget(
    _builder_uid,
    AccentButtonBO,
    "AccentButton",
    ("ttk", _designer_tab_label),
    GROUP_INPUT,
)


class CheckbuttonBO(WidgetAsMethodBO):
    master_add_method = "Checkbutton"
    pos_args = ("text", "variable")
    kw_args = ("command", "args", "disabled") + WidgetAsMethodBO.kw_args
    properties = pos_args + kw_args
    ro_properties = properties
    command_properties = ("command",)

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "text": self.wmeta.identifier,
            "variable": None,
        }


_builder_uid = f"{_plugin_uid}.Checkbutton"
register_widget(
    _builder_uid,
    CheckbuttonBO,
    "Checkbutton",
    ("ttk", _designer_tab_label),
    GROUP_INPUT,
)


class ToggleButtonBO(CheckbuttonBO):
    master_add_method = "ToggleButton"


_builder_uid = f"{_plugin_uid}.ToggleButton"
register_widget(
    _builder_uid,
    ToggleButtonBO,
    "ToggleButton",
    ("ttk", _designer_tab_label),
    GROUP_INPUT,
)


class SlideSwitchBO(CheckbuttonBO):
    master_add_method = "SlideSwitch"


_builder_uid = f"{_plugin_uid}.SlideSwitch"
register_widget(
    _builder_uid,
    SlideSwitchBO,
    "SlideSwitch",
    ("ttk", _designer_tab_label),
    GROUP_INPUT,
)


class RadiobuttonBO(CheckbuttonBO):
    master_add_method = "Radiobutton"
    pos_args = ("text", "variable", "value")
    properties = pos_args + CheckbuttonBO.kw_args
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "text": self.wmeta.identifier,
            "variable": None,
            "value": 0,
        }


_builder_uid = f"{_plugin_uid}.Radiobutton"
register_widget(
    _builder_uid,
    RadiobuttonBO,
    "Radiobutton",
    ("ttk", _designer_tab_label),
    GROUP_INPUT,
)


class EntryBO(WidgetAsMethodBO):
    master_add_method = "Entry"
    pos_args = ("textvariable",)
    kw_args = (
        "validatecommand",
        "validatecommandargs",
        "validatecommandmode",
        "invalidcommand",
        "invalidcommandargs",
        "validate",
    ) + WidgetAsMethodBO.kw_args
    properties = pos_args + kw_args
    ro_properties = properties
    command_properties = ("validatecommand", "invalidcommand")

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "textvariable": None,
        }


_builder_uid = f"{_plugin_uid}.Entry"
register_widget(
    _builder_uid, EntryBO, "Entry", ("ttk", _designer_tab_label), GROUP_INPUT
)


class NumericalSpinboxBO(WidgetAsMethodBO):
    master_add_method = "NumericalSpinbox"
    pos_args = ("lower", "upper", "increment", "variable")
    properties = pos_args + WidgetAsMethodBO.kw_args
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "lower": 0,
            "upper": 10,
            "increment": 1,
            "variable": None,
        }

    def _process_property_value(self, pname, value):
        if pname in ("lower", "upper", "increment"):
            return float(value)
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.NumericalSpinbox"
register_widget(
    _builder_uid,
    NumericalSpinboxBO,
    "NumericalSpinbox",
    ("ttk", _designer_tab_label),
    GROUP_INPUT,
)


class NonnumericalSpinboxBO(WidgetAsMethodBO):
    master_add_method = "NonnumericalSpinbox"
    pos_args = ("values", "variable")
    properties = pos_args + WidgetAsMethodBO.kw_args
    ro_properties = properties
    json_to_list = ListDTO([], ["values should be a json list"])

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "values": [],
            "variable": None,
        }

    def _process_property_value(self, pname, value):
        if pname == "values":
            return self.json_to_list.transform(value)
        return super()._process_property_value(pname, value)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname == "values":
            return str(self.json_to_list.transform(value))
        return super()._code_process_property_value(targetid, pname, value)


_builder_uid = f"{_plugin_uid}.NonnumericalSpinbox"
register_widget(
    _builder_uid,
    NonnumericalSpinboxBO,
    "NonnumericalSpinbox",
    ("ttk", _designer_tab_label),
    GROUP_INPUT,
)


class TreeviewBO(WidgetAsMethodBO):
    master_add_method = "Treeview"
    pos_args = ("columnnames", "columnwidths", "height", "data", "subentryname")
    kw_args = (
        "datacolumnnames",
        "openkey",
        "anchor",
        "newframe",
    ) + WidgetAsMethodBO.kw_args
    properties = pos_args + kw_args
    ro_properties = properties
    json_to_colname = ListDTO([], ["values should be a json list"])
    json_to_colwidth = ListDTO([], [])

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "columnnames": [],
            "columnwidths": [],
            "height": 5,
            "data": {},
            "subentryname": "",
        }

    def _process_property_value(self, pname, value):
        if pname in ("columnnames", "datacolumnnames"):
            return self.json_to_colname.transform(value)
        if pname == "columnwidths":
            return self.json_to_colwidth.transform(value)
        if pname == "newframe":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname in ("columnnames", "datacolumnnames"):
            return str(self.json_to_colname.transform(value))
        if pname == "columnwidths":
            return str(self.json_to_colwidth.transform(value))
        return super()._code_process_property_value(targetid, pname, value)

    def _post_process_properties(self, tkmaster: tk.Widget, pbag: dict) -> None:
        if running_in_designer:
            self._fix_initargs_in_designer(pbag)

    def _fix_initargs_in_designer(self, kargs: dict) -> None:
        key_names = "columnnames"
        key_widths = "columnwidths"
        key_datacn = "datacolumnnames"

        # Fix names and widths
        if key_names in kargs and key_widths in kargs:
            name_count = len(kargs[key_names])
            width_count = len(kargs[key_widths])

            if width_count > name_count:
                kargs[key_widths] = kargs[key_widths][:name_count]
            if width_count < name_count:
                diff = name_count - width_count
                for i in range(0, diff):
                    kargs[key_widths].append(100)
        elif key_names in kargs and key_widths not in kargs:
            name_count = len(kargs[key_names])
            kargs[key_widths] = []
            for i in range(0, name_count):
                kargs[key_widths].append(100)
        elif key_names not in kargs and key_widths in kargs:
            width_count = len(kargs[key_widths])
            kargs[key_names] = []
            for i in range(0, width_count):
                kargs[key_names].append(f"column {i+1}")

        # fix datacolumnnames if we are in designer editing.
        if key_datacn in kargs:
            name_count = len(kargs[key_names])
            dcn_count = len(kargs[key_datacn])
            if name_count != dcn_count:
                # just clear data names until user enter correct ones
                kargs[key_datacn] = None

        # Fix data if we are in designer and no resource is set.
        key_data = "data"
        if key_data in kargs:
            kargs[key_data] = {}


_builder_uid = f"{_plugin_uid}.Treeview"
register_widget(
    _builder_uid,
    TreeviewBO,
    "Treeview",
    ("ttk", _designer_tab_label),
    GROUP_DISPLAY,
)


class OptionMenuBO(WidgetAsMethodBO):
    master_add_method = "OptionMenu"
    pos_args = ("values", "variable")
    kw_args = ("command", "args") + WidgetAsMethodBO.kw_args
    properties = pos_args + kw_args
    ro_properties = properties
    command_properties = ("command",)
    jlist_values = ListDTO([], ["values should be a json list"])

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "values": ["Test Item"],
            "variable": tk.StringVar(master),
        }

    def _process_property_value(self, pname, value):
        if pname == "values":
            return self.jlist_values.transform(value)
        return super()._process_property_value(pname, value)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname == "values":
            return str(self.jlist_values.transform(value))
        return super()._code_process_property_value(targetid, pname, value)

    def _code_define_callback_args(self, cmd_pname, cmd):
        # arg for command callback
        fargs = ["value"]
        user_args = self.wmeta.properties.get("args", None)
        if user_args:
            user_args = self._process_property_value("args", user_args)
        if user_args:
            for idx, arg in enumerate(user_args):
                fargs.insert(0, f"arg{idx}")
        return fargs


_builder_uid = f"{_plugin_uid}.OptionMenu"
register_widget(
    _builder_uid,
    OptionMenuBO,
    "OptionMenu",
    ("ttk", _designer_tab_label),
    GROUP_INPUT,
)


class ComboboxBO(WidgetAsMethodBO):
    master_add_method = "Combobox"
    pos_args = ("values", "variable")
    properties = pos_args + WidgetAsMethodBO.kw_args
    ro_properties = properties
    jlist_values = ListDTO([], ["values should be a json list"])

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "values": ["Test Item"],
            "variable": tk.StringVar(master),
        }

    def _process_property_value(self, pname, value):
        if pname == "values":
            return self.jlist_values.transform(value)
        return super()._process_property_value(pname, value)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname == "values":
            return str(self.jlist_values.transform(value))
        return super()._code_process_property_value(targetid, pname, value)


_builder_uid = f"{_plugin_uid}.Combobox"
register_widget(
    _builder_uid,
    ComboboxBO,
    "Combobox",
    ("ttk", _designer_tab_label),
    GROUP_INPUT,
)


class MenuButtonBO(WidgetAsMethodBO):
    master_add_method = "MenuButton"
    pos_args = ("menu", "defaulttext")
    properties = pos_args + WidgetAsMethodBO.kw_args
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "menu": None,
            "defaulttext": "MenuButton",
        }


_builder_uid = f"{_plugin_uid}.MenuButton"
register_widget(
    _builder_uid,
    MenuButtonBO,
    "MenuButton",
    ("ttk", _designer_tab_label),
    GROUP_INPUT,
)


class NotebookBO(WidgetAsMethodBO):
    master_add_method = "Notebook"
    pos_args = ("name",)
    properties = pos_args + WidgetAsMethodBO.kw_args
    ro_properties = properties
    container = True

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "name": self.wmeta.identifier,
        }


_builder_uid = f"{_plugin_uid}.Notebook"
_notebook = _builder_uid
register_widget(
    _builder_uid,
    NotebookBO,
    "Notebook",
    ("ttk", _designer_tab_label),
    GROUP_CONTAINER,
)


class NotebookTabBO(WidgetAsMethodBO):
    master_add_method = "addTab"
    pos_args = ("text",)
    kw_args = ()
    properties = pos_args + ("makeResizable",)
    ro_properties = pos_args
    container = True

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "text": self.wmeta.identifier,
        }


_builder_uid = f"{_plugin_uid}.NotebookTab"
_notebok_tab = _builder_uid
register_widget(
    _builder_uid,
    NotebookTabBO,
    "Notebook.Tab",
    ("ttk", _designer_tab_label),
    GROUP_CONTAINER,
)

NotebookBO.add_allowed_child(_notebok_tab)
NotebookTabBO.add_allowed_parent(_notebook)


class PanedWindowBO(WidgetAsMethodBO):
    master_add_method = "PanedWindow"
    pos_args = ("name", "orient")
    properties = pos_args + WidgetAsMethodBO.kw_args
    ro_properties = properties
    container = True

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "name": self.wmeta.identifier,
        }


_builder_uid = f"{_plugin_uid}.PanedWindow"
_panedwindow = _builder_uid
register_widget(
    _builder_uid,
    PanedWindowBO,
    "PanedWindow",
    ("ttk", _designer_tab_label),
    GROUP_CONTAINER,
)


class PanedWindowPaneBO(WidgetAsMethodBO):
    master_add_method = "addWindow"
    pos_args = ("weight",)
    properties = pos_args
    ro_properties = properties
    container = True

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "weight": 1,
        }


_builder_uid = f"{_plugin_uid}.PanedWindowPane"
_panedwindow_pane = _builder_uid
register_widget(
    _builder_uid,
    PanedWindowPaneBO,
    "PanedWindow.Pane",
    ("ttk", _designer_tab_label),
    GROUP_CONTAINER,
)

PanedWindowBO.add_allowed_child(_panedwindow_pane)
PanedWindowPaneBO.add_allowed_parent(_panedwindow)


class BlankBO(WidgetAsMethodBO):
    master_add_method = "Blank"
    pos_args = ("name",)
    kw_args = ("row", "col", "rowspan", "colspan")
    properties = pos_args + kw_args
    ro_properties = properties

    def realize(self, parent, extra_init_args: dict = None):
        super().realize(parent, extra_init_args)
        self.widget = parent.widget
        return self.widget

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "name": "Blank",
        }


_builder_uid = f"{_plugin_uid}.Blank"
register_widget(
    _builder_uid, BlankBO, "Blank", ("ttk", _designer_tab_label), GROUP_DISPLAY
)


class LabelBO(WidgetAsMethodBO):
    master_add_method = "Label"
    pos_args = ("text",)
    properties = pos_args + WidgetAsMethodBO.kw_args
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {"text": self.wmeta.identifier}


_builder_uid = f"{_plugin_uid}.Label"
_labelframe = _builder_uid
register_widget(
    _builder_uid, LabelBO, "Label", ("ttk", _designer_tab_label), GROUP_DISPLAY
)


class TextBO(WidgetAsMethodBO):
    master_add_method = "Text"
    pos_args = ("text",)
    properties = pos_args + WidgetAsMethodBO.kw_args
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {"text": self.wmeta.identifier}


_builder_uid = f"{_plugin_uid}.Text"
_labelframe = _builder_uid
register_widget(
    _builder_uid, TextBO, "Text", ("ttk", _designer_tab_label), GROUP_DISPLAY
)


class ScaleBO(WidgetAsMethodBO):
    master_add_method = "Scale"
    pos_args = ("lower", "upper", "variable")
    properties = pos_args + WidgetAsMethodBO.kw_args
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "lower": 0,
            "upper": 10,
            "variable": None,
        }

    def _process_property_value(self, pname, value):
        if pname in ("lower", "upper"):
            return float(value)
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.Scale"
register_widget(
    _builder_uid, ScaleBO, "Scale", ("ttk", _designer_tab_label), GROUP_INPUT
)


class ProgressbarBO(WidgetAsMethodBO):
    master_add_method = "Progressbar"
    pos_args = ("variable",)
    properties = pos_args + WidgetAsMethodBO.kw_args
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "variable": None,
        }

    def _process_property_value(self, pname, value):
        if pname in ("lower", "upper"):
            return float(value)
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.Progressbar"
register_widget(
    _builder_uid,
    ProgressbarBO,
    "Progressbar",
    ("ttk", _designer_tab_label),
    GROUP_DISPLAY,
)

# TODO: matplotlibFrame
