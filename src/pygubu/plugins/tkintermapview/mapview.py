from pygubu.i18n import _
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from tkintermapview import TkinterMapView
from ..tkintermapview import _designer_tab_label, _plugin_uid


class TkinterMapViewBuilder(BuilderObject):
    class_ = TkinterMapView
    _int_props = ("width", "height", "corner_radius", "max_zoom")
    OPTIONS_CUSTOM = _int_props + ("bg_color",)
    ro_properties = OPTIONS_CUSTOM

    def _process_property_value(self, pname, value):
        if pname in self._int_props:
            return int(value)
        return super()._process_property_value(pname, value)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname in self._int_props:
            return self._process_property_value(pname, value)
        return super()._code_process_property_value(targetid, pname, value)

    @staticmethod
    def configure_for_preview(widget):
        """Make widget just display with minimal functionality."""

        def _no_op(event=None):
            pass

        seqlist = (
            "<B1-Motion>",
            "<Button-1>",
            "<Button-2>",
            "<Button-3>",
            "<Button-4>",
            "<Button-5>",
            "<ButtonRelease-1>",
            "<MouseWheel>",
        )
        for seq in seqlist:
            widget.canvas.bind(seq, _no_op)
        widget.button_zoom_in.command = _no_op
        widget.button_zoom_out.command = _no_op


_builder_uid = f"{_plugin_uid}.TkinterMapView"
register_widget(
    _builder_uid,
    TkinterMapViewBuilder,
    "TkinterMapView",
    ("ttk", _designer_tab_label),
)

_none = {}
# pname, editor, options
_properties = (
    ("widht", "naturalnumber", _none),
    ("height", "naturalnumber", _none),
    (
        "corner_radius",
        "choice",
        {"values": [""] + [x for x in range(0, 31)], "state": "readonly"},
    ),
    ("bg_color", "colorentry", _none),
    (
        "max_zoom",
        "choice",
        {"values": [x for x in range(1, 20)], "state": "readonly"},
    ),
)

for pname, editor, options in _properties:
    register_custom_property(_builder_uid, pname, editor, **options)
