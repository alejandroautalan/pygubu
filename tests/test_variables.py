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


class TestVariables(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = "test_variables.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object('mainwindow')


    def tearDown(self):
        support.root_withdraw()

    def test_string_var(self):
        var = self.builder.get_variable('strvar')
        self.assertIsInstance(var, tk.StringVar)
        self.widget.destroy()

    def test_int_var(self):
        var = self.builder.get_variable('intvar')
        self.assertIsInstance(var, tk.IntVar)
        self.widget.destroy()

    def test_double_var(self):
        var = self.builder.get_variable('doublevar')
        self.assertIsInstance(var, tk.DoubleVar)
        self.widget.destroy()

    def test_boolean_var(self):
        var = self.builder.get_variable('booleanvar')
        self.assertIsInstance(var, tk.BooleanVar)
        self.assertEqual(False, var.get())
        self.widget.destroy()
    
    def test_bugged_oldformat_var(self):
        var = self.builder.get_variable('testoldformat')
        self.assertIsInstance(var, tk.StringVar)
        self.widget.destroy()
        
    def test_invalid_variable_type(self):
        # self.builder.create_variable('complex:mycomplexvar')
        self.assertRaises(Exception, self.builder.create_variable,
                          'complex:mycomplexvar')
        self.widget.destroy()



if __name__ == '__main__':
    unittest.main()

