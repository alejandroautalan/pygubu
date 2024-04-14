from ..base import Constraint, ConstraintValidator
from .notblank import NotBlank
from pygubu.i18n import _


class Required(NotBlank):
    code = "required"
    message = _("This value is required.")


class Form(Constraint):
    def get_targets(self):
        return self.CLASS_CONSTRAINT

    def validated_by(self):
        return FormValidator


class FormValidator(ConstraintValidator):
    def validate(self, form, constraint):
        for name, field in form.fields.items():
            field_constraints = []
            if field.required:
                field_constraints.append(Required())
            field_constraints.extend(field.constraints)
            for fc in field_constraints:
                validator_class = fc.validated_by()
                validator = validator_class()
                validator.initialize(self.context)
                validator.validate(field.data, fc)
            violations = self.context.violations
            if violations:
                form.add_error(name, violations)
            self.context.clear()
