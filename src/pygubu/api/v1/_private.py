import logging
from ...component.builderobject import (
    CLASS_MAP,
    WidgetDescription,
    CUSTOM_PROPERTIES,
)

logger = logging.getLogger(__name__)


def register_builder(
    classname, builder, label=None, tags=None, group=None, public=True
):
    if label is None:
        label = classname
    if tags is None:
        tags = tuple()
    if group is None:
        group = 9

    CLASS_MAP[classname] = WidgetDescription(
        classname, builder, label, tags, group, public
    )


def register_widget(
    classname, builder, label=None, tags=None, group=None, public=True
):
    return register_builder(classname, builder, label, tags, group, public)


def register_property(name, description):
    if name in CUSTOM_PROPERTIES:
        CUSTOM_PROPERTIES[name].update(description)
        logger.debug("Updating registered property %s", name)
    else:
        CUSTOM_PROPERTIES[name] = description
        logger.debug("Registered property %s", name)


def register_custom_property(
    builder_uid,
    prop_name,
    editor,
    default_value=None,
    help=None,
    **editor_params,
):
    """Helper function to register a custom property.
    All custom properties are created using internal dynamic editor.
    """
    description = {
        "editor": "dynamic",
        builder_uid: {
            "params": {
                "mode": editor,
            }
        },
    }
    description[builder_uid]["params"].update(editor_params)
    if default_value is not None:
        description[builder_uid]["default"] = default_value
    if help is not None:
        description[builder_uid]["help"] = help
    register_property(prop_name, description)


def copy_custom_property(from_builder_id, pname, to_builder_id):
    if pname not in CUSTOM_PROPERTIES:
        raise RuntimeError(f"Property {pname} not registered.")
    elif from_builder_id not in CUSTOM_PROPERTIES[pname]:
        raise RuntimeError(f"Builder ID {from_builder_id} not registered.")
    else:
        description = CUSTOM_PROPERTIES[pname][from_builder_id].copy()
        CUSTOM_PROPERTIES[pname][to_builder_id] = description
