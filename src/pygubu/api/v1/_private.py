import logging
from ...component.builderobject import (
    CLASS_MAP,
    WidgetDescription,
)
from ...component.property_registry import PropertyRegistry


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
    PropertyRegistry.register(name, description)


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
    PropertyRegistry.register_custom(
        builder_uid, prop_name, editor, default_value, help, **editor_params
    )


def copy_custom_property(from_builder_id, pname, to_builder_id):
    PropertyRegistry.copy_to_builder(from_builder_id, pname, to_builder_id)
