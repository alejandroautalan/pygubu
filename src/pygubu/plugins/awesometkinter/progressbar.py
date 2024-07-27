import awesometkinter as atk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)

from ..awesometkinter import _plugin_uid, _designer_tabs


class RadialProgressbarBO(BuilderObject):
    OPTIONS_CUSTOM = (
        "bg",
        "fg",
        "text_fg",
        "font",
        "font_size_ratio",
        "base_img",
        "indicator_img",
        "parent_bg",
    )
    ro_properties = OPTIONS_CUSTOM
    class_ = atk.RadialProgressbar

    def _process_property_value(self, pname, value):
        if pname == "font_size_ratio":
            value_ = 0.1
            try:
                value_ = float(value)
            except ValueError:
                pass
            return value_
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.RadialProgressbar"
register_widget(
    _builder_uid,
    RadialProgressbarBO,
    "RadialProgressbar",
    _designer_tabs,
)


class RadialProgressbar3dBO(BuilderObject):
    OPTIONS_CUSTOM = ("fg", "text_fg", "text_bg")
    ro_properties = OPTIONS_CUSTOM
    class_ = atk.RadialProgressbar3d


_builder_uid = f"{_plugin_uid}.RadialProgressbar3d"
register_widget(
    _builder_uid,
    RadialProgressbar3dBO,
    "RadialProgressbar3d",
    _designer_tabs,
)


class SegmentbarBO(BuilderObject):
    OPTIONS_CUSTOM = ("bg", "fg", "width", "height")
    ro_properties = OPTIONS_CUSTOM
    class_ = atk.Segmentbar

    def _process_property_value(self, pname, value):
        if pname in ("width",):
            return int(value)
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.Segmentbar"
register_widget(_builder_uid, SegmentbarBO, "Segmentbar", _designer_tabs)
