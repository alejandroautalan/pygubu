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

        def __init__(self, master=None, **kw):
            self.scrolltype = kw.pop('scrolltype', self.VERTICAL)
            super(ScrollbarHelper, self).__init__(master, **kw)
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

    return ScrollbarHelper

TkScrollbarHelper = ScrollbarHelperFactory(tk.Frame, tk.Scrollbar)
