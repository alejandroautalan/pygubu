import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame, TTKEntry, TTKLabel
from pygubu.forms.fields import Field
from pygubu.forms.ttkfields import Form, CharField, LabelFieldInfo, LabelField


class FieldNameMixin:
    def _get_init_args(self, extra_init_args: dict = None):
        args = super()._get_init_args(extra_init_args)
        name = args.get("fname", None)
        if not name:
            args["fname"] = self.wmeta.identifier
        return args


class FormBO(FieldNameMixin, TTKFrame):
    class_ = Form
    properties = TTKFrame.properties + ("fname",)
    ro_properties = TTKFrame.ro_properties + ("fname",)

    def add_child(self, bobject):
        if issubclass(bobject.class_, Field):
            self.widget.add_field(bobject.widget)
            print(f"Field {bobject.widget.fname} added")


register_widget(
    "pygubu.forms.Form",
    FormBO,
    "Form",
    ("ttk", "Pygubu-Forms"),
)


class LabelFieldBO(FieldNameMixin, TTKLabel):
    class_ = LabelField
    properties = TTKLabel.properties + ("fname",)
    ro_properties = TTKLabel.ro_properties + ("fname",)


register_widget(
    "pygubu.forms.LabelField",
    LabelFieldBO,
    "LabelField",
    ("ttk", "Pygubu-Forms"),
)


class CharFieldBO(FieldNameMixin, TTKEntry):
    class_ = CharField
    properties = (
        "class_",
        "cursor",
        "takefocus",
        "style" "exportselection",
        "font",
        "justify",
        "show",
        "state",
        "textvariable",
        "validate",
        "width",
        #
        "fname",
        "initial",
        "required",
        "help_text",
        "max_length",
        "min_length",
        "strip",
        "empty_value",
    )
    ro_properties = (
        "fname",
        "initial",
        "required",
        "help_text",
        "max_length",
        "min_length",
        "strip",
        "empty_value",
    )

    def _process_property_value(self, pname, value):
        if pname in ("required", "strip"):
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)


register_widget(
    "pygubu.forms.CharField",
    CharFieldBO,
    "CharField",
    ("ttk", "Pygubu-Forms"),
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


class LabelFieldInfoBO(FieldNameMixin, TTKLabel):
    class_ = LabelFieldInfo
    properties = TTKLabel.properties + ("fname",)
    ro_properties = TTKLabel.ro_properties + ("fname",)


register_widget(
    "pygubu.forms.LabelFieldInfo",
    LabelFieldInfoBO,
    "LabelFieldInfo",
    ("ttk", "Pygubu-Forms"),
)
