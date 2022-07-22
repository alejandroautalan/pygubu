import awesometkinter as atk
from pygubu.i18n import _
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)

from ..awesometkinter import _designer_tab_label, _plugin_uid


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


_builder_uid = _plugin_uid + ".RadialProgressbar"
register_widget(
    _builder_uid,
    RadialProgressbarBO,
    "RadialProgressbar",
    ("ttk", _designer_tab_label),
)
register_custom_property(
    _builder_uid,
    "bg",
    "colorentry",
    help=_("color of base ring"),
)
register_custom_property(
    _builder_uid,
    "fg",
    "colorentry",
    help=_("color of indicator ring"),
)
register_custom_property(
    _builder_uid,
    "text_fg",
    "colorentry",
    help=_("percentage text color"),
)
register_custom_property(
    _builder_uid,
    "font",
    "fontentry",
    help=_("tkinter font for percentage text"),
)
register_custom_property(
    _builder_uid,
    "font_size_ratio",
    "spinbox",
    from_=0.1,
    to=1,
    increment=0.1,
    help=_(
        "font size to progressbar width ratio, e.g. for a progressbar size 100 pixels, a 0.1 ratio means font size 10"
    ),
)
register_custom_property(
    _builder_uid,
    "base_img",
    "imageentry",
    help=_("base image for progressbar"),
)
register_custom_property(
    _builder_uid,
    "indicator_img",
    "imageentry",
    help=_("indicator image for progressbar"),
)
register_custom_property(
    _builder_uid,
    "parent_bg",
    "colorentry",
    help=_("color of parent container"),
)


class RadialProgressbar3dBO(BuilderObject):
    OPTIONS_CUSTOM = ("fg", "text_fg", "text_bg")
    ro_properties = OPTIONS_CUSTOM
    class_ = atk.RadialProgressbar3d


_builder_uid = _plugin_uid + ".RadialProgressbar3d"
register_widget(
    _builder_uid,
    RadialProgressbar3dBO,
    "RadialProgressbar3d",
    ("ttk", _designer_tab_label),
)
register_custom_property(
    _builder_uid,
    "fg",
    "colorentry",
)
register_custom_property(
    _builder_uid,
    "text_fg",
    "colorentry",
)
register_custom_property(
    _builder_uid,
    "text_bg",
    "colorentry",
)


class SegmentbarBO(BuilderObject):
    OPTIONS_CUSTOM = ("bg", "fg", "width", "height")
    ro_properties = OPTIONS_CUSTOM
    class_ = atk.Segmentbar

    def _process_property_value(self, pname, value):
        if pname in ("width",):
            return int(value)
        return super()._process_property_value(pname, value)


_builder_uid = _plugin_uid + ".Segmentbar"
register_widget(
    _builder_uid, SegmentbarBO, "Segmentbar", ("ttk", _designer_tab_label)
)
register_custom_property(
    _builder_uid,
    "bg",
    "colorentry",
)
register_custom_property(
    _builder_uid,
    "fg",
    "colorentry",
)
register_custom_property(
    _builder_uid,
    "width",
    "naturalnumber",
)
register_custom_property(
    _builder_uid,
    "height",
    "dimensionentry",
)
