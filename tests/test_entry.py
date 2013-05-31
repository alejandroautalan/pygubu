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
      <object class="ttk.Entry" id="entry">
        <property name="justify">center</property>
        <property name="style">MyEntryStyle.TEntry</property>
        <property name="textvariable">entry_var</property>
        <property name="validate">key</property>
        <property name="validatecommand">entry_validate</property>
        <property name="text">Hello</property>
        <property name="validatecommand_args">%d %P</property>
        <property name="invalidcommand">entry_invalid</property>
        <property name="invalidcommand_args">%P</property>
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
        self.widget = builder.get_object('entry')

        self.is_style_setup = False
        if self.is_style_setup:
            self.is_style_setup = True
            s = ttk.Style()
            s.configure('MyEntryStyle.TEntry', color='Blue')


    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.widget, ttk.Entry)
        self.widget.destroy()

#    def test_class_(self):
#        tclobj = self.widget.cget('class')
#        class_ = str(tclobj)
#        self.assertEqual('MyEntry', class_)
#        self.widget.destroy()

    def test_style(self):
        stylename = 'MyEntryStyle.TEntry'
        tclobj = self.widget.cget('style')
        style = str(tclobj)
        self.assertEqual(stylename, style)
        self.widget.destroy()

    def test_text(self):
        txt = self.widget.get()
        self.assertEqual('Hello', txt)
        self.widget.destroy()

    def test_variable(self):
        varname = 'entry_var'
        var = self.builder.get_variable(varname)
        self.assertIsInstance(var, tk.StringVar)
        self.assertEqual('Hello', var.get())

        newlabel = 'Changed'
        var.set(newlabel)
        self.assertEqual(newlabel, self.widget.get())
        self.widget.destroy()

    def test_validate_command(self):
        valid_values = ('Valid value1', 'Valid value2')

        def entry_validate(action, newvalue):
            valid = False
            if action == '1':   #1: insert 0: delete
                if newvalue in valid_values:
                    valid = True
            else:
                valid = True
            return valid

        def entry_invalid(newvalue):
            pass

        callback = {'entry_validate': entry_validate,
            'entry_invalid': entry_invalid}

        self.builder.connect_callbacks(callback)

        self.widget.delete('0', tk.END)
        self.assertEqual('', self.widget.get())

        self.widget.insert('0', valid_values[0])
        self.assertEqual(valid_values[0], self.widget.get())

        self.widget.delete('0', tk.END)
        self.widget.insert('0', 'Invalid value')
        self.assertEqual('', self.widget.get())

        self.widget.destroy()

    def test_invalid_command(self):
        invalid_text = []

        def entry_validate(action, newvalue):
            valid = False
            if action == '1':   #1: insert 0: delete
                if newvalue == 'Allowed':
                    valid = True
            else:
                valid = True
            return valid

        def entry_invalid(newvalue):
            invalid_text.append(newvalue)

        callback = {'entry_validate': entry_validate,
            'entry_invalid': entry_invalid}

        self.widget.delete('0', tk.END)

        self.builder.connect_callbacks(callback)

        self.widget.insert('0', 'Not Allowed')
        self.assertEqual(invalid_text[0], 'Not Allowed')

        self.widget.destroy()

    def test_justify(self):
        prop = 'justify'
        expected_value = 'center'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()

    def test_validate(self):
        prop = 'validate'
        expected_value = 'key'
        tclobj = self.widget.cget(prop)
        value = str(tclobj)
        self.assertEqual(expected_value, value)
        self.widget.destroy()




if __name__ == '__main__':
    unittest.main()

