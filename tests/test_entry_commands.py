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


class TestEntryCommands(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = xmldata = 'test_entry_commands.ui'
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object('entry')

    def tearDown(self):
        support.root_withdraw()

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

        callback = {
            'entry_validate': entry_validate,
            'entry_invalid': entry_invalid
        }

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

        callback = {
            'entry_validate': entry_validate,
            'entry_invalid': entry_invalid
        }

        self.widget.delete('0', tk.END)

        self.builder.connect_callbacks(callback)

        self.widget.insert('0', 'Not Allowed')
        self.assertEqual(invalid_text[0], 'Not Allowed')

        self.widget.destroy()


if __name__ == '__main__':
    unittest.main()

