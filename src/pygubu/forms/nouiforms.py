"""No UI forms"""

from .forms import FormBase
from .widgets import FieldWidget, DataManager, ViewManager, ChoiceWidget
from .fields import (
    CharField as CharFieldBase,
    IntegerField as IntegerFieldBase,
    ChoiceField as ChoiceFieldBase,
)


class Form(FormBase):
    pass


class NoUIWidget(FieldWidget):
    class DataManager(DataManager):
        def __init__(self, field):
            super().__init__(field)
            self._value = None

        def set_value(self, value):
            # will set the value in the widget format
            self._value = value

        def get_value(self):
            return self._value

    class ViewManager(ViewManager):
        def mark_invalid(self, state: bool):
            print(f"Field {self._field.fname} invalid: {state}")

        def is_disabled(self) -> bool:
            return False

    data_manager = DataManager
    view_manager = ViewManager


class CharField(CharFieldBase, NoUIWidget):
    pass


class IntegerField(IntegerFieldBase, NoUIWidget):
    pass


class NoUIChoiceWidget(NoUIWidget, ChoiceWidget):
    pass


class ChoiceField(ChoiceFieldBase, NoUIChoiceWidget):
    pass
