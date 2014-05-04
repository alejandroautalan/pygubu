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


class TestPanedwindow(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = 'test_panedwindow.ui'
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object('mainframe')
        self.pw1 = builder.get_object('Panedwindow_1')
        self.pw2 = builder.get_object('Panedwindow_2')

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.pw1, ttk.Panedwindow)
        self.assertIsInstance(self.pw2, ttk.Panedwindow)
        self.widget.destroy()
