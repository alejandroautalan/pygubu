import math
import pygubu.forms.validators as validators
from pygubu.i18n import _
from .exceptions import ValidationError, ValidationErrorList
from .widgets import FieldWidget
from .transformer import NoopTransfomer


class FieldBase(FieldWidget):
    default_validators = []
    default_error_messages = {
        "required": _("This field is required."),
    }
    empty_values = list(validators.EMPTY_VALUES)

    def __init__(
        self,
        *args,
        field_name,
        field_required=True,
        field_initial=None,
        field_help="",
        error_messages=None,
        validators=(),
        **kw,
    ):
        self.model_transfomer = NoopTransfomer()
        self.view_transformer = NoopTransfomer()
        self.field_name = field_name
        self.field_required = field_required
        self.field_initial = field_initial
        self.field_help = field_help

        messages = {}
        for c in reversed(self.__class__.__mro__):
            messages.update(getattr(c, "default_error_messages", {}))
        messages.update(error_messages or {})
        self.error_messages = messages

        self.validators = [*self.default_validators, *validators]
        print("Field init")
        super().__init__(*args, **kw)

    def validate(self, value):
        # Default required validation
        if value in self.empty_values and self.field_required:
            raise ValidationError(
                self.error_messages["required"], code="required"
            )

    def run_validators(self, value):
        if value in self.empty_values:
            return
        errors = []
        for v in self.validators:
            try:
                v(value)
            except ValidationError as e:
                if hasattr(e, "code") and e.code in self.error_messages:
                    e.message = self.error_messages[e.code]
                errors.append(e)
        if errors:
            raise ValidationErrorList(errors)

    def clean(self, value):
        """
        Validate the given value and return its "cleaned" value as an
        appropriate Python object. Raise ValidationError for any errors.
        """
        value = self.view_transformer.reversetransform(self.wget_value())
        self.validate(value)
        self.run_validators(value)
        return value

    def has_changed(self, initial):
        """Return True if data differs from initial."""
        # Always return False if the field is disabled since self.data
        # always uses the initial value in this case.
        if self.wis_disabled():
            return False
        try:
            data = self.model_transfomer.reversetransform(
                self.view_transformer.reversetransform(self.wget_value())
            )
        except ValidationError:
            return True
        # For purposes of seeing whether something has changed, None is
        # the same as an empty string, if the data or initial value we get
        # is None, replace it with ''.
        initial_value = initial if initial is not None else ""
        data_value = data if data is not None else ""
        return initial_value != data_value

    @property
    def data(self):
        # NOTE: should return initial if field is disabled.
        if self.wis_disabled():
            return self.field_initial
        return self.model_transfomer.reversetransform(
            self.view_transformer.reversetransform(self.wget_value())
        )

    @data.setter
    def data(self, value):
        self.wset_value(
            self.view_transformer.transform(
                self.model_transfomer.transform(value)
            )
        )


class DisplayField(FieldBase):
    """A Display only field"""

    def __init__(self, *args, **kw):
        kw["field_required"] = False
        super().__init__(*args, **kw)

    def has_changed(self, initial):
        # Display only field, should never change
        return False
