from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.i18n import _
from pygubu.plugins.tk.tkstdwidgets import TKFrame as TKFrameBO
from pygubu.plugins.tk.tkstdwidgets import TKLabel as TKLabelBO
from pygubu.plugins.tk.tkstdwidgets import TKEntry as TKEntryBO
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkButton,
    CTkProgressBar,
    CTkSlider,
    CTkEntry,
)

from ..customtkinter import _designer_tab_label, _plugin_uid
from .ctkbase import CTkBaseMixin


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
    group=0,
)
register_custom_property(_builder_uid, "bg_color", "colorentry")
register_custom_property(_builder_uid, "fg_color", "colorentry")
register_custom_property(_builder_uid, "border_color", "colorentry")
register_custom_property(_builder_uid, "border_width", "entry")
register_custom_property(_builder_uid, "corner_radius", "entry")


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
    group=1,
)
register_custom_property(_builder_uid, "bg_color", "colorentry")
register_custom_property(_builder_uid, "fg_color", "colorentry")
register_custom_property(_builder_uid, "border_color", "colorentry")
register_custom_property(_builder_uid, "border_width", "entry")
register_custom_property(_builder_uid, "corner_radius", "entry")


class CTkProgressBarBO(CTkBaseMixin, BuilderObject):
    class_ = CTkProgressBar
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
    group=1,
)


class CTkButtonBO(CTkBaseMixin, BuilderObject):
    class_ = CTkButton
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
    group=1,
)

register_custom_property(_builder_uid, "bg_color", "colorentry")
register_custom_property(_builder_uid, "fg_color", "colorentry")
register_custom_property(_builder_uid, "border_color", "colorentry")
register_custom_property(_builder_uid, "border_width", "entry")
register_custom_property(_builder_uid, "corner_radius", "entry")
register_custom_property(_builder_uid, "hover_color", "colorentry")
register_custom_property(_builder_uid, "text_color", "colorentry")
register_custom_property(_builder_uid, "text_color_disabled", "colorentry")
register_custom_property(_builder_uid, "text_font", "fontentry")
register_custom_property(
    _builder_uid,
    "hover",
    "choice",
    values=("", "True", "False"),
    state="readonly",
)


class CTkSliderBO(CTkBaseMixin, BuilderObject):
    class_ = CTkSlider
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
    group=1,
)

register_custom_property(_builder_uid, "bg_color", "colorentry")
register_custom_property(_builder_uid, "fg_color", "colorentry")
register_custom_property(_builder_uid, "border_color", "colorentry")
register_custom_property(_builder_uid, "border_width", "entry")
register_custom_property(_builder_uid, "corner_radius", "entry")
register_custom_property(_builder_uid, "progress_color", "colorentry")
register_custom_property(_builder_uid, "button_color", "colorentry")
register_custom_property(_builder_uid, "button_hover_color", "colorentry")
register_custom_property(_builder_uid, "button_corner_radius", "entry")
register_custom_property(_builder_uid, "button_length", "entry")
register_custom_property(_builder_uid, "number_of_steps", "entry")


class CTkEntryBO(CTkBaseMixin, TKEntryBO):
    class_ = CTkEntry
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
    group=1,
)

register_custom_property(_builder_uid, "bg_color", "colorentry")
register_custom_property(_builder_uid, "fg_color", "colorentry")
register_custom_property(_builder_uid, "border_color", "colorentry")
register_custom_property(_builder_uid, "border_width", "entry")
register_custom_property(_builder_uid, "corner_radius", "entry")
register_custom_property(_builder_uid, "text_color", "colorentry")
register_custom_property(_builder_uid, "placeholder_text_color", "colorentry")
register_custom_property(_builder_uid, "text_font", "fontentry")
register_custom_property(_builder_uid, "placeholder_text", "entry")
