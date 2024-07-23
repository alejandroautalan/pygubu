from pygubu.api.v1 import register_custom_property
from pygubu.plugins.pygubu import _designer_tab_label, _plugin_uid


_builder_uid = f"{_plugin_uid}.*"

plugin_properties = {
    "mask": dict(buid=f"{_plugin_uid}.Floodgauge"),
}

for prop in plugin_properties:
    definitions = plugin_properties[prop]
    if isinstance(definitions, dict):
        definitions = [definitions]
    for definition in definitions:
        builder_uid = definition.pop("buid", _builder_uid)
        editor = definition.pop("editor", "entry")
        register_custom_property(builder_uid, prop, editor, **definition)
