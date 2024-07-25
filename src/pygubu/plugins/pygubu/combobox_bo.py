# encoding: utf-8
from pygubu.api.v1 import register_widget
from pygubu.plugins.ttk.ttkstdwidgets import TTKCombobox
from pygubu.widgets.combobox import Combobox
from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid


class ComboboxBO(TTKCombobox):
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


ComboboxBuilder = ComboboxBO  # Alias for future rename of builder.


_builder_id = f"{_plugin_uid}.Combobox"
register_widget(
    _builder_id, ComboboxBO, "Combobox", ("ttk", _tab_widgets_label)
)

# Register old name until removal
register_widget("pygubu.builder.widgets.combobox", ComboboxBO, public=False)
