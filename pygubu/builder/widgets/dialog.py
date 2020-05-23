# encoding: utf8
from __future__ import unicode_literals
try:
    import tkinter as tk
except:
    import Tkinter as tk

from pygubu.builder.builderobject import *
from pygubu.builder.tkstdwidgets import TKToplevel
from pygubu.widgets.dialog import Dialog


class DialogBO(TKToplevel):
    class_ = Dialog
    OPTIONS_STANDARD = TKToplevel.OPTIONS_STANDARD
    OPTIONS_SPECIFIC = TKToplevel.OPTIONS_SPECIFIC
    OPTIONS_CUSTOM = \
        TKToplevel.OPTIONS_CUSTOM + ('modal',)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    
    def layout(self, target=None):
        super(DialogBO, self).layout(self.widget.toplevel)

    def _set_property(self, target_widget, pname, value):
        if pname == 'modal':
            modal = False
            value = value.lower()
            if value == 'true':
                modal = True
            self.widget.set_modal(modal)
        else:
            super(DialogBO, self)._set_property(
                self.widget.toplevel, pname, value)

    def get_child_master(self):
        return self.widget.toplevel
    
    #
    # Code generation methods
    #
    def code_child_master(self):
        return '{0}.toplevel'.format(self.code_identifier())
    
    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == 'modal':
            code_bag[pname] = "'{0}'".format(value)
        else:
            super(DialogBO, self)._code_set_property(targetid, pname,
                                                     value, code_bag)


register_widget('pygubu.builder.widgets.dialog', DialogBO,
                'Dialog', ('Pygubu Widgets', 'ttk'))


modal_prop = {
    'editor': 'choice',
    'params': {
        'values': ('true', 'false'), 'state': 'readonly'},
    'default': 'false'}

register_property('modal', modal_prop)
