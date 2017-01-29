# encoding: utf8
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
# For further info, check  https://github.com/alejandroautalan/pygubu

from __future__ import unicode_literals
import platform

try:
    import tkinter as tk
except:
    import Tkinter as tk

def _autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed.
    Code from Joe English (JE) at http://wiki.tcl.tk/950"""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


def ScrollbarHelperFactory(frame_class, scrollbar_class):

    class ScrollbarHelper(frame_class, object):
        VERTICAL = 'vertical'
        HORIZONTAL = 'horizontal'
        BOTH = 'both'
        # Mouse wheel support
        __active_area = None
        __init_binding = True
        __OS = platform.system()
        
        @staticmethod
        def on_mouse_wheel(event):
            if ScrollbarHelper.__active_area:
                ScrollbarHelper.__active_area.on_mouse_wheel(event)
        
        @staticmethod
        def mouse_wheel_bind(widget):
            ScrollbarHelper.__active_area = widget
        
        @staticmethod
        def mouse_wheel_unbind():
            ScrollbarHelper.__active_area = None

        def __init__(self, master=None, **kw):
            self.scrolltype = kw.pop('scrolltype', self.VERTICAL)
            super(ScrollbarHelper, self).__init__(master, **kw)
            self.vsb = None
            self.hsb = None
            self._create_scrollbars()
            
            if ScrollbarHelper.__init_binding == True:
                
                if self.__OS == "Linux" :
                    master.bind_all('<4>', ScrollbarHelper.on_mouse_wheel,  add='+')
                    master.bind_all('<5>', ScrollbarHelper.on_mouse_wheel,  add='+')
                else:
                    # Windows and MacOS
                    master.bind_all("<MouseWheel>", ScrollbarHelper.on_mouse_wheel,  add='+')
            ScrollbarHelper.__init_binding = False
        
        def _make_onmousewheel_cb(self, widget, orient, factor = 1):
            view_command = getattr(widget, orient+'view')
            if self.__OS == 'Linux':
                def on_mouse_wheel(event):
                    if event.num == 4:
                        view_command("scroll",(-1)*factor,"units")
                    elif event.num == 5:
                        view_command("scroll",factor,"units") 
            
            elif self.__OS == 'Windows':
                def on_mouse_wheel(event):        
                    view_command("scroll",(-1)*int((event.delta/120)*factor),"units") 
            
            elif self.__OS == 'Darwin':
                def on_mouse_wheel(event):        
                    view_command("scroll",event.delta,"units")             
            
            return on_mouse_wheel

        def _create_scrollbars(self):
            if self.scrolltype in (self.BOTH, self.VERTICAL):
                self.vsb = scrollbar_class(self, orient="vertical")
                #layout
                self.vsb.grid(column=1, row=0, sticky=tk.NS)

            if self.scrolltype in (self.BOTH, self.HORIZONTAL):
                self.hsb = scrollbar_class(self, orient="horizontal")
                self.hsb.grid(column=0, row=1, sticky=tk.EW)

            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)

        def add_child(self, cwidget):
            cwidget.grid(column=0, row=0, sticky=tk.NSEW, in_=self)

            if self.scrolltype in (self.BOTH, self.VERTICAL):
                if hasattr(cwidget, 'yview'):
                    self.vsb.configure(command=cwidget.yview)
                    cwidget.configure(yscrollcommand=lambda f, l: _autoscroll(self.vsb, f, l))
                else:
                    msg = "widget {} has no attribute 'yview'".format(str(cwidget))
                    logger.warning(msg)

            if self.scrolltype in (self.BOTH, self.HORIZONTAL):
                if hasattr(cwidget, 'xview'):
                    self.hsb.configure(command=cwidget.xview)
                    cwidget.configure(xscrollcommand=lambda f, l: _autoscroll(self.hsb, f, l))
                else:
                    msg = "widget {} has no attribute 'xview'".format(str(cwidget))
                    logger.warning(msg)
            
            if self.hsb and not hasattr(self.hsb, 'on_mouse_wheel'):
                self.hsb.on_mouse_wheel = self._make_onmousewheel_cb(cwidget, 'x', 2)
            if self.vsb and not hasattr(self.vsb, 'on_mouse_wheel'):
                self.vsb.on_mouse_wheel = self._make_onmousewheel_cb(cwidget, 'y', 2)
            
            main_sb = self.vsb or self.hsb
            if main_sb:
                cwidget.on_mouse_wheel = main_sb.on_mouse_wheel
                cwidget.bind('<Enter>', lambda event: ScrollbarHelper.mouse_wheel_bind(cwidget))
                cwidget.bind('<Leave>', lambda event: ScrollbarHelper.mouse_wheel_unbind())
            for s in (self.vsb, self.hsb):
                if s:
                    s.bind('<Enter>', lambda event, scrollbar=s: ScrollbarHelper.mouse_wheel_bind(scrollbar) )
                    s.bind('<Leave>', lambda event: ScrollbarHelper.mouse_wheel_unbind())

    return ScrollbarHelper

TkScrollbarHelper = ScrollbarHelperFactory(tk.Frame, tk.Scrollbar)
