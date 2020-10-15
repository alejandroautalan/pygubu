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



class TestToplevelMenuHelper(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = 'test_toplevelmenuhelper.ui'
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object('toplevel')
        self.menuhelper = builder.get_object('topmenuhelper')
        self.menu = builder.get_object('topmenu')

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.menu, tk.Menu)
        self.widget.destroy()
        
    def test_class_topmenu(self):
        menu1 = self.widget.nametowidget(self.widget.cget('menu'))
        self.assertEqual(menu1, self.menu)
        self.widget.destroy()
