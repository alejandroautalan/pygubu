# encoding: UTF-8

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


try:
    import tkinter as tk
    from tkinter import ttk
except:
    import Tkinter as tk
    import ttk


"""A frame widget that autoarrange children when is resized.
Usefull for frames with several children of same size.
"""

class AutoArrangeFrame(ttk.Frame):

    def __init__(self, master=None, **kw):
        self.__cb = None
        self.__recurse_check = 0
        ttk.Frame.__init__(self, master, **kw)
        self.bind('<Configure>', self.__on_configure)

    def __arrange(self):
        self.__cb = None
        
        self.__recurse_check += 1
        self.update_idletasks()
        self.__recurse_check += -1
        if self.__recurse_check != 0:
            return

        order = []
        sum_width = 0
        count = 0
        maxc, maxr = self.grid_size()
        for r in range(0, maxr):
            for c in range(0, maxc):
                w = self.grid_slaves(row=r, column=c)
                if w:
                    order.append(w[0])
                    width = w[0].winfo_reqwidth()
                    sum_width += width
                    count += 1
        avg_width = sum_width / count

        max_w = self.winfo_width()
        calc_w = 0
        r = c = 0
        first_item = True
        for child in order:
            calc_w += avg_width

            if first_item:
                first_item = False
                continue

            if calc_w >= max_w:
                calc_w = avg_width
                c = 0
                r = r + 1
            else:
                c = c + 1

            info = child.grid_info()
            oldr, oldc = int(info['row']), int(info['column'])
            if oldr != r or oldc != c:
                child.grid_remove()
                child.grid(row=r, column=c)


    def __on_configure(self, event):
        if self.__cb is None:
            self.__cb = self.after_idle(self.__arrange)



if __name__ == '__main__':
    import random

    root = tk.Tk()

    a = AutoArrangeFrame(root)

    for idx in range(1, 20):
        rand = random.randrange(0, 20)
        txt = str(idx) + '_' * rand
        b = ttk.Button(a, text=txt, style='Toolbutton')
        b.grid()

    a.grid(sticky='nsew')

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    tk.mainloop()
