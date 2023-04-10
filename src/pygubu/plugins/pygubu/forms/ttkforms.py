import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
import pygubu.forms.ttkforms as ttkforms
import pygubu.plugins.tk.tkstdwidgets as tkw
import pygubu.plugins.ttk.ttkstdwidgets as ttkw
from pygubu.i18n import _
from pygubu.utils.datatrans import ListDTO
from pygubu.forms.fields import FieldBase
from .base import FieldBOMixin


_plugin_uid = "pygubu.forms.ttk"
_designer_tabs = ("ttk", _("Pygubu Forms"))
_list_dto = ListDTO()


class FrameFormBO(FieldBOMixin, ttkw.TTKFrame):
    class_ = ttkforms.FrameForm
    properties = ttkw.TTKFrame.properties + ("fname",)
    ro_properties = ttkw.TTKFrame.ro_properties + ("fname",)

    def add_child(self, bobject):
        if issubclass(bobject.class_, FieldBase):
            self.widget.add_field(bobject.widget)


_builder_uid = f"{_plugin_uid}.FrameForm"
register_widget(
    _builder_uid,
    FrameFormBO,
    "Form",
    _designer_tabs,
)


class LabelFieldInfoBO(FieldBOMixin, ttkw.TTKLabel):
    class_ = ttkforms.LabelFieldInfo
    properties = ttkw.TTKLabel.properties + ("fname",)
    ro_properties = ttkw.TTKLabel.ro_properties + ("fname",)


_builder_uid = f"{_plugin_uid}.LabelFieldInfo"
register_widget(
    _builder_uid,
    LabelFieldInfoBO,
    "LabelFieldInfo",
    _designer_tabs,
)


class LabelDisplayFieldBO(FieldBOMixin, ttkw.TTKLabel):
    class_ = ttkforms.LabelDisplayField
    properties = ttkw.TTKLabel.properties + ("fname",)
    ro_properties = ttkw.TTKLabel.ro_properties + ("fname",)


_builder_uid = f"{_plugin_uid}.LabelDisplayField"
register_widget(
    _builder_uid,
    LabelDisplayFieldBO,
    "LabelDisplayField",
    _designer_tabs,
)


_entry_charfield_props = (
    "class_",
    "cursor",
    "takefocus",
    "style",
    "exportselection",
    "font",
    "justify",
    "show",
    "state",
    "textvariable",
    "validate",
    "width",
)

_char_field_props = (
    "max_length",
    "min_length",
    "strip",
    "empty_value",
)


class EntryCharFieldBO(FieldBOMixin, ttkw.TTKEntry):
    class_ = ttkforms.EntryCharField
    properties = (
        _entry_charfield_props
        + _char_field_props
        + FieldBOMixin.base_properties
    )
    ro_properties = _entry_charfield_props + FieldBOMixin.base_properties

    def _process_property_value(self, pname, value):
        if pname == "strip":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.EntryCharField"
register_widget(
    _builder_uid,
    EntryCharFieldBO,
    "EntryCharField",
    _designer_tabs,
)


class TextCharFieldBO(FieldBOMixin, tkw.TKText):
    class_ = ttkforms.TextCharField
    properties = (
        tkw.TKText.properties + _char_field_props + FieldBOMixin.base_properties
    )
    ro_properties = _entry_charfield_props + FieldBOMixin.base_properties

    def _process_property_value(self, pname, value):
        if pname == "strip":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.TextCharField"
register_widget(
    _builder_uid,
    TextCharFieldBO,
    "TextCharField",
    _designer_tabs,
)


class EntryIntegerFieldBO(FieldBOMixin, ttkw.TTKEntry):
    class_ = ttkforms.EntryIntegerField
    _field_props = (
        "max_value",
        "min_value",
        "step_size",
    )
    properties = (
        _entry_charfield_props + _field_props + FieldBOMixin.base_properties
    )
    ro_properties = _field_props + FieldBOMixin.base_properties


_builder_uid = f"{_plugin_uid}.EntryIntegerField"
register_widget(
    _builder_uid,
    EntryIntegerFieldBO,
    "EntryIntegerField",
    _designer_tabs,
)


class EntryFloatFieldBO(EntryIntegerFieldBO):
    class_ = ttkforms.EntryFloatField


_builder_uid = f"{_plugin_uid}.EntryFloatField"
register_widget(
    _builder_uid,
    EntryFloatFieldBO,
    "EntryFloatField",
    _designer_tabs,
)


class CheckbuttonBoolFieldBO(FieldBOMixin, ttkw.TTKCheckbutton):
    class_ = ttkforms.CheckbuttonBoolField


_builder_uid = f"{_plugin_uid}.CheckbuttonBoolField"
register_widget(
    _builder_uid,
    CheckbuttonBoolFieldBO,
    "CheckbuttonBoolField",
    _designer_tabs,
)
