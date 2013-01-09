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

_sticky_prop = {
        'input_method': 'choice',
        'values': ('', tkinter.constants.N, tkinter.constants.S,
            tkinter.constants.E, tkinter.constants.W,
            tkinter.constants.NE, tkinter.constants.NW,
            tkinter.constants.SE, tkinter.constants.SW,
            tkinter.constants.EW, tkinter.constants.NS,
            tkinter.constants.NS + tkinter.constants.W,
            tkinter.constants.NS + tkinter.constants.E,
            tkinter.constants.NSEW
            )
        }

TK_WIDGET_PROPS = {
    'activestyle': {
        'input_method': 'choice',
        'values': ('', 'underline', 'dotbox', 'none')
        },
    'activebackground': _default_entry_prop, #FIXME color property
    'activeborderwidth': _default_spinbox_prop,
    'activeforeground': _default_entry_prop, #FIXME color property
    'anchor': {
        'input_method': 'choice',
        'values': ('', tkinter.W, tkinter.CENTER, tkinter.E),
        },
    'background': _default_entry_prop,
    'borderwidth': _dimension_prop,
    'class_': _default_entry_prop,
    'command': _default_entry_prop,
    'compound': {
        'input_method': 'choice',
        'values': {
            'ttk.Label': ('', 'bottom', 'image', 'left', 'none',
                'right', 'text', 'top'),
            'ttk.Button': ('', tkinter.constants.TOP, tkinter.constants.BOTTOM,
                tkinter.constants.LEFT, tkinter.constants.RIGHT),
            'ttk.Checkbutton':
                ('', tkinter.constants.TOP, tkinter.constants.BOTTOM,
                tkinter.constants.LEFT, tkinter.constants.RIGHT),
            'ttk.Notebook.Tab':
                ('', tkinter.constants.TOP, tkinter.constants.BOTTOM,
                tkinter.constants.LEFT, tkinter.constants.RIGHT)
            }
        },
    'cursor': {
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
        },
    'direction': {
        'input_method': 'choice',
        'values': ('', 'above', 'below', 'flush', 'left', 'right')
        },
    'disabledforeground': _default_entry_prop, #FIXME color prop
    'exportselection': {
        'input_method': 'choice',
        'values': ('', '0', '1')
        },
    'font': _default_entry_prop,
    'foreground': _default_entry_prop, #FIXME color prop
    'height': _dimension_prop, #FIXME this prop has diferent interpretations
    'highlightbackground': _default_entry_prop, #FIXME color prop
    'highlightcolor': _default_entry_prop, #FIXME color prop
    'highlightthickness': _default_entry_prop,
    'invalidcommand': _default_entry_prop,
    'image': _default_entry_prop, #FIXME image property
    'justify': {
        'input_method': 'choice',
        'values': ('', tkinter.constants.LEFT, tkinter.constants.CENTER,
            tkinter.constants.RIGHT),
        },
    'listvariable': _default_entry_prop,
    'onvalue': _default_entry_prop,
    'orient': {
        'input_method': 'choice',
        'values': (tkinter.constants.VERTICAL, tkinter.constants.HORIZONTAL)
        },
    'padding': _dimension_prop,
    'postcommand': _default_entry_prop,
    'relief': {
        'input_method': 'choice',
        'values': ('', tkinter.constants.FLAT, 'raised', 'sunken', 'groove', 'ridge')
        },
    'selectbackground': _default_entry_prop, #FIXME color prop
    'selectborderwidth': _default_spinbox_prop,
    'selectforeground': _default_entry_prop, #FIXME color prop
    'selectmode': {
        'input_method': 'choice',
        'values': ('', tkinter.constants.BROWSE, tkinter.constants.SINGLE,
            tkinter.constants.MULTIPLE, tkinter.constants.EXTENDED)
        },
    'show': _default_entry_prop,
    'state': {
        'input_method': 'choice',
        'values': {
            'Entry': ('', tkinter.constants.NORMAL,
                tkinter.constants.DISABLED, 'disabled'),
            'Combobox': ('', 'readonly'),
            'Listbox': ('', tkinter.constants.NORMAL,
                tkinter.constants.DISABLED)
            }
        },
    'sticky': _sticky_prop,
    'style': _default_entry_prop,
    'tearoff': _default_entry_prop,
    'takefocus': {
        'input_method': 'choice',
        'values': ('', tkinter.constants.TRUE, tkinter.constants.FALSE),
        },
    'text': _default_entry_prop,
    'textvariable': _default_entry_prop,
    'underline': _default_spinbox_prop,
    'validate': _default_entry_prop,
    'validatecommand': _default_entry_prop,
    'value': _default_entry_prop,
    'values': _default_entry_prop, #FIXME This should be treated as a list?
    'width': _dimension_prop, #FIXME width is not a dimension for Entry
    'wraphlength':_dimension_prop,
    'xscrollcommand': _default_entry_prop,
    'yscrollcommand': _default_entry_prop,
}

TK_GRID_PROPS = {
#grid packing properties
    'column': _default_spinbox_prop,
    'columnspan': _default_spinbox_prop,
    'in_': _default_entry_prop,
    'ipadx': _default_spinbox_prop,
    'ipady': _default_spinbox_prop,
    'padx': _default_spinbox_prop,
    'pady': _default_spinbox_prop,
    'row': _default_spinbox_prop,
    'rowspan': _default_spinbox_prop,
    'sticky': _sticky_prop
}

TK_GRID_RC_PROPS = {
#grid row and column properties (can be applied to each row or column)
    'minsize': _default_spinbox_prop,
    'pad': _default_spinbox_prop,
    'weight': _default_spinbox_prop
}
