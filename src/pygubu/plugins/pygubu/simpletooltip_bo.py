from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from pygubu.widgets.simpletooltip import Tooltip, Tooltipttk
from pygubu.component.builderobject import FamilyType
from ._config import nspygubu, _designer_tabs_widgets_ttk


class TooltipBaseBO(BuilderObject):
    allow_bindings = False
    layout_required = False
    family = FamilyType.MODIFIER

    def realize(self, parent, extra_init_args: dict = None):
        self.widget = parent.get_child_master()
        self.widget.simple_tooltip = self.class_(self.widget)
        return self.widget

    def _set_property(self, target_widget, pname, value):
        target_widget.simple_tooltip.label_options[pname] = value


class SimpleTooltipBO(TooltipBaseBO):
    class_ = Tooltip
    properties = (
        "text",
        "font",
        "background",
        "foreground",
        "justify",
        "wraplength",
        "relief",
        "borderwidth",
        "padx",
        "pady",
    )


register_widget(
    nspygubu.widgets.Tooltip,
    SimpleTooltipBO,
    "Tooltip",
    _designer_tabs_widgets_ttk,
)


class SimpleTooltipttkBO(SimpleTooltipBO):
    class_ = Tooltipttk
    properties = (
        "text",
        "font",
        "foreground",
        "background",
        "justify",
        "wraplength",
        "relief",
        "borderwidth",
        "style",
    )


register_widget(
    nspygubu.widgets.Tooltipttk,
    SimpleTooltipttkBO,
    "Tooltipttk",
    _designer_tabs_widgets_ttk,
)
