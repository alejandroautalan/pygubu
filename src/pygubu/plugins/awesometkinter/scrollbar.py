from pygubu.api.v1 import register_widget
from pygubu.plugins.ttk.ttkstdwidgets import TTKScrollbar
import awesometkinter as atk

from ..awesometkinter import _plugin_uid, _designer_tabs


class SimpleScrollbarBO(TTKScrollbar):
    OPTIONS_STANDARD = tuple(
        set(TTKScrollbar.OPTIONS_STANDARD) - set(("style",))
    )
    OPTIONS_CUSTOM = ("bg", "slider_color", "width")
    properties = (
        OPTIONS_STANDARD + TTKScrollbar.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = TTKScrollbar.ro_properties + OPTIONS_CUSTOM + ("orient",)
    class_ = atk.scrollbar.SimpleScrollbar

    def _process_property_value(self, pname, value):
        if pname in ("width",):
            value_ = 5
            try:
                value_ = int(value)
            except ValueError:
                pass
            return value_
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.SimpleScrollbar"
register_widget(
    _builder_uid,
    SimpleScrollbarBO,
    "SimpleScrollbar",
    _designer_tabs,
)
