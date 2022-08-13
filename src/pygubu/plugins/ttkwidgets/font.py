import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.tk.tkstdwidgets import TKListbox
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame, TTKCombobox
from ttkwidgets.font import (
    FontFamilyDropdown,
    FontFamilyListbox,
    FontSelectFrame,
    FontPropertiesFrame,
    FontSizeDropdown,
)

from ..ttkwidgets import _designer_tab_label, _plugin_uid
from .utils import CallbakInitArgMixin
from .autocomplete import AutocompleteComboboxBO
from .scrolledlistbox import ScrolledListboxBO


class FontFamilyDropdownBO(CallbakInitArgMixin, AutocompleteComboboxBO):
    class_ = FontFamilyDropdown
    init_completevalues = False
    container = False
    OPTIONS_SPECIFIC = tuple(
        set(AutocompleteComboboxBO.OPTIONS_SPECIFIC) - set(("textvariable",))
    )
    OPTIONS_CUSTOM = ("callback",)
    properties = (
        AutocompleteComboboxBO.OPTIONS_STANDARD
        + OPTIONS_SPECIFIC
        + OPTIONS_CUSTOM
    )
    ro_properties = TTKCombobox.ro_properties
    command_properties = ("callback",)

    def _code_define_callback_args(self, cmd_pname, cmd):
        args = None
        if cmd_pname == "callback":
            args = ("family",)
        else:
            args = super()._code_define_callback_args(cmd_pname, cmd)
        return args


_builder_uid = f"{_plugin_uid}.FontFamilyDropdown"
register_widget(
    _builder_uid,
    FontFamilyDropdownBO,
    "FontFamilyDropdown",
    ("ttk", _designer_tab_label),
)

register_custom_property(
    _builder_uid,
    "callback",
    "simplecommandentry",
    help=_(
        "name of the callback function with one argument: the font family name"
    ),
)


class FontFamilyListboxBO(CallbakInitArgMixin, ScrolledListboxBO):
    class_ = FontFamilyListbox
    container = False
    OPTIONS_STANDARD = tuple(
        set(TKListbox.OPTIONS_STANDARD)
        - set(("xscrollcommand", "yscrollcommand"))
    )
    OPTIONS_SPECIFIC = tuple(
        set(TKListbox.OPTIONS_SPECIFIC) - set(("listvariable",))
    )
    OPTIONS_CUSTOM = ("autohidescrollbar", "callback")
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = TKListbox.ro_properties + ("autohidescrollbar",)
    command_properties = ("callback",)

    def _process_property_value(self, pname, value):
        if pname == "autohidescrollbar":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def _code_process_property_value(self, targetid, pname, value):
        if pname == "autohidescrollbar":
            return tk.getboolean(value)
        return super()._code_process_property_value(targetid, pname, value)

    def _code_define_callback_args(self, cmd_pname, cmd):
        args = None
        if cmd_pname == "callback":
            args = ("family",)
        else:
            args = super()._code_define_callback_args(cmd_pname, cmd)
        return args


_builder_uid = f"{_plugin_uid}.FontFamilyListbox"
register_widget(
    _builder_uid,
    FontFamilyListboxBO,
    "FontFamilyListbox",
    ("ttk", _designer_tab_label),
)

register_custom_property(
    _builder_uid,
    "autohidescrollbar",
    "choice",
    values=("", "true", "false"),
    state="readonly",
)
register_custom_property(
    _builder_uid,
    "callback",
    "simplecommandentry",
    help=_(
        "name of the callback function with one argument: the font family name"
    ),
)


class FontSelectFrameBO(CallbakInitArgMixin, TTKFrame):
    class_ = FontSelectFrame
    container = False
    OPTIONS_CUSTOM = ("callback",)
    properties = (
        TTKFrame.OPTIONS_STANDARD + TTKFrame.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = TTKFrame.ro_properties + OPTIONS_CUSTOM
    command_properties = ("callback",)

    def _code_define_callback_args(self, cmd_pname, cmd):
        args = None
        if cmd_pname == "callback":
            args = ("family", "size", "bold", "italic", "underline")
        else:
            args = super(FontSelectFrameBO, self)._code_define_callback_args(
                cmd_pname, cmd
            )
        return args


_builder_uid = f"{_plugin_uid}.FontSelectFrame"
register_widget(
    _builder_uid,
    FontSelectFrameBO,
    "FontSelectFrame",
    ("ttk", _designer_tab_label),
)

register_custom_property(
    _builder_uid,
    "callback",
    "simplecommandentry",
    help=_(
        "name of the callback function with arguments: (family: str, size: int, bold: bool, italic: bool, underline: bool)"
    ),
)


class FontPropertiesFrameBO(CallbakInitArgMixin, TTKFrame):
    class_ = FontPropertiesFrame
    container = False
    OPTIONS_CUSTOM = ("callback", "label", "fontsize")
    properties = (
        TTKFrame.OPTIONS_STANDARD + TTKFrame.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = TTKFrame.ro_properties + OPTIONS_CUSTOM
    command_properties = ("callback",)

    def _process_property_value(self, pname, value):
        if pname == "label":
            return tk.getboolean(value)
        if pname == "fontsize":
            return int(value)
        return super()._process_property_value(pname, value)

    def _code_define_callback_args(self, cmd_pname, cmd):
        if cmd_pname == "callback":
            return ("family", "size", "bold", "italic", "underline")
        return super()._code_define_callback_args(cmd_pname, cmd)


_builder_uid = f"{_plugin_uid}.FontPropertiesFrame"
register_widget(
    _builder_uid,
    FontPropertiesFrameBO,
    "FontPropertiesFrame",
    ("ttk", _designer_tab_label),
)

register_custom_property(
    _builder_uid,
    "callback",
    "simplecommandentry",
    help=_(
        "name of the callback function with arguments: (bold: bool, italic: bool, underline: bool, overstrike: bool)"
    ),
)
register_custom_property(
    _builder_uid,
    "label",
    "choice",
    values=("", "true", "false"),
    default_value="true",
    state="readonly",
    help=_("Show/hide Header label"),
)
register_custom_property(
    _builder_uid,
    "fontsize",
    "naturalnumber",
    help=_("size of the font on the buttons"),
)


class FontSizeDropdownBO(CallbakInitArgMixin, AutocompleteComboboxBO):
    class_ = FontSizeDropdown
    init_completevalues = False
    container = False
    OPTIONS_SPECIFIC = tuple(
        set(AutocompleteComboboxBO.OPTIONS_SPECIFIC) - set(("textvariable",))
    )
    OPTIONS_CUSTOM = ("callback",)
    properties = (
        AutocompleteComboboxBO.OPTIONS_STANDARD
        + OPTIONS_SPECIFIC
        + OPTIONS_CUSTOM
    )
    ro_properties = TTKCombobox.ro_properties
    command_properties = ("callback",)

    def _code_define_callback_args(self, cmd_pname, cmd):
        args = None
        if cmd_pname == "callback":
            args = ("size",)
        else:
            args = super(FontSizeDropdownBO, self)._code_define_callback_args(
                cmd_pname, cmd
            )
        return args


_builder_uid = f"{_plugin_uid}.FontSizeDropdown"
register_widget(
    _builder_uid,
    FontSizeDropdownBO,
    "FontSizeDropdown",
    ("ttk", _designer_tab_label),
)

register_custom_property(
    _builder_uid,
    "callback",
    "simplecommandentry",
    help=_(
        "name of the callback function on click with single argument: size: int"
    ),
)
