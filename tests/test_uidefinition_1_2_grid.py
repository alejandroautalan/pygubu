# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import support
import pygubu


class TestUIDefinition_1_2(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_uidefinition_1_2_grid.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("fmain")
        self.fgrid = builder.get_object("fgrid")

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.widget, ttk.Frame)
        self.widget.destroy()

    def test_gridrc_row_options(self):
        config = self.fgrid.grid_rowconfigure(0)
        # {'minsize': 10, 'pad': 10, 'weight': 1, 'uniform': 'x'}
        self.assertEqual(config["minsize"], 10)
        self.assertEqual(config["pad"], 10)
        self.assertEqual(config["weight"], 1)
        self.assertEqual(config["uniform"], "x")

    def test_gridrc_column_options(self):
        config = self.fgrid.grid_columnconfigure(0)
        # {'minsize': 30, 'pad': 15, 'weight': 1, 'uniform': 'y'}
        self.assertEqual(config["minsize"], 30)
        self.assertEqual(config["pad"], 15)
        self.assertEqual(config["weight"], 1)
        self.assertEqual(config["uniform"], "y")
