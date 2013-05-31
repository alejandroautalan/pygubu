# encoding: utf8
import os
import sys
import unittest
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

import pygubu.widgets.scrollbarhelper
import pygubu.widgets.tkscrollbarhelper


class TestScrollbarHelper(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = """<?xml version="1.0" ?>
<interface>
  <object class="pygubu.builder.widgets.scrollbarhelper" id="scrollbarhelper">
    <property name="scrolltype">both</property>
    <property name="padding">5 5 5 5</property>
    <property name="relief">raised</property>
    <layout>
      <property name="column">0</property>
      <property name="propagate">True</property>
      <property name="row">0</property>
    </layout>
    <child>
      <object class="tk.Canvas" id="tk.Canvas_1">
        <property name="background">#d9d900</property>
        <property name="scrollregion">0 0 10i 10i</property>
        <layout>
          <property name="column">0</property>
          <property name="propagate">True</property>
          <property name="row">0</property>
        </layout>
      </object>
    </child>
  </object>
</interface>
"""
        builder = pygubu.Builder()
        builder.add_from_string(xmldata)
        self.widget = builder.get_object('scrollbarhelper')


    def tearDown(self):
        support.root_withdraw()


    def test_class(self):
        self.assertIsInstance(self.widget,
            pygubu.widgets.scrollbarhelper.ScrollbarHelper)
        self.widget.destroy()

    def test_padding(self):
        expected_value = ('5', '5', '5', '5')
        tclobj = self.widget.cget('padding')
        padding = (str(tclobj[0]), str(tclobj[1]), str(tclobj[2]), str(tclobj[3]))
        self.assertEqual(expected_value, padding)
        self.widget.destroy()



class TestTkScrollbarHelper(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = """<?xml version="1.0" ?>
<interface>
  <object class="pygubu.builder.widgets.tkscrollbarhelper" id="scrollbarhelper">
    <property name="scrolltype">both</property>
    <property name="padx">5</property>
    <property name="pady">10</property>
    <property name="relief">raised</property>
    <layout>
      <property name="column">0</property>
      <property name="propagate">True</property>
      <property name="row">0</property>
    </layout>
    <child>
      <object class="tk.Canvas" id="tk.Canvas_1">
        <property name="background">#d9d900</property>
        <property name="scrollregion">0 0 10i 10i</property>
        <layout>
          <property name="column">0</property>
          <property name="propagate">True</property>
          <property name="row">0</property>
        </layout>
      </object>
    </child>
  </object>
</interface>
"""
        builder = pygubu.Builder()
        builder.add_from_string(xmldata)
        self.widget = builder.get_object('scrollbarhelper')


    def tearDown(self):
        support.root_withdraw()


    def test_class(self):
        self.assertIsInstance(self.widget,
            pygubu.widgets.tkscrollbarhelper.TkScrollbarHelper)
        self.widget.destroy()

    def test_padx(self):
        prop = 'padx'
        expected_value = '5'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()

    def test_pady(self):
        prop = 'pady'
        expected_value = '10'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()


if __name__ == '__main__':
    unittest.main()

