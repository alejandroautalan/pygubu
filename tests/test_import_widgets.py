# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk


import fixpath
import pygubu
import support


class MyContainer(object):
    pass


class TestImportWidgets(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_import_widgets.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainwindow")

    def tearDown(self):
        support.root_withdraw()

    def test_import_widgets_named(self):
        container = MyContainer()
        self.builder.import_widgets(container)
        self.assertIsInstance(container.label_username, ttk.Label)
        self.assertIsInstance(container.entry_username, ttk.Entry)
        self.assertFalse(hasattr(container, "frame2"))
        self.assertFalse(hasattr(container, "button1"))

    def test_import_widgets_all(self):
        container = MyContainer()
        self.builder.import_widgets(container, user_named=False)
        self.assertIsInstance(container.label_username, ttk.Label)
        self.assertIsInstance(container.entry_username, ttk.Entry)
        self.assertIsInstance(container.mainwindow, ttk.Frame)
        self.assertIsInstance(container.frame2, ttk.Frame)
        self.assertIsInstance(container.button1, ttk.Button)
