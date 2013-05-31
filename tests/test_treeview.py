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


class TestTreeview(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = """<?xml version="1.0" ?>
<interface>
  <object class="ttk.Frame" id="mainwindow">
    <property name="height">250</property>
    <property name="width">250</property>
    <layout>
      <property name="sticky">nesw</property>
      <property name="row">0</property>
      <property name="column">0</property>
      <property name="propagate">True</property>
    </layout>
    <child>
      <object class="ttk.Treeview" id="treeview">
        <property name="selectmode">browse</property>
        <layout>
          <property name="column">0</property>
          <property name="row">0</property>
          <property name="propagate">True</property>
        </layout>
        <child>
          <object class="ttk.Treeview.Column" id="treecolumn">
            <property name="tree_column">True</property>
            <property name="visible">True</property>
            <property name="text">Tree</property>
            <property name="command">on_treecolumn_click</property>
            <property name="heading_anchor">w</property>
            <property name="column_anchor">w</property>
            <property name="minwidth">200</property>
            <property name="stretch">True</property>
            <property name="width">200</property>
          </object>
        </child>
        <child>
          <object class="ttk.Treeview.Column" id="column1">
            <property name="tree_column">False</property>
            <property name="visible">True</property>
            <property name="text">Column 1</property>
            <property name="heading_anchor">center</property>
            <property name="column_anchor">w</property>
            <property name="minwidth">200</property>
            <property name="stretch">False</property>
            <property name="width">200</property>
          </object>
        </child>
        <child>
          <object class="ttk.Treeview.Column" id="hidden_column">
            <property name="tree_column">False</property>
            <property name="visible">False</property>
            <property name="text">hidden</property>
            <property name="heading_anchor">w</property>
            <property name="column_anchor">w</property>
            <property name="minwidth">20</property>
            <property name="stretch">True</property>
            <property name="width">200</property>
          </object>
        </child>
      </object>
    </child>
  </object>
</interface>
"""
        self.builder = builder = pygubu.Builder()
        builder.add_from_string(xmldata)
        self.widget = builder.get_object('treeview')
        self.widget.wait_visibility()


    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.widget, ttk.Treeview)
        self.widget.destroy()

    def test_selectmode(self):
        expected = 'browse'
        value = str(self.widget.cget('selectmode'))
        self.assertEqual(expected, value)
        self.widget.destroy()

    def test_columns(self):
        columns = ('column1', 'hidden_column')
        wcolumns = self.widget.cget('columns')
        self.assertEqual(columns, wcolumns)

        dcolumns = ('column1',)
        wdcolumns = self.widget.cget('displaycolumns')
        self.assertEqual(dcolumns, wdcolumns)

        self.widget.destroy()

    def test_tree_heading(self):
        wh = self.widget.heading('#0')
        heading = {
            'text': 'Tree',
            'anchor': 'w',
            }
        for k, v in heading.items():
            self.assertEqual(v, wh[k])
        self.widget.destroy()

    def test_tree_column(self):
        wc = self.widget.column('#0')
        column = {
            'anchor': 'w',
            'stretch': 1,
            'width': 200,
            'minwidth': 200,
            }

        for k, v in column.items():
            self.assertEqual(v, wc[k])
        self.widget.destroy()

    def test_command_dict(self):
        success = []

        def on_treecolumn_click():
            success.append(1)

        cbdic = { 'on_treecolumn_click': on_treecolumn_click }
        self.builder.connect_callbacks(cbdic)

        x, y = self.widget.winfo_x(), self.widget.winfo_y()
        self.widget.event_generate('<ButtonPress-1>', x=x+5, y=y+5)
        self.widget.event_generate('<ButtonRelease-1>', x=x+5, y=y+5)
        self.widget.update()

        self.assertTrue(success)
        self.widget.destroy()

    def test_command_self(self):
        success = []

        class AnObject:
            def on_treecolumn_click(self):
                success.append(1)

        cbobj = AnObject()
        self.builder.connect_callbacks(cbobj)

        x, y = self.widget.winfo_x(), self.widget.winfo_y()
        self.widget.event_generate('<ButtonPress-1>', x=x+5, y=y+5)
        self.widget.event_generate('<ButtonRelease-1>', x=x+5, y=y+5)
        self.widget.update()

        self.assertTrue(success)
        self.widget.destroy()



if __name__ == '__main__':
    unittest.main()

