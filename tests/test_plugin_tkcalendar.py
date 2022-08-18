# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk


import fixpath
import pygubu
import support
from tkcalendar import Calendar, DateEntry


class TestTkcalendarCalendar(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_plugin_tkcalendar.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("frame1")
        self.calendar = builder.get_object("calendar")

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.calendar, Calendar)
        self.widget.destroy()


class TestTkcalendarDateEntry(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_plugin_tkcalendar.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("frame2")
        self.entry = builder.get_object("dateentry")

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.entry, DateEntry)
        self.widget.destroy()
