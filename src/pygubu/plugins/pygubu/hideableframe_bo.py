from pygubu.api.v1 import register_widget
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from pygubu.widgets.hideableframe import HideableFrame
from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid


class HideableFrameBO(TTKFrame):
    class_ = HideableFrame


_builder_uid = f"{_plugin_uid}.hideableframe"
register_widget(
    _builder_uid,
    HideableFrameBO,
    "HideableFrame",
    (_tab_widgets_label, "ttk"),
)
