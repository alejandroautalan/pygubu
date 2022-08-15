# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import pygubu
import support


class TestButtonCommand(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_button_command.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainwindow")
        self.button1 = builder.get_object("button1")
        self.button2 = builder.get_object("button2")

    def tearDown(self):
        support.root_withdraw()

    def test_command_simple(self):
        success = []

        class AnObject:
            def button1_clicked(self):
                success.append(1)

            def on_button_clicked(self):
                pass

        cbobj = AnObject()
        self.builder.connect_callbacks(cbobj)
        self.button1.invoke()
        self.widget.update()

        self.assertTrue(success)
        self.widget.destroy()

    def test_command_with_widgetid(self):
        success = []
        received_id = []

        class AnObject:
            def button1_clicked(self):
                pass

            def on_button_clicked(self, widgetid):
                success.append(1)
                received_id.append(widgetid)

        cbobj = AnObject()
        self.builder.connect_callbacks(cbobj)
        self.button2.invoke()
        self.widget.update()

        self.assertTrue(success)
        self.assertEqual(received_id[0], "button2")
        self.widget.destroy()

    # def test_command_generate_event(self):
    # success = []

    # class AnObject:
    # def button1_clicked(self):
    # pass
    # def on_button_clicked(self):
    # pass
    # def catch_button_event(self, event):
    # success.append(1)

    # cbobj = AnObject()
    # self.button3.bind('<<MyButtonEvent>>', cbobj.catch_button_event)
    # self.builder.connect_callbacks(cbobj)
    # self.button3.invoke()
    # self.widget.update()

    # self.assertTrue(success)
    # self.widget.destroy()
