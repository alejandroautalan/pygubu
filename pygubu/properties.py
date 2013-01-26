#
# Copyright 2012 Alejandro Autalán
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  http://pygubu.web.here

from collections import OrderedDict
import tkinter
from tkinter import ttk


_default_entry_prop = {
    'input_method': 'entry',
}

_default_textentry_prop = {
    'input_method': 'textentry',
}

_default_color_prop = {
    'input_method': 'colorentry',
}

_default_spinbox_prop = {
    'input_method': 'spinbox',
    'min': 0,
    'max': 999,
    'validator': 'number_integer',
}

_default_spinbox_float_prop = {
    'input_method': 'spinbox',
    'min': 0,
    'max': 999,
    'validator': 'number_float',
    'increment': 0.1
}

_default_dimension_prop = {
    'input_method': 'spinbox',
    'min': 0,
    'max': 999,
    'validator': 'number_integer'
}

_default_relief_prop = {
    'input_method': 'choice',
    'values': ('', tkinter.FLAT, tkinter.RAISED, tkinter.SUNKEN,
        tkinter.GROOVE, tkinter.RIDGE)
}

_empty_choice = {'input_method': 'choice', 'readonly': True }

_default_true_false_prop = { 'input_method': 'choice',
    'values': ('', tkinter.TRUE, tkinter.FALSE)}

_default_cursor_prop = {
    'input_method': 'choice',
    'values': ('', 'arrow', 'based_arrow_down', 'based_arrow_up', 'boat',
        'bogosity', 'bottom_left_corner', 'bottom_right_corner',
        'bottom_side', 'bottom_tee', 'box_spiral', 'center_ptr', 'circle',
        'clock', 'coffee_mug', 'cross', 'cross_reverse', 'crosshair',
        'diamond_cross', 'dot', 'dotbox', 'double_arrow',  'draft_large',
        'draft_small', 'draped_box', 'exchange', 'fleur', 'gobbler',
        'gumby', 'hand1', 'hand2', 'heart', 'icon', 'iron_cross',
        'left_ptr', 'left_side', 'left_tee', 'leftbutton', 'll_angle',
        'lr_angle', 'man', 'middlebutton', 'mouse', 'pencil', 'pirate',
        'plus', 'question_arrow', 'right_ptr', 'right_side', 'right_tee',
        'rightbutton', 'rtl_logo', 'sailboat', 'sb_down_arrow',
        'sb_h_double_arrow', 'sb_left_arrow', 'sb_right_arrow',
        'sb_up_arrow', 'sb_v_double_arrow', 'shuttle', 'sizing', 'spider',
        'spraycan', 'star', 'target', 'tcross', 'top_left_arrow',
        'top_left_corner', 'top_right_corner', 'top_side', 'top_tee',
        'trek', 'ul_angle', 'umbrella', 'ur_angle', 'watch', 'xterm',
        'X_cursor')
}

_sticky_prop = {
        'input_method': 'choice',
        'values': ('', tkinter.N, tkinter.S,
            tkinter.E, tkinter.W,
            tkinter.NE, tkinter.NW,
            tkinter.SE, tkinter.SW,
            tkinter.EW, tkinter.NS,
            tkinter.NS + tkinter.W,
            tkinter.NS + tkinter.E,
            tkinter.NSEW
            )
        }

GROUP_WIDGET = 'widget__'
GROUP_LAYOUT_GRID = 'layoutgrid__'
GROUP_LAYOUT_GRID_RC = 'layoutgridrc__'
GROUP_CUSTOM = 'custom__'

GROUPS = (GROUP_WIDGET, GROUP_LAYOUT_GRID, GROUP_LAYOUT_GRID_RC, GROUP_CUSTOM)


PropertiesMap = {}

__widget = (
    ('accelerator', _default_entry_prop),
    ('activerelief', _default_relief_prop),
    ('activestyle', {
        'input_method': 'choice',
        'values': ('', 'underline', 'dotbox', 'none')
        }),
    ('activebackground', _default_color_prop),
    ('activeborderwidth', _default_spinbox_prop),
    ('activeforeground', _default_color_prop),
    ('after', _empty_choice),
    ('anchor', {
        'input_method': 'choice',
        'values': ('', tkinter.W, tkinter.CENTER, tkinter.E),
        }),
    ('aspect', _default_spinbox_prop),
    ('autoseparators', _default_true_false_prop),
    ('background', _default_color_prop),
    ('before', _empty_choice),
    ('bitmap', {
        'input_method': 'choice',
        'values': ('', 'error', 'gray75', 'gray50', 'gray25', 'gray12',
            'hourglass', 'info', 'questhead', 'question', 'warning')
        }),
    ('borderwidth', _default_dimension_prop),
    ('buttonbackground', _default_color_prop),
    ('buttoncursor', _default_cursor_prop),
    ('buttondownrelief', _default_relief_prop),
    ('buttonup', _default_relief_prop),
    ('class_', _default_entry_prop),
    ('closeenough', _default_spinbox_prop),
    ('columnbreak', _default_true_false_prop),
    ('command', _default_entry_prop),
    ('command_id_arg', {
        'input_method': 'choice',
        'values': ('True', 'False'),
        'default': 'False'}),
    ('compound', {
        'input_method': 'choice',
        'values': ('', tkinter.TOP, tkinter.BOTTOM,
            tkinter.LEFT, tkinter.RIGHT),
        'tk.Radiobutton': {
            'values': ('', tkinter.NONE, tkinter.TOP, tkinter.BOTTOM,
                tkinter.LEFT, tkinter.RIGHT)},
        'tk.Menubutton': {
            'values': ('', tkinter.NONE, tkinter.TOP, tkinter.BOTTOM,
                tkinter.LEFT, tkinter.RIGHT)},
        'ttk.Label': {
            'values' : ('', tkinter.BOTTOM, 'image', tkinter.LEFT, 'none',
                tkinter.RIGHT, 'text', tkinter.TOP)},
        }),
    ('confine', _default_true_false_prop),
    ('cursor', _default_cursor_prop),
    ('digits', _default_spinbox_prop),
    ('default', {
        'input_method': 'choice',
        'values': (tkinter.NORMAL, tkinter.DISABLED)
        }),
    ('direction', {
        'input_method': 'choice', 'values': None,
        'tk.Menubutton': {
            'values': ('', tkinter.LEFT, tkinter.RIGHT, 'above')},
        'ttk.Menubutton': {
            'values': ('', 'above', 'below', 'flush',
                tkinter.LEFT, tkinter.RIGHT)},
        }),
    ('disabledbackground', _default_color_prop),
    ('disabledforeground', _default_color_prop),
    ('elementborderwidth', {'input_method': 'spinbox', 'min': -1, 'max': 99,
        'validator': 'number_integer'}),
    ('exportselection', _default_true_false_prop),
    ('font', _default_entry_prop),
    ('foreground', _default_color_prop),
    ('format', _default_entry_prop),
    ('from_', {
            'input_method': 'spinbox',
            'min': -999, 'max': 999, 'default': 0,
            'validator': 'number_float',
            'increment': 0.1
        }),
    ('to', {
            'input_method': 'spinbox',
            'min': -999, 'max': 999, 'default': 100,
            'validator': 'number_float',
            'increment': 0.1
        }),
    ('increment', _default_spinbox_float_prop),
    ('handlepad', _default_dimension_prop),
    ('handlesize', _default_dimension_prop),
    ('hidemargin', _default_true_false_prop),
    ('height', {
        'input_method': 'spinbox', 'min': 0, 'max': 999,
        'validator': 'number_integer',
        'tk.Frame': { 'default': 250 },
        'ttk.Frame': { 'default': 250 },
        'tk.Text': { 'default': 10 },
        }), #FIXME this prop has diferent interpretations
    ('width', {
        'input_method': 'spinbox', 'min': 0, 'max': 999,
        'validator': 'number_integer',
        'tk.Frame': { 'default': 250 },
        'ttk.Frame': { 'default': 250 },
        'tk.Text': { 'default': 50 },
        }), #FIXME width is not a dimension for Entry
    ('highlightbackground', _default_color_prop),
    ('highlightcolor', _default_color_prop),
    ('highlightthickness', _default_spinbox_prop),
    ('indicatoron', _default_true_false_prop),
    ('insertbackground', _default_color_prop),
    ('insertborderwidth', _default_dimension_prop),
    ('insertofftime', _default_spinbox_prop),
    ('insertontime', _default_spinbox_prop),
    ('insertwidth', _default_dimension_prop),
    ('image', _empty_choice), #FIXME image property
    ('jump', {'input_method': 'choice', 'values': ('', '0', '1')}),
    ('justify', {
        'input_method': 'choice',
        'values': ('', tkinter.LEFT, tkinter.CENTER,
            tkinter.RIGHT),
        }),
    ('label', _default_entry_prop),
    ('labelanchor', {
        'input_method': 'choice',
        'values': ('', tkinter.NW, tkinter.N, tkinter.NE,
            tkinter.E + tkinter.N, tkinter.E, tkinter.E + tkinter.S,
            tkinter.W + tkinter.N, tkinter.W, tkinter.W + tkinter.S,
            tkinter.SW, tkinter.S, tkinter.SE)
        }),
    ('labelwidget', _empty_choice),
    ('length', _default_dimension_prop),
    ('listvariable', _default_entry_prop),
    ('maximum', _default_spinbox_prop),
    ('maxundo', {
        'input_method': 'spinbox', 'min':-1, 'max':999, 'default': ''}),
    ('minsize', _default_dimension_prop),
    ('mode', { 'input_method': 'choice',
        'values': ('', 'determinate', 'indeterminate')}),
    ('offrelief', _default_relief_prop),
    ('offvalue', _default_entry_prop),
    ('onvalue', _default_entry_prop),
    ('opaqueresize', _default_true_false_prop),
    ('orient', {
        'input_method': 'choice',
        'values': (tkinter.VERTICAL, tkinter.HORIZONTAL),
        'default': tkinter.HORIZONTAL
        }),
    ('overrelief', _default_relief_prop),
    ('padding', _default_dimension_prop),
    ('padx', _default_spinbox_prop),
    ('pady', _default_spinbox_prop),
    ('postcommand', _default_entry_prop),
    ('readonlybackground', _default_color_prop),
    ('relief', _default_relief_prop),
    ('repeatdelay', _default_spinbox_prop),
    ('repeatinterval', _default_spinbox_prop),
    ('resolution', _default_spinbox_float_prop),
    ('scrollregion', _default_entry_prop),
    ('sashpad', _default_dimension_prop),
    ('sashrelief', _default_relief_prop),
    ('sashwidth', _default_dimension_prop),
    ('selectcolor', _default_color_prop),
    ('selectbackground', _default_color_prop),
    ('selectborderwidth', _default_spinbox_prop),
    ('selectforeground', _default_color_prop),
    ('selectimage', _empty_choice), #FIXME image property
    ('selectmode', {
        'input_method': 'choice',
        'values': ('', tkinter.BROWSE, tkinter.SINGLE,
            tkinter.MULTIPLE, tkinter.EXTENDED)
        }),
    ('show', _default_entry_prop),
    ('showhandle', _default_true_false_prop),
    ('showvalue', _default_true_false_prop),
    ('sliderlength', _default_dimension_prop),
    ('sliderrelief', _default_relief_prop),
    ('spacing1', _default_spinbox_prop),
    ('spacing2', _default_spinbox_prop),
    ('spacing3', _default_spinbox_prop),
    ('state', {
        'input_method': 'choice',
        'values': ('', tkinter.NORMAL, tkinter.DISABLED),
        'tk.Entry': {
            'values': ('', tkinter.NORMAL, tkinter.DISABLED, 'disabled')},
        'tk.Combobox': {'values': ('', 'readonly')},
        'ttk.Entry': {
            'values': ('', tkinter.NORMAL, tkinter.DISABLED, 'disabled')},
        'ttk.Combobox': { 'values': ('', 'readonly')},
        }),
    ('sticky', _sticky_prop),
    ('style', _empty_choice), #FIXME Howto manage this property?
    ('tabs', _default_entry_prop), #FIXME see tk.Text tab property 
    ('takefocus', _default_true_false_prop),
    ('tearoff', _default_entry_prop),
    ('tearoffcommand', _default_entry_prop),
    ('text', _default_textentry_prop),
    ('textvariable', _empty_choice), #FIXME Howto manage this property?
    ('tickinterval', _default_spinbox_float_prop),
    ('title', _default_entry_prop),
    ('troughcolor', _default_color_prop),
    ('undo', _default_true_false_prop),
    ('underline', _default_spinbox_prop),
    ('validate', { 'input_method': 'choice',
        'values': ('none', 'focus', 'focusin', 'focusout', 'key', 'all'),
        'default': 'none'
        }),
    ('validatecommand', _default_entry_prop),
    ('validatecommand_args', _default_entry_prop),
    ('invalidcommand', _default_entry_prop),
    ('invalidcommand_args', _default_entry_prop),
    ('value', { 'input_method': 'entry', 'validator': 'alphanumeric',
        'ttk.Scale': { 'validator': 'number_float'}
        }),
    ('values', _default_entry_prop), #FIXME This should be treated as a list?
    ('variable', _empty_choice), #FIXME Howto manage this property?
    ('weight', _default_spinbox_prop),
    ('wrap', { 'input_method': 'choice',
        'values': ('', tkinter.TRUE, tkinter.FALSE),
        'tk.Text': {
            'values': (tkinter.CHAR, tkinter.WORD, tkinter.NONE),
            'default': tkinter.CHAR}
        }),
    ('wraplength', _default_dimension_prop),
    ('xscrollcommand', _default_entry_prop),
    ('xscrollincrement', _default_dimension_prop),
    ('yscrollcommand', _default_entry_prop),
    ('yscrollincrement', _default_dimension_prop),
)
PropertiesMap[GROUP_WIDGET] = OrderedDict(__widget)

__grid = (
#grid packing properties
    ('row', {
        'input_method': 'spinbox',
        'min': 0, 'max': 50, 'validator': 'number_integer'}),
    ('column', {
        'input_method': 'spinbox',
        'min': 0, 'max': 50, 'validator': 'number_integer' }),
    ('sticky', _sticky_prop),
    ('rowspan', {
        'input_method': 'spinbox',
        'min': 1, 'max': 50, 'validator': 'number_integer'}),
    ('columnspan', {
        'input_method': 'spinbox',
        'min': 1, 'max': 50, 'validator': 'number_integer'}),
    ('padx', _default_spinbox_prop),
    ('pady', _default_spinbox_prop),
    ('ipadx', _default_spinbox_prop),
    ('ipady', _default_spinbox_prop),
)

PropertiesMap[GROUP_LAYOUT_GRID] = OrderedDict(__grid)

__grid_rc = (
    #grid row and column properties (can be applied to each row or column)
    ('minsize', _default_spinbox_prop),
    ('pad', _default_spinbox_prop),
    ('weight', _default_spinbox_prop)
)

PropertiesMap[GROUP_LAYOUT_GRID_RC] = OrderedDict(__grid_rc)

__custom = (
    ('class', {
        'input_method': 'entry',
        'readonly': True
        }),
    ('id', {'input_method': 'entry'}),
)

PropertiesMap[GROUP_CUSTOM] = OrderedDict(__custom)

def register_custom(name, descr):
    if name not in PropertiesMap[GROUP_CUSTOM]:
        PropertiesMap[GROUP_CUSTOM][name] = descr
    else:
        raise ValueError('Property "{}" already registered'.format(name))


OBJECT_DEFAULT_ATTRS = ('class', 'id')


