from pygubu.i18n import _
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from tksheet import Sheet
from ..tksheet import _designer_tab_label, _plugin_uid


class SheetBuilder(BuilderObject):
    class_ = Sheet


_builder_uid = f"{_plugin_uid}.Sheet"
register_widget(
    _builder_uid, SheetBuilder, "Sheet", ("ttk", _designer_tab_label)
)
