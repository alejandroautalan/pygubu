from __future__ import unicode_literals

from pygubu.builder.builderobject import *
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
    OPTIONS_CUSTOM = ('scrolltype',)
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = ('class_', 'scrolltype')

    def get_child_master(self):
        return self.widget.innerframe

    def configure(self, target=None):
        super(TKScrolledFrameBO, self).configure(self.widget.innerframe)

    def layout(self, target=None):
        self._grid_layout(self.widget, configure_rc=False)
        self._grid_rc_layout(self.widget.innerframe)

register_widget('pygubu.builder.widgets.tkscrolledframe', TKScrolledFrameBO,
    'ScrolledFrame', ('Pygubu Widgets', 'tk'))
