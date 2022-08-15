# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk


import fixpath
import pygubu
import support


class TestTkSpinbox(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_tkspinbox.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.widget = self.builder.get_object("test_from")
        self.spinbox = self.builder.get_object("spinbox1")
        self.assertIsInstance(self.spinbox, tk.Spinbox)
        self.widget.destroy()

    def test_from_(self):
        self.widget = self.builder.get_object("test_from")
        spinbox = self.builder.get_object("spinbox1")
        value = spinbox.cget("from")
        self.assertEqual(5, value)
        self.widget.destroy()

    def test_to(self):
        self.widget = self.builder.get_object("test_to")
        spinbox = self.builder.get_object("spinbox2")
        value = spinbox.cget("to")
        self.assertEqual(10, value)
        self.widget.destroy()

    def test_from_to(self):
        self.widget = self.builder.get_object("test_from_to")
        spinbox = self.builder.get_object("spinbox3")
        value_from = spinbox.cget("from")
        value_to = spinbox.cget("to")
        self.assertEqual(2, value_from)
        self.assertEqual(10, value_to)
        self.widget.destroy()
