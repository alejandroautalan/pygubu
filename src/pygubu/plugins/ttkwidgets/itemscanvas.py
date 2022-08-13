from pygubu.i18n import _
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.plugins.ttk.ttkstdwidgets import TTKFrame
from ttkwidgets import ItemsCanvas

from ..ttkwidgets import _designer_tab_label, _plugin_uid


class ItemsCanvasBO(TTKFrame):
    class_ = ItemsCanvas
    container = False
    OPTIONS_CUSTOM = (
        "canvaswidth",
        "canvasheight",
        "callback_add",
        "callback_del",
        "callback_move",
        "function_new",
    )
    properties = (
        TTKFrame.OPTIONS_STANDARD + TTKFrame.OPTIONS_SPECIFIC + OPTIONS_CUSTOM
    )
    command_properties = (
        "callback_add",
        "callback_del",
        "callback_move",
        "function_new",
    )

    def _process_property_value(self, pname, value):
        if pname in ("canvaswidth", "canvasheight"):
            return int(value)
        return super(ItemsCanvasBO, self)._process_property_value(pname, value)

    def _code_define_callback_args(self, cmd_pname, cmd):
        args = None
        if cmd_pname in ("callback_add", "callback_del"):
            args = ("item", "rectangle")
        elif cmd_pname == "callback_move":
            args = ("item", "rectangle", "x", "y")
        elif cmd_pname == "function_new":
            args = ("add_item",)
        else:
            args = super(ItemsCanvasBO, self)._code_define_callback_args(
                cmd_pname, cmd
            )
        return args


_builder_uid = f"{_plugin_uid}.ItemsCanvas"
register_widget(
    _builder_uid,
    ItemsCanvasBO,
    "ItemsCanvas",
    ("ttk", _designer_tab_label),
    group=6,
)

register_custom_property(
    _builder_uid,
    "canvaswidth",
    "integernumber",
    help=_("width of the canvas in pixels"),
)
register_custom_property(
    _builder_uid,
    "canvasheight",
    "integernumber",
    help=_("height of the canvas in pixels"),
)
register_custom_property(
    _builder_uid,
    "callback_add",
    "simplecommandentry",
    help=_(
        "callback for when an item is created, with args: (int item, int rectangle)"
    ),
)
register_custom_property(
    _builder_uid,
    "callback_del",
    "simplecommandentry",
    help=_(
        "callback for when an item is deleted, with args: (int item, int rectangle)"
    ),
)
register_custom_property(
    _builder_uid,
    "callback_move",
    "simplecommandentry",
    help=_(
        "callback for when an item is moved, with args: (int item, int rectangle, int x, int y)"
    ),
)
register_custom_property(
    _builder_uid,
    "function_new",
    "simplecommandentry",
    help=_(
        "user defined function for when an item is created, with arg (add_item).\nWhere add_item is a function of this widget."
    ),
)
