from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid
from pygubu.widgets.simpletooltip import Tooltip, Tooltipttk
from pygubu.component.builderobject import FamilyType


class SimpleTooltipBO(BuilderObject):
    layout_required = False
    properties = (
        "text",
        "font",
        "background",
        "foreground",
        "justify",
        "wraplength",
        "relief",
        "padx",
        "pady",
    )
    class_ = Tooltip
    family = FamilyType.MODIFIER

    def realize(self, parent, extra_init_args: dict = None):
        self.widget = parent.get_child_master()
        self.widget.simple_tooltip = self.class_(self.widget)
        return self.widget

    def _set_property(self, target_widget, pname, value):
        target_widget.simple_tooltip.label_options[pname] = value


_builder_uid = f"{_plugin_uid}.Tooltip"
register_widget(
    _builder_uid,
    SimpleTooltipBO,
    "Tooltip",
    (_tab_widgets_label, "ttk"),
)


# class SimpleTooltipttkBO(
