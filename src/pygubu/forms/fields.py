from pygubu.i18n import _
from .exceptions import ValidationError, ValidationErrorList
from .validators import EMPTY_VALUES


class Field:
    default_validators = []
    default_error_messages = {
        "required": _("This field is required."),
    }
    empty_values = list(EMPTY_VALUES)

    def __init__(
        self,
        *args,
        fname,
        required=True,
        initial=None,
        help_text="",
        error_messages=None,
        validators=(),
        **kw,
    ):
        self.fname = fname
        self.required = required
        self.initial = initial
        self.help_text = help_text

        messages = {}
        for c in reversed(self.__class__.__mro__):
            messages.update(getattr(c, "default_error_messages", {}))
        messages.update(error_messages or {})
        self.error_messages = messages

        self.validators = [*self.default_validators, *validators]

        super().__init__(*args, **kw)

    def prepare_value(self, value):
        return value

    def to_python(self, value):
        return value

    def validate(self, value):
        if value in self.empty_values and self.required:
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
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return value

    #
    # -------------------
    #

    def mark_invalid(self):
        raise NotImplementedError

    def clear_invalid(self):
        raise NotImplementedError

    @property
    def disabled(self):
        return False

    @property
    def data(self):
        raise NotImplementedError

    @data.setter
    def data(self, value):
        raise NotImplementedError


class InfoDisplay:
    def __init__(self, *args, fname: str, **kw):
        self.fname = fname
        super().__init__(*args, **kw)

    def show_error(self, error):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


class FieldInfoDisplay(InfoDisplay):
    ...


class FormInfoDisplay(InfoDisplay):
    ...
