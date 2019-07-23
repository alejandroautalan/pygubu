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

register_widget('pygubu.builder.widgets.combobox', ComboboxBuilder, 'Combobox',
                ('ttk', 'Pygubu Widgets'))

props = {
    'keyvariable': {
        'editor': 'tkvarentry'
        },
    'state': {
        'editor': 'choice',
        'pygubu.builder.widgets.combobox': {
            'params': {
                'values': ('', 'normal', 'disabled'),
                'state': 'readonly'}},
        }
    }

for p in props:
    register_property(p, props[p])
