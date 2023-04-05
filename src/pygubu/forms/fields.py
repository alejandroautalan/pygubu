import math
import pygubu.forms.validators as validators
from pygubu.i18n import _
from .exceptions import ValidationError, ValidationErrorList
from .widgets import FieldWidget, ChoiceWidget


class FieldBase(FieldWidget):
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

    def validate(self, value):
        # Default required validation
        if value in self.empty_values and self.required:
            raise ValidationError(
                self.error_messages["required"], code="required"
            )
        # Trigger specific field validation
        self.wdata.validate(value)

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
        value = self.__to_python(self.wdata.data)
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
            data = self.__to_python(self.wdata.data)
        except ValidationError:
            return True
        # For purposes of seeing whether something has changed, None is
        # the same as an empty string, if the data or initial value we get
        # is None, replace it with ''.
        initial_value = initial if initial is not None else ""
        data_value = data if data is not None else ""
        return initial_value != data_value

    def __to_python(self, value):
        # Trigger default field to_python and user to_python
        return self.wdata.to_python(self.to_python(value))

    def to_python(self, value):
        return value

    @property
    def data(self):
        if self.wdata is None:
            raise RuntimeError("Data manager not set")
        # NOTE: should return initial if field is disabled.
        if self.disabled:
            return self.initial
        return self.wdata.data

    @data.setter
    def data(self, value):
        if self.wdata is None:
            raise RuntimeError("Data manager not set")
        self.wdata.data = value


class DisplayField(FieldBase):
    """A Display only field"""

    def __init__(self, *args, **kw):
        kw["required"] = False
        super().__init__(*args, **kw)

    def has_changed(self, initial):
        # Display only field, should never change
        return False


class CharField(FieldBase):
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

    def to_python(self, value):
        """Return a string."""
        if value not in self.empty_values:
            value = str(value)
            if self.strip:
                value = value.strip()
        if value in self.empty_values:
            return self.empty_value
        return value


class IntegerField(FieldBase):
    default_error_messages = {
        "invalid": _("Enter a whole number."),
    }
    # re_decimal = _lazy_re_compile(r"\.0*\s*$")

    def __init__(
        self, *args, max_value=None, min_value=None, step_size=None, **kw
    ):
        self.max_value, self.min_value, self.step_size = (
            max_value,
            min_value,
            step_size,
        )

        # if kwargs.get("localize") and self.widget == NumberInput:
        #    # Localized number input is not well supported on most browsers
        #    kwargs.setdefault("widget", super().widget)
        super().__init__(*args, **kw)

        if max_value is not None:
            self.validators.append(validators.MaxValueValidator(max_value))
        if min_value is not None:
            self.validators.append(validators.MinValueValidator(min_value))
        if step_size is not None:
            self.validators.append(validators.StepValueValidator(step_size))

    def to_python(self, value):
        """
        Validate that int() can be called on the input. Return the result
        of int() or None for empty values.
        """
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        # if self.localize:
        #    value = formats.sanitize_separators(value)
        # Strip trailing decimal and zeros.
        try:
            # value = int(self.re_decimal.sub("", str(value)))
            value = int(str(value))
        except (ValueError, TypeError):
            raise ValidationError(
                self.error_messages["invalid"], code="invalid"
            )
        return value


class FloatField(IntegerField):
    default_error_messages = {
        "invalid": _("Enter a number."),
    }

    def to_python(self, value):
        """
        Validate that float() can be called on the input. Return the result
        of float() or None for empty values.
        """
        value = super(IntegerField, self).to_python(value)
        if value in self.empty_values:
            return None
        # if self.localize:
        #    value = formats.sanitize_separators(value)
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValidationError(
                self.error_messages["invalid"], code="invalid"
            )
        return value

    def validate(self, value):
        super().validate(value)
        if value in self.empty_values:
            return
        if not math.isfinite(value):
            raise ValidationError(
                self.error_messages["invalid"], code="invalid"
            )


class BooleanField(FieldBase):
    def to_python(self, value):
        """Return a Python boolean object."""
        # Explicitly check for the string 'False', which is what a hidden field
        # will submit for False. Also check for '0', since this is what
        # RadioSelect will provide. Because bool("True") == bool('1') == True,
        # we don't need to handle that explicitly.
        if isinstance(value, str) and value.lower() in ("false", "0"):
            value = False
        else:
            value = bool(value)
        return super().to_python(value)

    def validate(self, value):
        print("validating value:", value)
        if not value and self.required:
            raise ValidationError(
                self.error_messages["required"], code="required"
            )
        # Trigger specific field validation
        self.wdata.validate(value)

    def has_changed(self, initial):
        if self.disabled:
            return False
        # Sometimes data or initial may be a string equivalent of a boolean
        # so we should run it through to_python first to get a boolean value
        return self.to_python(initial) != self.to_python(self.wdata.data)


class ChoiceField(FieldBase, ChoiceWidget):
    default_error_messages = {
        "invalid_choice": _(
            "Select a valid choice. %(value)s is not one of the available choices."
        ),
    }

    def to_python(self, value):
        """Return a string."""
        if value in self.empty_values:
            return ""
        return str(value)

    def validate(self, value):
        """Validate that the input is in self.choices."""
        super().validate(value)
        if value and not self.valid_value(value):
            raise ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": value},
            )
