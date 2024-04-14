from .form import Form, FormField


class FormBuilder:
    def __init__(self, *args, field_name: str, **kw):
        super().__init__(*args, **kw)
        self.field_name = field_name
        self.fields_scanned = False
        self.widgets = {}
        self.widgets_info = {}
        self.form_info = {}

    def iter_widgets(self, force_scan=False):
        if self.fields_scanned is False or force_scan:
            self.scan_widgets()
        for name, widget in self.widgets.items():
            yield name, widget
        self.fields_scanned = True

    def scan_widgets(self):
        pass

    def get_form(self, config: dict):
        form = Form()
        for name, widget in self.iter_widgets():
            params = {}
            if name in config:
                params = config[name]
            field = FormField(widget, **params)
            form.add(name, field)
        for name, info in self.widgets_info.items():
            form.add_info_display(name, info)
        trans_key = "translator"
        if trans_key in config:
            form.translator = config[trans_key]
        return form
