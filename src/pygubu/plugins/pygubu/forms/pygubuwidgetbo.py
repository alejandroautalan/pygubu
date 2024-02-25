import tkinter as tk
import pygubu.plugins.pygubu.combobox as cbb
import pygubu.forms.pygubuwidget as pygubuwidget

from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
    copy_custom_property,
)
from pygubu.i18n import _
from .base import (
    WidgetBOMixin,
    _plugin_uid as base_plugin_uid,
    _designer_tabname,
)


_plugin_uid = f"{base_plugin_uid}.pygubuwidget"
_designer_tabs = ("tk", _designer_tabname)


class PygubuComboboxBO(WidgetBOMixin, cbb.ComboboxBO):
    class_ = pygubuwidget.PygubuCombobox
    properties = cbb.ComboboxBuilder.properties + WidgetBOMixin.base_properties
    ro_properties = (
        cbb.ComboboxBuilder.ro_properties + WidgetBOMixin.base_properties
    )


_builder_uid = f"{_plugin_uid}.PygubuCombobox"
register_widget(
    _builder_uid,
    PygubuComboboxBO,
    "PygubuCombobox",
    _designer_tabs,
)

copy_custom_property(cbb._builder_id, "values", _builder_uid)
copy_custom_property(cbb._builder_id, "keyvariable", _builder_uid)
copy_custom_property(cbb._builder_id, "state", _builder_uid)
