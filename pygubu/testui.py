#!/usr/bin/python3
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
# For further info, check  http://pygubu.web.here

from __future__ import unicode_literals

import sys
import os
try:
    import tkinter as tk
except:
    import Tkinter as tk

pygubu_basedir = os.path.abspath(os.path.dirname(
                    os.path.dirname(os.path.realpath(sys.argv[0]))))
if pygubu_basedir not in sys.path:
    sys.path.insert(0, pygubu_basedir)


from pygubu import Builder, TkApplication


class UITester(TkApplication):
    def _create_ui(self):
        self.builder = Builder()
        self.builder.add_from_file(sys.argv[1])
        self.builder.get_object('mainwindow', self.master)

        try:
            menu = self.builder.get_object('mainmenu', top)
            self.set_menu(menu)
        except:
            pass

        #show callbacks defined
        self.builder.connect_callbacks({})

        self.set_title('Pygubu UI tester')
        self.set_resizable()

if len(sys.argv) == 1:
    print('Nombre archivo:')
    filename = input()
    sys.argv = [sys.argv[0], filename]

if __name__ == '__main__':
    app = UITester(tk.Tk())
    app.run()
