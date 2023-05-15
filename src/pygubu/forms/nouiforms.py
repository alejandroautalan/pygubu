"""No UI forms"""

from .forms import FormBase
from .widgets import FieldWidget
from .fields import (
    CharField as CharFieldBase,
    IntegerField as IntegerFieldBase,
    ChoiceField as ChoiceFieldBase,
)


class Form(FormBase):
    pass


class NoUIWidget(FieldWidget):
    def __init__(self, *args, **kw):
        self._value = None
        super().__init__(*args, **kw)

    def wset_value(self, value):
        self._value = value

    def wget_value(self):
        return self._value

    def wmark_invalid(self, state: bool):
        print(f"Field {self._field.fname} invalid: {state}")

    def wis_disabled(self) -> bool:
        return False


class CharField(CharFieldBase, NoUIWidget):
    pass


class IntegerField(IntegerFieldBase, NoUIWidget):
    pass


# class NoUIChoiceWidget(NoUIWidget, ChoiceWidget):
#    pass


# class ChoiceField(ChoiceFieldBase, NoUIChoiceWidget):
#    pass
