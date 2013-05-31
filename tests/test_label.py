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


class TestEntry(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = """<?xml version="1.0" ?>
<interface>
  <object class="ttk.Frame" id="mainwindow">
    <property name="height">250</property>
    <property name="width">250</property>
    <layout>
      <property name="column">0</property>
      <property name="sticky">nsew</property>
      <property name="propagate">True</property>
      <property name="row">0</property>
    </layout>
    <child>
      <object class="ttk.Label" id="label">
        <property name="anchor">e</property>
        <property name="background">#94f900</property>
        <property name="borderwidth">2</property>
        <property name="compound">right</property>
        <property name="foreground">#690400</property>
        <property name="padding">2</property>
        <property name="relief">ridge</property>
        <property name="text">-- A Label --</property>
        <property name="textvariable">label_var</property>
        <property name="width">20</property>
        <property name="justify">right</property>
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
        self.builder = builder = pygubu.Builder()
        builder.add_from_string(xmldata)
        self.widget = builder.get_object('label')

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.widget, ttk.Label)
        self.widget.destroy()

    def test_text(self):
        prop = 'text'
        expected_value = '-- A Label --'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()

    def test_textvariable(self):
        varname = 'label_var'
        expected_value = '-- A Label --'
        var = self.builder.get_variable(varname)
        self.assertIsInstance(var, tk.StringVar)
        self.assertEqual(expected_value, var.get())

        newlabel = 'Changed'
        var.set(newlabel)
        self.assertEqual(newlabel, self.widget.cget('text'))
        self.widget.destroy()

    def test_justify(self):
        prop = 'justify'
        expected_value = 'right'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()

    def test_anchor(self):
        prop = 'anchor'
        expected_value = 'e'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()

    def test_background(self):
        prop = 'background'
        expected_value = '#94f900'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()

    def test_borderwidth(self):
        prop = 'borderwidth'
        expected_value = '2'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()

    def test_compound(self):
        prop = 'compound'
        expected_value = 'right'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()

    def test_foreground(self):
        prop = 'foreground'
        expected_value = '#690400'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()

    def test_padding(self):
        prop = 'padding'
        expected_value = '2'
        tclobj = self.widget.cget(prop)[0]
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()

    def test_relief(self):
        prop = 'relief'
        expected_value = 'ridge'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()

    def test_width(self):
        prop = 'width'
        expected_value = '20'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()



if __name__ == '__main__':
    unittest.main()

