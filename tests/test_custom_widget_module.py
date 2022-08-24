import tkinter.ttk as ttk
from pygubu.api.v1 import BuilderObject, register_widget


class CustomLabel(ttk.Label):
    def get_message(self):
        return "CustomLabel"


class TestCustomWidgetBuilder(BuilderObject):
    class_ = CustomLabel


register_widget(
    "test_custom_widget_module.custom_label",
    TestCustomWidgetBuilder,
    "CustomWidget",
    ("ttk", "Test Custom Widget"),
)
