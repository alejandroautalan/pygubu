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
import logging
try:
    import tkinter as tk
except:
    import Tkinter as tk
from pygubu import ApplicationLevelBindManager as BindManager


logger = logging.getLogger(__name__)

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

        def __init__(self, master=None, **kw):
            self.scrolltype = kw.pop('scrolltype', self.VERTICAL)
            self.usemousewheel = tk.getboolean(kw.pop('usemousewheel', False))
            super(ScrollbarHelper, self).__init__(master, **kw)
            self.vsb = None
            self.hsb = None
            self.cwidget = None
            self._bindingids = []
            self._create_scrollbars()

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
            self.cwidget = cwidget
            cwidget.grid(column=0, row=0, sticky=tk.NSEW, in_=self)

            if self.scrolltype in (self.BOTH, self.VERTICAL):
                if hasattr(cwidget, 'yview'):
                    self.vsb.configure(command=cwidget.yview)
                    cwidget.configure(yscrollcommand=lambda f, l: _autoscroll(self.vsb, f, l))
                else:
                    msg = "widget {} has no attribute 'yview'".format(str(cwidget))
                    logger.info(msg)

            if self.scrolltype in (self.BOTH, self.HORIZONTAL):
                if hasattr(cwidget, 'xview'):
                    self.hsb.configure(command=cwidget.xview)
                    cwidget.configure(xscrollcommand=lambda f, l: _autoscroll(self.hsb, f, l))
                else:
                    msg = "widget {} has no attribute 'xview'".format(str(cwidget))
                    logger.info(msg)
            self._configure_mousewheel()
        
        def configure(self, cnf=None, **kw):
            args = tk._cnfmerge((cnf, kw))
            key = 'usemousewheel'
            if key in args:
                self.usemousewheel = tk.getboolean(args[key])
                del args[key]
                self._configure_mousewheel()
            frame_class.configure(self, args)

        config = configure

        def cget(self, key):
            option = 'usemousewheel'
            if key == option:
                return self.usemousewheel
            return frame_class.cget(self, key)

        __getitem__ = cget
        
        def _configure_mousewheel(self):
            cwidget = self.cwidget
            if self.usemousewheel:
                BindManager.init_mousewheel_binding(self)

                if self.hsb and not hasattr(self.hsb, 'on_mousewheel'):
                    self.hsb.on_mousewheel = BindManager.make_onmousewheel_cb(cwidget, 'x', 2)
                if self.vsb and not hasattr(self.vsb, 'on_mousewheel'):
                    self.vsb.on_mousewheel = BindManager.make_onmousewheel_cb(cwidget, 'y', 2)

                main_sb = self.vsb or self.hsb
                if main_sb:
                    cwidget.on_mousewheel = main_sb.on_mousewheel
                    bid = cwidget.bind('<Enter>',
                                       lambda event: BindManager.mousewheel_bind(cwidget),
                                       add='+')
                    self._bindingids.append((cwidget, bid))
                    bid = cwidget.bind('<Leave>',
                                       lambda event: BindManager.mousewheel_unbind(),
                                       add='+')
                    self._bindingids.append((cwidget, bid))
                for s in (self.vsb, self.hsb):
                    if s:
                        bid = s.bind('<Enter>',
                                     lambda event, scrollbar=s: BindManager.mousewheel_bind(scrollbar),
                                     add='+')
                        self._bindingids.append((s, bid))
                        bid = s.bind('<Leave>',
                                     lambda event: BindManager.mousewheel_unbind(),
                                     add='+')
                        self._bindingids.append((s, bid))
            else:
                for widget, bid in self._bindingids:
                    remove_binding(widget, bid)

    return ScrollbarHelper

TkScrollbarHelper = ScrollbarHelperFactory(tk.Frame, tk.Scrollbar)
