NON_FIELD_ERRORS = "__all__"


class FormError(Exception):
    pass


class ValidationError(Exception):
    """An error while validating data."""

    def __init__(self, message, *, code=None, params=None):
        super().__init__(message, code, params)
        self._message = message
        self.code = code
        self.params = params

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


class ValidationErrorList(ValidationError):
    def __init__(self, error_list):
        super().__init__(None)
        self.error_list = error_list

    @property
    def message(self):
        msgs = [error.message for error in self.error_list]
        return "\n".join(msgs)

    def messages(self):
        for error in self.error_list:
            yield error.code, error.message
