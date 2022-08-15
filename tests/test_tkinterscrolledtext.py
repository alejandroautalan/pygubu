# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText


import fixpath
import pygubu
import support


class TestText(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_tkinterscrolledtext.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainframe")
        self.text = builder.get_object("scrolledtext_1")

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.text, tk.Text)
        self.widget.destroy()
