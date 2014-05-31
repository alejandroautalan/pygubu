from __future__ import unicode_literals
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

    def realize(self, parent):
        BuilderObject.realize(self, parent)

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


register_widget('pygubu.builder.widgets.dialog', DialogBO,
                'Dialog', ('Pygubu Widgets', 'ttk'))


modal_prop = {
    'editor': 'choice',
    'params': {
        'values': ('true', 'false'), 'state': 'readonly'},
    'default': 'false'}

register_property('modal', modal_prop)
