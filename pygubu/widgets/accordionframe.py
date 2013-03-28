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

import tkinter as tk
from tkinter import ttk

from ..builderobject import *


class AccordionFrame(ttk.Frame):
    """ An accordion like widget.
    Usage:
        acframe = AccordionFrame(master)
        acframe.grid()
        g = acframe.add_group('g1', 'Group1')
        label = ttk.Label(g, text='Label on group1')
        label.grid()
    """

    def __init__(self, master=None, **kw):
        super(AccordionFrame, self).__init__(master, **kw)
        self.__groups = {}
        self.columnconfigure(0, weight=1)


    def add_group(self, gid, label=None):

        glabel = label
        if label is None:
            glabel = str(gid)

        #button creation
        btn = ttk.Button(self, text=glabel, style='DDFButton.TButton')
        btn.grid(sticky=tk.EW)
        btn.dd_show = True
        btn.configure(command=lambda:self.on_grp_button_clicked(gid))

        #frame creation
        frame = ttk.Frame(self, width=100, height=100)
        frame.grid(sticky=tk.NSEW)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        #Configure resizing of rows
        #position = len(self.__groups)  + 1
        #self.rowconfigure(position, weight=1)

        #store button, and frame
        self.__groups[gid] = (btn, frame)

        return frame

    def on_grp_button_clicked(self, gid):
        btn, frame = self.__groups[gid]
        if btn.dd_show == True:
            btn.dd_show = False
            frame.grid_remove()
        else:
            btn.dd_show = True
            frame.grid()



class AccordionFrameBO(BuilderObject):
    class_ = AccordionFrame
    container = False


register_widget('pygubu.widgets.accordionframe', AccordionFrameBO,
    'AccordionFrame', ('container',))


if __name__ == '__main__':
    root = tk.Tk()

    s = ttk.Style()
    s.configure('DDFButton.TButton', anchor=tk.W)

    app = AccordionFrame(root)
    app.grid(sticky=tk.NSEW)

    top = app.winfo_toplevel()
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)

    g = app.add_group('g1', 'Group1')
    l = tk.Label(g, text="Label1")
    l.grid()
    l = tk.Label(g, text="Label2")
    l.grid()
    g = app.add_group('g2', 'Group2')
    l = tk.Label(g, text="Label3")
    l.grid()
    l = tk.Label(g, text="Label4")
    l.grid()

    tk.mainloop()


