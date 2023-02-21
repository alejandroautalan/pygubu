import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.i18n import _
import pygubu.forms.pgwf as pgforms
from .base import FieldMixin


_plugin_uid = "pygubu.forms.pgwf"
_designer_tabs = ("ttk", _("Pygubu Forms"))


class ChoiceKeyFieldBO(FieldMixin, BuilderObject):
    class_ = pgforms.ComboboxField
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
        "values",
        "height",
        "postcommand",
        # Pygubu combobox
        "keyvariable",
    ) + FieldMixin.base_properties
    ro_properties = ("class_",) + FieldMixin.base_properties
    tkvar_properties = ("textvariable", "keyvariable")


_builder_uid = f"{_plugin_uid}.ChoiceKeyField"
register_widget(
    _builder_uid,
    ChoiceKeyFieldBO,
    "ChoiceKeyField",
    _designer_tabs,
)

register_custom_property(_builder_uid, "keyvariable", "tkvarentry")
register_custom_property(
    _builder_uid,
    "state",
    "choice",
    values=("", "normal", "disabled"),
    state="readonly",
)
_values_help = _(
    "Specifies the list of values to display. \n"
    "In code you can pass an iterable of (key, value) pairs.\n"
    'In Designer, a json like list: [["key1", "value1"], ["key2", "value2"]]'
)
register_custom_property(_builder_uid, "values", "entry", help=_values_help)
