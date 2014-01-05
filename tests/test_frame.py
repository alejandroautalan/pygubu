# encoding: utf8
from __future__ import print_function
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


class TestFrame(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = """<?xml version="1.0" ?>
<interface>
    <object class="ttk.Frame" id="mainwindow">
        <property name="height">250</property>
        <property name="padding">10</property>
        <property name="width">250</property>
        <property name="class_">MyCustomFrame</property>
        <property name="relief">sunken</property>
        <property name="style">MyFrameStyle.TFrame</property>
        <property name="takefocus">1</property>
        <property name="cursor">cross</property>
        <bind add="" handler="on_button_click" sequence="&lt;Button-1&gt;"/>
        <bind add="True" handler="on_button_click2" sequence="&lt;Button-1&gt;"/>
        <layout>
            <property name="row">0</property>
            <property name="column">0</property>
            <property name="sticky">nesw</property>
            <property name="pady">10</property>
            <property name="padx">5</property>
            <property name="propagate">False</property>
            <property name="ipady">4</property>
            <property name="ipadx">2</property>
            <property name="rowspan">1</property>
            <property name="columnspan">2</property>
        </layout>
        <child>
            <object class="ttk.Label" id="label">
            <property name="text">label</property>
                <layout>
                    <property name="column">0</property>
                    <property name="propagate">True</property>
                    <property name="row">1</property>
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


    def test_class(self):
        self.assertIsInstance(self.widget, ttk.Frame)
        self.widget.destroy()

    def test_padding(self):
        tclobj = self.widget.cget('padding')[0]
        padding = str(tclobj)
        self.assertEqual('10', padding)
        self.widget.destroy()

    def test_width(self):
        tclobj = self.widget.cget('width')
        width = str(tclobj)
        self.assertEqual('250', width)
        self.widget.destroy()

    def test_class_(self):
        tclobj = self.widget.cget('class')
        class_ = str(tclobj)
        self.assertEqual('MyCustomFrame', class_)
        self.widget.destroy()

    def test_relief(self):
        tclobj = self.widget.cget('relief')
        relief = str(tclobj)
        self.assertEqual(tk.SUNKEN, relief)
        self.widget.destroy()

    def test_style(self):
        tclobj = self.widget.cget('style')
        style = str(tclobj)
        self.assertEqual('MyFrameStyle.TFrame', style)
        self.widget.destroy()

    def test_takefocus(self):
        tclobj = self.widget.cget('takefocus')
        takefocus = str(tclobj)
        self.assertEqual('1', takefocus)
        self.widget.destroy()

    def test_cursor(self):
        tclobj = self.widget.cget('cursor')
        cursor = str(tclobj)
        self.assertEqual('cross', cursor)
        self.widget.destroy()

    def test_layout(self):
        ginfo = self.widget.grid_info()
        expected = [
            ('row', '0'),
            ('column', '0'),
            ('sticky', 'nesw'),
            ('pady', '10'),
            ('padx', '5'),
            ('ipadx', '2'),
            ('ipady', '4'),
            ('rowspan', '1'),
            ('columnspan', '2'),
        ]
        for k, ev in expected:
            value = str(ginfo[k])
            self.assertEqual(value, ev)

        propagate = self.widget.grid_propagate()
        self.assertEqual(None, propagate)
        self.widget.destroy()

    def test_child_count(self):
        count = len(self.widget.children)
        self.assertEqual(1, count)
        self.widget.destroy()

    def test_binding_dict(self):
        success = []

        def on_button_click(event):
            success.append(1)

        def on_button_click2(event):
            success.append(1)

        cbdic = {
            'on_button_click': on_button_click,
            'on_button_click2': on_button_click2
            }
        self.builder.connect_callbacks(cbdic)

        support.simulate_mouse_click(self.widget, 5, 5)
        self.widget.update_idletasks()

        self.assertTrue(success)
        self.widget.destroy()

    def test_binding_object(self):
        success = []

        class AnObject:
            def on_button_click(self, event):
                success.append(1)
            def on_button_click2(self, event):
                success.append(1)

        cbobj = AnObject()
        self.builder.connect_callbacks(cbobj)

        support.simulate_mouse_click(self.widget, 5, 5)
        self.widget.update_idletasks()

        self.assertTrue(success)
        self.widget.destroy()

    def test_binding_add(self):
        success = []

        def on_button_click(event):
            success.append(1)
        def on_button_click2(event):
            success.append(1)

        cbdic = {
            'on_button_click': on_button_click,
            'on_button_click2': on_button_click2
            }
        self.builder.connect_callbacks(cbdic)

        support.simulate_mouse_click(self.widget, 5, 5)
        self.widget.update_idletasks()

        self.assertTrue(len(success) == 2)
        self.widget.destroy()


if __name__ == '__main__':
    unittest.main()

