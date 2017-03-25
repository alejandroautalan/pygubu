from __future__ import unicode_literals

from pygubu.builder.builderobject import *
from pygubu.widgets.scrolledframe import ScrolledFrame


class TTKScrolledFrameBO(BuilderObject):
    class_ = ScrolledFrame
    container = True
#    maxchildren = 1
#    allowed_children = ('tk.Frame', 'ttk.Frame' )
    OPTIONS_STANDARD = ('class_', 'cursor', 'takefocus', 'style')
    OPTIONS_SPECIFIC = ('borderwidth', 'relief', 'padding', 'height', 'width')
    OPTIONS_CUSTOM = ('scrolltype', 'usemousewheel')
    properties = OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    ro_properties = ('class_', 'scrolltype', )

    def get_child_master(self):
        return self.widget.innerframe

    def configure(self, target=None):
        super(TTKScrolledFrameBO, self).configure(self.widget.innerframe)

    def _set_property(self, target_widget, pname, value):
        if pname in ('usemousewheel',):
            super(TTKScrolledFrameBO, self)._set_property(self.widget, pname, value)
        else:
            super(TTKScrolledFrameBO, self)._set_property(target_widget, pname, value)
    
    def layout(self, target=None):
        self._grid_layout(self.widget, configure_rc=False)
        self._grid_rc_layout(self.widget.innerframe)
        

register_widget('pygubu.builder.widgets.scrolledframe', TTKScrolledFrameBO,
    'ScrolledFrame', ('Pygubu Widgets', 'ttk'))
