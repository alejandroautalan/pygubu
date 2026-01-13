import tkinter as tk
import pygubu.plugins.pygubu.combobox_bo as cbb
import pygubu.plugins.pygubu.fontinputbo as fib
import pygubu.plugins.pygubu.colorinput_bo as cib
import pygubu.forms.pygubuwidget as pygubuwidget

from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
    copy_custom_property,
)
from pygubu.plugins.pygubu._config import (
    nspygubu,
    _designer_tabs_forms as _designer_tabs,
)
from .base import WidgetBOMixin


class PygubuComboboxBO(WidgetBOMixin, cbb.ComboboxBO):
    class_ = pygubuwidget.PygubuCombobox
    properties = cbb.ComboboxBuilder.properties + WidgetBOMixin.base_properties
    ro_properties = (
        cbb.ComboboxBuilder.ro_properties + WidgetBOMixin.base_properties
    )


register_widget(
    nspygubu.forms.pygubuwidget.PygubuCombobox,
    PygubuComboboxBO,
    "PygubuCombobox",
    _designer_tabs,
)


class FontInputFWBO(WidgetBOMixin, fib.FontInputBO):
    class_ = pygubuwidget.FontInputFW
    properties = fib.FontInputBO.properties + WidgetBOMixin.base_properties
    ro_properties = (
        fib.FontInputBO.ro_properties + WidgetBOMixin.base_properties
    )


register_widget(
    nspygubu.forms.pygubuwidget.FontInput,
    FontInputFWBO,
    "FontInput",
    _designer_tabs,
)


class ColorInputFWBO(WidgetBOMixin, cib.ColorInputBO):
    class_ = pygubuwidget.ColorInputFW
    properties = cib.ColorInputBO.properties + WidgetBOMixin.base_properties
    ro_properties = (
        cib.ColorInputBO.ro_properties + WidgetBOMixin.base_properties
    )


register_widget(
    nspygubu.forms.pygubuwidget.ColorInput,
    ColorInputFWBO,
    "ColorInput",
    _designer_tabs,
)
