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
    ('activestyle', {
        'input_method': 'choice',
        'values': ('', 'underline', 'dotbox', 'none')
        }),
    ('activebackground', _default_entry_prop), #FIXME color property
    ('activeborderwidth', _default_spinbox_prop),
    ('activeforeground', _default_entry_prop), #FIXME color property
    ('anchor', {
        'input_method': 'choice',
        'values': ('', tkinter.W, tkinter.CENTER, tkinter.E),
        }),
    ('bitmap', {
        'input_method': 'choice',
        'values': ('', 'error', 'gray75', 'gray50', 'gray25', 'gray12',
            'hourglass', 'info', 'questhead', 'question', 'warning')
        }),
    ('background', _default_entry_prop),
    ('borderwidth', _dimension_prop),
    ('class_', _default_entry_prop),
    ('command', _default_entry_prop),
    ('compound', {
        'input_method': 'choice',
        'values': {
            'tk.Button': ('', tkinter.TOP, tkinter.BOTTOM,
                tkinter.LEFT, tkinter.RIGHT),
            'tk.Checkbutton': ('', tkinter.TOP, tkinter.BOTTOM,
                tkinter.LEFT, tkinter.RIGHT),
            'tk.Radiobutton': ('', tkinter.NONE, tkinter.TOP, tkinter.BOTTOM,
                tkinter.LEFT, tkinter.RIGHT),
            'tk.Menubutton': ('', tkinter.NONE, tkinter.TOP, tkinter.BOTTOM,
                tkinter.LEFT, tkinter.RIGHT),
            'ttk.Label': ('', tkinter.BOTTOM, 'image', tkinter.LEFT, 'none',
                tkinter.RIGHT, 'text', tkinter.TOP),
            'ttk.Button': ('', tkinter.TOP, tkinter.BOTTOM,
                tkinter.LEFT, tkinter.RIGHT),
            'ttk.Checkbutton':
                ('', tkinter.TOP, tkinter.BOTTOM,
                tkinter.LEFT, tkinter.RIGHT),
            'ttk.Notebook.Tab':
                ('', tkinter.TOP, tkinter.BOTTOM,
                tkinter.LEFT, tkinter.RIGHT),
            'ttk.Menubutton': ('', tkinter.TOP, tkinter.BOTTOM,
                tkinter.LEFT, tkinter.RIGHT),
            }
        }),
    ('cursor', {
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
        }),
    ('default', {
        'input_method': 'choice',
        'values': (tkinter.NORMAL, tkinter.DISABLED)
        }),
    ('direction', {
        'input_method': 'choice',
        'values': {
            'tk.Menubutton': ('', tkinter.LEFT, tkinter.RIGHT, 'above'),
            'ttk.Menubutton': ('', 'above', 'below', 'flush', tkinter.LEFT,
                tkinter.RIGHT),
            }
        }),
    ('disabledforeground', _default_entry_prop), #FIXME color prop
    ('exportselection', {
        'input_method': 'choice',
        'values': ('', '0', '1')
        }),
    ('font', _default_entry_prop),
    ('foreground', _default_entry_prop), #FIXME color prop
    ('height', _dimension_prop), #FIXME this prop has diferent interpretations
    ('highlightbackground', _default_entry_prop), #FIXME color prop
    ('highlightcolor', _default_entry_prop), #FIXME color prop
    ('highlightthickness', _default_entry_prop),
    ('indicatoron', {
        'input_method': 'choice',
        'values': ('', '0', '1')
        }),
    ('invalidcommand', _default_entry_prop),
    ('image', _default_entry_prop), #FIXME image property
    ('justify', {
        'input_method': 'choice',
        'values': ('', tkinter.LEFT, tkinter.CENTER,
            tkinter.RIGHT),
        }),
    ('labelanchor', {
        'input_method': 'choice',
        'values': ('', tkinter.NW, tkinter.N, tkinter.NE,
            tkinter.E + tkinter.N, tkinter.E, tkinter.E + tkinter.S,
            tkinter.W + tkinter.N, tkinter.W, tkinter.W + tkinter.S,
            tkinter.SW, tkinter.S, tkinter.SE)
        }),
    ('listvariable', _default_entry_prop),
    ('offrelief', _relief_prop),
    ('onvalue', _default_entry_prop),
    ('orient', {
        'input_method': 'choice',
        'values': (tkinter.VERTICAL, tkinter.HORIZONTAL)
        }),
    ('overrelief', _relief_prop),
    ('padding', _dimension_prop),
    ('padx', _default_spinbox_prop),
    ('pady', _default_spinbox_prop),
    ('postcommand', _default_entry_prop),
    ('relief', _relief_prop),
    ('repeatdelay', _default_spinbox_prop),
    ('repeatinterval', _default_spinbox_prop),
    ('scrollregion', _default_entry_prop),
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
    ('state', {
        'input_method': 'choice',
        'values': {
            'tk.Label': ('', tkinter.NORMAL, tkinter.DISABLED),
            'tk.Entry': ('', tkinter.NORMAL, tkinter.DISABLED),
            'tk.Combobox': ('', 'readonly'),
            'tk.Listbox': ('', tkinter.NORMAL,
                tkinter.DISABLED),
            'tk.Button': (tkinter.NORMAL, tkinter.DISABLED),
            'tk.Checkbutton': (tkinter.NORMAL, tkinter.DISABLED),
            'ttk.Entry': ('', tkinter.NORMAL,
                tkinter.DISABLED, 'disabled'),
            'ttk.Combobox': ('', 'readonly'),
            }
        }),
    ('sticky', _sticky_prop),
    ('style', _default_entry_prop),
    ('tearoff', _default_entry_prop),
    ('takefocus', {
        'input_method': 'choice',
        'values': ('', tkinter.TRUE, tkinter.FALSE),
        }),
    ('text', _default_entry_prop),
    ('textvariable', _default_entry_prop),
    ('underline', _default_spinbox_prop),
    ('validate', _default_entry_prop),
    ('validatecommand', _default_entry_prop),
    ('value', _default_entry_prop),
    ('values', _default_entry_prop), #FIXME This should be treated as a list?
    ('width', _dimension_prop), #FIXME width is not a dimension for Entry
    ('wraphlength', _dimension_prop),
    ('xscrollcommand', _default_entry_prop),
    ('yscrollcommand', _default_entry_prop),
)
PropertiesMap[GROUP_WIDGET] = OrderedDict(__widget)

__grid = (
#grid packing properties
    ('row', _default_spinbox_prop),
    ('column', _default_spinbox_prop),
    ('sticky', _sticky_prop),
    ('rowspan', {
        'input_method': 'spinbox',
        'min': 1,
        'max': 999 }),
    ('columnspan', {
        'input_method': 'spinbox',
        'min': 1,
        'max': 999 }),
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


