from ..base import Constraint, ConstraintValidator


class NotBlank(Constraint):
    code = "is_blank_error"
    message = "This value should not be blank."
    empty_values = (None, "", [], (), {})

    def __init__(
        self, *args, message=None, allow_none=False, empty_values=None, **kw
    ):
        super().__init__(*args, **kw)
        if message is not None:
            self.message = message
        if empty_values is not None:
            self.empty_values = empty_values
        self.allow_none = allow_none

    def validated_by(self):
        return NotBlankValidator


class NotBlankValidator(ConstraintValidator):
    def validate(self, value, constraint):
        if constraint.allow_none and value is None:
            return
        if value in constraint.empty_values:
            self.context.add_violation(
                message=constraint.message,
                constraint=constraint,
                code=constraint.code,
                params=None,
            )
