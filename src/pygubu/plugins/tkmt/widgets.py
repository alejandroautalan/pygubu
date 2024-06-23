import os
import json
import tkinter as tk
import TKinterModernThemes as tkmt

from pygubu.i18n import _
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.utils.datatrans import ListDTO
from ..tkmt import _designer_tab_label, _plugin_uid


running_in_designer = os.getenv("PYGUBU_DESIGNER_RUNNING")


class ThemedTkFrameBO(BuilderObject):
    allow_bindings = False
    layout_required = False
    allowed_parents = ("root",)
    class_ = tkmt.ThemedTKinterFrame
    container = True
    properties = ("title", "theme", "mode")
    ro_properties = properties

    def realize(self, parent, extra_init_args: dict = None):
        kargs = self._get_init_args(extra_init_args)
        # master = parent.get_child_master()
        args = []
        for arg in ("title",):
            args.append(kargs.pop(arg))
        self.widget = self.class_(*args, **kargs)
        return self.widget


_builder_uid = f"{_plugin_uid}.ThemedTKinterFrame"
_themedtkinterframe = _builder_uid
register_widget(
    _builder_uid,
    ThemedTkFrameBO,
    "ThemedTKinterFrame",
    ("ttk", _designer_tab_label),
)

register_custom_property(
    _builder_uid,
    "theme",
    "choice",
    values=("azure", "sun-valley", "park"),
    default_value="park",
    state="readonly",
)

register_custom_property(
    _builder_uid,
    "mode",
    "choice",
    values=("light", "dark"),
    default_value="dark",
    state="readonly",
)


class TkmtWidgetBO(BuilderObject):
    allow_bindings = False
    layout_required = False
    properties = ("row", "col", "padx", "pady", "rowspan", "colspan", "sticky")
    ro_properties = properties
    pos_args = tuple()
    master_add_method = None

    def realize(self, parent, extra_init_args: dict = None):
        master = parent.get_child_master()
        assert self.master_add_method is not None
        add_method = getattr(master, self.master_add_method)
        pbag = self._process_properties(parent.widget)
        kargs = self._get_keyword_args(pbag)
        args = self._get_positional_args(pbag)
        self.widget = add_method(*args, **kargs)
        return self.widget

    def configure(self, target=None):
        pass

    def _process_properties(self, tkmaster: tk.Widget) -> dict:
        defaults = self._get_property_defaults(tkmaster)
        pbag = {}
        for pname in self.properties:
            if pname in self.wmeta.properties:
                pvalue = self.wmeta.properties[pname]
                pbag[pname] = self._process_property_value(pname, pvalue)
            elif pname in defaults:
                pbag[pname] = defaults[pname]
        self._post_process_properties(tkmaster, pbag)
        return pbag

    def _post_process_properties(self, tkmaster: tk.Widget, pbag: dict) -> None:
        pass

    def _get_keyword_args(self, bag: dict) -> dict:
        kargs = {}
        for pname in self.properties:
            if pname not in self.pos_args and pname in bag:
                kargs[pname] = bag[pname]
        return kargs

    def _get_positional_args(self, bag: dict) -> list:
        args = []
        for pname in self.pos_args:
            if pname in bag:
                value = bag[pname]
                args.append(value)
        return args

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {}

    def _process_property_value(self, pname, value):
        if pname in ("row", "col", "rowspan", "colspan"):
            return int(value)
        return super()._process_property_value(pname, value)


class FrameBO(TkmtWidgetBO):
    container = True
    master_add_method = "addFrame"
    pos_args = ("name",)
    properties = pos_args + TkmtWidgetBO.properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {"name": self.wmeta.identifier}


_builder_uid = f"{_plugin_uid}.Frame"
_frame = _builder_uid
register_widget(_builder_uid, FrameBO, "Frame", ("ttk", _designer_tab_label))

FrameBO.add_allowed_parent(_themedtkinterframe)
FrameBO.add_allowed_parent(_frame)


class LabelFrameBO(TkmtWidgetBO):
    container = True
    master_add_method = "addLabelFrame"
    properties = ("text",) + TkmtWidgetBO.properties
    ro_properties = properties
    pos_args = ("text",)

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {"text": self.wmeta.identifier}


_builder_uid = f"{_plugin_uid}.LabelFrame"
_labelframe = _builder_uid
register_widget(
    _builder_uid, LabelFrameBO, "LabelFrame", ("ttk", _designer_tab_label)
)

FrameBO.add_allowed_parent(_themedtkinterframe)
FrameBO.add_allowed_parent(_frame)
FrameBO.add_allowed_parent(_labelframe)


class SeparatorBO(TkmtWidgetBO):
    master_add_method = "Seperator"


_builder_uid = f"{_plugin_uid}.Separator"
register_widget(
    _builder_uid, SeparatorBO, "Separator", ("ttk", _designer_tab_label)
)


class ButtonBO(TkmtWidgetBO):
    master_add_method = "Button"
    pos_args = ("text", "command")
    properties = pos_args + TkmtWidgetBO.properties
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "text": self.wmeta.identifier,
            "command": None,
        }


_builder_uid = f"{_plugin_uid}.Button"
register_widget(_builder_uid, ButtonBO, "Button", ("ttk", _designer_tab_label))


class AccentButtonBO(ButtonBO):
    master_add_method = "AccentButton"


_builder_uid = f"{_plugin_uid}.AccentButton"
register_widget(
    _builder_uid, AccentButtonBO, "AccentButton", ("ttk", _designer_tab_label)
)


class CheckbuttonBO(TkmtWidgetBO):
    master_add_method = "Checkbutton"
    pos_args = ("text", "variable")
    properties = pos_args + TkmtWidgetBO.properties
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "text": self.wmeta.identifier,
            "variable": None,
        }


_builder_uid = f"{_plugin_uid}.Checkbutton"
register_widget(
    _builder_uid, CheckbuttonBO, "Checkbutton", ("ttk", _designer_tab_label)
)


class ToggleButtonBO(CheckbuttonBO):
    master_add_method = "ToggleButton"


_builder_uid = f"{_plugin_uid}.ToggleButton"
register_widget(
    _builder_uid, ToggleButtonBO, "ToggleButton", ("ttk", _designer_tab_label)
)


class SlideSwitchBO(CheckbuttonBO):
    master_add_method = "SlideSwitch"


_builder_uid = f"{_plugin_uid}.SlideSwitch"
register_widget(
    _builder_uid, SlideSwitchBO, "SlideSwitch", ("ttk", _designer_tab_label)
)


class RadiobuttonBO(CheckbuttonBO):
    master_add_method = "Radiobutton"
    pos_args = ("text", "variable", "value")
    properties = pos_args + TkmtWidgetBO.properties
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "text": self.wmeta.identifier,
            "variable": None,
            "value": 0,
        }


_builder_uid = f"{_plugin_uid}.Radiobutton"
register_widget(
    _builder_uid, RadiobuttonBO, "Radiobutton", ("ttk", _designer_tab_label)
)


class EntryBO(TkmtWidgetBO):
    master_add_method = "Entry"
    pos_args = ("textvariable",)
    properties = pos_args + TkmtWidgetBO.properties
    ro_properties = properties

    def _get_property_defaults(self, master: tk.Widget = None) -> dict:
        return {
            "textvariable": None,
        }


_builder_uid = f"{_plugin_uid}.Entry"
register_widget(_builder_uid, EntryBO, "Entry", ("ttk", _designer_tab_label))


class NumericalSpinboxBO(TkmtWidgetBO):
    master_add_method = "NumericalSpinbox"
    pos_args = ("lower", "upper", "increment", "variable")
    properties = pos_args + TkmtWidgetBO.properties
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
)


class NonnumericalSpinboxBO(TkmtWidgetBO):
    master_add_method = "NonnumericalSpinbox"
    pos_args = ("values", "variable")
    properties = pos_args + TkmtWidgetBO.properties
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


_builder_uid = f"{_plugin_uid}.NonnumericalSpinbox"
register_widget(
    _builder_uid,
    NonnumericalSpinboxBO,
    "NonnumericalSpinbox",
    ("ttk", _designer_tab_label),
)


class TreeviewBO(TkmtWidgetBO):
    master_add_method = "Treeview"
    pos_args = ("columnnames", "columnwidths", "height", "data", "subentryname")
    kw_args = ("datacolumnnames",)
    properties = pos_args + kw_args + TkmtWidgetBO.properties
    ro_properties = pos_args + TkmtWidgetBO.properties
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
        print(kargs[key_names], kargs[key_datacn])
        # Fix data if we are in designer and no resource is set.
        key_data = "data"
        if key_data in kargs and kargs[key_data] is None:
            kargs[key_data] = {}

    def _process_property_value(self, pname, value):
        if pname in ("columnnames", "datacolumnnames"):
            return self.json_to_colname.transform(value)
        if pname == "columnwidths":
            return self.json_to_colwidth.transform(value)
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.Treeview"
register_widget(
    _builder_uid,
    TreeviewBO,
    "Treeview",
    ("ttk", _designer_tab_label),
)


class OptionMenuBO(TkmtWidgetBO):
    master_add_method = "OptionMenu"
    pos_args = ("values", "variable")
    properties = pos_args + TkmtWidgetBO.properties
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


_builder_uid = f"{_plugin_uid}.OptionMenu"
register_widget(
    _builder_uid, OptionMenuBO, "OptionMenu", ("ttk", _designer_tab_label)
)
