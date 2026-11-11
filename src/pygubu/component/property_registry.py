import os
import logging

from typing import Optional, List
from abc import ABC, abstractmethod


logger = logging.getLogger(__name__)


class IPropertyRegistry(ABC):
    def __init__(self):
        self.properties = {}

    def register(self, name: str, description: dict):
        if name in self.properties:
            self._update_existent(name, description)
        else:
            self._add_new(name, description)

    @abstractmethod
    def _add_new(self, name: str, description: dict): ...

    @abstractmethod
    def _update_existent(self: str, name, description: dict): ...

    @abstractmethod
    def iter_names(self): ...

    @abstractmethod
    def register_custom(
        self,
        builder_uid: str,
        prop_name: str,
        editor: str,
        default_value=None,
        help=None,
        **editor_params,
    ): ...


class PropertyRegistryDummy(IPropertyRegistry):
    """If designer is not running there is no need to maintain
    more structures in memory. This class will ignore all method calls.
    """

    def _add_new(self, name: str, description: dict):
        logger.debug("New property %s, ignored.", name)

    def _update_existent(self: str, name, description: dict):
        logger.debug("Update property %s, ignored.", name)

    def iter_names(self):
        return None

    def register_custom(
        self,
        builder_uid: str,
        prop_name: str,
        editor: str,
        default_value=None,
        help=None,
        **editor_params,
    ):
        return None

    def copy_to_builder(
        self, from_builder_id: str, pname: str, to_builder_id: str
    ):
        return None


class PropertyRegistryBase(IPropertyRegistry):
    """Mantain and manage property definitions."""

    def __init__(self):
        super().__init__()
        self._is_sorted: bool = False
        self._sorted_names: list[str] = None

    def _add_new(self, name: str, description: dict):
        self.properties[name] = description
        self._is_sorted = False
        logger.debug("Registered property %s", name)

    def _update_existent(self, name: str, description: dict):
        self.properties[name].update(description)
        logger.debug("Updating registered property %s", name)

    def iter_names(self):
        if not self._is_sorted:
            self._sorted_names = sorted(self.properties.keys())
            self._is_sorted = True
        yield from self._sorted_names

    def register(self, name: str, description: dict):
        if name in self.properties:
            self._update_existent(name, description)
        else:
            self._add_new(name, description)

    def register_custom(
        self,
        builder_uid: str,
        prop_name: str,
        editor: str,
        default_value=None,
        help=None,
        **editor_params,
    ):
        """All custom properties are created using internal dynamic editor."""
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
        self.register(prop_name, description)

    def copy_to_builder(
        self, from_builder_id: str, pname: str, to_builder_id: str
    ):
        """Copy property definition from one builder to another."""
        if pname not in self.properties:
            raise RuntimeError(f"Property {pname} not registered.")
        from_definition = self.find_definition_for(pname, from_builder_id)
        if from_definition:
            new_definition = {to_builder_id: from_definition.copy()}
            self._update_existent(pname, new_definition)
        else:
            logger.info(
                "Builder %s has no definition for %s.", from_builder_id, pname
            )

    def find_definition_for(self, pname: str, builder_uid: str) -> dict:
        """Search for specific definition of pname added by builder_uid."""

        definition = self.properties[pname]
        specific = {}
        # Get editor parameters for a specific builder_uid
        # First, search for exact match
        for key in definition:
            if key == builder_uid:
                specific = definition[key]
                break
        if not specific:
            # Search for partial match
            for key in definition:
                if key.endswith(".*"):
                    needle = key[:-2]
                    if needle in builder_uid:
                        specific = definition[key]
                        break
        return specific


if "PYGUBU_DESIGNER_RUNNING" in os.environ:
    from blinker import Signal

    class PropertyRegistryWithSignals(PropertyRegistryBase):
        on_property_new = Signal()
        on_property_update = Signal()

        def _add_new(self, name: str, description: dict):
            super()._add_new(name, description)
            if self.on_property_new.receivers:
                self.on_property_new.send(name=name)

        def _update_existent(self, name: str, description: dict):
            super()._update_existent(name, description)
            if self.on_property_update.receivers:
                self.on_property_update.send(name=name, description=description)

    PropertyRegistry = PropertyRegistryWithSignals()

else:
    PropertyRegistry = PropertyRegistryDummy()
