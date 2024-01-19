import tkinter as tk
from pygubu.api.v1 import BuilderObject, register_custom_property


class FieldBOMixin:
    """Manages base field properties."""

    base_properties = (
        "field_name",
        "field_initial",
        "field_required",
        "field_help",
    )

    def _get_init_args(self, extra_init_args: dict = None):
        args = super()._get_init_args(extra_init_args)
        name = args.get("field_name", None)
        if not name:
            args["field_name"] = self.wmeta.identifier
        return args

    def _process_property_value(self, pname, value):
        if pname == "field_required":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

    def _code_get_init_args(self, code_identifier):
        args = super()._code_get_init_args(code_identifier)
        field_name_value = args.get("field_name", None)
        if not field_name_value:
            field_name_value = self.wmeta.identifier
            args["field_name"] = self._code_process_property_value(
                code_identifier, "field_name", field_name_value
            )
        return args


register_custom_property("pygubu.forms.*", "field_name", "fieldname_entry")
register_custom_property("pygubu.forms.*", "field_initial", "entry")
register_custom_property(
    "pygubu.forms.*",
    "field_required",
    "choice",
    values=("", "false", "true"),
    state="readonly",
)
register_custom_property("pygubu.forms.*", "field_help", "entry")
register_custom_property("pygubu.forms.*", "max_length", "naturalnumber")
register_custom_property("pygubu.forms.*", "min_length", "naturalnumber")
register_custom_property(
    "pygubu.forms.*",
    "strip",
    "choice",
    values=("", "false", "true"),
    state="readonly",
)
register_custom_property("pygubu.forms.*", "empty_value", "entry")
