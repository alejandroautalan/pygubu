import os
import sys
import unittest
import tkinter as tk


pygubu_basedir = os.path.abspath(os.path.dirname(
                    os.path.dirname(os.path.realpath(sys.argv[0]))))
if pygubu_basedir not in sys.path:
    sys.path.insert(0, pygubu_basedir)

import pygubu
import support


class TestVariables(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = """<?xml version="1.0" ?>
<interface>
  <object class="ttk.Frame" id="mainwindow">
    <property name="height">250</property>
    <property name="width">250</property>
    <layout>
      <property name="column">0</property>
      <property name="sticky">nesw</property>
      <property name="propagate">True</property>
      <property name="row">0</property>
    </layout>
    <child>
      <object class="ttk.Entry" id="string_entry">
        <property name="textvariable">string_var</property>
        <property name="validate">none</property>
        <property name="text">string</property>
        <layout>
          <property name="column">0</property>
          <property name="propagate">True</property>
          <property name="row">0</property>
        </layout>
      </object>
    </child>
    <child>
      <object class="ttk.Entry" id="int_entry">
        <property name="textvariable">int_var</property>
        <property name="validate">none</property>
        <property name="text">22</property>
        <layout>
          <property name="column">0</property>
          <property name="propagate">True</property>
          <property name="row">1</property>
        </layout>
      </object>
    </child>
    <child>
      <object class="ttk.Entry" id="double_entry">
        <property name="textvariable">double_var</property>
        <property name="validate">none</property>
        <property name="text">22.22</property>
        <layout>
          <property name="column">0</property>
          <property name="propagate">True</property>
          <property name="row">2</property>
        </layout>
      </object>
    </child>
    <child>
      <object class="ttk.Entry" id="boolean_entry">
        <property name="textvariable">boolean_var</property>
        <property name="validate">none</property>
        <property name="text">False</property>
        <layout>
          <property name="column">0</property>
          <property name="propagate">True</property>
          <property name="row">3</property>
        </layout>
      </object>
    </child>
  </object>
</interface>
"""
        self.builder = builder = pygubu.Builder()
        builder.add_from_string(xmldata)
        self.widget = builder.get_object('mainwindow')


    def tearDown(self):
        support.root_withdraw()

    def test_string_var(self):
        var = self.builder.get_variable('string_var')
        self.assertIsInstance(var, tk.StringVar)
        self.widget.destroy()

    def test_int_var(self):
        var = self.builder.get_variable('int_var')
        self.assertIsInstance(var, tk.IntVar)
        self.widget.destroy()

    def test_double_var(self):
        var = self.builder.get_variable('double_var')
        self.assertIsInstance(var, tk.DoubleVar)
        self.widget.destroy()

    def test_boolean_var(self):
        var = self.builder.get_variable('boolean_var')
        self.assertIsInstance(var, tk.BooleanVar)
        self.assertEqual(False, var.get())
        self.widget.destroy()



if __name__ == '__main__':
    unittest.main()

