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


TK_CURSORS = ('arrow', 'based_arrow_down', 'based_arrow_up', 'boat',
              'bogosity', 'bottom_left_corner', 'bottom_right_corner',
              'bottom_side', 'bottom_tee', 'box_spiral', 'center_ptr',
              'circle', 'clock', 'coffee_mug', 'cross', 'cross_reverse',
              'crosshair', 'diamond_cross', 'dot', 'dotbox', 'double_arrow',
              'draft_large', 'draft_small', 'draped_box', 'exchange', 'fleur',
              'gobbler', 'gumby', 'hand1', 'hand2', 'heart', 'icon',
              'iron_cross', 'left_ptr', 'left_side', 'left_tee', 'leftbutton',
              'll_angle', 'lr_angle', 'man', 'middlebutton', 'mouse',
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
        {'editor': 'entry'}),
    ('activeborderwidth',
        {'editor': 'entry'}),
    ('activeforeground',
        {'editor': 'entry'}),
    ('after',
        {'editor': 'entry'}),
    #
    # ttk
    #
    ('class_',
        {'editor': 'entry'}),
    ('cursor',
        {'editor': 'choice',
         'params': {'values': ('',) + TK_CURSORS, 'state': 'readonly'}}),
    ('takefocus',
        {'editor': 'choice',
         'params': {'values': ('', tk.TRUE, tk.FALSE), 'state': 'readonly'}}),
    ('style',
        {'editor': 'choice'}),
    ('state',
        {'editor': 'choice',
         'params':
            {'values': ('', tk.NORMAL, tk.DISABLED), 'state': 'readonly'},
        'tk.Entry':
            {'params': {'values': ('', tk.NORMAL, tk.DISABLED, 'readonly')}},
        'tk.Combobox':
            {'params': {'values': ('', 'readonly')}},
        'ttk.Entry':
            {'params': {'values': ('', tk.NORMAL, tk.DISABLED, 'readonly')}},
        'ttk.Combobox':
            {'params': {'values': ('', 'readonly')}},
        'ttk.Button':
            {'params': {'values': ('', 'normal', 'disabled')}}}),
    # ttk.Label
    ('text',
        {'editor': 'text'}),
    # ttk.Label
    ('textvariable',
        {'editor': 'tkvarentry'}),
    # ttk.Label
    ('underline',
        {'editor': 'spinbox'}),
    # ttk.Label
    ('image',
        {'editor': 'entry'}),
    # ttk.Label
    ('compound',
        {'editor': 'choice',
         'params':
            {'values': ('', tk.TOP, tk.BOTTOM, tk.LEFT, tk.RIGHT)}}),
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
    # ttk.Frame, ttk.Label
    ('borderwidth', {'editor': 'entry'}),
    # ttk.Frame,
    ('relief',
        {'editor': 'choice',
         'params': {'values': ('',) + TK_RELIEFS, 'state': 'readonly'}}),
    # ttk.Frame, ttk.Label
    ('padding', {'editor': 'entry'}),
    # ttk.Label
    ('anchor',
        {'editor': 'choice',
         'params': {'values': ('', tk.W, tk.CENTER, tk.E)}}),
    # ttk.Label
    ('background',
        {'editor': 'entry'}),
    # ttk.Label
    ('font',
        {'editor': 'entry'}),
    # ttk.Label
    ('foreground',
        {'editor': 'entry'}),
    # ttk.Label
    ('justify',
        {'editor': 'entry'}),
]

WIDGET_SPECIFIC_OPTIONS = [
    # ttk.Button
    ('command',
        {'editor': 'entry'}),
    # ttk.Button
    ('default',
        {'editor': 'choice',
         'params':{'values':('', 'normal', 'active', 'disabled')}}),
    # ttk.Label
    ('wraplength',
        {'editor': 'entry'}),
    # ttk.Checkbutton
    ('offvalue',
        {'editor': 'entry',
         'help': _('offvalue_help')}),
    # ttk.Checkbutton
    ('onvalue',
        {'editor': 'entry'}),
    # ttk.Checkbutton
    ('variable',
        {'editor': 'tkvarentry'}),
]

WIDGET_CUSTOM_OPTIONS = []


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
