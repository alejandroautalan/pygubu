# encoding: utf8
import os
import sys
import unittest
import tkinter as tk
import tkinter.ttk as ttk

pygubu_basedir = os.path.abspath(os.path.dirname(
    os.path.dirname(os.path.realpath(sys.argv[0]))))
if pygubu_basedir not in sys.path:
    sys.path.insert(0, pygubu_basedir)

import pygubu
import support


class TestIdtocommand(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = 'test_idtocommand.ui'
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object('mainwindow')
        self.button = builder.get_object('button1')

    def tearDown(self):
        support.root_withdraw()

    def test_idtocommand(self):
        success = []

        class AnObject:
            def on_button_clicked(self, widgetid):
                success.append(1)

        cbobj = AnObject()
        self.builder.connect_callbacks(cbobj)
        self.button.invoke()
        self.widget.update()

        self.assertTrue(success)
        self.widget.destroy()
