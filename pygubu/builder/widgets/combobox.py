# encoding: utf8
from pygubu import register_custom_property, register_widget
from pygubu.builder.ttkstdwidgets import TTKCombobox
from pygubu.widgets.combobox import Combobox


class ComboboxBuilder(TTKCombobox):
    OPTIONS_SPECIFIC = tuple(
        set(TTKCombobox.OPTIONS_SPECIFIC) - set(('state',)))
    OPTIONS_CUSTOM = TTKCombobox.OPTIONS_CUSTOM + ('keyvariable',)
    properties = (TTKCombobox.OPTIONS_STANDARD + TTKCombobox.OPTIONS_SPECIFIC
                  + OPTIONS_CUSTOM)
    tkvar_properties = TTKCombobox.tkvar_properties + ('keyvariable',)
    class_ = Combobox


_builder_id = 'pygubu.builder.widgets.combobox'
register_widget(_builder_id, ComboboxBuilder, 'Combobox',
                ('ttk', 'Pygubu Widgets'))

_help = 'Tk variable associated to the key value.'
register_custom_property(_builder_id, 'keyvariable', 'tkvarentry',
                         help=_help)
_help = 'Combobox state.'
register_custom_property(_builder_id, 'state', 'choice',
                         values=('', 'normal', 'disabled'),
                         state='readonly',
                         help=_help)
