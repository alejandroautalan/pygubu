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
from pygubu.plugins.pygubu.tkscrollbarhelper_bo import TKSBHelperBO
from pygubu.plugins.pygubu._config import (
    nspygubu,
    _designer_tabs_forms as _designer_tabs,
    GINPUT,
)
from .base import WidgetBOMixin


class TextBO(WidgetBOMixin, tkw.TKText):
    class_ = tkwidget.Text
    properties = tkw.TKText.properties + WidgetBOMixin.base_properties
    ro_properties = tkw.TKText.ro_properties + WidgetBOMixin.base_properties


_tk_text_builder_uid = nspygubu.forms.tkwidget.Text

register_widget(
    _tk_text_builder_uid,
    TextBO,
    "Text",
    _designer_tabs,
    group=GINPUT,
)


TKSBHelperBO.add_allowed_child(_tk_text_builder_uid)
