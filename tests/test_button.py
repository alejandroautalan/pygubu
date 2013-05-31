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


class TestButton(unittest.TestCase):

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
      <object class="ttk.Button" id="testbutton">
        <property name="class_">CustomButton</property>
        <property name="command">on_button_click</property>
        <property name="compound">right</property>
        <property name="style">CustomButton.TButton</property>
        <property name="text">Button Label</property>
        <property name="textvariable">button_var</property>
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
        self.widget = builder.get_object('testbutton')

        self.is_style_setup = False
        if self.is_style_setup:
            self.is_style_setup = True
            s = ttk.Style()
            s.configure('CustomButton.TButton', color='Blue')


    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.widget, ttk.Button)
        self.widget.destroy()

    def test_class_(self):
        tclobj = self.widget.cget('class')
        class_ = str(tclobj)
        self.assertEqual('CustomButton', class_)
        self.widget.destroy()

    def test_style(self):
        tclobj = self.widget.cget('style')
        style = str(tclobj)
        self.assertEqual('CustomButton.TButton', style)
        self.widget.destroy()

    def test_command_dict(self):
        success = []

        def on_button_click():
            success.append(1)

        cbdic = { 'on_button_click': on_button_click }
        self.builder.connect_callbacks(cbdic)

        self.widget.invoke()
        self.assertTrue(success)
        self.widget.destroy()

    def test_command_self(self):
        success = []

        class AnObject:
            def on_button_click(self):
                success.append(1)

        cbobj = AnObject()
        self.builder.connect_callbacks(cbobj)

        self.widget.invoke()
        self.assertTrue(success)
        self.widget.destroy()

    def test_compound(self):
        compound = str(self.widget.cget('compound'))
        self.assertEqual('right', compound)
        self.widget.destroy()

    def test_btn_text(self):
        txt = self.widget.cget('text')
        self.assertEqual('Button Label', txt)
        self.widget.destroy()

    def test_btn_variable(self):
        var = self.builder.get_variable('button_var')
        self.assertIsInstance(var, tk.StringVar)
        self.assertEqual('Button Label', var.get())

        newlabel = 'Label Changed'
        var.set(newlabel)
        self.assertEqual(newlabel, self.widget.cget('text'))
        self.widget.destroy()




if __name__ == '__main__':
    unittest.main()

