import unittest

import support

import pygubu
from pygubu.widgets.colorinput import ColorInput


class TestColorInput(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_colorinput.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainframe")
        self.wcolor = builder.get_object("colorinput1")

    def tearDown(self):
        support.root_withdraw()

    def test_class(self):
        self.assertIsInstance(self.wcolor, ColorInput)
        self.widget.destroy()
