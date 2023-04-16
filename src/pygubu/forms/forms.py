from typing import Optional
from .validators import ValidationError
from .fields import FieldBase
from .exceptions import FormError


class FormInfoBase:
    def __init__(self, *args, fname: str, **kw):
        self.fname = fname
        super().__init__(*args, **kw)

    def show_error(self, error):
        raise NotImplementedError

    def show_help(self, message):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


class FieldInfo(FormInfoBase):
    pass


class FormInfo(FormInfoBase):
    pass


class FormBase:
    def __init__(
        self,
        *args,
        fname,
        empty_permitted=False,
        use_required_attribute=None,
        **kw,
    ):
        self.fname = fname
        self.fields = {}
        self.empty_permitted = empty_permitted

        if use_required_attribute is not None:
            self.use_required_attribute = use_required_attribute

        self.is_bound = False
        self._errors = None
        self._fields_initial = {}
        self._info_displays = {}
        super().__init__(*args, **kw)

    @property
    def errors(self):
        """Return an ErrorDict for the data provided for the form."""
        if self._errors is None:
            self.full_clean()
        return self._errors

    def is_valid(self):
        """Return True if the form has no errors, or False otherwise."""
        return self.is_bound and not self.errors

    def full_clean(self):
        """
        Clean all of self.data and populate self._errors and self.cleaned_data.
        """
        self._errors = {}
        if not self.is_bound:  # Stop further processing.
            return
        self.cleaned_data = {}
        # If the form is permitted to be empty, and none of the form data has
        # changed from the initial data, short circuit any validation.
        if self.empty_permitted and not self.has_changed():
            return

        self._clean_fields()
        self._clean_form()
        self._post_clean()

    def _clean_fields(self):
        for name, field in self._iter_fields():
            value = field.initial if field.wis_disabled() else field.data
            try:
                value = field.clean(value)
                self.cleaned_data[name] = value
                self._field_clean_pass(field)
            except ValidationError as e:
                self.add_error(name, e)
                self._field_clean_error(field, e)

    def _clean_form(self):
        try:
            cleaned_data = self.clean()
        except ValidationError as e:
            self.add_error(None, e)
        else:
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data

    def _post_clean(self):
        """
        An internal hook for performing additional cleaning after form cleaning
        is complete. Used for model validation in model forms.
        """
        pass

    def clean(self):
        """
        Hook for doing any extra form-wide cleaning after Field.clean() has been
        called on every field. Any ValidationError raised by this method will
        not be associated with a particular field; it will have a special-case
        association with the field named '__all__'.
        """
        return self.cleaned_data

    def has_changed(self):
        """Return True if data differs from initial."""
        return self.is_bound and bool(self.changed_data)

    @property
    def changed_data(self):
        if self.is_bound:
            return [
                name
                for name, f in self._iter_fields()
                if f.has_changed(self._fields_initial[name])
            ]
        return []

    def add_error(self, field, error):
        self._errors[field] = error

    #
    # ---------
    #
    def _iter_fields(self, force_scan=False):
        for name, field in self.fields.items():
            yield name, field

    def add_field(self, field):
        self.fields[field.fname] = field

    def edit(self, data: dict, initial: Optional[dict] = None):
        """Intializes form to edit data values."""
        self._initialized = True
        self._fields_initial = {}
        if initial is None:
            initial = {}
        for name, field in self._iter_fields():
            field_initial = initial.get(name, field.initial)
            field_initial = "" if field_initial is None else field_initial
            self._fields_initial[name] = field_initial
            field.data = data.get(name, field_initial)
            self._edit_field_init(field)

    def _field_clean_pass(self, field):
        pass

    def _field_clean_error(self, field, error):
        pass

    def _edit_field_init(self, field):
        pass

    def _submit_init(self):
        pass

    def submit(self):
        if self._initialized:
            self.is_bound = True
            self._submit_init()
            self.full_clean()
        else:
            raise FormError(
                "Form initialization error. Call form.edit() before submit"
            )


class FormWidget(FormBase):
    def __init__(self, *args, **kw):
        self._fields_scanned = False
        super().__init__(*args, **kw)

    def _iter_fields(self, force_scan=False):
        if self._fields_scanned is False or force_scan:
            print("Searching for fields in iter function.")
            self._find_fields()
        for name, field in self.fields.items():
            yield name, field
        self._fields_scanned = True

    def _find_fields(self, master=None):
        if master is None:
            master = self
        for widget in master.winfo_children():
            if isinstance(widget, FieldBase):
                self.fields[widget.fname] = widget
                print(f"Field Found: {widget.fname}")
            elif isinstance(widget, FieldInfo):
                self._info_displays[widget.fname] = widget
            else:
                self._find_fields(widget)

    def _field_clean_pass(self, field):
        if field.help_text:
            field_info = self._info_displays.get(field.fname, None)
            if field_info is not None:
                field_info.show_help(field.help_text)

    def _field_clean_error(self, field, error):
        field.wmark_invalid(True)
        field_info = self._info_displays.get(field.fname, None)
        if field_info is not None:
            field_info.show_error(error)

    def _edit_field_init(self, field):
        if field.fname in self._info_displays:
            field_info = self._info_displays[field.fname]
            field_info.clear()
            if field.help_text:
                field_info.show_help(field.help_text)

    def _submit_init(self):
        for name, field in self._iter_fields():
            field.wmark_invalid(False)
        for name in self._info_displays:
            self._info_displays[name].clear()
