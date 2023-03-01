"""Base clases for form field definition."""

import json
import tkinter as tk
import pygubu.forms.validators as validators
from typing import Optional
from pygubu.i18n import _
from .exceptions import ValidationError, ValidationErrorList
from .fieldm import FieldDataManager, FieldViewManager


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

        # Subclasess should set its own widget manager
        self.data_manager: Optional[FieldDataManager] = None
        self.view_manager: Optional[FieldViewManager] = None

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
        if value in self.empty_values and self.required:
            raise ValidationError(
                self.error_messages["required"], code="required"
            )
        # Trigger specific field validation
        self.data_manager.validate(value)

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
        value = self.data_manager.to_python(self.data_manager.data)
        self.validate(value)
        self.run_validators(value)
        return value

    def has_changed(self, initial):
        """Return True if data differs from initial."""
        # Always return False if the field is disabled since self.data
        # always uses the initial value in this case.
        if self.disabled:
            return False
        try:
            data = self.data_manager.to_python(self.data_manager.data)
        except ValidationError:
            return True
        # For purposes of seeing whether something has changed, None is
        # the same as an empty string, if the data or initial value we get
        # is None, replace it with ''.
        initial_value = initial if initial is not None else ""
        data_value = data if data is not None else ""
        return initial_value != data_value

    #
    # -------------------
    #

    def mark_invalid(self, state: bool):
        if self.view_manager is None:
            raise RuntimeError("View manager not set")
        self.view_manager.mark_invalid(state)

    @property
    def disabled(self):
        if self.view_manager is None:
            raise RuntimeError("View manager not set")
        return self.view_manager.disabled

    @property
    def data(self):
        if self.data_manager is None:
            raise RuntimeError("Data manager not set")
        # NOTE: should return initial if field is disabled.
        if self.disabled:
            return self.initial
        return self.data_manager.data

    @data.setter
    def data(self, value):
        if self.data_manager is None:
            raise RuntimeError("Data manager not set")
        self.data_manager.data = value


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
    choices_pname = "choices"
    choices_pop = True  # Remove property from kw or not.
    default_error_messages = {
        "invalid_choice": _(
            "Select a valid choice. %(value)s is not one of the available choices."
        ),
    }

    def __init__(self, *args, **kw):
        if self.choices_pop:
            choices = kw.pop(self.choices_pname, None)
        else:
            choices = kw.get(self.choices_pname, None)
        self._choices = [] if choices is None else self._strto_choices(choices)
        super().__init__(*args, **kw)

    def validate_choice(self, value):
        """Validate that the input is in self._choices."""
        if value and not (value in self._choices):
            raise ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": value},
            )

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
