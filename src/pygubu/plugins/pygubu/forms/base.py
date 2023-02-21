import tkinter as tk


class FieldMixin:
    """Manages base field properties."""

    base_properties = ("fname", "initial", "required", "help_text")

    def _get_init_args(self, extra_init_args: dict = None):
        args = super()._get_init_args(extra_init_args)
        name = args.get("fname", None)
        if not name:
            args["fname"] = self.wmeta.identifier
        return args

    def _process_property_value(self, pname, value):
        if pname == "required":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)
