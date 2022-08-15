# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import pygubu
import support


class TestIdtocommand(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_idtocommand.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainwindow")
        self.button = builder.get_object("button1")

    def tearDown(self):
        support.root_withdraw()

    def test_idtocommand(self):
        success = []

        class AnObject:
            def on_button_clicked(self, widgetid):
                success.append(1)

        cbobj = AnObject()
        self.builder.connect_callbacks(cbobj)
        self.button.invoke()
        self.widget.update()

        self.assertTrue(success)
        self.widget.destroy()
