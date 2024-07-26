import tkinter as tk
import pygubu.forms.ttkwidget as ttkwidget
import pygubu.plugins.tk.tkstdwidgets as tkw
import pygubu.plugins.ttk.ttkstdwidgets as ttkw

from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.i18n import _
from .base import (
    WidgetBOMixin,
    _plugin_forms_uid,
    _tab_form_widgets_label,
)
from pygubu.plugins.pygubu.scrollbarhelper_bo import TTKSBHelperBO
from .tkwidget_bo import _tk_text_builder_uid

# Groups for ordering buttons in designer palette.
GROUP0: int = 0
GROUP1: int = 10
GROUP2: int = 20
GROUP3: int = 30

_plugin_uid = f"{_plugin_forms_uid}.ttkwidget"
_designer_tabs = ("ttk", _tab_form_widgets_label)

# Register text as child of TTKSBHelperBO
TTKSBHelperBO.add_allowed_child(_tk_text_builder_uid)


class FrameFormBuilderBO(WidgetBOMixin, ttkw.TTKFrame):
    class_ = ttkwidget.FrameFormBuilder
    properties = ttkw.TTKFrame.properties + WidgetBOMixin.base_properties
    ro_properties = ttkw.TTKFrame.ro_properties + WidgetBOMixin.base_properties


_builder_uid = f"{_plugin_uid}.FrameFormBuilder"
register_widget(
    _builder_uid,
    FrameFormBuilderBO,
    "FrameFormBuilder",
    _designer_tabs,
    group=GROUP0,
)


class EntryBO(WidgetBOMixin, ttkw.TTKEntry):
    class_ = ttkwidget.Entry
    properties = ttkw.TTKEntry.properties + WidgetBOMixin.base_properties
    ro_properties = ttkw.TTKEntry.ro_properties + WidgetBOMixin.base_properties


_builder_uid = f"{_plugin_uid}.Entry"
register_widget(
    _builder_uid,
    EntryBO,
    "Entry",
    _designer_tabs,
    group=GROUP0,
)


class LabelWidgetInfoBO(WidgetBOMixin, ttkw.TTKLabel):
    class_ = ttkwidget.LabelWidgetInfo
    properties = ttkw.TTKLabel.properties + WidgetBOMixin.base_properties
    ro_properties = ttkw.TTKLabel.ro_properties + WidgetBOMixin.base_properties


_builder_uid = f"{_plugin_uid}.LabelWidgetInfo"
register_widget(
    _builder_uid,
    LabelWidgetInfoBO,
    "LabelWidgetInfo",
    _designer_tabs,
    group=GROUP1,
)


class LabelBO(WidgetBOMixin, ttkw.TTKLabel):
    class_ = ttkwidget.Label
    properties = ttkw.TTKLabel.properties + WidgetBOMixin.base_properties
    ro_properties = ttkw.TTKLabel.ro_properties + WidgetBOMixin.base_properties


_builder_uid = f"{_plugin_uid}.Label"
register_widget(
    _builder_uid,
    LabelBO,
    "Label",
    _designer_tabs,
    group=GROUP0,
)


class CheckbuttonBO(WidgetBOMixin, ttkw.TTKCheckbutton):
    class_ = ttkwidget.Checkbutton
    properties = ttkw.TTKCheckbutton.properties + WidgetBOMixin.base_properties
    ro_properties = (
        ttkw.TTKCheckbutton.ro_properties + WidgetBOMixin.base_properties
    )


_builder_uid = f"{_plugin_uid}.Checkbutton"
register_widget(
    _builder_uid,
    CheckbuttonBO,
    "Checkbutton",
    _designer_tabs,
    group=GROUP0,
)


class ComboboxBO(WidgetBOMixin, ttkw.TTKCombobox):
    class_ = ttkwidget.Combobox
    properties = ttkw.TTKCombobox.properties + WidgetBOMixin.base_properties
    ro_properties = (
        ttkw.TTKCombobox.ro_properties + WidgetBOMixin.base_properties
    )


_builder_uid = f"{_plugin_uid}.Combobox"
register_widget(
    _builder_uid,
    ComboboxBO,
    "Combobox",
    _designer_tabs,
    group=GROUP0,
)
