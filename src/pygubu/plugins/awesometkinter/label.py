import awesometkinter as atk
from pygubu.i18n import _
from pygubu.api.v1 import register_widget
from pygubu.plugins.tk.tkstdwidgets import TKLabel
from ..awesometkinter import _plugin_uid, _designer_tabs


class AutoWrappingLabelBO(TKLabel):
    class_ = atk.label.AutoWrappingLabel


_builder_uid = f"{_plugin_uid}.AutoWrappingLabel"
register_widget(
    _builder_uid,
    AutoWrappingLabelBO,
    "AutoWrappingLabel",
    _designer_tabs,
    group=1,
)


class AutofitLabelBO(TKLabel):
    OPTIONS_CUSTOM = ("refresh_time",)
    properties = (
        TKLabel.OPTIONS_STANDARD + TKLabel.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = TKLabel.ro_properties + OPTIONS_CUSTOM
    class_ = atk.label.AutofitLabel


_builder_uid = f"{_plugin_uid}.AutofitLabel"
register_widget(
    _builder_uid,
    AutofitLabelBO,
    "AutofitLabel",
    _designer_tabs,
    group=1,
)
