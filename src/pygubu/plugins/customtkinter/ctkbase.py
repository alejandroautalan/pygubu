import os
import tkinter as tk
import customtkinter
from pathlib import Path
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.i18n import _
from pygubu.plugins.tk.tkstdwidgets import TKFrame as TKFrameBO
from pygubu.utils.font import tkfontstr_to_dict
from pygubu.stockimage import StockImage
from ..customtkinter import _designer_tab_label, _plugin_uid
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass
from customtkinter import CTkFont, CTkImage
from PIL import Image, ImageTk


# Groups for ordering buttons in designer palette.
GCONTAINER = 0
GDISPLAY = 1
GINPUT = 2


_use_fixed_image_class = False

if os.getenv("PYGUBU_DESIGNER_RUNNING"):
    _use_fixed_image_class = True

    class CTKImageFix(CTkImage):
        "Fix loader for pygubu designer toplevel preview"

        def __init__(
            self,
            light_image: "Image.Image" = None,
            dark_image: "Image.Image" = None,
            size=(20, 20),
            tk_master=None,
        ):
            super().__init__(light_image, dark_image, size)
            self._tk_master = tk_master

        def _get_scaled_light_photo_image(
            self, scaled_size
        ) -> "ImageTk.PhotoImage":
            if scaled_size in self._scaled_light_photo_images:
                return self._scaled_light_photo_images[scaled_size]
            else:
                self._scaled_light_photo_images[
                    scaled_size
                ] = ImageTk.PhotoImage(
                    self._light_image.resize(scaled_size),
                    master=self._tk_master,
                )
                return self._scaled_light_photo_images[scaled_size]

        def _get_scaled_dark_photo_image(
            self, scaled_size
        ) -> "ImageTk.PhotoImage":
            if scaled_size in self._scaled_dark_photo_images:
                return self._scaled_dark_photo_images[scaled_size]
            else:
                self._scaled_dark_photo_images[
                    scaled_size
                ] = ImageTk.PhotoImage(
                    self._dark_image.resize(scaled_size), master=self._tk_master
                )
                return self._scaled_dark_photo_images[scaled_size]


def ctk_image_loader(source_type, source, tk_master):
    if _use_fixed_image_class:
        return CTKImageFix(Image.open(source), tk_master=tk_master)
    return CTkImage(Image.open(source))


int_properties = {
    "border_width": {},
    "border_spacing": {},
    "button_corner_radius": {},
    "button_length": {},
    "corner_radius": {},
    "height": {},
    "from_": {},
    "to": {},
    "number_of_steps": {},
    "width": {},
    "checkbox_width": {},
    "checkbox_height": {},
    "radiobutton_width": {},
    "radiobutton_height": {},
    "border_width_unchecked": {},
    "border_width_checked": {},
    "switch_width": {},
    "switch_height": {},
    "minimum_pixel_length": {},
    "determinate_speed": {"editor": "realnumber"},
    "indeterminate_speed": {"editor": "realnumber"},
    # "": {},
}

bool_properties = {
    "dynamic_resizing": {},
    "hover": {},
    "activate_scrollbars": {},
    "round_width_to_even_numbers": {},
    "round_height_to_even_numbers": {},
    # "": {},
}

font_properties = {
    "font": {},
    "dropdown_text_font": {},
    "dropdown_font": {},
    "label_font": {},
    # "": {},
}


class CTkBaseMixin:
    uses_ctk_font = False
    uses_ctk_image = False

    def _can_set_tcl_widget_name(self) -> bool:
        """Returns True if widget accepts the tcl "name" init argument."""
        return False

    def _process_property_value(self, pname, value):
        if pname in bool_properties:
            return tk.getboolean(value)
        if pname in int_properties:
            return float(value)
        if pname in font_properties:
            fdesc = tkfontstr_to_dict(value)
            _modifiers = (
                [] if fdesc["modifiers"] is None else fdesc["modifiers"]
            )
            family = fdesc["family"]
            size = None if fdesc["size"] is None else int(fdesc["size"])
            weight = "bold" if "bold" in _modifiers else None
            slant = "italic" if "italic" in _modifiers else "roman"
            underline = True if "underline" in _modifiers else False
            overstrike = True if "overstrike" in _modifiers else False
            _font = CTkFont(family, size, weight, slant, underline, overstrike)
            return _font
        if pname == "image":
            name = Path(value).name
            if not StockImage.is_registered(name):
                StockImage.find_and_register(name)
            img = StockImage.get(value, ctk_image_loader)
            return img
        return super()._process_property_value(pname, value)

    #
    # Code generation methods
    #

    def _code_process_property_value(self, targetid, pname, value: str):
        if (
            pname in int_properties
            or pname in bool_properties
            or pname in font_properties
        ):
            return super()._process_property_value(pname, value)
        return super()._code_process_property_value(targetid, pname, value)

    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname in font_properties:
            CTkBaseMixin.uses_ctk_font = True
            fdesc = tkfontstr_to_dict(value)
            _modifiers = (
                [] if fdesc["modifiers"] is None else fdesc["modifiers"]
            )
            family = f'"{fdesc["family"]}"'
            size = None if fdesc["size"] is None else int(fdesc["size"])
            weight = '"bold"' if "bold" in _modifiers else None
            slant = '"italic"' if "italic" in _modifiers else '"roman"'
            underline = True if "underline" in _modifiers else False
            overstrike = True if "overstrike" in _modifiers else False

            fvalue = f"CTkFont({family}, {size}, {weight}, {slant}, {underline}, {overstrike})"
            code_bag[pname] = fvalue
        elif pname == "image":
            CTkBaseMixin.uses_ctk_image = True
            lines = [
                f'_img = Image.open("{value}")',
                f"{targetid}.configure(image=CTkImage(_img))",
            ]
            code_bag[pname] = lines
        else:
            super()._code_set_property(targetid, pname, value, code_bag)

    def code_imports(self):
        imports = [
            ("customtkinter", self.class_.__name__),
        ]
        if CTkBaseMixin.uses_ctk_font:
            imports.append(("customtkinter", "CTkFont"))
        if CTkBaseMixin.uses_ctk_image:
            imports.append(("customtkinter", "CTkImage"))
            imports.append(("PIL", "Image"))
        return imports


# I will register here all common properties used by customtkinter widgets
# so I don't have to repeat for each one (notice the .* at end of _builder_uid):
_builder_uid = f"{_plugin_uid}.*"

color_properties = {
    "bg_color": {
        "help": _("Color behind the widget if it has rounded corners.")
    },
    "border_color": {},
    "button_color": {},
    "button_hover_color": {},
    "checkmark_color": {},
    "dropdown_color": {},
    "dropdown_hover_color": {},
    "dropdown_text_color": {},
    "dropdown_fg_color": {},
    "fg_color": {"help": _("Main color of the widget.")},
    "hover_color": {},
    "placeholder_text_color": {},
    "progress_color": {},
    "segmented_button_fg_color": {},
    "segmented_button_selected_color": {},
    "segmented_button_selected_hover_color": {},
    "segmented_button_unselected_color": {},
    "segmented_button_unselected_hover_color": {},
    "text_color": {},
    "text_color_disabled": {},
    "scrollbar_button_color": {},
    "scrollbar_button_hover_color": {},
    "scrollbar_fg_color": {},
    "background_corner_colors": {},
    "label_fg_color": {},
    "label_text_color": {},
    # "": {},
}

for color in color_properties:
    register_custom_property(
        _builder_uid, color, "colorentry", **color_properties[color]
    )

for prop in int_properties:
    editor = int_properties[prop].pop("editor", "naturalnumber")
    register_custom_property(_builder_uid, prop, editor, **int_properties[prop])

for prop in bool_properties:
    register_custom_property(
        _builder_uid,
        prop,
        "choice",
        values=("", "True", "False"),
        state="readonly",
        **bool_properties[prop],
    )

for prop in font_properties:
    register_custom_property(_builder_uid, prop, "fontentry")

register_custom_property(_builder_uid, "placeholder_text", "entry")
register_custom_property(_builder_uid, "command", "simplecommandentry")
register_custom_property(_builder_uid, "text", "text")
register_custom_property(_builder_uid, "values", "entry")
register_custom_property(_builder_uid, "variable", "tkvarentry")
register_custom_property(_builder_uid, "label_text", "text")


register_custom_property(
    _builder_uid,
    "orientation",
    "choice",
    values=("vertical", "horizontal"),
    state="readonly",
    default_value="horizontal",
)
register_custom_property(
    _builder_uid,
    "state",
    "choice",
    values=("", "normal", "active", "disabled"),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "appearance_mode",
    "choice",
    values=("", "dark", "light"),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "color_theme",
    "choice",
    values=("", "blue", "green", "dark-blue", "sweetkind"),
    state="readonly",
    help=_("Default color theme."),
)
