from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.tk.tkstdwidgets import TKCanvas
from ttkwidgets.color import AlphaBar, ColorSquare, GradientBar
from ttkwidgets.color.functions import rgb_to_hsv
from PIL.ImageColor import getrgb
from ..ttkwidgets import _designer_tab_label, _plugin_uid


class AlphaBarBO(TKCanvas):
    class_ = AlphaBar
    container = False
    OPTIONS_CUSTOM = ("alpha", "color", "variable")
    properties = (
        TKCanvas.OPTIONS_STANDARD + TKCanvas.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = OPTIONS_CUSTOM + ("height", "width")
    virtual_events = ("<<AlphaChanged>>",)

    def _process_property_value(self, pname, value):
        final_value = None
        if pname in ("alpha", "height", "width"):
            final_value = int(value)
        elif pname == "color":
            final_value = getrgb(value)
        else:
            final_value = super(AlphaBarBO, self)._process_property_value(
                pname, value
            )
        return final_value

    def _code_process_property_value(self, targetid, pname, value):
        if pname == "color":
            return f'getrgb("{value}")'
        return super()._code_process_property_value(targetid, pname, value)

    def code_imports(self):
        return (("PIL.ImageColor", "getrgb"), ("ttkwidgets.color", "AlphaBar"))


_builder_uid = f"{_plugin_uid}.AlphaBar"

register_widget(
    _builder_uid, AlphaBarBO, "AlphaBar", ("ttk", _designer_tab_label), group=5
)

register_custom_property(
    _builder_uid,
    "alpha",
    "integernumber",
    help=_("initially selected alpha value (between 0 and 255)"),
)
register_custom_property(
    _builder_uid, "color", "colorentry", help=_("gradient color")
)
register_custom_property(
    _builder_uid,
    "variable",
    "tkvarentry",
    help=_("variable linked to the alpha value"),
)


class ColorSquareBO(TKCanvas):
    class_ = ColorSquare
    container = False
    OPTIONS_CUSTOM = ("hue", "color")
    properties = (
        TKCanvas.OPTIONS_STANDARD + TKCanvas.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = OPTIONS_CUSTOM + ("height", "width")
    virtual_events = ("<<ColorChanged>>",)

    def realize(self, parent, extra_init_args: dict = None):
        args = self._get_init_args(extra_init_args)
        master = parent.get_child_master()
        hue_value = args.pop("hue", 0)
        self.widget = self.class_(master, hue_value, **args)
        return self.widget

    def _process_property_value(self, pname, value):
        final_value = None
        if pname in ("hue", "height", "width"):
            final_value = int(value)
        elif pname == "color":
            rgb = getrgb(value)
            final_value = rgb_to_hsv(*rgb)
        else:
            final_value = super(ColorSquareBO, self)._process_property_value(
                pname, value
            )
        return final_value

    def _code_process_property_value(self, targetid, pname, value):
        if pname == "color":
            return f'rgb_to_hsv(*getrgb("{value}"))'
        return super()._code_process_property_value(targetid, pname, value)

    def code_imports(self):
        return (
            ("PIL.ImageColor", "getrgb"),
            ("ttkwidgets.color", "ColorSquare"),
            ("ttkwidgets.color.functions", "rgb_to_hsv"),
        )


_builder_uid = f"{_plugin_uid}.ColorSquare"

register_widget(
    _builder_uid,
    ColorSquareBO,
    "ColorSquare",
    ("ttk", _designer_tab_label),
    group=5,
)

# Custom properties
register_custom_property(
    _builder_uid,
    "hue",
    "integernumber",
    default_value=0,
    help=_("hue (between 0 and 360) of the color square gradient"),
)
register_custom_property(
    _builder_uid, "color", "colorentry", help=_("initially selected color")
)


class GradientBarBO(TKCanvas):
    class_ = GradientBar
    container = False
    OPTIONS_CUSTOM = ("hue", "variable")
    properties = (
        TKCanvas.OPTIONS_STANDARD + TKCanvas.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = OPTIONS_CUSTOM + ("height", "width")
    virtual_events = ("<<HueChanged>>",)

    def _process_property_value(self, pname, value):
        final_value = None
        if pname in ("hue", "height", "width"):
            final_value = int(value)
        else:
            final_value = super(GradientBarBO, self)._process_property_value(
                pname, value
            )
        return final_value

    def code_imports(self):
        return (("ttkwidgets.color", "GradientBar"),)


_builder_uid = f"{_plugin_uid}.GradientBar"

register_widget(
    _builder_uid,
    GradientBarBO,
    "GradientBar",
    ("ttk", _designer_tab_label),
    group=5,
)

register_custom_property(
    _builder_uid,
    "hue",
    "integernumber",
    help=_("initially selected hue value (between 0 and 360)"),
)
register_custom_property(
    _builder_uid,
    "variable",
    "tkvarentry",
    help=_("variable linked to the hue value"),
)
