# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk


import fixpath
import pygubu
import support
from unittest.case import SkipTest

has_tkcalendar = True
try:
    from tkcalendar import Calendar, DateEntry
except ImportError:
    has_tkcalendar = False


class TestTkcalendarCalendar(unittest.TestCase):
    def setUp(self):
        if not has_tkcalendar:
            raise SkipTest("tkcalendar not installed")
        
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
        if not has_tkcalendar:
            raise SkipTest("tkcalendar not installed")
        
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
