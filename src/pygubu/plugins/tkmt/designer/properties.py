from pygubu.api.v1 import register_custom_property
from pygubu.plugins.tkmt import _designer_tab_label, _plugin_uid

_builder_uid = f"{_plugin_uid}.*"

int_properties = {"row": {}, "col": {}, "rowspan": {}, "colspan": {}}

for prop in int_properties:
    editor = int_properties[prop].pop("editor", "naturalnumber")
    register_custom_property(_builder_uid, prop, editor, **int_properties[prop])

float_properties = {
    "lower": {},
    "upper": {},
    "increment": {},
}

for prop in float_properties:
    editor = float_properties[prop].pop("editor", "realnumber")
    register_custom_property(
        _builder_uid, prop, editor, **float_properties[prop]
    )

# "sticky" style  "padx", "pady"
