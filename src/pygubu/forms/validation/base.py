from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class Constraint(ABC):
    CLASS_CONSTRAINT = 1
    PROPERTY_CONSTRAINT = 2

    def __init__(self, *args, options=None, groups=None, payload=None):
        self.groups = groups
        self.payload = payload
        self.options = options

    @abstractmethod
    def validated_by(self):
        ...

    def get_targets(self):
        return self.PROPERTY_CONSTRAINT


class ConstraintViolation:
    def __init__(self, message, constraint, *, code=None, params=None):
        self._message = message
        self.code = code
        self.params = params
        self.constraint = constraint

    def _msg_format(self):
        if self.params is None:
            return self._message
        else:
            return self._message % self.params

    @property
    def message(self):
        return self._msg_format()

    def messages(self):
        yield self.code, self.message


class ConstraintViolationList(ConstraintViolation):
    def __init__(self, violations: list):
        self.violations = violations

    @property
    def message(self):
        msgs = [violation.message for violation in self.violations]
        return "\n".join(msgs)

    def messages(self):
        for violation in self.violations:
            yield violation.code, violation.message

    def __bool__(self):
        return bool(self.violations)


class ExecutionContext:
    def __init__(self, translator=None):
        self._violations = []
        self._translator = (
            self._noop_trans if translator is None else translator
        )

    def _noop_trans(self, s):
        """Default no-op translator"""
        return s

    @property
    def violations(self):
        return ConstraintViolationList(self._violations)

    def add_violation(self, /, **kw):
        msg_key = "message"
        if msg_key in kw:
            kw[msg_key] = str(self._translator(kw[msg_key]))
        violation = ConstraintViolation(**kw)
        self._violations.append(violation)

    def clear(self):
        self._violations = []


class ConstraintValidator(ABC):
    def __init__(self):
        self.context: ExecutionContext = None

    def initialize(self, context: ExecutionContext):
        self.context = context

    @abstractmethod
    def validate(self, value, constraint):
        ...
