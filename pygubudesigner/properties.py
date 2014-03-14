# encoding: UTF-8
#
# Copyright 2012-2013 Alejandro Autalán
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
from __future__ import unicode_literals
from collections import OrderedDict
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk



_default_entry_prop = {
    'input_method': 'entry',
}

_default_textentry_prop = {
    'input_method': 'textentry',
}

_default_color_prop = {
    'input_method': 'colorentry',
}

_default_image_prop = {
    'input_method': 'imageentry',
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

_default_tkvariable_prop = {
    'input_method': 'tkvarentry',
}

_default_dimension_prop = {
    'input_method': 'sizeentry',
}

_default_relief_prop = {
    'input_method': 'choice',
    'values': ('', tk.FLAT, tk.RAISED, tk.SUNKEN,
        tk.GROOVE, tk.RIDGE), 'readonly': True
}

_empty_choice = {'input_method': 'choice', 'readonly': True }

_default_true_false_prop = { 'input_method': 'choice',
    'values': ('', tk.TRUE, tk.FALSE), 'readonly': True}

_default_cursor_prop = {
    'input_method': 'choice',
    'values': ('', 'arrow', 'based_arrow_down','based_arrow_up','boat',
       'bogosity','bottom_left_corner','bottom_right_corner',
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
        'X_cursor'),
    'readonly': True
}

_sticky_prop = {
        'input_method': 'choice',
        'values': ('', tk.N, tk.S,
            tk.E, tk.W,
            tk.NE, tk.NW,
            tk.SE, tk.SW,
            tk.EW, tk.NS,
            tk.NS + tk.W,
            tk.NS + tk.E,
            #tk.NSEW
            tk.NE + tk.SW
            ),
        'tk.Frame': {'default': tk.NE + tk.SW},
        'ttk.Frame': {'default': tk.NE + tk.SW},
        'tk.LabelFrame': {'default': tk.NE + tk.SW},
        'ttk.Labelframe': {'default': tk.NE + tk.SW},
        'tk.ScrollbarHelper': {'default': tk.NE + tk.SW},
        'ttk.ScrollbarHelper': {'default': tk.NE + tk.SW},
        'tk.ScrolledFrame': {'default': tk.NE + tk.SW},
        'ttk.ScrolledFrame': {'default': tk.NE + tk.SW},
        'ttk.Notebook': {'default': tk.NE + tk.SW}
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
        'values': ('', tk.W, tk.CENTER, tk.E),
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
        'values': ('', tk.TOP, tk.BOTTOM,
            tk.LEFT, tk.RIGHT),
        'tk.Radiobutton': {
            'values': ('', tk.NONE, tk.TOP, tk.BOTTOM,
                tk.LEFT, tk.RIGHT)},
        'tk.Menubutton': {
            'values': ('', tk.NONE, tk.TOP, tk.BOTTOM,
                tk.LEFT, tk.RIGHT)},
        'ttk.Label': {
            'values' : ('', tk.BOTTOM, 'image', tk.LEFT, 'none',
                tk.RIGHT, 'text', tk.TOP)},
        }),
    ('confine', _default_true_false_prop),
    ('cursor', _default_cursor_prop),
    ('digits', _default_spinbox_prop),
    ('default', {
        'input_method': 'choice',
        'values': (tk.NORMAL, tk.DISABLED)
        }),
    ('direction', {
        'input_method': 'choice', 'values': None,
        'tk.Menubutton': {
            'values': ('', tk.LEFT, tk.RIGHT, 'above')},
        'ttk.Menubutton': {
            'values': ('', 'above', 'below', 'flush',
                tk.LEFT, tk.RIGHT)},
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
        'tk.Toplevel': { 'default': 200 },
        'tk.Frame': { 'default': 200 },
        'ttk.Frame': { 'default': 200 },
        'tk.LabelFrame': { 'default': 200 },
        'ttk.Labelframe': { 'default': 200 },
        'tk.PanedWindow': { 'default': 200 },
        'ttk.Panedwindow': { 'default': 200 },
        'ttk.Notebook': { 'default': 200 },
        'tk.Text': { 'default': 10 },
        'pygubu.builder.widgets.dialog': { 'default': 100 },
        }), #FIXME this prop has diferent interpretations
    ('width', {
        'input_method': 'spinbox', 'min': 0, 'max': 999,
        'validator': 'number_integer',
        'tk.Toplevel': { 'default': 200 },
        'tk.Frame': { 'default': 200 },
        'ttk.Frame': { 'default': 200 },
        'tk.LabelFrame': { 'default': 200 },
        'ttk.Labelframe': { 'default': 200 },
        'tk.PanedWindow': { 'default': 200 },
        'ttk.Panedwindow': { 'default': 200 },
        'ttk.Notebook': { 'default': 200 },
        'tk.Text': { 'default': 50 },
        'ttk.Treeview.Column': {'min':5, 'default': 200 },
        'pygubu.builder.widgets.dialog': { 'default': 200 },
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
    ('image', _default_image_prop),
    ('jump', {'input_method': 'choice', 'values': ('', '0', '1')}),
    ('justify', {
        'input_method': 'choice',
        'values': ('', tk.LEFT, tk.CENTER,
            tk.RIGHT),
        }),
    ('label', _default_entry_prop),
    ('labelanchor', {
        'input_method': 'choice',
        'values': ('', tk.NW, tk.N, tk.NE,
            tk.E + tk.N, tk.E, tk.E + tk.S,
            tk.W + tk.N, tk.W, tk.W + tk.S,
            tk.SW, tk.S, tk.SE)
        }),
    ('labelwidget', _empty_choice),
    ('length', _default_dimension_prop),
    ('listvariable', _default_entry_prop),
    ('maximum', _default_spinbox_prop),
    ('maxundo', {
        'input_method': 'spinbox', 'min':-1, 'max':999, 'default': ''}),
    # maxize: method from Toplevel as property
    ('maxsize', {'input_method': 'sizeentry', 'mode':'whsize'}),
    ('minsize', {'input_method': 'sizeentry',
        'tk.Toplevel': {'mode':'whsize'},
        'pygubu.builder.widgets.dialog': {'mode':'whsize'}
        }),
    ('minwidth', {
        'input_method': 'spinbox', 'min':5, 'max':999, 'default': '20'}),
    ('mode', { 'input_method': 'choice',
        'values': ('', 'determinate', 'indeterminate')}),
    ('offrelief', _default_relief_prop),
    ('offvalue', _default_entry_prop),
    ('onvalue', _default_entry_prop),
    ('opaqueresize', _default_true_false_prop),
    ('orient', {
        'input_method': 'choice',
        'values': (tk.VERTICAL, tk.HORIZONTAL),
        'default': tk.HORIZONTAL
        }),
    ('overrelief', _default_relief_prop),
    ('padding', {'input_method': 'entry', 'validator': 'tkpadding'}),
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
    ('selectimage', _default_image_prop),
    ('selectmode', {
        'input_method': 'choice',
        'values': ('', tk.BROWSE, tk.SINGLE,
            tk.MULTIPLE, tk.EXTENDED),
        'ttk.Treeview': {
            'values': (tk.EXTENDED, tk.BROWSE, tk.NONE),
            'default': tk.EXTENDED,
            }
        }),
    ('show', {
        'input_method': 'choice',
        'tk.Entry': {
            'values': ('', '•'),
            'readonly': False,
            'default': ''},
        'ttk.Entry': {
            'values': ('', '•'),
            'readonly': False,
            'default': ''},
        'ttk.Treeview': {
            'values': ('', 'tree', 'headings'),
            'default': '',
            'readonly': True},
        'pygubu.builder.widgets.editabletreeview': {
            'values': ('', 'tree', 'headings'),
            'default': '',
            'readonly': True},
        }),
    ('showhandle', _default_true_false_prop),
    ('showvalue', _default_true_false_prop),
    ('sliderlength', _default_dimension_prop),
    ('sliderrelief', _default_relief_prop),
    ('spacing1', _default_spinbox_prop),
    ('spacing2', _default_spinbox_prop),
    ('spacing3', _default_spinbox_prop),
    ('state', {
        'input_method': 'choice',
        'values': ('', tk.NORMAL, tk.DISABLED),
        'tk.Entry': {
            'values': ('', tk.NORMAL, tk.DISABLED, 'readonly')},
        'tk.Combobox': {'values': ('', 'readonly')},
        'ttk.Entry': {
            'values': ('', tk.NORMAL, tk.DISABLED, 'readonly')},
        'ttk.Combobox': { 'values': ('', 'readonly')},
        }),
    ('sticky', _sticky_prop),
    ('stretch', {
        'input_method': 'choice',
        'values': ('True', 'False'),
        'default': 'True',
        'readonly': True}),
    ('style', {
        'input_method': 'entry'
        }), #FIXME Howto manage this property?
    ('tabs', _default_entry_prop), #FIXME see tk.Text tab property
    ('takefocus', _default_true_false_prop),
    ('tearoff', { 'input_method': 'choice',
        'values': ('', tk.TRUE, tk.FALSE),
        'tk.Men': {'default': tk.FALSE},
        'tk.Menuitem.Submen': {'default': tk.FALSE}
        }),
    ('tearoffcommand', _default_entry_prop),
    ('text', _default_textentry_prop),
    ('textvariable', _default_tkvariable_prop),
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
    ('validatecommand_args', { 'input_method': 'entry',
        'validator': 'entry_validate_args' }),
    ('invalidcommand', _default_entry_prop),
    ('invalidcommand_args',  { 'input_method': 'entry',
        'validator': 'entry_validate_args' }),
    ('value', { 'input_method': 'entry', 'validator': 'alphanumeric',
        'ttk.Scale': { 'validator': 'number_float'}
        }),
    ('values', _default_entry_prop), #FIXME This should be treated as a list?
    ('variable',_default_tkvariable_prop),
    ('weight', _default_spinbox_prop),
    ('wrap', { 'input_method': 'choice',
        'values': ('', tk.TRUE, tk.FALSE),
        'tk.Text': {
            'values': (tk.CHAR, tk.WORD, tk.NONE),
            'default': tk.CHAR}
        }),
    ('wraplength', _default_dimension_prop),
    ('xscrollcommand', _default_entry_prop),
    ('xscrollincrement', _default_dimension_prop),
    ('yscrollcommand', _default_entry_prop),
    ('yscrollincrement', _default_dimension_prop),
    #toplevel methods as properties
    ('title', _default_entry_prop),
    ('geometry', _default_entry_prop),
    ('overrideredirect', _default_true_false_prop),
    ('resizable', { 'input_method': 'choice',
        'values': ('', 'both', 'horizontally', 'vertically', 'none'),
        'readonly': True,
        }),
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
        'min': 1, 'max': 50, 'validator': 'number_integer', 'readonly': True}),
    ('columnspan', {
        'input_method': 'spinbox',
        'min': 1, 'max': 50, 'validator': 'number_integer', 'readonly': True}),
    ('padx', {'input_method':'entry', 'validator': 'tkpadding2'}),
    ('pady', {'input_method':'entry', 'validator': 'tkpadding2'}),
    ('ipadx', _default_spinbox_prop),
    ('ipady', _default_spinbox_prop),
    ('propagate', {'input_method': 'choice',
        'values': ('True', 'False'), 'default': 'True'})
)

PropertiesMap[GROUP_LAYOUT_GRID] = OrderedDict(__grid)

__grid_rc = (
    #grid row and column properties (can be applied to each row or column)
    ('minsize', {
        'input_method': 'spinbox',
        'min': 0, 'max':999, 'validator': 'number_integer', 'readonly': True}),
    ('pad', {
        'input_method': 'spinbox',
        'min': 0, 'validator': 'number_integer', 'readonly': True}),
    ('weight', {
        'input_method': 'spinbox',
        'min': 0, 'validator': 'number_integer', 'readonly': True})
)

PropertiesMap[GROUP_LAYOUT_GRID_RC] = OrderedDict(__grid_rc)

__custom = (
    ('class', {
        'input_method': 'entry',
        'readonly': True
        }),
    ('id', {'input_method': 'entry'}),
    ('tree_column', {
        'input_method': 'choice',
        'values': ('True', 'False'),
        'default': 'False',
        'readonly': True
        }),
    ('visible', {
        'input_method': 'choice',
        'values': ('True', 'False'),
        'default': 'True',
        'readonly': True}),
    ('heading_anchor', {
        'input_method': 'choice',
        'values': ('', tk.W, tk.CENTER, tk.E),
        'default': tk.W,
        'readonly': True
        }),
    ('column_anchor', {
        'input_method': 'choice',
        'values': ('', tk.W, tk.CENTER, tk.E),
        'default': tk.W,
        'readonly': True
        }),
    ('scrolltype', {
        'input_method': 'choice',
        'values': ('both', 'vertical', 'horizontal'),
        'default': 'both',
        'readonly': True
        }),
)

PropertiesMap[GROUP_CUSTOM] = OrderedDict(__custom)

def register_custom(name, descr):
    if name not in PropertiesMap[GROUP_CUSTOM]:
        PropertiesMap[GROUP_CUSTOM][name] = descr
    else:
        raise ValueError('Property "{}" already registered'.format(name))


OBJECT_DEFAULT_ATTRS = ('class', 'id')

TRANSLATABLE_PROPERTIES = [
    'label', 'text', 'title',
]
