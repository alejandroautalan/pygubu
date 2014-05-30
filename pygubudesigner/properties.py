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
#    import tkinter.ttk as ttk
except:
    import Tkinter as tk
#    import ttk


# translator marker
def _(x):
    return x

TK_BITMAPS = (
    'error', 'gray75', 'gray50', 'gray25', 'gray12',
    'hourglass', 'info', 'questhead', 'question', 'warning',
    'document', 'stationery', 'edition', 'application', 'accesory',
    'forder', 'pfolder', 'trash', 'floppy', 'ramdisk', 'cdrom',
    'preferences', 'querydoc', 'stop', 'note', 'caution'
)
TK_CURSORS = (
    'arrow', 'based_arrow_down', 'based_arrow_up', 'boat',
    'bogosity', 'bottom_left_corner', 'bottom_right_corner',
    'bottom_side', 'bottom_tee', 'box_spiral', 'center_ptr',
    'circle', 'clock', 'coffee_mug', 'cross', 'cross_reverse',
    'crosshair', 'diamond_cross', 'dot', 'dotbox', 'double_arrow',
    'draft_large', 'draft_small', 'draped_box', 'exchange', 'fleur',
    'gobbler', 'gumby', 'hand1', 'hand2', 'heart', 'icon',
    'iron_cross', 'left_ptr', 'left_side', 'left_tee', 'leftbutton',
    'll_angle', 'lr_angle', 'man', 'middlebutton', 'mouse', 'none',
    'pencil', 'pirate', 'plus', 'question_arrow', 'right_ptr',
    'right_side', 'right_tee', 'rightbutton', 'rtl_logo',
    'sailboat', 'sb_down_arrow', 'sb_h_double_arrow',
    'sb_left_arrow', 'sb_right_arrow', 'sb_up_arrow',
    'sb_v_double_arrow', 'shuttle', 'sizing', 'spider', 'spraycan',
    'star', 'target', 'tcross', 'top_left_arrow', 'top_left_corner',
    'top_right_corner', 'top_side', 'top_tee', 'trek', 'ul_angle',
    'umbrella', 'ur_angle', 'watch', 'xterm', 'X_cursor')

TK_RELIEFS = (tk.FLAT, tk.RAISED, tk.SUNKEN, tk.GROOVE, tk.RIDGE)

WIDGET_REQUIRED_OPTIONS = (
    ('class',
        {'editor': 'entry',
         'params': {'state': 'readonly'}}),
    ('id',
        {'editor': 'entry'}),
)

WIDGET_STANDARD_OPTIONS = [
    ('accelerator',
        {'editor': 'entry'}),
    ('activerelief',
        {'editor': 'choice',
         'params':
            {'values': ('', tk.FLAT, tk.RAISED, tk.SUNKEN,
                        tk.GROOVE, tk.RIDGE),
             'state': 'readonly'}}),
    ('activestyle',
        {'editor': 'choice',
         'params':
            {'values': ('', 'underline', 'dotbox', 'none')}}),
    ('activebackground',
        {'editor': 'colorentry'}),
    ('activeborderwidth',
        {'editor': 'entry'}),
    ('activeforeground',
        {'editor': 'colorentry'}),
    ('after',
        {'editor': 'entry'}),
    ('bitmap',
        {'editor': 'choice',
         'params': {'values': ('',) + TK_BITMAPS, 'state': 'readonly'}}),
    ('cursor',
        {'editor': 'choice',
         'params': {'values': ('',) + TK_CURSORS, 'state': 'readonly'}}),
    ('highlightbackground',
        {'editor': 'colorentry'}),
    ('highlightcolor',
        {'editor': 'colorentry'}),
    ('highlightthickness',
        {'editor': 'colorentry'}),
    ('indicatoron', {
        'editor': 'choice',
        'params': {'values': ('', tk.TRUE, tk.FALSE), 'state': 'readonly'}}),
    ('insertbackground', {
        'editor': 'colorentry'}),
    ('insertborderwidth', {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999},
        }),
    ('insertofftime', {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 9999, 'increment': 100},
        }),
    ('insertontime', {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 9999, 'increment': 100},
        }),
    ('insertwidth', {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999},
        }),
    ('padx', {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999},
        }),
    ('pady', {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999},
        }),
    ('repeatdelay', {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 9999, 'increment':100},
        }),
    ('repeatinterval', {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 9999, 'increment':100},
        }),
    ('selectbackground', {
        'editor': 'colorentry'}),
    ('selectborderwidth', {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999},
        }),
    ('selectforeground', {
        'editor': 'colorentry'}),
    #
    # ttk
    #

    ('class_',
        {'editor': 'entry'}),
    ('style',
        {'editor': 'choice'}),
    ('takefocus', {
        'editor': 'choice',
        'params': {'values': ('', tk.TRUE, tk.FALSE), 'state': 'readonly'}}),
    # ttk.Entry
    ('xscrollcommand',
        {'editor': 'entry'}),
    # ttk.Treeview
    ('yscrollcommand',
        {'editor': 'entry'}),
]

WIDGET_SPECIFIC_OPTIONS = [
    # ttk.Label
    ('anchor', {
        'editor': 'choice',
        'params': {'values': ('', tk.W, tk.CENTER, tk.E),
                   'state': 'readonly'},
        'tk.Button': {
            'params': {
                'values': (
                    '', 'n', 'ne', 'nw', 'e', 'w', 's', 'se', 'sw', 'center'),
                'state': 'readonly'}},
        }),
    # ttk.Label
    ('background',
        {'editor': 'colorentry'}),
    # ttk.Frame, ttk.Label
    ('borderwidth', {'editor': 'entry'}),
    # ttk.Treeview.Column
    ('column_anchor', {
        'editor': 'choice',
        'params': {'values': ('', tk.W, tk.CENTER, tk.E), 'state': 'readonly'},
        'default': tk.W}),
    # ttk.Button
    ('command',
        {'editor': 'entry'}),
    # ttk.Label
    ('compound',
        {'editor': 'choice',
         'params':
            {'values': ('', tk.TOP, tk.BOTTOM, tk.LEFT, tk.RIGHT)}}),
    ('closeenough', {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999},
        }),
    ('confine', {
        'editor': 'choice',
        'params': {'values': ('', tk.TRUE, tk.FALSE), 'state': 'readonly'}}),
    # ttk.Button
    ('default',
        {'editor': 'choice',
         'params': {'values': ('', 'normal', 'active', 'disabled')}}),
    ('direction', {
        'editor': 'choice',
        'tk.Menubutton': {
            'params': {'values': ('', tk.LEFT, tk.RIGHT, 'above'),
                       'state': 'readonly'}},
        'ttk.Menubutton': {
            'params': {
                'values': ('', 'above', 'below', 'flush',
                           tk.LEFT, tk.RIGHT),
                'state': 'readonly'}},
        }),
    ('disabledbackground',
        {'editor': 'colorentry'}),
    ('disabledforeground',
        {'editor': 'colorentry'}),
    # ttk.Checkbutton, ttk.Entry
    ('exportselection',
        {'editor': 'entry'}),
    # ttk.Label
    ('font',
        {'editor': 'entry'}),
    # ttk.Label
    ('foreground',
        {'editor': 'colorentry'}),
    # ttk.Spinbox
    ('format',
        {'editor': 'entry'}),
    # ttk.Scale, ttk.Spinbox
    ('from_', {
        'editor': 'spinbox',
        'params': {'from_': -999, 'to': 999},
        }),
    # ttk.Scale, ttk.Spinbox
    ('to', {
        'editor': 'spinbox',
        'params': {'from_': -999, 'to': 999},
        }),
    # ttk.Spinbox
    ('increment', {
        'editor': 'spinbox',
        'params': {'from_': -999, 'to': 999}
        }),
    # ttk.Entry
    ('invalidcommand',
        {'editor': 'entry'}),
    # ttk.Label
    ('justify',
        {'editor': 'choice',
         'params': {'values': ('left', 'center', 'right'),
                    'state': 'readonly'}}),
    # ttk.Treeview.Column
    ('heading_anchor', {
        'editor': 'choice',
        'params': {'values': ('', tk.W, tk.CENTER, tk.E), 'state': 'readonly'},
        'default': tk.W}),
    # ttk.Frame,
    ('height',
        {'editor': 'spinbox',
         'params': {'from_': 0, 'to': 999},
         'validator': 'number_integer',
         'tk.Toplevel': {'default': 200},
         'tk.Frame': {'default': 200},
         'ttk.Frame': {'default': 200},
         'tk.LabelFrame': {'default': 200},
         'ttk.Labelframe': {'default': 200},
         'tk.PanedWindow': {'default': 200},
         'ttk.Panedwindow': {'default': 200},
         'ttk.Notebook': {'default': 200},
         'tk.Text': {'default': 10},
         'pygubu.builder.widgets.dialog': {'default': 100}}),
    # ttk.Label
    ('image',
        {'editor': 'imageentry'}),
    # ttk.Labelframe
    ('labelanchor',
        {'editor': 'choice',
         'params': {'values': ('', tk.W, tk.CENTER, tk.E),
                    'state': 'readonly'}}),
    # ttk.Progressbar
    ('length', {
        'editor': 'entry'}),
    # ttk.Treeview.Column
    ('minwidth', {
        'editor': 'spinbox',
        'params': {'from_': 5, 'to': 999},
        'default': '20'}),
    # ttk.Progressbar
    ('mode', {
        'editor': 'choice',
        'params': {
            'values': ('', 'determinate', 'indeterminate'),
            'state': 'readonly'}}),
    # ttk.Progressbar
    ('maximum', {
        'editor': 'entry'}),
    ('offrelief', {
        'editor': 'choice',
        'params': {'values': ('',) + TK_RELIEFS, 'state': 'readonly'}}),
    # ttk.Checkbutton
    ('offvalue',
        {'editor': 'entry',
         'help': _('offvalue_help')}),
    # ttk.Checkbutton
    ('onvalue',
        {'editor': 'entry'}),
    # ttk.Panedwindow
    ('orient', {
        'editor': 'choice',
        'params': {'values': (tk.VERTICAL, tk.HORIZONTAL),
                   'state': 'readonly'},
        'default': tk.HORIZONTAL
        }),
    ('overrelief', {
        'editor': 'choice',
        'params': {'values': ('',) + TK_RELIEFS, 'state': 'readonly'}
        }),
    # ttk.Frame, ttk.Label
    ('padding', {'editor': 'entry'}),
    # ttk.Checkbutton
    ('postcommand', {
        'editor': 'entry'}),
    ('readonlybackground', {
        'editor': 'colorentry'}),
    # ttk.Frame,
    ('relief', {
        'editor': 'choice',
        'params': {'values': ('',) + TK_RELIEFS, 'state': 'readonly'}}),
    ('scrollregion', {
        'editor': 'entry'}),
    ('selectcolor', {
        'editor': 'colorentry'}),
    ('selectimage', {
        'editor': 'imageentry'}),
    # ttk.Treeview
    ('selectmode', {
        'editor': 'choice',
        'params': {
            'values': ('', tk.BROWSE, tk.SINGLE, tk.MULTIPLE, tk.EXTENDED),
            'state': 'readonly'},
        'ttk.Treeview': {
            'params': {
                'values': (tk.EXTENDED, tk.BROWSE, tk.NONE),
                'state': 'readonly'},
            'default': tk.EXTENDED}
        }),
    # ttk.Entry
    ('show', {
        'editor': 'choice',
        'tk.Entry': {
            'params': {'values': ('', '•'), 'state': 'normal'},
            },
        'ttk.Entry': {
            'params': {'values': ('', '•'), 'state': 'normal'},
            },
        'ttk.Treeview': {
            'params': {
                'values': ('', 'tree', 'headings'), 'state': 'readonly'}
            },
        'pygubu.builder.widgets.editabletreeview': {
            'params': {
                'values': ('', 'tree', 'headings'), 'state': 'readonly'}
            },
        }),
    ('state', {
        'editor': 'choice',
        'params': {'values': ('', tk.NORMAL, tk.DISABLED),
                   'state': 'readonly'},
        'tk.Entry': {
            'params': {
                'values': ('', tk.NORMAL, tk.DISABLED, 'readonly'),
                'state': 'readonly'}},
        'tk.Combobox': {
            'params': {
                'values': ('', 'readonly'), 'state': 'readonly'}},
        'ttk.Entry': {
            'params': {
                'values': ('', tk.NORMAL, tk.DISABLED, 'readonly'),
                'state': 'readonly'}},
        'ttk.Combobox': {
            'params': {'values': ('', 'readonly'), 'state': 'readonly'}},
        'ttk.Button': {
            'params': {
                'values': ('', 'normal', 'disabled'),
                'state': 'readonly'}},
        'ttk.Notebook.Tab': {
            'params': {
                'values': ('', 'normal', 'disabled', 'hidden'),
                'state': 'readonly'}}}),
    # ttk.Notebook.Tab
    ('sticky',
        {'editor': 'choice',
         'params':
            {'values':
                ('', 'n', 's', 'w', 'e',
                 'nw', 'ne', 'sw', 'se',
                 'ns', 'we', 'nsw', 'nse', 'nswe'),
             'state': 'readonly'}}),
    # ttk.Treeview.Column
    ('stretch', {
        'editor': 'choice',
        'params': {'values': ('True', 'False'), 'state': 'readonly'},
        'default': 'True'}),
    # ttk.Label
    ('text',
        {'editor': 'text'}),
    # ttk.Label
    ('textvariable',
        {'editor': 'tkvarentry'}),
    ('tristateimage', {
        'editor': 'imageentry'}),
    ('tristatevalue', {
        'editor': 'entry'}),
    # ttk.Label
    ('underline',
        {'editor': 'spinbox'}),
    # ttk.Checkbutton
    ('values',
        {'editor': 'entry'}),
    # ttk.Checkbutton
    ('variable',
        {'editor': 'tkvarentry'}),
    # ttk.Panedwindow.Pane
    ('weight',
        {'editor': 'spinbox', 'params': {'from_': 0, 'to': 9999}}),
    # ttk.Frame, ttk.Label
    ('width',
        {'editor': 'spinbox',
         'params': {'from_': 0, 'to': 999},
         'validator': 'number_integer',
         'tk.Toplevel': {'default': 200},
         'tk.Frame': {'default': 200},
         'ttk.Frame': {'default': 200},
         'tk.LabelFrame': {'default': 200},
         'ttk.Labelframe': {'default': 200},
         'tk.PanedWindow': {'default': 200},
         'ttk.Panedwindow': {'default': 200},
         'ttk.Notebook': {'default': 200},
         'tk.Text': {'default': 50},
         'ttk.Treeview.Column': {'from_': 5, 'default': 200},
         'pygubu.builder.widgets.dialog': {'default': 200}}),
    # ttk.Spinbox
    ('wrap', {
        'editor': 'choice',
        'params': {
            'values': ('', tk.TRUE, tk.FALSE),
            'state': 'readonly'},
        'tk.Text': {
            'params': {
                'values': (tk.CHAR, tk.WORD, tk.NONE),
                'state': 'readonly'},
            'default': tk.CHAR}
        }),
    # ttk.Label
    ('wraplength',
        {'editor': 'entry'}),
    ('xscrollincrement', {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999}
        }),
    ('yscrollincrement', {
        'editor': 'spinbox',
        'params': {'from_': 0, 'to': 999}
        }),
]

WIDGET_CUSTOM_OPTIONS = [
    ('command_id_arg', {
        'editor': 'entry'}),
    ('invalidcommand_args', {
        'editor': 'entry'}),
    ('tree_column', {
        'editor': 'choice',
        'params': {'values': ('True', 'False'), 'state': 'readonly'},
        'default': 'False'}),
    ('validatecommand_args', {
        'editor': 'entry'}),
    ('visible', {
        'editor': 'choice',
        'params': {'values': ('True', 'False'), 'state': 'readonly'},
        'default': 'True'}),
    ('scrolltype', {
        'editor': 'choice',
        'params': {
            'values': ('both', 'vertical', 'horizontal'),
            'state': 'readonly'},
        'default': 'both'}),
]


WIDGET_REQUIRED_PROPERTIES = OrderedDict(WIDGET_REQUIRED_OPTIONS)
WIDGET_PROPERTIES = OrderedDict(WIDGET_STANDARD_OPTIONS +
                                WIDGET_SPECIFIC_OPTIONS +
                                WIDGET_CUSTOM_OPTIONS)

GRID_OPTIONS = (
    # grid packing properties
    ('row',
        {'editor': 'spinbox',
         'params': {'from_': 0, 'to': 50},
         'validator': 'number_integer'}),
    ('column',
        {'editor': 'spinbox',
         'params': {'from_': 0, 'to': 50},
         'validator': 'number_integer'}),
    ('sticky',
        {'editor': 'choice',
         'params':
            {'values':
                ('', 'n', 's', 'w', 'e',
                 'nw', 'ne', 'sw', 'se',
                 'ns', 'we', 'nsw', 'nse', 'nswe'),
             'state': 'readonly'}}),
    ('rowspan',
        {'editor': 'spinbox',
         'params':
            {'from_': 1, 'to': 50},
         'validator': 'number_integer'}),
    ('columnspan', {
        'editor': 'spinbox',
        'params': {'from_': 1, 'to': 50},
        'validator': 'number_integer'}),
    ('padx', {'editor': 'entry', 'validator': 'tkpadding2'}),
    ('pady', {'editor': 'entry', 'validator': 'tkpadding2'}),
    ('ipadx',
        {'editor': 'spinbox',
         'params': {'from_': 0, 'to': 999},
         'validator': 'number_integer'}),
    ('ipady',
        {'editor': 'spinbox',
         'params': {'from_': 0, 'to': 999},
         'validator': 'number_integer'}),
    ('propagate',
        {'editor': 'choice',
         'params': {'values': ('True', 'False')},
         'default': 'True'})
)

GRID_PROPERTIES = OrderedDict(GRID_OPTIONS)

TRANSLATABLE_PROPERTIES = [
    'label', 'text', 'title',
]


def register_custom(name, descr):
    pass
