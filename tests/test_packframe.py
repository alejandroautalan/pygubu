# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import pygubu
import support

from pygubu.widgets.packframe import PackFrame, Direction


class TestPackFrame(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_packframe.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainframe")
        self.pfh = builder.get_object("pfh")
        self.pfv = builder.get_object("pfv")

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.pfh, PackFrame)
        self.assertIsInstance(self.pfv, PackFrame)
        self.widget.destroy()

    def test_direction_horizontal(self):
        prop = "pack_direction"
        expected_value = Direction.ROW
        value = self.pfh.cget(prop)
        self.assertEqual(value, expected_value)
        self.widget.destroy()

    def test_direction_vertical(self):
        prop = "pack_direction"
        expected_value = Direction.COLUMN
        value = self.pfv.cget(prop)
        self.assertEqual(value, expected_value)
        self.widget.destroy()
