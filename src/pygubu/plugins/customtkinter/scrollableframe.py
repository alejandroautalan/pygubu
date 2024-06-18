from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.i18n import _
from ..customtkinter import _designer_tab_label, _plugin_uid
from .ctkbase import CTkBaseMixin, GCONTAINER

from customtkinter import CTkScrollableFrame


class CTkScrollableFrameBO(CTkBaseMixin, BuilderObject):
    class_ = CTkScrollableFrame
    container = True
    # CTkScrollableFrame does some weird things
    # with layout so I disable container layout here on purpose.
    container_layout = False
    properties = (
        "width",
        "height",
        "corner_radius",
        "border_width",
        "bg_color",
        "fg_color",
        "border_color",
        "scrollbar_fg_color",
        "scrollbar_button_color",
        "scrollbar_button_hover_color:",
        "label_fg_color",
        "label_text_color",
        "label_text",
        "label_font",
        "label_anchor",
        "orientation",
    )
    ro_properties = ("orientation",)


_builder_uid = f"{_plugin_uid}.CTkScrollableFrame"
register_widget(
    _builder_uid,
    CTkScrollableFrameBO,
    "CTkScrollableFrame",
    ("ttk", _designer_tab_label),
    group=GCONTAINER,
)

register_custom_property(
    _builder_uid,
    "label_anchor",
    "choice",
    values=(
        "",
        "n",
        "ne",
        "nw",
        "e",
        "w",
        "s",
        "se",
        "sw",
        "center",
    ),
    state="readonly",
)

register_custom_property(
    _builder_uid,
    "orientation",
    "choice",
    values=("vertical", "horizontal"),
    default_value="vertical",
    state="readonly",
)
