from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from pygubu.i18n import _

from pygubu.widgets.hideableframe import HideableFrame


class HideableFrameBO(TTKFrame):
    class_ = HideableFrame


_builder_uid = "pygubu.widgets.hideableframe"
register_widget(
    _builder_uid,
    HideableFrameBO,
    "HideableFrame",
    (_("Pygubu Widgets"), "ttk"),
)

register_custom_property(
    _builder_uid, "width", "dimensionentry", default_value=200
)

register_custom_property(
    _builder_uid, "height", "dimensionentry", default_value=200
)
