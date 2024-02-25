import tkinter as tk
from pygubu.api.v1 import BuilderObject, register_custom_property
from pygubu.i18n import _


_plugin_uid = "pygubu.forms"
_designer_tabname = _("Pygubu Forms")


class WidgetBOMixin:
    """Manages base widget properties."""

    FIELD_NAME_PROP = "field_name"
    base_properties = (FIELD_NAME_PROP,)

    # @classmethod
    # def properties(cls):
    # if isinstance(super().properties, tuple):
    # return super().properties + cls.base_properties
    # return super().properties() + cls.base_properties

    # @classmethod
    # def ro_properties(cls):
    # if isinstance(super().ro_properties, tuple):
    # return super().ro_properties + cls.base_properties
    # return super().ro_properties() + cls.base_properties

    def _get_init_args(self, extra_init_args: dict = None):
        args = super()._get_init_args(extra_init_args)
        name = args.get(self.FIELD_NAME_PROP, None)
        if not name:
            args[self.FIELD_NAME_PROP] = self.wmeta.identifier
        return args

    def _code_get_init_args(self, code_identifier):
        args = super()._code_get_init_args(code_identifier)
        field_name_value = args.get("_name", None)
        if not field_name_value:
            field_name_value = self.wmeta.identifier
            args[self.FIELD_NAME_PROP] = self._code_process_property_value(
                code_identifier, self.FIELD_NAME_PROP, field_name_value
            )
        return args


register_custom_property(
    f"{_plugin_uid}.*", WidgetBOMixin.FIELD_NAME_PROP, "fieldname_entry"
)
