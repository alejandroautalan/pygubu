import tkinter as tk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
import pygubu.forms.tkforms as tkforms
import pygubu.plugins.tk.tkstdwidgets as tkw
from pygubu.i18n import _
from .base import FieldBOMixin


_plugin_uid = "pygubu.forms.tk"
_designer_tabs = ("tk", _("Pygubu Forms"))


class TextFieldBO(FieldBOMixin, tkw.TKText):
    class_ = tkforms.TextField
    properties = tkw.TKText.properties + FieldBOMixin.base_properties
    ro_properties = tkw.TKText.properties + FieldBOMixin.base_properties


_builder_uid = f"{_plugin_uid}.TextField"
register_widget(
    _builder_uid,
    TextFieldBO,
    "TextField",
    _designer_tabs + ("ttk",),
)
