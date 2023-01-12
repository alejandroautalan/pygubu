from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.i18n import _
from ..customtkinter import _designer_tab_label, _plugin_uid
from .ctkbase import CTkBaseMixin, GCONTAINER

from customtkinter import CTkTabview


class CTkTabviewBO(CTkBaseMixin, BuilderObject):
    class_ = CTkTabview
    allow_bindings = False
    container = True
    properties = (
        "width",
        "height",
        "corner_radius",
        "border_width",
        "bg_color",
        "fg_color",
        "border_color",
        "segmented_button_fg_color",
        "segmented_button_selected_color",
        "segmented_button_selected_hover_color",
        "segmented_button_unselected_color",
        "segmented_button_unselected_hover_color",
        "text_color",
        "text_color_disabled",
        "command",
        "state",
    )
    command_properties = ("command",)


_builder_uid = f"{_plugin_uid}.CTkTabview"
register_widget(
    _builder_uid,
    CTkTabviewBO,
    "CTkTabview",
    ("ttk", _designer_tab_label),
    group=GCONTAINER,
)


class CTkTabviewTabBO(BuilderObject):
    class_ = None
    container = True
    container_layout = True
    layout_required = False
    allow_bindings = False
    allowed_parents = (f"{_plugin_uid}.CTkTabview",)
    properties = ("label",)

    def _get_tab_name(self):
        return self.wmeta.properties.get("label", self.wmeta.identifier)

    def realize(self, parent, extra_init_args: dict = None):
        view = parent.get_child_master()
        self.widget = view.add(self._get_tab_name())
        return self.widget

    def configure(self, target=None):
        pass

    #
    # Code generation methods
    #
    def code_realize(self, boparent, code_identifier=None):
        view = boparent.code_child_master()
        tabid = self.code_identifier()
        tab_name = self._get_tab_name()
        lines = [f'{tabid} = {view}.add("{tab_name}")']
        return lines

    def code_configure(self, targetid=None):
        return tuple()


_builder_uid = f"{_plugin_uid}.CTkTabview.Tab"

CTkTabviewBO.add_allowed_child(_builder_uid)

register_widget(
    _builder_uid,
    CTkTabviewTabBO,
    "CTkTabview.Tab",
    ("ttk", _designer_tab_label),
    group=GCONTAINER,
)

_help = _("The 'name' argument of method: CTkTabview.add(self, name: str)")
register_custom_property(_builder_uid, "label", "entry", help=_help)
