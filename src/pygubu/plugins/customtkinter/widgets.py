import customtkinter as ctk
import pygubu.plugins.customtkinter.tabview
import pygubu.plugins.customtkinter.scrollableframe

from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.i18n import _
from pygubu.utils.datatrans import ListDTO
from pygubu.plugins.tk.tkstdwidgets import TKCanvas as TKCanvasBO

from ._config import nsctk, GCONTAINER, GDISPLAY, GINPUT, _designer_tabs
from .ctkbase import CTkBaseMixin


class CTkFrameBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkFrame
    container = True
    container_layout = True
    properties = (
        "width",
        "height",
        "corner_radius",
        "border_width",
        "bg_color",
        "fg_color",
        "border_color",
        "background_corner_colors",
    )


register_widget(
    nsctk.CTkFrame,
    CTkFrameBO,
    "CTkFrame",
    _designer_tabs,
    group=GCONTAINER,
)


class CTkLabelBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkLabel
    properties = (
        "anchor",
        "compound",
        "cursor",
        "image",
        "justify",
        "font",
        "height",
        "padx",
        "pady",
        "state",
        "takefocus",
        "text",
        "textvariable",
        "underline",
        "width",
        # CTK properties
        "corner_radius",
        "bg_color",
        "fg_color",
        "text_color",
        "text_color_disabled",
        "border_color",
        "border_width",
    )


register_widget(
    nsctk.CTkLabel,
    CTkLabelBO,
    "CTkLabel",
    _designer_tabs,
    group=GDISPLAY,
)


class CTkProgressBarBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkProgressBar
    allow_bindings = False
    properties = (
        "width",
        "height",
        "variable",
        "mode",
        "orientation",
        # CTK properties
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "corner_radius",
        "progress_color",
        "determinate_speed",
        "indeterminate_speed",
    )
    ro_properties = ("orientation",)


register_widget(
    nsctk.CTkProgressBar,
    CTkProgressBarBO,
    "CTkProgressBar",
    _designer_tabs,
    group=GDISPLAY,
)


class CTkButtonBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkButton
    allow_bindings = False
    properties = (
        "text",
        "width",
        "height",
        "textvariable",
        "image",
        "compound",
        "state",
        "command",
        # CTK properties
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "border_spacing",
        "corner_radius",
        "hover_color",
        "text_color",
        "text_color_disabled",
        "hover",
        "font",
        "background_corner_colors",
        "round_width_to_even_numbers",
        "round_height_to_even_numbers",
        "anchor",
    )
    command_properties = ("command",)
    ro_properties = ("hover",)


register_widget(
    nsctk.CTkButton,
    CTkButtonBO,
    "CTkButton",
    _designer_tabs,
    group=GINPUT,
)


class CTkSliderBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkSlider
    allow_bindings = False
    properties = (
        "width",
        "height",
        "variable",
        "from_",
        "to",
        "command",
        "state",
        # CTK properties
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
        "orientation",
    )
    command_properties = ("command",)
    ro_properties = (
        "orientation",
        "button_length",
    )

    def _code_define_callback_args(self, cmd_pname, cmd):
        return ("value",)


register_widget(
    nsctk.CTkSlider,
    CTkSliderBO,
    "CTkSlider",
    _designer_tabs,
    group=GINPUT,
)


class CTkEntryBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkEntry
    allow_bindings = False
    properties = (
        "cursor",
        "exportselection",
        "font",
        "insertborderwidth",
        "insertofftime",
        "insertontime",
        "insertwidth",
        "justify",
        "selectborderwidth",
        "takefocus",
        "textvariable",
        "xscrollcommand",
        # specific
        "readonlybackground",
        "show",
        "state",
        "validate",
        "validatecommand",
        "width",
        # custom
        "text",
        # CTK options
        "bg_color",
        "fg_color",
        "border_color",
        "border_width",
        "corner_radius",
        "text_color",
        "placeholder_text_color",
        "placeholder_text",
    )
    # CTkEntry does not accept invalidcommand, so it is not offered above and
    # is not listed here.
    command_properties = ("validatecommand", "xscrollcommand")

    def _set_property(self, target_widget, pname, value):
        if pname == "text":
            target_widget.delete(0, "end")
            if value:
                target_widget.insert(0, value)
        else:
            super()._set_property(target_widget, pname, value)

    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == "text":
            sval = self.builder.code_translate_str(value)
            lines = [
                f"""{targetid}.delete(0, "end")""",
                f"{targetid}.insert(0, {sval})",
            ]
            code_bag[pname] = lines
        else:
            super()._code_set_property(targetid, pname, value, code_bag)


register_widget(
    nsctk.CTkEntry,
    CTkEntryBO,
    "CTkEntry",
    _designer_tabs,
    group=GINPUT,
)


_list_dto = ListDTO()


class CTkOptionMenuBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkOptionMenu
    allow_bindings = False
    properties = (
        "command",
        "variable",
        "values",
        "bg_color",
        "fg_color",
        "button_color",
        "button_hover_color",
        "text_color",
        "text_color_disabled",
        "dropdown_hover_color",
        "dropdown_text_color",
        "dropdown_color",
        "dropdown_font",
        "width",
        "height",
        "corner_radius",
        "state",
        "dynamic_resizing",
        "font",
    )
    command_properties = ("command",)

    def _process_property_value(self, pname, value):
        if pname == "values":
            return _list_dto.transform(value)
        return super()._process_property_value(pname, value)

    def _code_define_callback_args(self, cmd_pname, cmd):
        return ("current_value",)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname == "values":
            return super()._process_property_value(pname, value)
        return super()._code_process_property_value(targetid, pname, value)


register_widget(
    nsctk.CTkOptionMenu,
    CTkOptionMenuBO,
    "CTkOptionMenu",
    _designer_tabs,
    group=GINPUT,
)


class CTkComboBoxBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkComboBox
    allow_bindings = False
    properties = (
        "corner_radius",
        "border_width",
        "bg_color",
        "fg_color",
        "border_color",
        "button_color",
        "button_hover_color",
        "dropdown_fg_color",
        "dropdown_hover_color",
        "dropdown_text_color",
        "text_color",
        "text_color_disabled",
        "font",
        "dropdown_font",
        "command",
        "variable",
        "values",
        "width",
        "height",
        "state",
        "hover",
    )
    command_properties = ("command",)
    ro_properties = ("hover",)

    def _process_property_value(self, pname, value):
        if pname == "values":
            return _list_dto.transform(value)
        return super()._process_property_value(pname, value)

    def _code_define_callback_args(self, cmd_pname, cmd):
        return ("value",)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname == "values":
            return super()._process_property_value(pname, value)
        return super()._code_process_property_value(targetid, pname, value)


register_widget(
    nsctk.CTkComboBox,
    CTkComboBoxBO,
    "CTkComboBox",
    _designer_tabs,
    group=GINPUT,
)


class CTkCheckBoxBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkCheckBox
    allow_bindings = False
    properties = (
        "width",
        "height",
        "checkbox_width",
        "checkbox_height",
        "corner_radius",
        "border_width",
        "bg_color",
        "fg_color",
        "hover_color",
        "border_color",
        "checkmark_color",
        "text_color",
        "text_color_disabled",
        "text",
        "font",
        "textvariable",
        "state",
        "hover",
        "command",
        "onvalue",
        "offvalue",
        "variable",
    )
    command_properties = ("command",)
    ro_properties = ("hover", "onvalue", "offvalue")


register_widget(
    nsctk.CTkCheckBox,
    CTkCheckBoxBO,
    "CTkCheckBox",
    _designer_tabs,
    group=GINPUT,
)


class CTkRadioButtonBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkRadioButton
    allow_bindings = False
    properties = (
        "width",
        "height",
        "radiobutton_width",
        "radiobutton_height",
        "corner_radius",
        "border_width_unchecked",
        "border_width_checked",
        "bg_color",
        "fg_color",
        "hover_color",
        "border_color",
        "text_color",
        "text_color_disabled",
        "text",
        "font",
        "textvariable",
        "variable",
        "value",
        "state",
        "hover",
        "command",
    )
    command_properties = ("command",)
    ro_properties = ("hover", "value")


register_widget(
    nsctk.CTkRadioButton,
    CTkRadioButtonBO,
    "CTkRadioButton",
    _designer_tabs,
    group=GINPUT,
)


class CTkSwitchBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkSwitch
    allow_bindings = False
    properties = (
        "width",
        "height",
        "switch_width",
        "switch_height",
        "corner_radius",
        "border_width",
        "button_length",
        "bg_color",
        "fg_color",
        "border_color",
        "progress_color",
        "button_color",
        "button_hover_color",
        "text_color",
        "text_color_disabled",
        "text",
        "font",
        "textvariable",
        "onvalue",
        "offvalue",
        "variable",
        "hover",
        "command",
        "state",
    )
    command_properties = ("command",)
    ro_properties = (
        "onvalue",
        "offvalue",
        "hover",
        "text_color",
        "text_color_disabled",
    )


register_widget(
    nsctk.CTkSwitch,
    CTkSwitchBO,
    "CTkSwitch",
    _designer_tabs,
    group=GINPUT,
)


class CTkTextboxBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkTextbox
    properties = (
        "autoseparators",
        "cursor",
        "exportselection",
        "insertborderwidth",
        "insertofftime",
        "insertontime",
        "insertwidth",
        "maxundo",
        "padx",
        "pady",
        "selectborderwidth",
        "spacing1",
        "spacing2",
        "spacing3",
        "state",
        "tabs",
        "takefocus",
        "undo",
        "wrap",
        # ctk
        "width",
        "height",
        "corner_radius",
        "border_width",
        "border_spacing",
        "bg_color",
        "fg_color",
        "border_color",
        "text_color",
        "font",
        "scrollbar_button_color",
        "scrollbar_button_hover_color",
        "activate_scrollbars",
        # custom
        "text",
    )

    def _set_property(self, target_widget, pname, value):
        if pname == "text":
            target_widget = target_widget._textbox
            state = target_widget.cget("state")
            if state == ctk.DISABLED:
                target_widget.configure(state=ctk.NORMAL)
                target_widget.delete("0.0", "end")
                if value:
                    target_widget.insert("0.0", value)
                target_widget.configure(state=ctk.DISABLED)
            else:
                target_widget.delete("0.0", "end")
                if value:
                    target_widget.insert("0.0", value)
        else:
            super()._set_property(target_widget, pname, value)

    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == "text":
            state_value = ""
            if "state" in self.wmeta.properties:
                state_value = self.wmeta.properties["state"]
            sval = self.builder.code_translate_str(value)
            lines = [
                f"_text_ = {sval}",
            ]
            if state_value == ctk.DISABLED:
                lines.extend(
                    (
                        f'{targetid}.configure(state="normal")',
                        f'{targetid}.delete("0.0", "end")',
                        f'{targetid}.insert("0.0", _text_)',
                        f'{targetid}.configure(state="disabled")',
                    )
                )
            else:
                lines.extend(
                    (
                        f'{targetid}.delete("0.0", "end")',
                        f'{targetid}.insert("0.0", _text_)',
                    )
                )
            code_bag[pname] = lines
        else:
            super()._code_set_property(targetid, pname, value, code_bag)


register_widget(
    nsctk.CTkTextbox,
    CTkTextboxBO,
    "CTkTextbox",
    _designer_tabs,
    group=GINPUT,
)


class CTkScrollbarBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkScrollbar
    properties = (
        "width",
        "height",
        "orientation",
        "command",
        # CTK
        "cursor",
        "corner_radius",
        "border_spacing",
        "minimum_pixel_length",
        "bg_color",
        "fg_color",
        "button_color",
        "button_hover_color",
        "hover",
    )
    ro_properties = ("orientation", "cursor")
    command_properties = ("command",)


register_widget(
    nsctk.CTkScrollbar,
    CTkScrollbarBO,
    "CTkScrollbar",
    _designer_tabs,
    group=GINPUT,
)


class CTkSegmentedButtonBO(CTkBaseMixin, BuilderObject):
    class_ = ctk.CTkSegmentedButton
    allow_bindings = False
    properties = (
        "width",
        "height",
        "corner_radius",
        "border_width",
        "bg_color",
        "fg_color",
        "selected_color",
        "selected_hover_color",
        "unselected_color",
        "unselected_hover_color",
        "text_color",
        "text_color_disabled",
        "background_corner_colors",
        "font",
        "values",
        "variable",
        "dynamic_resizing",
        "command",
        "state",
    )
    command_properties = ("command",)
    ro_properties = ("hover",)

    def _process_property_value(self, pname, value):
        if pname == "values":
            return _list_dto.transform(value)
        return super()._process_property_value(pname, value)

    def _code_define_callback_args(self, cmd_pname, cmd):
        return ("current_value",)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname == "values":
            return super()._process_property_value(pname, value)
        return super()._code_process_property_value(targetid, pname, value)


register_widget(
    nsctk.CTkSegmentedButton,
    CTkSegmentedButtonBO,
    "CTkSegmentedButton",
    _designer_tabs,
    group=GINPUT,
)


class CTkCanvasBO(TKCanvasBO):
    class_ = ctk.CTkCanvas


register_widget(
    nsctk.CTkCanvas,
    CTkCanvasBO,
    "CTkCanvas",
    _designer_tabs,
    group=GDISPLAY,
)
