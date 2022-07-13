# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk


pygubu_basedir = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
)
if pygubu_basedir not in sys.path:
    sys.path.insert(0, pygubu_basedir)

import pygubu
import support


class TestOptionMenu(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_optionmenu.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainwindow")

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        optionmenu = self.builder.get_object("optionmenu1")
        self.assertIsInstance(optionmenu, tk.OptionMenu)
        self.widget.destroy()

    def test_no_variable_defined(self):
        optionmenu2 = self.builder.get_object("optionmenu2")
        self.assertIsInstance(optionmenu2, tk.OptionMenu)
        self.widget.destroy()
