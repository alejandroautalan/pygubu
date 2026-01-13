import tkinter as tk
import pygubu.forms.ttkwidget as ttkwidget
import pygubu.plugins.tk.tkstdwidgets as tkw
import pygubu.plugins.ttk.ttkstdwidgets as ttkw

from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.plugins.pygubu.scrollbarhelper_bo import TTKSBHelperBO
from pygubu.plugins.pygubu._config import (
    nspygubu,
    _designer_tabs_forms as _designer_tabs,
)
from .base import WidgetBOMixin
from .tkwidget_bo import _tk_text_builder_uid

# Groups for ordering buttons in designer palette.
GROUP0: int = 0
GROUP1: int = 10
GROUP2: int = 20
GROUP3: int = 30

# Register text as child of TTKSBHelperBO
TTKSBHelperBO.add_allowed_child(_tk_text_builder_uid)


class FrameFormBuilderBO(WidgetBOMixin, ttkw.TTKFrame):
    class_ = ttkwidget.FrameFormBuilder
    properties = ttkw.TTKFrame.properties + WidgetBOMixin.base_properties
    ro_properties = ttkw.TTKFrame.ro_properties + WidgetBOMixin.base_properties


register_widget(
    nspygubu.forms.ttkwidget.FrameFormBuilder,
    FrameFormBuilderBO,
    "FrameFormBuilder",
    _designer_tabs,
    group=GROUP0,
)


class EntryBO(WidgetBOMixin, ttkw.TTKEntry):
    class_ = ttkwidget.Entry
    properties = ttkw.TTKEntry.properties + WidgetBOMixin.base_properties
    ro_properties = ttkw.TTKEntry.ro_properties + WidgetBOMixin.base_properties


register_widget(
    nspygubu.forms.ttkwidget.Entry,
    EntryBO,
    "Entry",
    _designer_tabs,
    group=GROUP0,
)


class LabelWidgetInfoBO(WidgetBOMixin, ttkw.TTKLabel):
    class_ = ttkwidget.LabelWidgetInfo
    properties = ttkw.TTKLabel.properties + WidgetBOMixin.base_properties
    ro_properties = ttkw.TTKLabel.ro_properties + WidgetBOMixin.base_properties


register_widget(
    nspygubu.forms.ttkwidget.LabelWidgetInfo,
    LabelWidgetInfoBO,
    "LabelWidgetInfo",
    _designer_tabs,
    group=GROUP1,
)


class LabelBO(WidgetBOMixin, ttkw.TTKLabel):
    class_ = ttkwidget.Label
    properties = ttkw.TTKLabel.properties + WidgetBOMixin.base_properties
    ro_properties = ttkw.TTKLabel.ro_properties + WidgetBOMixin.base_properties


register_widget(
    nspygubu.forms.ttkwidget.Label,
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


register_widget(
    nspygubu.forms.ttkwidget.Checkbutton,
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


register_widget(
    nspygubu.forms.ttkwidget.Combobox,
    ComboboxBO,
    "Combobox",
    _designer_tabs,
    group=GROUP0,
)
