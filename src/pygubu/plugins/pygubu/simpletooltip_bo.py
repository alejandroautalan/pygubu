from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property,
)
from pygubu.plugins.pygubu import _tab_widgets_label, _plugin_uid


class SimpleTooltipBO(BuilderObject):
    layout_required = False
    properties = ("text",)

    def realize(self, parent, extra_init_args: dict = None):
        self.widget = parent.get_child_master()
        print(f"creating tooltip for: {self.widget}")
        return self.widget


_builder_uid = f"{_plugin_uid}.SimpleTooltip"
register_widget(
    _builder_uid,
    SimpleTooltipBO,
    "SimpleTooltip",
    (_tab_widgets_label, "ttk"),
)


register_custom_property(
    _builder_uid,
    "text",
    "text",
    help="Pygubu simple tooltip",
)
