# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import pygubu
import support


class TestCustomWidget(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_custom_widget.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainwindow")
        self.custom_widget = builder.get_object("custom_widget")

    def tearDown(self):
        support.root_withdraw()

    def test_loading(self):
        message = self.custom_widget.get_message()
        self.assertEqual(message, "CustomLabel")
        self.widget.destroy()
