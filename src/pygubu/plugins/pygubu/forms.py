import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
import pygubu.forms.ttkfields as ttkfields
import pygubu.plugins.ttk.ttkstdwidgets as ttkw
from pygubu.i18n import _
from pygubu.utils.datatrans import ListDTO
from pygubu.forms.fields import Field


_plugin_uid = "pygubu.forms"
_designer_tabs = ("ttk", _("Pygubu-Forms"))
_list_dto = ListDTO()


class FieldMixin:
    """Manages base field properties."""

    base_properties = ("fname", "initial", "required", "help_text")

    def _get_init_args(self, extra_init_args: dict = None):
        args = super()._get_init_args(extra_init_args)
        name = args.get("fname", None)
        if not name:
            args["fname"] = self.wmeta.identifier
        return args

    def _process_property_value(self, pname, value):
        if pname == "required":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)


class FormBO(FieldMixin, ttkw.TTKFrame):
    class_ = ttkfields.Form
    properties = ttkw.TTKFrame.properties + ("fname",)
    ro_properties = ttkw.TTKFrame.ro_properties + ("fname",)

    def add_child(self, bobject):
        if issubclass(bobject.class_, Field):
            self.widget.add_field(bobject.widget)
            print(f"Field {bobject.widget.fname} added")


_builder_uid = f"{_plugin_uid}.Form"
register_widget(
    _builder_uid,
    FormBO,
    "Form",
    _designer_tabs,
)


class LabelFieldBO(FieldMixin, ttkw.TTKLabel):
    class_ = ttkfields.LabelField
    properties = ttkw.TTKLabel.properties + ("fname",)
    ro_properties = ttkw.TTKLabel.ro_properties + ("fname",)


_builder_uid = f"{_plugin_uid}.LabelField"
register_widget(
    _builder_uid,
    LabelFieldBO,
    "LabelField",
    _designer_tabs,
)


class CharFieldBO(FieldMixin, ttkw.TTKEntry):
    class_ = ttkfields.CharField
    properties = (
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
        # Field
        "max_length",
        "min_length",
        "strip",
        "empty_value",
    ) + FieldMixin.base_properties
    ro_properties = (
        "max_length",
        "min_length",
        "strip",
        "empty_value",
    ) + FieldMixin.base_properties

    def _process_property_value(self, pname, value):
        if pname == "strip":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.CharField"
register_widget(
    _builder_uid,
    CharFieldBO,
    "CharField",
    _designer_tabs,
)

register_custom_property("pygubu.forms.*", "fname", "identifierentry")
register_custom_property("pygubu.forms.*", "initial", "entry")
register_custom_property(
    "pygubu.forms.*",
    "required",
    "choice",
    values=("", "false", "true"),
    state="readonly",
)
register_custom_property("pygubu.forms.*", "help_text", "entry")
register_custom_property("pygubu.forms.*", "max_length", "naturalnumber")
register_custom_property("pygubu.forms.*", "min_length", "naturalnumber")
register_custom_property(
    "pygubu.forms.*",
    "strip",
    "choice",
    values=("", "false", "true"),
    state="readonly",
)
register_custom_property("pygubu.forms.*", "empty_value", "entry")


class LabelFieldInfoBO(FieldMixin, ttkw.TTKLabel):
    class_ = ttkfields.LabelFieldInfo
    properties = ttkw.TTKLabel.properties + ("fname",)
    ro_properties = ttkw.TTKLabel.ro_properties + ("fname",)


_builder_uid = f"{_plugin_uid}.LabelFieldInfo"
register_widget(
    _builder_uid,
    LabelFieldInfoBO,
    "LabelFieldInfo",
    _designer_tabs,
)


class ChoiceFieldBO(FieldMixin, ttkw.TTKCombobox):
    class_ = ttkfields.ChoiceField
    properties = (
        "class_",
        "cursor",
        "takefocus",
        "style" "exportselection",
        "justify",
        "height",
        "postcommand",
        "state",
        "width",
        # field props
        "choices",
    ) + FieldMixin.base_properties
    ro_properties = (
        "class_",
        "choices",
        "state",
    ) + FieldMixin.base_properties

    def _process_property_value(self, pname, value):
        if pname == "choices":
            return _list_dto.transform(value)
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.ChoiceField"
register_widget(
    _builder_uid,
    ChoiceFieldBO,
    "ChoiceField",
    _designer_tabs,
)

_choices_help = _(
    "Specifies the list of values to display. "
    "In code you can pass any iterable. "
    'In Designer, a json like list: ["item1", "item2"]'
)
register_custom_property(_builder_uid, "choices", "entry", help=_choices_help)


class CharComboFieldBO(FieldMixin, BuilderObject):
    class_ = ttkfields.CharComboField
    properties = (
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
        # Combobox
        "height",
        "postcommand",
        # field props
        "max_length",
        "min_length",
        "strip",
        "empty_value",
        "choices",
    ) + FieldMixin.base_properties
    ro_properties = (
        "class_",
        "max_length",
        "min_length",
        "strip",
        "empty_value",
        "choices",
    ) + FieldMixin.base_properties

    def _process_property_value(self, pname, value):
        if pname == "choices":
            return _list_dto.transform(value)
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.CharComboField"
register_widget(
    _builder_uid,
    CharComboFieldBO,
    "CharComboField",
    _designer_tabs,
)
register_custom_property(_builder_uid, "choices", "entry", help=_choices_help)
