# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk


import fixpath
import pygubu
import support


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
