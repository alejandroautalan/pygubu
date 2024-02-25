import tkinter as tk
import pygubu.plugins.tk.tkstdwidgets as tkw
import pygubu.plugins.ttk.ttkstdwidgets as ttkw
import pygubu.forms.tkwidget as tkwidget

from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.i18n import _
from pygubu.plugins.pygubu.tkscrollbarhelper import TKSBHelperBO
from .base import (
    WidgetBOMixin,
    _plugin_uid as base_plugin_uid,
    _designer_tabname,
)


_plugin_uid = f"{base_plugin_uid}.tkwidget"
_designer_tabs = ("tk", _designer_tabname)


class TextBO(WidgetBOMixin, tkw.TKText):
    class_ = tkwidget.Text
    properties = tkw.TKText.properties + WidgetBOMixin.base_properties
    ro_properties = tkw.TKText.ro_properties + WidgetBOMixin.base_properties


_builder_uid = f"{_plugin_uid}.Text"
_tk_text_builder_uid = _builder_uid

register_widget(
    _builder_uid,
    TextBO,
    "Text",
    _designer_tabs,
    group=0,
)


TKSBHelperBO.add_allowed_child(_builder_uid)
