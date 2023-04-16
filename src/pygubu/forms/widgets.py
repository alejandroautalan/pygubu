"""Widget related classes"""
import json


class FieldWidget:
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def wset_value(self, value):
        # will set the value in the widget format
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
            f" for field class {self.__class__}"
        )

    def wget_value(self):
        # Get value in the widget
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
            f" for field class {self.__class__}"
        )

    def wmark_invalid(self, state: bool):
        # Visually mark the widget as invalid depending on state parameter.
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
            f" for field class {self.__class__}"
        )

    def wis_disabled(self) -> bool:
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
            f" for field class {self.__class__}"
        )
