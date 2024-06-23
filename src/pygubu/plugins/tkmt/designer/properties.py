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
    "columnnames": {"help": "A json list of strings."},
    "datacolumnnames": {
        "help": "A json list of strings. Should be same size as columnnames."
    },
    "columnwidths": {
        "help": "A json list of ints. . Should be same size as columnnames."
    },
}

for prop in json_properties:
    editor = json_properties[prop].pop("editor", "json_entry")
    register_custom_property(
        _builder_uid, prop, editor, **json_properties[prop]
    )

string_properties = {
    # Treeview data argument
    "data": {
        "help": "Use a resource URI here, example:  res://my_treeview_data"
    },
    # Treeview data argument
    "subentryname": {},
}

for prop in string_properties:
    editor = string_properties[prop].pop("editor", "entry")
    register_custom_property(
        _builder_uid, prop, editor, **string_properties[prop]
    )

# "sticky" style  "padx", "pady"
