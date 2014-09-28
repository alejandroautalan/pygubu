# encoding: utf8
import os
import sys
import unittest
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk


pygubu_basedir = os.path.abspath(os.path.dirname(
                    os.path.dirname(os.path.realpath(sys.argv[0]))))
if pygubu_basedir not in sys.path:
    sys.path.insert(0, pygubu_basedir)

import pygubu
import support


class TestMenu(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = 'test_menu.ui'
        self.builder = builder = pygubu.Builder()
        filepath = os.path.dirname(os.path.realpath(__file__))
        builder.add_resource_path(filepath)
        builder.add_from_file(xmldata)
        self.widget = builder.get_object('mainmenu')

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.widget, tk.Menu)
        self.widget.destroy()
