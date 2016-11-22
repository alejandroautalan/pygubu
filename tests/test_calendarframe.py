# encoding: utf8
import os
import sys
import unittest
import datetime

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk


pygubu_basedir = os.path.abspath(os.path.dirname(
                    os.path.dirname(os.path.realpath(sys.argv[0]))))
if pygubu_basedir not in sys.path:
    sys.path.insert(0, pygubu_basedir)

import pygubu
import support
from pygubu.widgets.calendarframe import CalendarFrame


class TestCalendarFrame(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = 'test_calendarframe.ui'
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.mainwindow = builder.get_object('mainwindow')
        self.widget = builder.get_object('calendar')

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.widget, CalendarFrame)
        self.widget.destroy()
        
    def test_selection(self):
        self.assertEqual(None, self.widget.selection)
        
        testdate = datetime.datetime(1980, 9, 15)
        self.widget.select_day(15, 9, 1980)
        
        self.assertEqual(testdate, self.widget.selection)
        self.widget.destroy()
        
    def test_select_day(self):
        testdate = datetime.datetime(1980, 9, 15)
        self.widget.select_day(15, 9, 1980)
        self.assertEqual(testdate, self.widget.selection)
        self.widget.destroy()
        
    def test_event_CalendarDateSelected(self):
        success = []
        
        class AnObject:
            def on_date_selected(self, event=None):
                success.append(1)

        cbobj = AnObject()
        self.builder.connect_callbacks(cbobj)
        self.widget.select_day(15, 9, 1980)
        self.widget.update()
        
        self.assertTrue(success)
        self.widget.destroy()
        
    def test_uiset_options(self):
        widget = self.widget
        self.assertEqual('#f0e3f0', widget['calendarbg'])
        self.assertEqual('#0000a1', widget['calendarfg'])
        
        self.assertEqual('#abb8f0', widget['headerbg'])
        self.assertEqual('#ffffff', widget['headerfg'])
        
        self.assertEqual('#f06ba4', widget['markbg'])
        self.assertEqual('#ffffff', widget['markfg'])
        
        self.assertEqual('#d926ff', widget['selectbg'])
        self.assertEqual('#ffff00', widget['selectfg'])
        
        self.assertEqual('9', str(widget['month']))
        self.assertEqual('2000', str(widget['year']))
        
        self.widget.destroy()


