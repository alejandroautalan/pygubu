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
    properties = ttkw.TTKFrame.properties + ("field_name",)
    ro_properties = ttkw.TTKFrame.ro_properties + ("field_name",)

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
    properties = ttkw.TTKLabel.properties + ("field_name",)
    ro_properties = ttkw.TTKLabel.ro_properties + ("field_name",)


_builder_uid = f"{_plugin_uid}.LabelFieldInfo"
register_widget(
    _builder_uid,
    LabelFieldInfoBO,
    "LabelFieldInfo",
    _designer_tabs,
)


class LabelFieldBO(FieldBOMixin, ttkw.TTKLabel):
    class_ = ttkforms.LabelField
    properties = ttkw.TTKLabel.properties + FieldBOMixin.base_properties
    ro_properties = ttkw.TTKLabel.ro_properties + FieldBOMixin.base_properties


_builder_uid = f"{_plugin_uid}.LabelField"
register_widget(
    _builder_uid,
    LabelFieldBO,
    "LabelField",
    _designer_tabs,
)


class EntryFieldBO(FieldBOMixin, ttkw.TTKEntry):
    class_ = ttkforms.EntryField
    properties = ttkw.TTKEntry.properties + FieldBOMixin.base_properties
    ro_properties = ttkw.TTKEntry.ro_properties + FieldBOMixin.base_properties


_builder_uid = f"{_plugin_uid}.EntryField"
register_widget(
    _builder_uid,
    EntryFieldBO,
    "EntryField",
    _designer_tabs,
)


class CheckbuttonFieldBO(FieldBOMixin, ttkw.TTKCheckbutton):
    class_ = ttkforms.CheckbuttonField
    properties = ttkw.TTKCheckbutton.properties + FieldBOMixin.base_properties
    ro_properties = (
        ttkw.TTKCheckbutton.ro_properties + FieldBOMixin.base_properties
    )


_builder_uid = f"{_plugin_uid}.CheckbuttonField"
register_widget(
    _builder_uid,
    CheckbuttonFieldBO,
    "CheckbuttonField",
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
