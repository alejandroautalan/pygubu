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
from .base import FieldMixin


_plugin_uid = "pygubu.forms.ttk"
_designer_tabs = ("ttk", _("Pygubu Forms"))
_list_dto = ListDTO()


class FormBO(FieldMixin, ttkw.TTKFrame):
    class_ = ttkfields.Form
    properties = ttkw.TTKFrame.properties + ("fname",)
    ro_properties = ttkw.TTKFrame.ro_properties + ("fname",)

    def add_child(self, bobject):
        if issubclass(bobject.class_, Field):
            self.widget.add_field(bobject.widget)


_builder_uid = f"{_plugin_uid}.Form"
register_widget(
    _builder_uid,
    FormBO,
    "Form",
    _designer_tabs,
)


class LabelDisplayFieldBO(FieldMixin, ttkw.TTKLabel):
    class_ = ttkfields.LabelDisplayField
    properties = ttkw.TTKLabel.properties + ("fname",)
    ro_properties = ttkw.TTKLabel.ro_properties + ("fname",)


_builder_uid = f"{_plugin_uid}.LabelDisplayField"
register_widget(
    _builder_uid,
    LabelDisplayFieldBO,
    "LabelDisplayField",
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


class BooleanCheckboxFieldBO(FieldMixin, BuilderObject):
    class_ = ttkfields.BooleanCheckboxField
    properties = (
        "class_",
        "cursor",
        "takefocus",
        "style",
        "command",
        # "offvalue",
        # "onvalue",
        "text",
        "textvariable",
        "underline",
        "image",
        "compound",
        "width",
        "variable",
        "state",
    ) + FieldMixin.base_properties
    ro_properties = ("class_",) + FieldMixin.base_properties
    command_properties = ("command",)


_builder_uid = f"{_plugin_uid}.BooleanCheckboxField"
register_widget(
    _builder_uid,
    BooleanCheckboxFieldBO,
    "BooleanCheckboxField",
    _designer_tabs,
)

register_custom_property(
    _builder_uid,
    "variable",
    "tkvarentry",
    type_choices=("boolean",),
    type_default="boolean",
)


class TextFieldBO(FieldMixin, BuilderObject):
    class_ = ttkfields.TextField
    properties = (
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
        #
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
    ) + FieldMixin.base_properties
    ro_properties = FieldMixin.base_properties
    command_properties = ("xscrollcommand", "yscrollcommand")


_builder_uid = f"{_plugin_uid}.TextFieldBO"
register_widget(
    _builder_uid,
    TextFieldBO,
    "TextField",
    _designer_tabs,
)

register_custom_property(_builder_uid, "initial", "text")
