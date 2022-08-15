# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import pygubu
import support


class MyContainer(object):
    pass


class TestText(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_import_variables.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainwindow")

    def tearDown(self):
        support.root_withdraw()

    def test_import_variables(self):
        container = MyContainer()
        self.builder.import_variables(container)
        self.assertIsInstance(container.myvar_string, tk.StringVar)
        self.assertIsInstance(container.myvar_int, tk.IntVar)
        self.assertIsInstance(container.myvar_double, tk.DoubleVar)
        self.assertIsInstance(container.myvar_boolean, tk.BooleanVar)
