# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import support
import pygubu


class TestBuilder01(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_builder_forget_unnamed.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("fmain")
        builder.connect_callbacks({})
        builder.forget_unnamed()

    def tearDown(self):
        support.root_withdraw()

    def test_builder_forget_unnamed(self):
        expected = ["fmain", "mylabel1", "mylabel2"]
        result = list(self.builder.objects.keys())
        self.assertEqual(expected, result)
        self.widget.destroy()
