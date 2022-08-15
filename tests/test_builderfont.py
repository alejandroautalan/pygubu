# encoding: utf8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont

import fixpath
import pygubu
import support


class TestBuilderFont(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_builderfont.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)

        self.font = font = tkfont.Font(
            family="Helvetica", size=32, weight="bold"
        )
        builder.set_font("custom_font", font)

        self.widget = builder.get_object("mainwindow")

    def tearDown(self):
        support.root_withdraw()

    @unittest.skip("Not implemented yet")
    def test_get_font(self):
        font = self.builder.get_font("custom_font")
        self.assertEqual(self.font, font)
        self.widget.destroy()

    @unittest.skip("Not implemented yet")
    def test_get_font_notset(self):
        fname = "other_font"
        font = self.builder.get_font(fname)
        self.assertEqual(fname, font)
        self.widget.destroy()


if __name__ == "__main__":
    unittest.main()
