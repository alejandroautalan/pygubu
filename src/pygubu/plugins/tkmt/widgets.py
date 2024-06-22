import TKinterModernThemes as tkmt

from pygubu.i18n import _
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from ..tkmt import _designer_tab_label, _plugin_uid


class ThemedTkFrameBO(BuilderObject):
    allow_bindings = False
    layout_required = False
    allowed_parents = ("root",)
    class_ = tkmt.ThemedTKinterFrame
    container = True
    properties = ("title", "theme", "mode")
    ro_properties = properties

    def realize(self, parent, extra_init_args: dict = None):
        kargs = self._get_init_args(extra_init_args)
        # master = parent.get_child_master()
        args = []
        for arg in ("title",):
            args.append(kargs.pop(arg))
        self.widget = self.class_(*args, **kargs)
        return self.widget


_builder_uid = f"{_plugin_uid}.ThemedTKinterFrame"
_themedtkinterframe = _builder_uid
register_widget(
    _builder_uid,
    ThemedTkFrameBO,
    "ThemedTKinterFrame",
    ("ttk", _designer_tab_label),
)

register_custom_property(
    _builder_uid,
    "theme",
    "choice",
    values=("azure", "sun-valley", "park"),
    default_value="park",
    state="readonly",
)

register_custom_property(
    _builder_uid,
    "mode",
    "choice",
    values=("light", "dark"),
    default_value="dark",
    state="readonly",
)


class TkmtWidgetBO(BuilderObject):
    allow_bindings = False
    layout_required = False
    properties = ("row", "col", "padx", "pady", "rowspan", "colspan", "sticky")
    ro_properties = properties
    pos_args = tuple()
    master_add_method = None

    def realize(self, parent, extra_init_args: dict = None):
        master = parent.get_child_master()
        assert self.master_add_method is not None
        add_method = getattr(master, self.master_add_method)
        kargs = self._get_init_args(extra_init_args)
        args_defaults = self._get_positional_args_defaults()
        args = self._get_positional_args(kargs, args_defaults)
        self.widget = add_method(*args, **kargs)
        return self.widget

    def configure(self, target=None):
        pass

    def _get_positional_args(self, bag: dict, defaults: dict) -> list:
        args = []
        for pname in self.pos_args:
            if pname in bag:
                value = bag.pop(pname)
                args.append(value)
            elif pname in defaults:
                args.append(defaults[pname])
        return args

    def _get_positional_args_defaults(self) -> dict:
        return {}

    def _process_property_value(self, pname, value):
        if pname in ("row", "col", "rowspan", "colspan"):
            return int(value)
        return super()._process_property_value(pname, value)


class wFrameBO(TkmtWidgetBO):
    container = True
    master_add_method = "addFrame"
    pos_args = ("name",)

    def _get_positional_args_defaults(self) -> dict:
        return {"name": self.wmeta.identifier}


_builder_uid = f"{_plugin_uid}.wFrame"
_wframe = _builder_uid
register_widget(_builder_uid, wFrameBO, "wFrame", ("ttk", _designer_tab_label))

wFrameBO.add_allowed_parent(_themedtkinterframe)
wFrameBO.add_allowed_parent(_wframe)


class wLabelFrameBO(TkmtWidgetBO):
    container = True
    master_add_method = "addLabelFrame"
    properties = ("text",) + TkmtWidgetBO.properties
    ro_properties = properties
    pos_args = ("text",)

    def _get_positional_args_defaults(self) -> dict:
        return {"text": self.wmeta.identifier}


_builder_uid = f"{_plugin_uid}.wLabelFrame"
_wlabelframe = _builder_uid
register_widget(
    _builder_uid, wLabelFrameBO, "wLabelFrame", ("ttk", _designer_tab_label)
)

wFrameBO.add_allowed_parent(_themedtkinterframe)
wFrameBO.add_allowed_parent(_wframe)
wFrameBO.add_allowed_parent(_wlabelframe)


class wSeparatorBO(TkmtWidgetBO):
    master_add_method = "Seperator"


_builder_uid = f"{_plugin_uid}.wSeparator"
register_widget(
    _builder_uid, wSeparatorBO, "wSeparator", ("ttk", _designer_tab_label)
)


class wButtonBO(TkmtWidgetBO):
    master_add_method = "Button"
    pos_args = ("text", "command")
    properties = pos_args + TkmtWidgetBO.properties
    ro_properties = properties

    def _get_positional_args_defaults(self) -> dict:
        return {
            "text": self.wmeta.identifier,
            "command": None,
        }


_builder_uid = f"{_plugin_uid}.wButton"
register_widget(
    _builder_uid, wButtonBO, "wButton", ("ttk", _designer_tab_label)
)


class wAccentButtonBO(wButtonBO):
    master_add_method = "AccentButton"


_builder_uid = f"{_plugin_uid}.wAccentButton"
register_widget(
    _builder_uid, wAccentButtonBO, "wAccentButton", ("ttk", _designer_tab_label)
)


class wCheckbuttonBO(TkmtWidgetBO):
    master_add_method = "Checkbutton"
    pos_args = ("text", "variable")
    properties = pos_args + TkmtWidgetBO.properties
    ro_properties = properties

    def _get_positional_args_defaults(self) -> dict:
        return {
            "text": self.wmeta.identifier,
            "variable": None,
        }


_builder_uid = f"{_plugin_uid}.wCheckbutton"
register_widget(
    _builder_uid, wCheckbuttonBO, "wCheckbutton", ("ttk", _designer_tab_label)
)


class wToggleButtonBO(wCheckbuttonBO):
    master_add_method = "ToggleButton"


_builder_uid = f"{_plugin_uid}.wToggleButton"
register_widget(
    _builder_uid, wToggleButtonBO, "wToggleButton", ("ttk", _designer_tab_label)
)


class wSlideSwitchBO(wCheckbuttonBO):
    master_add_method = "SlideSwitch"


_builder_uid = f"{_plugin_uid}.wSlideSwitch"
register_widget(
    _builder_uid, wSlideSwitchBO, "wSlideSwitch", ("ttk", _designer_tab_label)
)


class wRadiobuttonBO(wCheckbuttonBO):
    master_add_method = "Radiobutton"
    pos_args = ("text", "variable", "value")
    properties = pos_args + TkmtWidgetBO.properties
    ro_properties = properties

    def _get_positional_args_defaults(self) -> dict:
        return {
            "text": self.wmeta.identifier,
            "variable": None,
            "value": 0,
        }


_builder_uid = f"{_plugin_uid}.wRadiobutton"
register_widget(
    _builder_uid, wRadiobuttonBO, "wRadiobutton", ("ttk", _designer_tab_label)
)


class wEntryBO(TkmtWidgetBO):
    master_add_method = "Entry"
    pos_args = ("textvariable",)
    properties = pos_args + TkmtWidgetBO.properties
    ro_properties = properties

    def _get_positional_args_defaults(self) -> dict:
        return {
            "textvariable": None,
        }


_builder_uid = f"{_plugin_uid}.wEntry"
register_widget(_builder_uid, wEntryBO, "wEntry", ("ttk", _designer_tab_label))


class wNumericalSpinboxBO(TkmtWidgetBO):
    master_add_method = "NumericalSpinbox"
    pos_args = ("lower", "upper", "increment", "variable")
    properties = pos_args + TkmtWidgetBO.properties
    ro_properties = properties

    def _get_positional_args_defaults(self) -> dict:
        return {
            "lower": 0,
            "upper": 10,
            "increment": 1,
            "variable": None,
        }

    def _process_property_value(self, pname, value):
        if pname in ("lower", "upper", "increment"):
            return float(value)
        return super()._process_property_value(pname, value)


_builder_uid = f"{_plugin_uid}.wNumericalSpinbox"
register_widget(
    _builder_uid,
    wNumericalSpinboxBO,
    "wNumericalSpinbox",
    ("ttk", _designer_tab_label),
)
