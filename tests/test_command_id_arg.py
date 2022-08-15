# encoding: utf-8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

import fixpath
import pygubu
import support


class TestCommandIdArg(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_command_id_arg.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainwindow")
        self.menu = builder.get_object("menu1")

    def tearDown(self):
        support.root_withdraw()

    def test_idtocommand(self):
        success = []
        received_id = []

        class AnObject:
            def menu_item_clicked(self, itemid):
                success.append(1)
                received_id.append(itemid)

        cbobj = AnObject()
        self.builder.connect_callbacks(cbobj)
        self.menu.invoke(0)
        self.widget.update()

        self.assertTrue(success)
        self.assertEqual(received_id[0], "menu_item_1")
        self.widget.destroy()
