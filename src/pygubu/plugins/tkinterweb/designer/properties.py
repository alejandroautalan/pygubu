from pygubu.i18n import _
from pygubu.api.v1 import register_custom_property
from pygubu.plugins.tkinterweb import _plugin_uid


_builder_all = f"{_plugin_uid}.*"
_htmlFrame = f"{_plugin_uid}.HtmlFrame"
_htmlLabel = f"{_plugin_uid}.HtmlLabel"
_notebook = f"{_plugin_uid}.Notebook"
_colourSelector = f"{_plugin_uid}.ColourSelector"


plugin_properties = {
    "colour": dict(
        buid=_colourSelector, editor="colorentry", default_value="white"
    ),
    "height": dict(
        buid=_notebook,
        editor="dimensionentry",
        default_value=200,
    ),
    "horizontal_scrollbar": dict(
        buid=_htmlFrame,
        editor="choice",
        values=("", "true", "false", "auto"),
        state="readonly",
    ),
    "messages_enabled": dict(
        buid=_builder_all,
        editor="choice",
        values=("", "false", "true"),
        state="readonly",
        help=_("Show debugging messages on console output."),
    ),
    "text": dict(
        buid=_htmlLabel,
        editor="text",
    ),
    "vertical_scrollbar": dict(
        buid=_htmlFrame,
        editor="choice",
        values=("", "true", "false", "auto"),
        state="readonly",
    ),
    "width": dict(
        buid=_notebook,
        editor="dimensionentry",
        default_value=200,
    ),
}

for prop in plugin_properties:
    definitions = plugin_properties[prop]
    if isinstance(definitions, dict):
        definitions = [definitions]
    for definition in definitions:
        builders = definition.pop("buid", _builder_all)
        if isinstance(builders, str):
            builders = [builders]
        editor = definition.pop("editor", "entry")
        for builder_uid in builders:
            register_custom_property(builder_uid, prop, editor, **definition)
