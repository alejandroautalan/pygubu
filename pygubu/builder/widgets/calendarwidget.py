from pygubu import BuilderObject, register_widget, register_property
from pygubu.builder.ttkstdwidgets import TTKFrame
from pygubu.widgets.calendarwidget import Calendar


class CalendarBuilder(BuilderObject):
    class_ = Calendar
    OPTIONS_STANDARD = TTKFrame.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = TTKFrame.OPTIONS_SPECIFIC
    OPTIONS_CUSTOM = ('firstweekday', 'year', 'month',
                      'calendarfg', 'calendarbg', 'headerfg', 'headerbg',
                      'selectbg', 'selectfg', 'markbg', 'markfg')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM

register_widget('pygubu.builder.widgets.calendarwidget', CalendarBuilder,
                'Calendar', ('ttk', 'Pygubu Widgets'))

props = {
    'firstweekday': {
        'editor': 'choice',
        'params': {
            'values': ('0', '6'), 'state': 'readonly'},
        'default': '6'
        },
    'year': {
        'editor': 'entry'
        },
    'month': {
        'editor': 'choice',
        'params': {
            'values': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                       '11', '12'), 'state': 'readonly'},
        'default': '1'
        },
# Better to change locale by code.
#    'locale': {
#        'editor': 'entry'
#        },
    'calendarfg': {
        'editor': 'colorentry'
        },
    'calendarbg': {
        'editor': 'colorentry'
        },
    'headerfg': {
        'editor': 'colorentry'
        },
    'headerbg': {
        'editor': 'colorentry'
        },
    'selectbg': {
        'editor': 'colorentry'
        },
    'selectfg': {
        'editor': 'colorentry'
        },
    'markbg': {
        'editor': 'colorentry'
        },
    'markfg': {
        'editor': 'colorentry'
        }
    }

for p in props:
    register_property(p, props[p])

