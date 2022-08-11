import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.ttk.ttkstdwidgets import TTKEntry, TTKFrame, TTKCombobox
from ttkwidgets.autocomplete import (
    AutocompleteEntry,
    AutocompleteEntryListbox,
    AutocompleteCombobox,
)

from ..ttkwidgets import _designer_tab_label, _plugin_uid
from .utils import AutocompleteBaseBO


class AutocompleteEntryBO(AutocompleteBaseBO, TTKEntry):
    class_ = AutocompleteEntry
    #
    # Note: completevalues property is managed by AutocompleteBaseBO
    #
    OPTIONS_CUSTOM = ("completevalues",)
    properties = (
        TTKEntry.OPTIONS_STANDARD + TTKEntry.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = TTKEntry.ro_properties + OPTIONS_CUSTOM

    def code_imports(self):
        return (("ttkwidgets.autocomplete", "AutocompleteEntry"),)


_builder_uid = f"{_plugin_uid}.AutocompleteEntry"

register_widget(
    _builder_uid,
    AutocompleteEntryBO,
    "AutocompleteEntry",
    ("ttk", _designer_tab_label),
    group=4,
)

register_custom_property(
    _builder_uid,
    "completevalues",
    "entry",
    help=_("Values separated by space. In code you can pass a full list"),
)


class AutocompleteEntryListboxBO(AutocompleteBaseBO, TTKFrame):
    class_ = AutocompleteEntryListbox
    container = False
    #
    # Note: completevalues property is managed by AutocompleteBaseBO
    #
    OPTIONS_CUSTOM = (
        "allow_other_values",
        "autohidescrollbar",
        "exportselection",
        "font",
        "justify",
        "completevalues",
    )
    properties = (
        TTKFrame.OPTIONS_STANDARD + TTKFrame.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = TTKFrame.ro_properties + ("completevalues",)

    def _process_property_value(self, pname, value):
        final_value = value
        if pname in (
            "autohidescrollbar",
            "allow_other_values",
            "exportselection",
        ):
            final_value = tk.getboolean(value)
        else:
            final_value = super(
                AutocompleteEntryListboxBO, self
            )._process_property_value(pname, value)
        return final_value

    def _code_process_property_value(self, targetid, pname, value):
        if pname in (
            "autohidescrollbar",
            "allow_other_values",
            "exportselection",
        ):
            return tk.getboolean(value)
        return super()._code_process_property_value(targetid, pname, value)


_builder_uid = f"{_plugin_uid}.AutocompleteEntryListbox"

register_widget(
    _builder_uid,
    AutocompleteEntryListboxBO,
    "AutocompleteEntryListbox",
    ("ttk", _designer_tab_label),
    group=4,
)

register_custom_property(
    _builder_uid,
    "autohidescrollbar",
    "choice",
    values=("", "true", "false"),
    state="readonly",
)

register_custom_property(
    _builder_uid, "font", "fontentry", help=_("font in entry and listbox")
)
register_custom_property(
    _builder_uid,
    "allow_other_values",
    "choice",
    values=("", "true", "false"),
    state="readonly",
    help=_("whether the user is allowed to enter values not in the list"),
)
register_custom_property(
    _builder_uid,
    "allow_other_values",
    "choice",
    values=("", "true", "false"),
    state="readonly",
    help=_("whether to automatically export selected text to the clipboard"),
)
register_custom_property(
    _builder_uid,
    "justify",
    "choice",
    values=("", "left", "center", "right"),
    state="readonly",
    help=_("text alignment in entry and listbox"),
)
register_custom_property(
    _builder_uid,
    "completevalues",
    "entry",
    help=_(
        "Values separated by space. In code you can pass a full python list."
    ),
)


class AutocompleteComboboxBO(AutocompleteBaseBO, TTKCombobox):
    class_ = AutocompleteCombobox
    OPTIONS_SPECIFIC = tuple(
        set(TTKCombobox.OPTIONS_SPECIFIC) - set(("values",))
    )
    OPTIONS_CUSTOM = ("completevalues",)
    properties = (
        TTKCombobox.OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    ro_properties = TTKCombobox.ro_properties + OPTIONS_CUSTOM


_builder_uid = f"{_plugin_uid}.AutocompleteCombobox"
register_widget(
    _builder_uid,
    AutocompleteComboboxBO,
    "AutocompleteCombobox",
    ("ttk", _designer_tab_label),
    group=4,
)

register_custom_property(
    _builder_uid,
    "completevalues",
    "entry",
    help=_("Values separated by space. In code you can pass a full list"),
)
