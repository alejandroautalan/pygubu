# encoding: utf8
from pygubu import BuilderObject, register_widget, register_property
from pygubu.builder.ttkstdwidgets import TTKFrame
from pygubu.widgets.calendarframe import CalendarFrame


class CalendarFrameBuilder(BuilderObject):
    class_ = CalendarFrame
    OPTIONS_STANDARD = TTKFrame.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = TTKFrame.OPTIONS_SPECIFIC
    OPTIONS_CUSTOM = ('firstweekday', 'year', 'month',
                      'calendarfg', 'calendarbg', 'headerfg', 'headerbg',
                      'selectbg', 'selectfg', 'state', 'markbg', 'markfg')
    ro_properties = TTKFrame.ro_properties
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    virtual_events = ('<<CalendarFrameDateSelected>>',)

_builder_id = 'pygubu.builder.widgets.calendarframe'
register_widget(_builder_id, CalendarFrameBuilder,
                'CalendarFrame', ('ttk', 'Pygubu Widgets'))

props = {
    'state': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'choice',
                'values': ('', 'normal', 'disabled'),
                'state': 'readonly'}},
        },
    'firstweekday': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'choice',
                'values': ('0', '6'), 'state': 'readonly'},
            'default': '6',
            }
        },
    'year': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'entry'}
            }
        },
    'month': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'choice',
                'values': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                           '11', '12'), 'state': 'readonly'},
            'default': '1'
            }
        },
# Better to change locale by code.
#    'locale': {
#        'editor': 'entry'
#        },
    'calendarfg': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'colorentry'},
            }
        },
    'calendarbg': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'colorentry'}
            }
        },
    'headerfg': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'colorentry'}
            }
        },
    'headerbg': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'colorentry'}
            }
        },
    'selectbg': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'colorentry'}
            }
        },
    'selectfg': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'colorentry'}
            }
        },
    'markbg': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'colorentry'}
            }
        },
    'markfg': {
        'editor': 'dynamic',
        _builder_id: {
            'params': {
                'mode': 'colorentry'}
            }
        }
    }

for p in props:
    register_property(p, props[p])

