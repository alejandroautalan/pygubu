from pygubu.api.v1 import register_widget
from pygubu.plugins.ttk.ttkstdwidgets import TTKCombobox
from pygubu.widgets.combobox import Combobox
from ._config import nspygubu, _section_widgets, GINPUT


class ComboboxBO(TTKCombobox):
    OPTIONS_SPECIFIC = tuple(set(TTKCombobox.OPTIONS_SPECIFIC) - {"state"})
    OPTIONS_CUSTOM = TTKCombobox.OPTIONS_CUSTOM + ("keyvariable",)
    properties = (
        TTKCombobox.OPTIONS_STANDARD
        + TTKCombobox.OPTIONS_SPECIFIC
        + OPTIONS_CUSTOM
    )
    tkvar_properties = TTKCombobox.tkvar_properties + ("keyvariable",)
    class_ = Combobox


ComboboxBuilder = ComboboxBO  # Alias for future rename of builder.


register_widget(
    nspygubu.widgets.Combobox,
    ComboboxBO,
    "Combobox",
    _section_widgets,
    group=GINPUT,
)

# Register old name until removal
register_widget(nspygubu.builder_old.combobox, ComboboxBO, public=False)
