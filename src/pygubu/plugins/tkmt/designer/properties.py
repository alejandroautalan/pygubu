from pygubu.api.v1 import register_custom_property
from pygubu.plugins.tkmt import _designer_tab_label, _plugin_uid

_builder_uid = f"{_plugin_uid}.*"

tkmt_properties = {
    "col": {"editor": "naturalnumber"},
    "colspan": {"editor": "naturalnumber", "min_value": 1},
    "columnnames": {  # Treeview
        "editor": "json_entry",
        "help": "A json list of strings.",
    },
    "columnwidths": {  # Treeview
        "editor": "json_entry",
        "help": "A json list of ints. Should be same size as columnnames.",
    },
    "datacolumnnames": {  # Treeview
        "editor": "json_entry",
        "help": "A json list of strings. Should be same size as columnnames.",
    },
    "data": {  # Treeview
        "editor": "entry",
        "help": "Use a resource URI here, example:  res://my_treeview_data",
    },
    "defaulttext": {"editor": "entry"},  # MenuButton
    "increment": {"editor": "realnumber"},
    "lower": {"editor": "realnumber"},
    "menu": {  # MenuButton
        "buid": f"{_plugin_uid}.MenuButton",
        "editor": "entry",
        "help": "Use a resource URI here, example:  res://my_menu",
    },
    "newframe": {  # Treeview
        "editor": "choice",
        "values": ("", "True", "False"),
        "state": "readonly",
    },
    "openkey": {  # Treeview
        "editor": "alphanumentry",
    },
    "orient": {
        "editor": "choice",
        "values": ("", "horizontal", "vertical"),
        "state": "readonly",
    },
    "padx": {
        "editor": "twodimensionentry",
    },
    "pady": {
        "editor": "twodimensionentry",
    },
    "row": {"editor": "naturalnumber"},
    "rowspan": {"editor": "naturalnumber", "min_value": 1},
    "subentryname": {"editor": "entry"},  # Treeview
    "upper": {"editor": "realnumber"},
    "values": [
        {  # OptionMenu
            "editor": "json_entry",
            "buid": f"{_plugin_uid}.OptionMenu",
            "help": "A json list of strings.",
        },
        {  # Combobox
            "editor": "json_entry",
            "buid": f"{_plugin_uid}.Combobox",
            "help": "A json list of strings.",
        },
        {  # NonnumericalSpinbox
            "editor": "json_entry",
            "buid": f"{_plugin_uid}.NonnumericalSpinbox",
            "help": "A json list of strings.",
        },
    ],
    "variable": [
        {
            "buid": f"{_plugin_uid}.Scale",
            "editor": "tkvarentry",
            "type_choices": ("int", "double"),
            "type_default": "int",
        },
        {
            "buid": f"{_plugin_uid}.NonnumericalSpinbox",
            "editor": "tkvarentry",
            "type_choices": ("string",),
            "type_default": "string",
        },
    ],
}

for prop in tkmt_properties:
    definitions = tkmt_properties[prop]
    if isinstance(definitions, dict):
        definitions = [definitions]
    for definition in definitions:
        builder_uid = definition.pop("buid", _builder_uid)
        editor = definition.pop("editor", "entry")
        register_custom_property(builder_uid, prop, editor, **definition)
