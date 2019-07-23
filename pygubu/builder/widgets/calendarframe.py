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
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM

register_widget('pygubu.builder.widgets.calendarframe', CalendarFrameBuilder,
                'CalendarFrame', ('ttk', 'Pygubu Widgets'))

props = {
    'state': {
        'editor': 'choice',
        'pygubu.builder.widgets.calendarframe': {
            'params': {
                'values': ('', 'normal', 'disabled'),
                'state': 'readonly'}},
        },
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

