from __future__ import unicode_literals
from pygubu.builder.builderobject import *
from pygubu.builder.tkstdwidgets import TKToplevel
from pygubu.widgets.dialog import Dialog


class DialogBO(TKToplevel):
    class_ = Dialog
    
    properties = TKToplevel.properties + ('modal',)
    
    def realize(self, parent):
        BuilderObject.realize(self, parent)
        
    def _set_property(self, target_widget, pname, value):
        if pname == 'modal':
            modal = False
            if value == 'True':
                modal = True
            self.widget.set_modal(modal)
        else:
            super(DialogBO, self)._set_property(self.widget.toplevel, pname, value)

    def get_child_master(self):
        return self.widget.toplevel


register_widget('pygubu.builder.widgets.dialog', DialogBO,
    'Dialog', ('Pygubu Widgets', 'ttk'))


modal_prop = { 'input_method': 'choice',
    'values': ('True', 'False'), 'default':'False', 'readonly': True}

register_property('modal', modal_prop)
