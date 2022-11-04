from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.i18n import _
from pygubu.plugins.tk.tkstdwidgets import TKFrame as TKFrameBO
from pygubu.plugins.tk.tkstdwidgets import TKLabel as TKLabelBO
from pygubu.plugins.tk.tkstdwidgets import TKEntry as TKEntryBO
from pygubu.plugins.tk.tkstdwidgets import TKCanvas as TKCanvasBO
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkButton,
    CTkProgressBar,
    CTkSlider,
    CTkEntry,
    CTkOptionMenu,
    CTkComboBox,
    CTkCheckBox,
    CTkRadioButton,
    CTkSwitch,
    CTkTextbox,
    CTkCanvas,
    CTkScrollbar,
)

from ..customtkinter import _designer_tab_label, _plugin_uid
from .ctkbase import CTkBaseMixin

GCONTAINER = 0
GINPUT = 1
GDISPLAY = 2


class CTkFrameBO(CTkBaseMixin, TKFrameBO):
    class_ = CTkFrame
    OPTIONS_CUSTOM = (
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "corner_radius",
    )
    properties = (
        TKFrameBO.OPTIONS_STANDARD + TKFrameBO.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )


_builder_uid = f"{_plugin_uid}.CTkFrame"
register_widget(
    _builder_uid,
    CTkFrameBO,
    "CTkFrame",
    ("ttk", _designer_tab_label),
    group=GCONTAINER,
)


class CTkLabelBO(CTkBaseMixin, TKLabelBO):
    class_ = CTkLabel
    OPTIONS_CUSTOM = (
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "corner_radius",
    )
    properties = (
        TKLabelBO.OPTIONS_STANDARD + TKLabelBO.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )


_builder_uid = f"{_plugin_uid}.CTkLabel"
register_widget(
    _builder_uid,
    CTkLabelBO,
    "CTkLabel",
    ("ttk", _designer_tab_label),
    group=GDISPLAY,
)


class CTkProgressBarBO(CTkBaseMixin, BuilderObject):
    class_ = CTkProgressBar
    allow_bindings = False
    OPTIONS_SPECIFIC = ("width", "height", "variable", "orient", "mode")
    OPTIONS_CUSTOM = (
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "corner_radius",
        "progress_color",
        "determinate_speed",
        "indeterminate_speed",
    )
    properties = OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = ("orient",)


_builder_uid = f"{_plugin_uid}.CTkProgressBar"
register_widget(
    _builder_uid,
    CTkProgressBarBO,
    "CTkProgressBar",
    ("ttk", _designer_tab_label),
    group=GDISPLAY,
)


class CTkButtonBO(CTkBaseMixin, BuilderObject):
    class_ = CTkButton
    allow_bindings = False
    OPTIONS_SPECIFIC = (
        "text",
        "width",
        "height",
        "textvariable",
        "image",
        "compound",
        "state",
        "command",
    )
    OPTIONS_CUSTOM = (
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "corner_radius",
        "hover_color",
        "text_color",
        "text_color_disabled",
        "text_font",
        "hover",
    )
    properties = OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = ("hover",)


_builder_uid = f"{_plugin_uid}.CTkButton"
register_widget(
    _builder_uid,
    CTkButtonBO,
    "CTkButton",
    ("ttk", _designer_tab_label),
    group=GINPUT,
)


class CTkSliderBO(CTkBaseMixin, BuilderObject):
    class_ = CTkSlider
    allow_bindings = False
    OPTIONS_SPECIFIC = (
        "width",
        "height",
        "orient",
        "variable",
        "from_",
        "to",
        "command",
        "state",
    )
    OPTIONS_CUSTOM = (
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "corner_radius",
        "progress_color",
        "button_color",
        "button_hover_color",
        "button_corner_radius",
        "button_length",
        "number_of_steps",
    )
    properties = OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = ("orient", "button_length")


_builder_uid = f"{_plugin_uid}.CTkSlider"
register_widget(
    _builder_uid,
    CTkSliderBO,
    "CTkSlider",
    ("ttk", _designer_tab_label),
    group=GINPUT,
)


class CTkEntryBO(CTkBaseMixin, TKEntryBO):
    class_ = CTkEntry
    allow_bindings = False
    OPTIONS_CUSTOM = TKEntryBO.OPTIONS_CUSTOM + (
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "corner_radius",
        "text_color",
        "placeholder_text_color",
        "text_font",
        "placeholder_text",
    )
    properties = (
        TKEntryBO.OPTIONS_STANDARD + TKEntryBO.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )

    def _set_property(self, target_widget, pname, value):
        real_entry = target_widget.entry
        if pname == "text":
            wstate = str(real_entry["state"])
            if wstate != "normal":
                # change state temporarily
                real_entry["state"] = "normal"
            real_entry.delete(0, "end")
            real_entry.insert(0, value)
            real_entry["state"] = wstate
        else:
            super()._set_property(target_widget, pname, value)


_builder_uid = f"{_plugin_uid}.CTkEntry"
register_widget(
    _builder_uid,
    CTkEntryBO,
    "CTkEntry",
    ("ttk", _designer_tab_label),
    group=GINPUT,
)


class CTkOptionMenuBO(CTkBaseMixin, BuilderObject):
    class_ = CTkOptionMenu
    allow_bindings = False
    OPTIONS_SPECIFIC = ("command", "variable", "values")
    OPTIONS_CUSTOM = (
        "bg_color",
        "fg_color",
        "button_color",
        "button_hover_color",
        "text_color",
        "text_color_disabled",
        "dropdown_hover_color",
        "dropdown_text_color",
        "dropdown_color",
        "width",
        "height",
        "corner_radius",
        "text_font",
        "state",
        "dynamic_resizing",
    )
    properties = (
        BuilderObject.OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    command_properties = ("command",)

    def _code_define_callback_args(self, cmd_pname, cmd):
        return ("current_value",)


_builder_uid = f"{_plugin_uid}.CTkOptionMenu"
register_widget(
    _builder_uid,
    CTkOptionMenuBO,
    "CTkOptionMenu",
    ("ttk", _designer_tab_label),
    group=GINPUT,
)


class CTkComboBoxBO(CTkBaseMixin, BuilderObject):
    class_ = CTkComboBox
    allow_bindings = False
    OPTIONS_SPECIFIC = ("command", "variable", "values")
    OPTIONS_CUSTOM = (
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "button_color",
        "button_hover_color",
        "text_color",
        "text_color_disabled",
        "dropdown_hover_color",
        "dropdown_text_color",
        "dropdown_color",
        "width",
        "height",
        "corner_radius",
        "text_font",
        "dropdown_text_font",
        "state",
        "hover",
    )
    properties = (
        BuilderObject.OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    command_properties = ("command",)
    ro_properties = ("hover",)

    def _code_define_callback_args(self, cmd_pname, cmd):
        return ("value",)


_builder_uid = f"{_plugin_uid}.CTkComboBox"
register_widget(
    _builder_uid,
    CTkComboBoxBO,
    "CTkComboBox",
    ("ttk", _designer_tab_label),
    group=GINPUT,
)


class CTkCheckBoxBO(CTkBaseMixin, BuilderObject):
    class_ = CTkCheckBox
    allow_bindings = False
    OPTIONS_STANDARD = ("textvariable",)
    OPTIONS_SPECIFIC = (
        "command",
        "variable",
        "variable",
        "onvalue",
        "offvalue",
        "state",
        "width",
        "height",
    )
    OPTIONS_CUSTOM = (
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "checkmark_color",
        "text",
        "text_font",
        "text_color",
        "text_color_disabled",
        "corner_radius",
        "hover",
        "hover_color",
    )
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = ("command",)
    ro_properties = ("hover",)


_builder_uid = f"{_plugin_uid}.CTkCheckBox"
register_widget(
    _builder_uid,
    CTkCheckBoxBO,
    "CTkCheckBox",
    ("ttk", _designer_tab_label),
    group=GINPUT,
)


class CTkRadioButtonBO(CTkBaseMixin, BuilderObject):
    class_ = CTkRadioButton
    allow_bindings = False
    OPTIONS_STANDARD = ("textvariable",)
    OPTIONS_SPECIFIC = (
        "command",
        "variable",
        "variable",
        "onvalue",
        "offvalue",
        "state",
        "width",
        "height",
    )
    OPTIONS_CUSTOM = (
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "checkmark_color",
        "text",
        "text_font",
        "text_color",
        "text_color_disabled",
        "corner_radius",
        "hover",
        "hover_color",
    )
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = ("command",)
    ro_properties = ("hover",)


_builder_uid = f"{_plugin_uid}.CTkRadioButton"
register_widget(
    _builder_uid,
    CTkRadioButtonBO,
    "CTkRadioButton",
    ("ttk", _designer_tab_label),
    group=GINPUT,
)


class CTkSwitchBO(CTkBaseMixin, BuilderObject):
    class_ = CTkSwitch
    allow_bindings = False
    OPTIONS_STANDARD = ("textvariable",)
    OPTIONS_SPECIFIC = (
        "command",
        "variable",
        "variable",
        "onvalue",
        "offvalue",
        "state",
        "width",
        "height",
    )
    OPTIONS_CUSTOM = (
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "checkmark_color",
        "text",
        "text_font",
        "text_color",
        "text_color_disabled",
        "corner_radius",
        "hover",
        "hover_color",
        "progress_color",
        "button_color",
        "button_hover_color",
        "button_length",
    )
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    command_properties = ("command",)
    ro_properties = ("hover", "text_color", "text_color_disabled")


_builder_uid = f"{_plugin_uid}.CTkSwitch"
register_widget(
    _builder_uid,
    CTkSwitchBO,
    "CTkSwitch",
    ("ttk", _designer_tab_label),
    group=GINPUT,
)


class CTkTextboxBO(CTkBaseMixin, BuilderObject):
    class_ = CTkTextbox
    OPTIONS_SPECIFIC = (
        "width",
        "height",
    )
    OPTIONS_CUSTOM = (
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "corner_radius",
        "text_font",
        "text_color",
    )
    properties = OPTIONS_SPECIFIC + OPTIONS_CUSTOM


_builder_uid = f"{_plugin_uid}.CTkTextbox"
register_widget(
    _builder_uid,
    CTkTextboxBO,
    "CTkTextbox",
    ("ttk", _designer_tab_label),
    group=GINPUT,
)


class CTkCanvasBO(CTkBaseMixin, TKCanvasBO):
    class_ = CTkCanvas


_builder_uid = f"{_plugin_uid}.CTkCanvas"
register_widget(
    _builder_uid,
    CTkCanvasBO,
    "CTkCanvas",
    ("ttk", _designer_tab_label),
    group=GDISPLAY,
)


class CTkScrollbarBO(CTkBaseMixin, BuilderObject):
    class_ = CTkScrollbar
    OPTIONS_SPECIFIC = ("width", "height", "orientation", "command")
    OPTIONS_CUSTOM = (
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "corner_radius",
        "scrollbar_color",
        "scrollbar_hover_color",
        "border_spacing",
        "minimum_pixel_length",
        "hover",
    )
    properties = OPTIONS_SPECIFIC + OPTIONS_CUSTOM


_builder_uid = f"{_plugin_uid}.CTkScrollbar"
register_widget(
    _builder_uid,
    CTkScrollbarBO,
    "CTkScrollbar",
    ("ttk", _designer_tab_label),
    group=GINPUT,
)
