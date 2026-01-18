# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import pygubu
import support
from pygubu.widgets.accordionframe import AccordionFrame


class TestWidgetTkNames(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_tknames.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("myframe1")

    def tearDown(self):
        support.root_withdraw()

    def test_widget_tk_names(self):
        map = [
            (".myframe1", self.widget),
            (".myframe1.mylabel1", self.builder.get_object("mylabel1")),
            (".myframe1.mybutton1", self.builder.get_object("mybutton1")),
            (".myframe1.myentry1", self.builder.get_object("myentry1")),
            (".myframe1.mbtn.mmain", self.builder.get_object("mmain")),
            (".myframe1.mbtn.mmain.mfile", self.builder.get_object("mfile")),
            (
                ".myframe1.mbtn.mmain.mfile.mrecent",
                self.builder.get_object("mrecent"),
            ),
            (
                ".myframe1.mbtn.mmain.help",
                self.builder.get_object("mhelp_special"),
            ),
        ]
        for name, widget in map:
            self.assertEqual(name, str(widget))
        self.widget.destroy()
