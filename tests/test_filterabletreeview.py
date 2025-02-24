# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import pygubu
import support
from pygubu.widgets.filterabletreeview import FilterableTreeview


class TestFilterableTreeview(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_filterabletreeview.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainframe")
        self.wtree = builder.get_object("treeview1")

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.wtree, FilterableTreeview)
        self.widget.destroy()
