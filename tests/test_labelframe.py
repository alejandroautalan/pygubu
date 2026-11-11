import unittest
from tkinter import ttk

import support

import pygubu


class TestLabelframe(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_labelframe.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("Labelframe")

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.widget, ttk.Labelframe)
        self.widget.destroy()
