#
# Copyright 2012 Alejandro Autalán
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

import sys

import tkinter
from tkinter import ttk

import util
import builder


class UITester(util.Application):
    def _create_ui(self):
        self.builder = builder.Tkbuilder()
        self.builder.add_from_file(sys.argv[1])
        self.builder.get_object(self, 'mainwindow')

        self.grid(row=0, column=0, sticky='nswe')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.set_title('Pygubu UI tester')

        self.set_resizable()

try:
    __file__
except:
    sys.argv = [sys.argv[0], 'exampleui_2.tkb']

if __name__ == '__main__':
    app = UITester(tkinter.Tk())
    app.run()
