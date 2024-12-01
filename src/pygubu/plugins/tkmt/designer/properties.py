from pygubu.api.v1 import register_custom_property
from pygubu.plugins.tkmt import _designer_tab_label, _plugin_uid

_builder_uid = f"{_plugin_uid}.*"

tkmt_properties = {
    "args": {
        "editor": "json_entry",
        "help": "Args passsed to command property. In designer, a json list.",
    },
    "col": {"editor": "naturalnumber"},
    "colspan": {"editor": "naturalnumber", "min_value": 1},
    "columnnames": {  # Treeview
        "editor": "json_entry",
        "help": "Column header names. In designer, a json list of strings.",
        "json_type": list,
        "json_item_type": str,
    },
    "columnwidths": {  # Treeview
        "editor": "json_entry",
        "help": ("Width of each column, should be same size as columnnames." 
                 + " In designer, a json list of ints"),
        "json_type": list,
        "json_item_type": int,
    },
    "command": {"editor": "simplecommandentry"},
    "datacolumnnames": {  # Treeview
        "editor": "json_entry",
        "help": """Defaults to columnnames, a mapping of columnnames to the data file.
Should be same size as columnnames. In designer, a json list of strings.""",
        "json_type": list,
        "json_item_type": str,
    },
    "data": {  # Treeview
        "editor": "entry",
        "help": """The tree data.
In designer, use a resource URI here, example:  res://my_treeview_data""",
    },
    "defaulttext": {"editor": "entry"},  # MenuButton
    "disabled": {
        "editor": "choice",
        "values": ("", "True"),
        "state": "readonly",
    },
    "increment": {"editor": "realnumber"},
    "invalidcommand": {
        "editor": "simplecommandentry",
    },
    "invalidcommandargs": {
        "editor": "json_entry",
        "help": "Args passsed to invalidcommand property. In designer, a json list.",
    },
    "lower": {"editor": "realnumber"},
    "makeResizable": {
        "editor": "choice",
        "values": ("", "all", "recursive", "onlyframes"),
        "state": "readonly",
    },
    "menu": {  # MenuButton
        "buid": f"{_plugin_uid}.MenuButton",
        "editor": "entry",
        "help": "Use a resource URI here, example:  res://my_menu",
    },
    "mode": {
        "editor": "choice",
        "values": ("", "light", "dark"),
        "state": "readonly",
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
    "theme": {
        "editor": "choice",
        "values": ("", "azure", "sun-valley", "park"),
        "state": "readonly",
    },
    "upper": {"editor": "realnumber"},
    "usecommandlineargs": {
        "editor": "choice",
        "values": ("", "True", "False"),
        "state": "readonly",
    },
    "useconfigfile": {
        "editor": "choice",
        "values": ("", "True", "False"),
        "state": "readonly",
    },
    "validate": {
        "editor": "choice",
        "values": (
            "",
            "all",
            "focus",
            "focusin",
            "focusout",
            "key",
            "none",
        ),
        "state": "readonly",
    },
    "validatecommand": {"editor": "simplecommandentry"},
    "validatecommandargs": {
        "editor": "json_entry",
        "help": "Args passsed to validatecommand property. In designer, a json list.",
    },
    "validatecommandmode": {
        "editor": "choice",
        "values": ("", "%P", "%d %i %P %s %S %v %V %W"),
        # "state": "readonly",
    },
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
            "buid": f"{_plugin_uid}.NumericalSpinbox",
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
