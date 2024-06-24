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

json_properties = {
    # Treeview begin
    "columnnames": {"help": "A json list of strings."},
    "datacolumnnames": {
        "help": "A json list of strings. Should be same size as columnnames."
    },
    "columnwidths": {
        "help": "A json list of ints. Should be same size as columnnames."
    },
    "values": [
        # OptionMenu begin
        {
            "buid": f"{_plugin_uid}.OptionMenu",
            "help": "A json list of strings.",
        },
        # Combobox begin
        {
            "buid": f"{_plugin_uid}.Combobox",
            "help": "A json list of strings.",
        },
    ],
}

for prop in json_properties:
    definitions = json_properties[prop]
    if isinstance(definitions, dict):
        definitions = [definitions]
    for definition in definitions:
        builder_uid = definition.pop("buid", _builder_uid)
        editor = definition.pop("editor", "json_entry")
        register_custom_property(builder_uid, prop, editor, **definition)

string_properties = {
    # Treeview begin
    "data": {
        "help": "Use a resource URI here, example:  res://my_treeview_data"
    },
    "subentryname": {},
    # MenuButton begin
    "menu": {
        "buid": f"{_plugin_uid}.MenuButton",
        "help": "Use a resource URI here, example:  res://my_menu",
    },
    "defaulttext": {},
}

for prop in string_properties:
    builder_uid = string_properties[prop].pop("buid", _builder_uid)
    editor = string_properties[prop].pop("editor", "entry")
    register_custom_property(
        builder_uid, prop, editor, **string_properties[prop]
    )

# Scale
register_custom_property(
    f"{_plugin_uid}.Scale",
    "variable",
    "tkvarentry",
    type_choices=("int", "double"),
    type_default="int",
)
