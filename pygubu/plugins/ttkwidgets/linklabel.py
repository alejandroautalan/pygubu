from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.ttk.ttkstdwidgets import TTKLabel
from ttkwidgets import LinkLabel

from ..ttkwidgets import _designer_tab_label, _plugin_uid


class LinkLabelBO(TTKLabel):
    class_ = LinkLabel
    OPTIONS_CUSTOM = ("link", "normal_color", "hover_color", "clicked_color")
    properties = (
        TTKLabel.OPTIONS_STANDARD + TTKLabel.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )


_builder_uid = f"{_plugin_uid}.LinkLabel"
register_widget(
    _builder_uid,
    LinkLabelBO,
    "LinkLabel",
    ("ttk", _designer_tab_label),
    group=1,
)

register_custom_property(
    _builder_uid, "link", "entry", help=_("link to be opened")
)
register_custom_property(
    _builder_uid,
    "normal_color",
    "colorentry",
    help=_("text color when widget is created"),
)
register_custom_property(
    _builder_uid,
    "hover_color",
    "colorentry",
    help=_("text color when hovering over the widget"),
)
register_custom_property(
    _builder_uid,
    "clicked_color",
    "colorentry",
    help=_("text color when link is clicked"),
)
