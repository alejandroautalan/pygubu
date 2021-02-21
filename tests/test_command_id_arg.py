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


class TestCommandIdArg(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = 'test_command_id_arg.ui'
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object('mainwindow')
        self.menu = builder.get_object('menu1')

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
        self.assertEqual(received_id[0], 'menu_item_1')
        self.widget.destroy()
