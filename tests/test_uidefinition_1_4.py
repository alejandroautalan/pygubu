# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import support
import pygubu


class TestUIDefinition_1_4(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_uidefinition_1_4.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("fmain")

    def tearDown(self):
        support.root_withdraw()

    def test_is_version_1_4(self):
        value = self.builder.uidefinition.version
        self.assertEqual("1.4", value)
        self.widget.destroy()
