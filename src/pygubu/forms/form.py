from typing import Optional
from collections import OrderedDict
from .transformer import NoopTransfomer, TransformationError
from .validation.base import ExecutionContext
from .validation.constraint.form import Form as FormConstraint
from .validation.constraint.form import FormValidator


class FormError(Exception):
    ...


class FormField:
    def __init__(self, widget, **kw):
        self.widget = widget
        self.required = kw.get("required", True)
        self.initial = kw.get("initial", None)
        self.constraints = kw.get("constraints", [])
        self.help = kw.get("help")
        # self.mapped = kw.get("mapped", True)
        noop_transformer = NoopTransfomer()
        self.model_transformer = kw.get("model_transformer", noop_transformer)
        self.view_transformer = kw.get("view_transformer", noop_transformer)

    @property
    def data(self):
        # NOTE: should return initial if field is disabled.
        if self.widget.wis_disabled():
            return self.initial
        return self.view_transformer.reversetransform(self.widget.wget_value())

    @data.setter
    def data(self, value):
        self.widget.wset_value(
            self.view_transformer.transform(
                self.model_transformer.transform(value)
            )
        )

    @property
    def field_name(self):
        return self.widget.field_name

    def clean(self, value):
        """
        Validate the given value and return its "cleaned" value as an
        appropriate Python object. Raise TransormationError for any errors.
        """
        value = self.model_transformer.reversetransform(value)
        return value


class Form:
    def __init__(self):
        self.fields = OrderedDict()
        self.initialized = False
        self.fields_initial = {}
        self.info_display = {}
        self.cleaned_data = {}
        self.transformation_error = None
        self._errors = {}
        self.translator = None

    def add(self, name: str, field: FormField):
        self.fields[name] = field

    def add_info_display(self, name: str, info_display):
        self.info_display[name] = info_display

    def edit(self, data: dict, initial_bag: Optional[dict] = None):
        """Intializes form to edit data values."""
        self.initialized = True
        self.fields_initial = {}
        if initial_bag is None:
            initial_bag = {}
        for name, field in self.fields.items():
            field_initial = initial_bag.get(name, field.initial)
            field_initial = "" if field_initial is None else field_initial
            self.fields_initial[name] = field_initial
            field.data = data.get(name, field_initial)
            self.edit_field_init(field)

    def edit_field_init(self, field):
        if field.field_name in self.info_display:
            field_info = self.info_display[field.field_name]
            field_info.clear()
            if field.help:
                field_info.show_help(field.help)

    def is_valid(self):
        return self.is_bound and not self._errors

    def get_data(self):
        return self.cleaned_data

    def submit(self):
        if self.initialized:
            self.is_bound = True
            self.submit_init()
            self.do_submit()
            self.do_validation()
        else:
            raise FormError(
                "Form initialization error. Call form.edit() before submit"
            )

    def submit_init(self):
        self.cleaned_data = {}
        self._errors = {}
        self.transformation_error = None
        for name, field in self.fields.items():
            field.widget.wmark_invalid(False)
        for name in self.info_display:
            self.info_display[name].clear()

    def do_submit(self):
        for name, field in self.fields.items():
            value = field.initial if field.widget.wis_disabled() else field.data
            try:
                value = field.clean(value)
                self.cleaned_data[name] = value
            except TransformationError as e:
                self.transformation_error = e

    def field_submit_pass(self, field):
        if field.help:
            field_info = self.info_display.get(field.field_name, None)
            if field_info is not None:
                field_info.show_help(field.help)

    def field_submit_error(self, field, error):
        field.widget.wmark_invalid(True)
        field_info = self.info_display.get(field.field_name, None)
        if field_info is not None:
            field_info.show_error(error)

    def do_validation(self):
        constraint = FormConstraint()
        validator = FormValidator()
        context = ExecutionContext(translator=self.translator)
        validator.initialize(context)
        validator.validate(self, constraint)

        for fname, field in self.fields.items():
            if fname in self._errors:
                self.field_submit_error(field, self._errors[fname])
            else:
                self.field_submit_pass(field)

    def add_error(self, field_name, error):
        self._errors[field_name] = error
