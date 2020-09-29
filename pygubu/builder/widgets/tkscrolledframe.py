# encoding: utf8
from __future__ import unicode_literals

try:
    import tkinter as tk
except:
    import Tkinter as tk

from pygubu.builder.builderobject import BuilderObject, register_widget
from pygubu.widgets.tkscrolledframe import TkScrolledFrame


class TKScrolledFrameBO(BuilderObject):
    class_ = TkScrolledFrame
    container = True
#    maxchildren = 1
#    allowed_children = ('tk.Frame', 'ttk.Frame' )
    OPTIONS_STANDARD = ('borderwidth', 'cursor', 'highlightbackground',
                        'highlightcolor', 'highlightthickness',
                        'padx', 'pady', 'relief', 'takefocus')
    OPTIONS_SPECIFIC = ('background',  'class_', 'container',
                        'height', 'width')
    OPTIONS_CUSTOM = ('scrolltype', 'usemousewheel')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = ('class_', 'scrolltype')

    def get_child_master(self):
        return self.widget.innerframe

    def configure(self, target=None):
        super(TKScrolledFrameBO, self).configure(self.widget.innerframe)
        
    def _set_property(self, target_widget, pname, value):
        if pname in ('usemousewheel',):
            super(TKScrolledFrameBO, self)._set_property(self.widget, pname, value)
        else:
            super(TKScrolledFrameBO, self)._set_property(target_widget, pname, value)

    #def layout(self, target=None, configure_gridrc=True):
    #    super(TKScrolledFrameBO, self).layout(target, False)
    #    self._gridrc_config(self.widget.innerframe)
    
    #
    # Code generation methods
    #
    def code_child_master(self):
        return '{0}.innerframe'.format(self.code_identifier())
    
    def code_configure(self, targetid=None):
        realtarget = '{0}.innerframe'.format(self.code_identifier())
        return super(TKScrolledFrameBO,self).code_configure(realtarget)
    
    def _code_set_property(self, targetid, pname, value, code_bag):
        if pname == 'usemousewheel':
            nvalue = '{0}.configure({1}={2})'.format(self.code_identifier(),
                                                     pname,
                                                     tk.getboolean(value))
            code_bag[pname] = [nvalue]
        else:
            super(TKScrolledFrameBO, self)._code_set_property(targetid, pname,
                                                             value, code_bag)

register_widget('pygubu.builder.widgets.tkscrolledframe', TKScrolledFrameBO,
    'ScrolledFrame', ('Pygubu Widgets', 'tk'))
