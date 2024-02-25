from ..base import Constraint, ConstraintValidator


class IsTrue(Constraint):
    code = "not_true_error"
    message = "This value should be true."
    true_values = (True, "1", 1)

    def __init__(
        self, *args, message=None, allow_none=False, true_values=None, **kw
    ):
        super().__init__(*args, **kw)
        if message is not None:
            self.message = message
        if true_values is not None:
            self.true_values = true_values
        self.allow_none = allow_none

    def validated_by(self):
        return IsTrueValidator


class IsTrueValidator(ConstraintValidator):
    def validate(self, value, constraint):
        if constraint.allow_none and value is None:
            return
        if value not in constraint.true_values:
            self.context.add_violation(
                message=constraint.message,
                constraint=constraint,
                code=constraint.code,
                params=None,
            )
