import unittest

import support

import pygubu


class TestCustomWidget(unittest.TestCase):
    def setUp(self):
        support.root_deiconify()
        xmldata = "test_custom_widget.ui"
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(xmldata)
        self.widget = builder.get_object("mainwindow")
        self.custom_widget = builder.get_object("custom_widget")

    def tearDown(self):
        support.root_withdraw()

    def test_loading(self):
        message = self.custom_widget.get_message()
        self.assertEqual(message, "CustomLabel")
        self.widget.destroy()
