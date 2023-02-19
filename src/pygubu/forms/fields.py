import json
import tkinter as tk
import pygubu.forms.validators as validators
from pygubu.i18n import _
from .exceptions import ValidationError, ValidationErrorList


class Field:
    default_validators = []
    default_error_messages = {
        "required": _("This field is required."),
    }
    empty_values = list(validators.EMPTY_VALUES)

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
        print("Field init")
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


class TkVariableBasedField(Field):
    tkvar_pname = "textvariable"
    tkvar_class = tk.StringVar

    def __init__(self, *args, **kw):
        user_var = kw.get(self.tkvar_pname, None)
        if user_var is None:
            self._data_var = self.tkvar_class()
            kw[self.tkvar_pname] = self._data_var
        elif isinstance(user_var, self.tkvar_class):
            self._data_var = user_var
        else:
            raise ValueError("Incorrect type for data variable")

        super().__init__(*args, **kw)

    @property
    def disabled(self):
        return "disabled" == self.cget("state")

    @property
    def data(self):
        return self._data_var.get()

    @data.setter
    def data(self, value):
        self._data_var.set(value)


class CharFieldMixin:
    def __init__(
        self,
        *args,
        max_length=None,
        min_length=None,
        strip=True,
        empty_value="",
        **kw,
    ):

        self.max_length = max_length
        self.min_length = min_length
        self.strip = strip
        self.empty_value = empty_value

        super().__init__(*args, **kw)

        if min_length is not None:
            self.validators.append(
                validators.MinLengthValidator(int(min_length))
            )
        if max_length is not None:
            self.validators.append(
                validators.MaxLengthValidator(int(max_length))
            )


class ChoiceFieldMixin:
    default_error_messages = {
        "invalid_choice": _(
            "Select a valid choice. %(value)s is not one of the available choices."
        ),
    }

    def __init__(self, *args, choices=None, **kw):
        self._choices = [] if choices is None else self._strto_choices(choices)
        super().__init__(*args, **kw)

    def validate(self, value):
        """Validate that the input is in self._choices."""
        super().validate(value)
        if value and not self.valid_value(value):
            raise ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": value},
            )

    def valid_value(self, value):
        return value in self._choices

    def _strto_choices(self, value):
        if isinstance(value, list):
            return value
        elif isinstance(value, str):
            try:
                choices = json.loads(value)
                if isinstance(choices, list):
                    return choices
                else:
                    raise ValueError("Json value must be a list")
            except json.JSONDecodeError:
                raise ValueError("Can't decode json value")
        else:
            raise ValueError("Value must be a list or json string")
