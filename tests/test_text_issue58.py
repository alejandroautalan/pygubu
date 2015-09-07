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


expected_text = """In the designer:
- Add a text widget
- Set state to disabled
- Enter content in the text property
- Text content should be set by pygubu-designer.
"""


class TestText(unittest.TestCase):

    def setUp(self):
        support.root_deiconify()
        xmldata = 'test_text_issue58.ui'
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object('mainframe')
        self.text = builder.get_object('Text_1')

    def tearDown(self):
        support.root_withdraw()

    def test_set_text_in_disabled_status(self):
        text_content = self.text.get('0.0', tk.END)
        self.assertEqual(text_content, expected_text)
        self.widget.destroy()

