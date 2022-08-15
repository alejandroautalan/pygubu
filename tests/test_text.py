# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk


import fixpath
import pygubu
import support


class TestText(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_text.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainframe")
        self.text = builder.get_object("Text_1")

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.text, tk.Text)
        self.widget.destroy()
