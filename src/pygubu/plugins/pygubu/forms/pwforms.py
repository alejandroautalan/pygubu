import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
    copy_custom_property,
)
import pygubu.forms.pwforms as pwforms
import pygubu.plugins.pygubu.combobox as cbb
from pygubu.i18n import _
from .base import FieldBOMixin


_plugin_uid = "pygubu.forms.pwforms"
_designer_tabs = ("ttk", _("Pygubu Forms"))


class ComboboxFieldBO(FieldBOMixin, cbb.ComboboxBuilder):
    class_ = pwforms.ComboboxField
    properties = cbb.ComboboxBuilder.properties + FieldBOMixin.base_properties
    ro_properties = (
        cbb.ComboboxBuilder.ro_properties + FieldBOMixin.base_properties
    )


_builder_uid = f"{_plugin_uid}.ComboboxField"
register_widget(
    _builder_uid,
    ComboboxFieldBO,
    "ComboboxField",
    _designer_tabs,
)

copy_custom_property(cbb._builder_id, "values", _builder_uid)
copy_custom_property(cbb._builder_id, "keyvariable", _builder_uid)
copy_custom_property(cbb._builder_id, "state", _builder_uid)
