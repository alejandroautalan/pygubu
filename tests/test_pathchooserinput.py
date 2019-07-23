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
from pygubu.widgets.pathchooserinput import PathChooserInput


class TestPathChooserInput(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = 'test_pathchooserinput.ui'
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.mainwindow = builder.get_object('mainwindow')
        self.widget = builder.get_object('pathchooserinput1')

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.widget, PathChooserInput)
        self.widget.destroy()
        
    def test_path_changed_event(self):
        success = []

        def on_path_changed(event=None):
            success.append(1)

        bag = { 'on_path_changed': on_path_changed }
        self.builder.connect_callbacks(bag)

        self.widget.configure(path='/new/path')
        self.assertTrue(success)
        self.widget.destroy()
    
    def test_type(self):
        itype = str(self.widget.cget('type'))
        self.assertEqual('file', itype)
        self.widget.destroy()
    
    def test_path(self):
        path = str(self.widget.cget('path'))
        self.assertEqual('/home/user', path)
        self.widget.destroy()
    
    def test_path_dictionary_like(self):
        path = str(self.widget['path'])
        self.assertEqual('/home/user', path)
        self.widget.destroy()
        
    def test_state(self):
        # allowed states normal/disabled/readonly
        
        # normal
        state = str(self.widget.cget('state'))
        self.assertEqual('normal', state)
        
        # disabled
        self.widget.config(state='disabled')
        state = str(self.widget.cget('state'))
        self.assertEqual('disabled', state)
        
        # readonly
        self.widget.config(state='readonly')
        state = str(self.widget.cget('state'))
        self.assertEqual('readonly', state)
        
        
        self.widget.destroy()

