# encoding: utf-8
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.ttk.ttkstdwidgets import TTKCombobox
from pygubu.i18n import _
from pygubu.widgets.combobox import Combobox


class ComboboxBuilder(TTKCombobox):
    OPTIONS_SPECIFIC = tuple(
        set(TTKCombobox.OPTIONS_SPECIFIC) - set(("state",))
    )
    OPTIONS_CUSTOM = TTKCombobox.OPTIONS_CUSTOM + ("keyvariable",)
    properties = (
        TTKCombobox.OPTIONS_STANDARD
        + TTKCombobox.OPTIONS_SPECIFIC
        + OPTIONS_CUSTOM
    )
    tkvar_properties = TTKCombobox.tkvar_properties + ("keyvariable",)
    class_ = Combobox


ComboboxBO = ComboboxBuilder  # Alias for future rename of builder.


_builder_id = "pygubu.builder.widgets.combobox"
register_widget(
    _builder_id, ComboboxBuilder, "Combobox", ("ttk", _("Pygubu Widgets"))
)

_help_values = _(
    "In designer: json list of key, value pairs\n"
    '    Example: [["A", "Option 1 Label"], ["B", "Option 2 Label"]]\n'
    "In code: an iterable of key, value pairs"
)
register_custom_property(_builder_id, "values", "entry", help=_help_values)

_help = "Tk variable associated to the key value."
register_custom_property(_builder_id, "keyvariable", "tkvarentry", help=_help)
_help = "Combobox state."
register_custom_property(
    _builder_id,
    "state",
    "choice",
    values=("", "normal", "disabled"),
    state="readonly",
    help=_help,
)
