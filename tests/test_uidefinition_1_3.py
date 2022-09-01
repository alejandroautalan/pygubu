# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import support
import pygubu


class TestUIDefinition_1_3(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_uidefinition_1_3.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("fmain")

    def tearDown(self):
        support.root_withdraw()

    def test_is_object_named(self):
        self.assertIsInstance(self.widget, ttk.Frame)
        is_named = self.builder.objects["fmain"].wmeta.is_named
        self.assertTrue(is_named)
        self.widget.destroy()
