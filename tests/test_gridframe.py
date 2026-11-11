# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import pygubu
import support

from pygubu.widgets.gridframe import GridFrame, Direction


class TestGridFrame(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_gridframe.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainframe")
        self.gfh = builder.get_object("gfh")
        self.gfv = builder.get_object("gfv")

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.gfh, GridFrame)
        self.assertIsInstance(self.gfv, GridFrame)
        self.widget.destroy()

    def test_flow_horizontal(self):
        prop = "grid_flow"
        expected_value = Direction.ROW
        value = self.gfh.cget(prop)
        self.assertEqual(value, expected_value)
        self.widget.destroy()

    def test_flow_vertical(self):
        prop = "grid_flow"
        expected_value = Direction.COLUMN
        value = self.gfv.cget(prop)
        self.assertEqual(value, expected_value)
        self.widget.destroy()
