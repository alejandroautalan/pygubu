import tkinter as tk
import unittest

import support

import pygubu


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
