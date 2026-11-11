import unittest
from tkinter import ttk

import support

import pygubu


class TestSpinbox(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_ttkspinbox.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainwindow")
        self.spinbox = builder.get_object("spinbox1")

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.spinbox, ttk.Spinbox)
        self.widget.destroy()
