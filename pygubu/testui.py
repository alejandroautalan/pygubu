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
import argparse
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
    def __init__(self, uifile, rootwidget, rootmenu=None, master=None):
        self.uifile = uifile
        self.rootwidget = rootwidget
        self.rootmenu = rootmenu
        TkApplication.__init__(self, master)

    def _create_ui(self):
        self.builder = Builder()
        self.builder.add_from_file(self.uifile)
        self.builder.get_object(self.rootwidget, self.master)

        if self.rootmenu:
            menu = self.builder.get_object(self.rootmenu, top)
            self.set_menu(menu)

        #show callbacks defined
        bag = {}
        callbacks = self.builder.connect_callbacks({})
        if callbacks is not None:
            for cb in callbacks:
                def create_cb(cbname):
                    def dummy_cb(event=None):
                        print('on:', cbname)
                    return dummy_cb
                bag[cb] = create_cb(cb)
            self.builder.connect_callbacks(bag)
            

        self.set_title('Pygubu UI Tester')
        self.set_resizable()


def main():
    # Setup logging level
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='.ui file')
    parser.add_argument('rootwidget', default='mainwindow', nargs='?',
                        help='Toplevel widget (default: mainwidow)')    
    parser.add_argument('rootmenu', default=None, nargs='?',
                        help='Toplevel menu (default: None)',)
    args = parser.parse_args()
    app = UITester(args.filename, args.rootwidget, args.rootmenu, tk.Tk())
    app.run()


if __name__ == '__main__':
    main()
