import tkinter as tk
import pygubu.plugins.pygubu.combobox_bo as cbb
import pygubu.forms.pygubuwidget as pygubuwidget

from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
    copy_custom_property,
)
from .base import (
    WidgetBOMixin,
    _plugin_forms_uid,
    _tab_form_widgets_label,
)


_plugin_uid = f"{_plugin_forms_uid}.pygubuwidget"
_designer_tabs = ("tk", _tab_form_widgets_label)


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
