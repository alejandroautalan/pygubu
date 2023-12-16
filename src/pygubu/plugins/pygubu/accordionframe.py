# encoding: utf-8
from pygubu.api.v1 import register_widget
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from pygubu.i18n import _
from pygubu.widgets.accordionframe import AccordionFrame


class AccordionFrameBO(TTKFrame):
    class_ = AccordionFrame


_builder_uid = "pygubu.widgets.accordionframe"

register_widget(
    _builder_uid,
    AccordionFrameBO,
    "AccordionFrame",
    (_("Pygubu Widgets"), "ttk"),
)
