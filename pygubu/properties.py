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

_default_spinbox_prop = {
    'input_method': 'spinbox',
    'min': 0,
    'max': 999,
}

_dimension_prop = {
    'input_method': 'spinbox',
    'min': 0,
    'max': 999,
}

_relief_prop = {
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
    ('activerelief', _relief_prop),
    ('activestyle', {
        'input_method': 'choice',
        'values': ('', 'underline', 'dotbox', 'none')
        }),
    ('activebackground', _default_entry_prop), #FIXME color property
    ('activeborderwidth', _default_spinbox_prop),
    ('activeforeground', _default_entry_prop), #FIXME color property
    ('after', _empty_choice),
    ('anchor', {
        'input_method': 'choice',
        'values': ('', tkinter.W, tkinter.CENTER, tkinter.E),
        }),
    ('aspect', _default_spinbox_prop),
    ('autoseparators', _default_true_false_prop),
    ('background', _default_entry_prop),
    ('before', _empty_choice),
    ('bitmap', {
        'input_method': 'choice',
        'values': ('', 'error', 'gray75', 'gray50', 'gray25', 'gray12',
            'hourglass', 'info', 'questhead', 'question', 'warning')
        }),
    ('borderwidth', _dimension_prop),
    ('buttonbackground', _default_entry_prop), #FIXME color property
    ('buttoncursor', _default_cursor_prop),
    ('buttondownrelief', _relief_prop),
    ('buttonup', _relief_prop),
    ('class_', _default_entry_prop),
    ('closeenough', _default_spinbox_prop),
    ('columnbreak', _default_true_false_prop),
    ('command', _default_entry_prop),
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
    ('disabledbackground', _default_entry_prop), #FIXME color prop
    ('disabledforeground', _default_entry_prop), #FIXME color prop
    ('elementborderwidth', {'input_method': 'spinbox', 'min': -1, 'max': 99}),
    ('exportselection', _default_true_false_prop),
    ('font', _default_entry_prop),
    ('foreground', _default_entry_prop), #FIXME color prop
    ('format', _default_entry_prop),
    ('from_', _default_spinbox_prop), #FIXME float property
    ('handlepad', _dimension_prop),
    ('handlesize', _dimension_prop),
    ('hidemargin', _default_true_false_prop),
    ('height', {
        'input_method': 'spinbox', 'min': 0, 'max': 999,
        'tk.Frame': { 'default': 250 },
        'ttk.Frame': { 'default': 250 },
        'tk.Text': { 'default': 10 },
        }), #FIXME this prop has diferent interpretations
    ('width', {
        'input_method': 'spinbox', 'min': 0, 'max': 999,
        'tk.Frame': { 'default': 250 },
        'ttk.Frame': { 'default': 250 },
        'tk.Text': { 'default': 50 },
        }), #FIXME width is not a dimension for Entry
    ('highlightbackground', _default_entry_prop), #FIXME color prop
    ('highlightcolor', _default_entry_prop), #FIXME color prop
    ('highlightthickness', _default_entry_prop),
    ('indicatoron', _default_true_false_prop),
    ('increment', _default_spinbox_prop), #FIXME float property
    ('insertbackground', _default_entry_prop), #FIXME color prop
    ('insertborderwidth', _dimension_prop),
    ('insertofftime', _default_spinbox_prop),
    ('insertontime', _default_spinbox_prop),
    ('insertwidth', _dimension_prop),
    ('invalidcommand', _default_entry_prop),
    ('image', _default_entry_prop), #FIXME image property
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
    ('length', _dimension_prop),
    ('listvariable', _default_entry_prop),
    ('maximum', _default_spinbox_prop),
    ('maxundo', {
        'input_method': 'spinbox', 'min':-1, 'max':999, 'default': ''}),
    ('minsize', _dimension_prop),
    ('mode', { 'input_method': 'choice',
        'values': ('', 'determinate', 'indeterminate')}),
    ('offrelief', _relief_prop),
    ('offvalue', _default_entry_prop),
    ('onvalue', _default_entry_prop),
    ('opaqueresize', _default_true_false_prop),
    ('orient', {
        'input_method': 'choice',
        'values': (tkinter.VERTICAL, tkinter.HORIZONTAL)
        }),
    ('overrelief', _relief_prop),
    ('padding', _dimension_prop),
    ('padx', _default_spinbox_prop),
    ('pady', _default_spinbox_prop),
    ('postcommand', _default_entry_prop),
    ('readonlybackground', _default_entry_prop), #FIXME color prop
    ('relief', _relief_prop),
    ('repeatdelay', _default_spinbox_prop),
    ('repeatinterval', _default_spinbox_prop),
    ('resolution', _default_spinbox_prop), #FIXME float property
    ('scrollregion', _default_entry_prop),
    ('sashpad', _dimension_prop),
    ('sashrelief', _relief_prop),
    ('sashwidth', _dimension_prop),
    ('selectcolor', _default_entry_prop), #FIXME color prop
    ('selectbackground', _default_entry_prop), #FIXME color prop
    ('selectborderwidth', _default_spinbox_prop),
    ('selectforeground', _default_entry_prop), #FIXME color prop
    ('selectimage', _default_entry_prop), #FIXME image property
    ('selectmode', {
        'input_method': 'choice',
        'values': ('', tkinter.BROWSE, tkinter.SINGLE,
            tkinter.MULTIPLE, tkinter.EXTENDED)
        }),
    ('show', _default_entry_prop),
    ('showhandle', _default_true_false_prop),
    ('showvalue', _default_true_false_prop),
    ('sliderlenght', _dimension_prop),
    ('sliderrelief', _relief_prop),
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
    ('style', _default_entry_prop),
    ('tabs', _default_entry_prop), #FIXME see tk.Text tab property 
    ('takefocus', _default_true_false_prop),
    ('tearoff', _default_entry_prop),
    ('tearoffcommand', _default_entry_prop),
    ('text', _default_entry_prop),
    ('textvariable', _default_entry_prop),
    ('tickinterval', _default_spinbox_prop), #FIXME float property
    ('title', _default_entry_prop),
    ('to', _default_spinbox_prop), #FIXME float property
    ('troughcolor', _default_entry_prop), #FIXME color property
    ('undo', _default_true_false_prop),
    ('underline', _default_spinbox_prop),
    ('validate', _default_entry_prop),
    ('validatecommand', _default_entry_prop),
    ('value', _default_entry_prop),
    ('values', _default_entry_prop), #FIXME This should be treated as a list?
    ('variable', _default_entry_prop),
    ('weight', _default_spinbox_prop),
    ('wrap', { 'input_method': 'choice',
        'values': ('', tkinter.TRUE, tkinter.FALSE),
        'tk.Text': {
            'values': (tkinter.CHAR, tkinter.WORD, tkinter.NONE),
            'default': tkinter.CHAR}
        }),
    ('wraplength', _dimension_prop),
    ('xscrollcommand', _default_entry_prop),
    ('xscrollincrement', _default_entry_prop),
    ('yscrollcommand', _default_entry_prop),
    ('yscrollincrement', _default_entry_prop),
)
PropertiesMap[GROUP_WIDGET] = OrderedDict(__widget)

__grid = (
#grid packing properties
    ('row', {
        'input_method': 'spinbox',
        'min': 0,
        'max': 50 }),
    ('column', {
        'input_method': 'spinbox',
        'min': 0,
        'max': 50 }),
    ('sticky', _sticky_prop),
    ('rowspan', {
        'input_method': 'spinbox',
        'min': 1,
        'max': 50 }),
    ('columnspan', {
        'input_method': 'spinbox',
        'min': 1,
        'max': 50 }),
    ('padx', _default_spinbox_prop),
    ('pady', _default_spinbox_prop),
    ('ipadx', _default_spinbox_prop),
    ('ipady', _default_spinbox_prop),
)

PropertiesMap[GROUP_LAYOUT_GRID] = OrderedDict(__grid)

__grid_rc = (
    #grid row and column properties (can be applied to each row or column)
    ('minsize', {
        'input_method': 'spinbox',
        'min': 0,
        'max': 999,
        'default': 0}),
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


