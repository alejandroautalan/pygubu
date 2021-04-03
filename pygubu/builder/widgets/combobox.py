# encoding: utf8
from pygubu import BuilderObject, register_widget, register_property
from pygubu.builder.ttkstdwidgets import TTKCombobox
from pygubu.widgets.combobox import Combobox


class ComboboxBuilder(TTKCombobox):
    OPTIONS_SPECIFIC = tuple(set(TTKCombobox.OPTIONS_SPECIFIC) - set(('state',)))
    OPTIONS_CUSTOM = TTKCombobox.OPTIONS_CUSTOM + ('keyvariable',)
    properties = (TTKCombobox.OPTIONS_STANDARD + TTKCombobox.OPTIONS_SPECIFIC +
                  OPTIONS_CUSTOM)
    tkvar_properties = TTKCombobox.tkvar_properties + ('keyvariable',)
    class_ = Combobox

_builder_id = 'pygubu.builder.widgets.combobox'
register_widget(_builder_id, ComboboxBuilder, 'Combobox',
                ('ttk', 'Pygubu Widgets'))

props = {
    'keyvariable': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'tkvarentry'},
            'help': 'Tk variable associated to the key value.'
            }
        },
    'state': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'choice',
                'values': ('', 'normal', 'disabled'),
                'state': 'readonly'},
            'help': 'Combobox state.'
        },
    }
}

for p in props:
    register_property(p, props[p])
